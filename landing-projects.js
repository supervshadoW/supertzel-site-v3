// "פרויקטים שביצענו" section for the pergola landing page. Built from projects-data.js, inserted before #why.
(function () {
  // Sections are inserted after the browser has already jumped to a #anchor, which shifts the layout.
  // Re-align to the anchor after each insert, unless the visitor has already started scrolling.
  var touched = false;
  ['wheel', 'touchmove', 'keydown', 'mousedown'].forEach(function (ev) { addEventListener(ev, function () { touched = true; }, { passive: true, once: true }); });
  function realign() {
    if (touched || !location.hash || location.hash.length < 2) return;
    var t = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (t) t.scrollIntoView();
  }
  var PICK = ['pergola-modern-lighting-1', 'pergola-white-wood', 'balcony-electric-pergola-window', 'winter-1', 'project-deck-view', 'pergola-cream-louvers', 'glass-1', 'pergola-lighting-rishon', 'awning-jaffa-1'];
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function build() {
    if (document.getElementById('projects')) return true;
    var anchor = document.getElementById('why');
    var list = window.STZ_PROJECTS;
    if (!anchor || !list) return false;
    var cards = [];
    PICK.forEach(function (key) {
      for (var i = 0; i < list.length; i++) {
        var p = list[i], ph = p.photos || [];
        for (var j = 0; j < ph.length; j++) if (ph[j].indexOf('/' + key + '.webp') > -1) { cards.push({ p: p, src: ph[j], all: ph }); return; }
      }
    });
    if (cards.length < 3) return true;
    var css = document.getElementById('projects-css') || document.createElement('style'); css.id = 'projects-css';
    css.textContent =
      '#projects .lp-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}' +
      '#projects .lp-card{position:relative;display:block;padding:0;border:0;border-radius:18px;overflow:hidden;aspect-ratio:4/3;cursor:zoom-in;background:#1B1712;font:inherit;text-align:start}' +
      '#projects .lp-card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .5s ease}' +
      '#projects .lp-card:hover img{transform:scale(1.04)}' +
      '#projects .lp-card span{position:absolute;inset-inline:0;bottom:0;padding:34px 16px 14px;color:#fff;font-size:15.5px;font-weight:600;line-height:1.3;background:linear-gradient(0deg,rgba(17,14,11,.88),rgba(17,14,11,0))}' +
      '@media (max-width:900px){#projects .lp-grid{grid-template-columns:repeat(2,1fr);gap:10px}#projects .lp-card:nth-child(9){display:none}#projects .lp-card span{font-size:13.5px;padding:26px 12px 11px}}' +
      '#lp-box{position:fixed;inset:0;z-index:2147483100;background:rgba(14,11,8,.94);display:flex;align-items:center;justify-content:center;padding:16px}' +
      '#lp-box img{max-width:100%;max-height:88vh;border-radius:12px;object-fit:contain}' +
      '#lp-box button{position:absolute;top:14px;inset-inline-start:14px;width:44px;height:44px;border-radius:50%;border:1px solid rgba(245,240,228,.5);background:rgba(27,23,18,.7);color:#F5F0E4;font-size:22px;cursor:pointer}';
    if (!css.parentNode) document.head.appendChild(css);
    var sec = document.createElement('section');
    sec.id = 'projects';
    sec.style.cssText = 'padding-block:0 clamp(3rem,8vh,5.5rem)';
    var html = '<div style="width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto">' +
      '<div style="display:inline-flex;align-items:center;gap:10px;color:#B4813C;font-size:14.5px;font-weight:600;margin-bottom:18px;white-space:nowrap"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>פרויקטים שביצענו</div>' +
      '<h2 style="font-size:clamp(28px,3.6vw,44px);letter-spacing:-0.02em;line-height:1.12;max-width:20ch">כך זה נראה אצל לקוחות</h2>' +
      '<p style="margin:14px 0 clamp(1.25rem,3vh,2rem);color:#4B443A;font-size:17px;max-width:52ch">פרגולות, סגירות והצללה מפרויקטים שבוצעו. לחצו על תמונה להגדלה.</p>' +
      '<div class="lp-grid">';
    cards.forEach(function (c, i) {
      html += '<button type="button" class="lp-card" data-i="' + i + '"><img src="' + esc(c.src) + '" alt="' + esc(c.p.title) + '" loading="lazy" decoding="async"><span>' + esc(c.p.title) + '</span></button>';
    });
    html += '</div>' +
      '<div style="margin-top:clamp(1.5rem,3vh,2.25rem)"><a href="#lead" style="display:inline-flex;align-items:center;min-height:48px;padding:0 26px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:16px;font-weight:600">תאמו שיחת ייעוץ</a></div></div>';
    sec.innerHTML = html;
    anchor.parentNode.insertBefore(sec, anchor);
    realign();
    sec.addEventListener('click', function (e) {
      var b = e.target.closest('.lp-card'); if (!b) return;
      var c = cards[+b.getAttribute('data-i')];
      var box = document.createElement('div'); box.id = 'lp-box'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-label', c.p.title);
      box.innerHTML = '<img src="' + esc(c.src) + '" alt="' + esc(c.p.title) + '"><button type="button" aria-label="סגירה">×</button>';
      function close() { box.remove(); removeEventListener('keydown', key); }
      function key(ev) { if (ev.key === 'Escape') close(); }
      box.addEventListener('click', close); addEventListener('keydown', key);
      document.body.appendChild(box);
    });
    return true;
  }
  function start() {
    var tries = 0;
    (function tick() { build(); if (tries < 14) realign(); if (++tries > 60) return; setTimeout(tick, 500); })();
  }
  if (window.STZ_PROJECTS) start();
  else { var s = document.createElement('script'); s.src = '/projects-data.js?v=2'; s.onload = start; document.head.appendChild(s); }
})();
