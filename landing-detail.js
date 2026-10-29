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
    [/עץ/, /עץ/, /סגירת|מסכי/, ['shade', 'deck']],
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
})();
