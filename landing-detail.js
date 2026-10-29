// Catalog detail sheet for the pergola landing page: a tap on a catalog card opens a sheet with the full text and real project photos
// for that solution (taken from projects-data.js), plus the consult CTA and a link to the matching projects category.
// Mobile: slides up from the bottom. Desktop: centred dialog.
(function () {
  if (window.__stzDetail) return;
  window.__stzDetail = true;
  var root = null;
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  // which projects fit which card: keywords found in the card title -> keywords looked for in the project title / description
  var KW = [
    [/סטטיות|אלומיניום/, ['אלומיניום']],
    [/חשמל|תריס/, ['חשמל', 'תריס', 'מתכווננ']],
    [/עץ/, ['עץ']],
    [/שילוב|מעוצב/, ['מטבח', 'זכוכית', 'גדר', 'דק', 'שער']],
    [/זרוע/, ['זרוע', 'סוכך']],
    [/גגון|סוככים/, ['גגון', 'סוכך']],
    [/רשת|מפרש/, ['רשת', 'מפרש', 'צל']]
  ];
  function tabInfo() {
    var t = document.querySelector('#catalog [role=tab][aria-selected=true]');
    var label = t ? t.textContent.replace(/\s+/g, ' ').replace(/\d+$/, '').trim() : '';
    if (/סגירות/.test(label)) return { cat: 'glass', label: label };
    if (/מטבח/.test(label)) return { cat: '', kw: ['מטבח', 'בר'], label: label };
    if (/דק/.test(label)) return { cat: 'deck', label: label };
    return { cat: 'shade', label: label };
  }
  function pick(title, info) {
    var list = window.STZ_PROJECTS || [], kws = null, i;
    for (i = 0; i < KW.length; i++) if (KW[i][0].test(title)) { kws = KW[i][1]; break; }
    if (info.kw) kws = info.kw;
    var scored = [];
    list.forEach(function (p) {
      if (!p.photos || !p.photos.length) return;
      if (info.cat && p.cat !== info.cat && !(info.cat === 'shade' && /שילוב|מעוצב/.test(title) && p.cat === 'envelope')) return;
      var hay = (p.title + ' ' + (p.desc || '')), s = 0;
      if (kws) kws.forEach(function (k) { if (hay.indexOf(k) > -1) s++; });
      if (kws && !s) return;
      scored.push({ p: p, s: s });
    });
    scored.sort(function (a, b) { return b.s - a.s; });
    var shots = [];
    scored.slice(0, 5).forEach(function (x) {
      x.p.photos.slice(0, shots.length < 2 ? 3 : 1).forEach(function (src, j) { if (shots.length < 6) shots.push({ src: src, cap: (x.p.captions && x.p.captions[j]) || x.p.title }); });
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
    var catKey = info.cat || (info.kw ? 'envelope' : 'shade');
    root.innerHTML =
      '<div class="dt-card"><button type="button" class="dt-x" aria-label="סגירה">&times;</button>' +
      '<div class="dt-eb">' + esc(ebT) + '</div><h3>' + esc(title) + '</h3>' +
      (sum ? '<p class="dt-p">' + esc(sum.trim()) + '</p>' : '') + (rest ? '<p class="dt-p">' + esc(rest.trim()) + '</p>' : '') +
      (shots.length ? '<div class="dt-h">דוגמאות מפרויקטים שביצענו</div><div class="dt-row">' + shots.map(function (s) { return '<figure><img src="' + esc(s.src) + '" alt="' + esc(s.cap) + '" loading="lazy" decoding="async"><figcaption>' + esc(s.cap) + '</figcaption></figure>'; }).join('') + '</div>' : '') +
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
