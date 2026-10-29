// Catalog detail sheet for the pergola landing page: a tap on a catalog card opens a sheet with the full text and real project photos
// for that solution (taken from projects-data.js), plus the consult CTA and a link to the matching projects category.
// Mobile: slides up from the bottom. Desktop: centred dialog.
(function () {
  if (window.__stzDetail) return;
  window.__stzDetail = true;
  var root = null;
  // Page title and description follow the ad group's topic (?s=...), so the page repeats the exact search wording of the ad that brought the visitor.
  (function () {
    var T = {
      electric: ['פרגולה חשמלית למרפסת ולגינה בהתאמה אישית | סופר צל', 'פרגולה חשמלית בהתאמה אישית עם פרופילי הצללה מתכווננים: אור, צל ואוורור לפי הצורך. מדידה בשטח והתקנה מקצועית. תאמו שיחת ייעוץ.'],
      alu: ['פרגולת אלומיניום בהתאמה אישית למרפסת ולגינה | סופר צל', 'פרגולת אלומיניום בהתאמה אישית למרפסת ולגינה, כולל גוון דמוי עץ. מדידה בשטח והתקנה מקצועית. תאמו שיחת ייעוץ.'],
      wood: ['פרגולת עץ טבעי ופרגולות מיוחדות ומעוצבות | סופר צל', 'פרגולת עץ טבעי, אלומיניום בגוון דמוי עץ ושילובים מיוחדים. בהתאמה אישית למרפסת ולגינה. תאמו שיחת ייעוץ.'],
      closure: ['סגירת חורף ומרפסת בזכוכית בהתאמה אישית | סופר צל', 'סגירת חורף למרפסת בזכוכית, מסכי גלילה וסגירה בשילוב פרגולה. מדידה בשטח והתקנה מקצועית. תאמו שיחת ייעוץ.'],
      kitchen: ['מטבח חוץ ובר בהתאמה אישית | סופר צל', 'מטבח חוץ ובר אירוח מתוכננים יחד עם ההצללה שמעליהם, ודקים בהתאמה לבית. תאמו שיחת ייעוץ.'],
      awning: ['סוככי זרועות חשמליים וידניים בהתאמה אישית | סופר צל', 'סוככי זרועות חשמליים וידניים למרפסות, חזיתות בתים וויטרינות עסקים. אריג וגוון לבחירה. תאמו שיחת ייעוץ.']
    };
    function apply() {
      var m = (location.search.match(/[?&]s=(\w+)/) || [])[1], t = T[m];
      if (!t) return;
      document.title = t[0];
      var d = document.querySelector('meta[name="description"]'); if (d) d.setAttribute('content', t[1]);
    }
    apply(); setTimeout(apply, 1200); setTimeout(apply, 3500);
  })();
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  // Which projects belong to which card. Matching is done on the PROJECT TITLE only (descriptions mention shading everywhere, which put pergolas
  // under shade sails). Each rule: [card title, project title must match, project title must not match, allowed project categories].
  var RULES = [
    [/זרוע/, /זרועות/, /(?!)/, ['shade']],
    [/גגון|קבועים/, /סוכך מעוצב|גגון|גלי/, /(?!)/, ['shade']],
    [/רשת|מפרש/, /מפרש|רשת/, /(?!)/, ['shade']],
    [/סטטיות/, /אלומיניום/, /חשמל|תריס|מתכוונ|עץ טבעי|במבוק|סוכך|מפרש|בטון|סנטף על פרגולת עץ/, ['shade']],
    [/חשמל|תריס/, /תריס|מתכוונ/, /סוכך|זרועות|מפרש/, ['shade', 'glass']],
    [/עץ/, /פרגולת עץ|פרגולה מעץ|דמוי עץ|קונסטרוקציית עץ|פרגולת דק/, /^דק|מעקה זכוכית|^סגירת|מסכי/, ['shade', 'deck']],
    [/שילוב|מעוצב/, /שילוב|מטבח|במבוק|תאורה|חיפוי|גדר|שער|דק /, /משרד|מחיצות/, ['shade', 'envelope']]
  ];
  function tabInfo() {
    var t = document.querySelector('#catalog [role=tab][aria-selected=true]');
    var label = t ? t.textContent.replace(/\s+/g, ' ').replace(/\d+$/, '').trim() : '';
    if (/סגירות/.test(label)) return { tab: 'glass', label: label };
    if (/מטבח/.test(label)) return { tab: 'kitchen', label: label };
    if (/דק/.test(label)) return { tab: 'deck', label: label };
    return { tab: 'shade', label: label };
  }
  function pick(title, info) {
    var list = window.STZ_PROJECTS || [], i, rule = null;
    if (info.tab === 'shade') { for (i = 0; i < RULES.length; i++) if (RULES[i][0].test(title)) { rule = RULES[i]; break; } if (!rule) return []; }
    var scored = [];
    list.forEach(function (p) {
      if (!p.photos || !p.photos.length || /משרד|מחיצות|מפעל/.test(p.title)) return; // home-owner page: no office or factory partitions
      var ok;
      if (rule) ok = rule[3].indexOf(p.cat) > -1 && rule[1].test(p.title) && !rule[2].test(p.title);
      else if (info.tab === 'glass') ok = p.cat === 'glass';
      else if (info.tab === 'deck') ok = p.cat === 'deck';
      else ok = /מטבח|בר /.test(p.title);
      if (ok) scored.push({ p: p, s: 0 });
    });    var shots = [];
    scored.slice(0, 5).forEach(function (x) {
      // one caption per project (its own photo captions if it has them); a project's extra photos carry no repeated title
      x.p.photos.slice(0, shots.length < 2 ? 3 : 1).forEach(function (src, j) {
        if (shots.length >= 6 || shots.some(function (s) { return s.src === src; })) return;
        shots.push({ src: src, cap: (x.p.captions && x.p.captions[j]) || (j === 0 ? x.p.title : '') });
      });
    });
    return shots;
  }
  function build() {
    if (root) return;
    var st = document.createElement('style');
    st.textContent =
      '#stz-dt{position:fixed;inset:0;z-index:520;display:none;align-items:center;justify-content:center;background:rgba(17,14,11,.78);padding:clamp(10px,3vw,32px)}' +
      '#stz-dt.on{display:flex}html.stz-dt-open{overflow:hidden}' +
      '#stz-dt .dt-card{position:relative;width:min(100%,760px);max-height:92vh;overflow:auto;background:#F5F0E4;color:#211C16;border-radius:26px;padding:clamp(1.1rem,2.4vw,1.8rem);animation:dt-in .38s cubic-bezier(.2,.7,.2,1) both}' +
      '#stz-dt .dt-x{position:sticky;top:0;float:inline-end;z-index:3;width:44px;height:44px;border-radius:50%;border:1px solid rgba(33,28,22,.3);background:#F5F0E4;color:#211C16;font-size:22px;line-height:1;cursor:pointer}' +
      '#stz-dt .dt-eb{color:#8A5F24;font-size:13.5px;font-weight:600;letter-spacing:.3px}' +
      '#stz-dt h3{margin:6px 0 0;font-size:clamp(22px,3vw,30px);line-height:1.2}' +
      '#stz-dt .dt-p{margin:12px 0 0;color:#4B443A;font-size:16.5px;line-height:1.6}' +
      '#stz-dt .dt-h{margin:20px 0 8px;font-size:14px;font-weight:600;color:#8A5F24}' +
      '#stz-dt .dt-row{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x proximity;scrollbar-width:none;margin-inline:-4px;padding:0 4px 4px}#stz-dt .dt-row::-webkit-scrollbar{display:none}' +
      '#stz-dt figure{flex:0 0 min(78%,300px);margin:0;scroll-snap-align:start}' +
      '#stz-dt figure img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px;background:#ECE4D2}' +
      '#stz-dt figcaption{margin-top:6px;font-size:13px;line-height:1.35;color:#4B443A}' +
      '#stz-dt .dt-cta{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-top:20px}' +
      '#stz-dt .dt-btn{display:inline-flex;align-items:center;justify-content:center;min-height:50px;padding:0 26px;border:0;border-radius:100px;background:#B4813C;color:#1B1712;font:inherit;font-size:16px;font-weight:600;cursor:pointer}' +
      '#stz-dt .dt-lnk{color:#6E4D1E;font-size:15px;font-weight:600;border-bottom:1px solid rgba(110,77,30,.4);min-height:44px;display:inline-flex;align-items:center}' +
      '@keyframes dt-in{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}' +
      '@media (max-width:700px){#stz-dt{align-items:flex-end;padding:0}#stz-dt .dt-card{width:100%;max-height:90vh;border-radius:24px 24px 0 0}#stz-dt .dt-btn{width:100%}}';
    document.head.appendChild(st);
    root = document.createElement('div'); root.id = 'stz-dt';
    root.setAttribute('role', 'dialog'); root.setAttribute('aria-modal', 'true'); root.setAttribute('aria-label', 'פרטי הפתרון');
    root.addEventListener('click', function (e) { if (e.target === root || e.target.closest('.dt-x')) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    document.body.appendChild(root);
  }
  function close() { if (!root) return; root.classList.remove('on'); document.documentElement.classList.remove('stz-dt-open'); }
  function open(card) {
    build();
    var h = card.querySelector('h3'), title = h ? h.textContent.replace(/\s*\+\s*$/, '').trim() : '';
    var eb = card.querySelector('span[style*="E8C48C"]'), ebT = eb ? eb.textContent.replace(/\s+/g, ' ').trim() : '';
    var sum = (card.querySelector('.stz-gsum') || {}).textContent || '';
    var rest = (card.querySelector('.stz-gmore p') || {}).textContent || '';
    var img = card.querySelector('img'), info = tabInfo(), shots = pick(title, info);
    if (!shots.length && img) shots = [{ src: img.getAttribute('src'), cap: title }];
    var catKey = { glass: 'glass', deck: 'deck', kitchen: 'envelope', shade: 'shade' }[info.tab] || 'shade';
    root.innerHTML =
      '<div class="dt-card"><button type="button" class="dt-x" aria-label="סגירה">&times;</button>' +
      '<div class="dt-eb">' + esc(ebT) + '</div><h3>' + esc(title) + '</h3>' +
      (sum ? '<p class="dt-p">' + esc(sum.trim()) + '</p>' : '') + (rest ? '<p class="dt-p">' + esc(rest.trim()) + '</p>' : '') +
      (shots.length ? '<div class="dt-h">דוגמאות מפרויקטים שביצענו</div><div class="dt-row">' + shots.map(function (s) { return '<figure><img src="' + esc(s.src) + '" alt="' + esc(s.cap || title) + '" loading="lazy" decoding="async">' + (s.cap ? '<figcaption>' + esc(s.cap) + '</figcaption>' : '') + '</figure>'; }).join('') + '</div>' : '') +
      '<div class="dt-cta"><button type="button" class="dt-btn" data-lead-open>לתיאום שיחת ייעוץ</button><a class="dt-lnk" href="/projects?cat=' + catKey + '">לכל הפרויקטים בקטגוריה ←</a></div></div>';
    root.querySelector('.dt-btn').addEventListener('click', function () { setTimeout(close, 0); });
    root.classList.add('on'); document.documentElement.classList.add('stz-dt-open');
    root.querySelector('.dt-card').scrollTop = 0;
    try { window.stzTrack && window.stzTrack('catalog_detail_open', { item: title }); } catch (e) {}
  }
  // capture phase: runs before the mobile "tap shows the summary" handler, which is then skipped for this tap
  document.addEventListener('click', function (e) {
    var card = e.target.closest && e.target.closest('#catalog .stz-gcard');
    if (!card || e.target.closest('a,button')) return;
    e.stopPropagation();
    open(card);
  }, true);
  document.addEventListener('keydown', function (e) {
    if ((e.key === 'Enter' || e.key === ' ') && e.target && e.target.classList && e.target.classList.contains('stz-gcard') && e.target.closest('#catalog')) { e.preventDefault(); open(e.target); }
  });

  // ---- always-visible "add to my enquiry" tick on every catalog card (it drives the hidden toggle inside the card, so the choice is sent with the enquiry)
  var pcss = document.createElement('style');
  pcss.textContent =
    '#catalog .stz-gcard .stz-pick{position:absolute;top:10px;inset-inline-end:10px;z-index:5;display:grid;place-items:center;width:44px;height:44px;border-radius:50%;border:1.5px solid rgba(245,240,228,.85);background:rgba(27,23,18,.55);color:#F5F0E4;font:inherit;font-size:24px;line-height:1;cursor:pointer;backdrop-filter:blur(3px);transition:background .2s,border-color .2s,transform .15s}' +
    '#catalog .stz-gcard .stz-pick[aria-pressed=true]{background:#B4813C;border-color:#B4813C;color:#1B1712;font-size:22px;font-weight:700}' +
    '#catalog .stz-gcard .stz-pick:active{transform:scale(.92)}' +
    '#catalog .stz-gcard .stz-pick-t{position:absolute;top:18px;inset-inline-end:60px;z-index:5;padding:3px 10px;border-radius:100px;background:rgba(27,23,18,.7);color:#E8C48C;font-size:12.5px;font-weight:600;pointer-events:none;opacity:0;transition:opacity .2s}' +
    '#catalog .stz-gcard .stz-pick[aria-pressed=true]+.stz-pick-t{opacity:1}';
  document.head.appendChild(pcss);
  function hiddenPk(card) { return card.querySelector('.stz-gmore button[aria-pressed]'); }
  function syncPicks() {
    [].forEach.call(document.querySelectorAll('#catalog .stz-gcard'), function (card) {
      var hp = hiddenPk(card), b = card.querySelector('.stz-pick');
      if (!hp) { if (b) { b.remove(); var t0 = card.querySelector('.stz-pick-t'); if (t0) t0.remove(); } return; }
      if (!b) {
        b = document.createElement('button'); b.type = 'button'; b.className = 'stz-pick'; b.setAttribute('aria-label', 'הוסיפו לפנייה');
        var t = document.createElement('span'); t.className = 'stz-pick-t'; t.textContent = 'נוסף לפנייה';
        card.appendChild(b); card.appendChild(t);
      }
      var on = hp.getAttribute('aria-pressed') === 'true';
      b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.textContent = on ? '✓' : '';
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('#catalog .stz-pick');
    if (!b) return;
    e.stopPropagation(); e.preventDefault();
    var hp = hiddenPk(b.closest('.stz-gcard')); if (hp) hp.click();
    setTimeout(syncPicks, 60);
  }, true);
  var pk = 0;
  (function wait() {
    var cat = document.getElementById('catalog');
    if (cat && !cat.closest('x-dc')) {
      syncPicks();
      new MutationObserver(function () { clearTimeout(pk); pk = setTimeout(syncPicks, 80); }).observe(cat, { childList: true, subtree: true, attributes: true, attributeFilter: ['aria-pressed'] });
    } else setTimeout(wait, 400);
  })();

  // ---- slim, inviting simulator strip right under the projects (the full banner stays further down)
  var scss = document.createElement('style');
  scss.textContent =
    '#sun-teaser{width:min(var(--stz-side,92%),var(--stz-max,1180px));margin:0 auto;padding-block:6px}' +
    '#sun-teaser button{display:flex;align-items:center;gap:14px;width:100%;min-height:64px;padding:10px 18px;border:0;border-radius:100px;background:#1B1712;color:#F5F0E4;font:inherit;cursor:pointer;text-align:start;box-shadow:0 14px 30px -20px rgba(33,28,22,.6)}' +
    '#sun-teaser .st-dot{flex:none;width:28px;height:28px;border-radius:50%;background:#E8B45C;box-shadow:0 0 0 6px rgba(232,180,92,.18),0 0 26px rgba(232,180,92,.55);animation:st-pulse 2.4s ease-in-out infinite}' +
    '#sun-teaser .st-t{flex:1 1 auto;min-width:0;font-size:15.5px;font-weight:600;line-height:1.3}#sun-teaser .st-t small{display:block;font-size:13px;font-weight:400;color:rgba(245,240,228,.75)}' +
    '#sun-teaser .st-go{flex:none;min-height:40px;padding:0 18px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:14.5px;font-weight:600;display:inline-flex;align-items:center}' +
    '@keyframes st-pulse{0%,100%{box-shadow:0 0 0 6px rgba(232,180,92,.18),0 0 26px rgba(232,180,92,.55)}50%{box-shadow:0 0 0 12px rgba(232,180,92,.08),0 0 38px rgba(232,180,92,.8)}}' +
    '@media (prefers-reduced-motion:reduce){#sun-teaser .st-dot{animation:none}}' +
    '@media (max-width:520px){#sun-teaser .st-go{padding:0 12px;font-size:13.5px}#sun-teaser .st-t small{display:none}}';
  document.head.appendChild(scss);
  var st = 0;
  (function placeTeaser() {
    var pr = document.getElementById('projects'), card = document.querySelector('#sun .stz-sun-card');
    if (pr && !pr.closest('x-dc') && card) {
      var tz = document.getElementById('sun-teaser');
      if (!tz) {
        tz = document.createElement('div'); tz.id = 'sun-teaser';
        tz.innerHTML = '<button type="button" aria-label="פתחו את סימולטור השמש"><span class="st-dot" aria-hidden="true"></span><span class="st-t">איך השמש נופלת אצלכם בשטח?<small>שחקו עם כיוון, עונה ושעה, עם פרגולה ובלי</small></span><span class="st-go">נסו את הסימולטור</span></button>';
        tz.querySelector('button').addEventListener('click', function () { var c = document.querySelector('#sun .stz-sun-card'); if (c) c.click(); });
      }
      if (pr.nextElementSibling !== tz) pr.parentNode.insertBefore(tz, pr.nextSibling);
    }
    if (++st < 40) setTimeout(placeTeaser, st < 20 ? 500 : 1500);
  })();
})();
