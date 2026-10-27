// "פרויקטים שביצענו" section for the pergola landing page. Built from projects-data.js, placed right after the 'who we are' section (or after #why).
(function () {
  if (window.__stzLandingProjects) return;
  window.__stzLandingProjects = true;
  // Sections are inserted after the browser has already jumped to a #anchor, which shifts the layout.
  // Re-align to the anchor after each insert, unless the visitor has already started scrolling.
  var touched = false;
  ['wheel', 'touchmove', 'keydown', 'mousedown'].forEach(function (ev) { addEventListener(ev, function () { touched = true; }, { passive: true, once: true }); });
  function realign() {
    if (touched || !location.hash || location.hash.length < 2) return;
    var t = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (t) t.scrollIntoView();
  }
  // Three flagship projects, three different outdoor-envelope styles (a full envelope, hosting, a balcony); a tagline under each title.
  var PICK = ['new-46-3', 'kitchen-1', 'balcony-electric-pergola-window'];
  var TAG = { 'new-46-3': 'כפר סבא · חזרנו ללקוח מ-2024 להשלים את מרחב החוץ', 'kitchen-1': 'מרחב אירוח בחוץ · מטבח, בר ופינת ישיבה', 'balcony-electric-pergola-window': 'מרפסת עם שליטה באור ובצל בלחיצת כפתור' };
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  // The page runtime re-renders while it boots and can drop or reorder nodes that were inserted by hand. Sections are only
  // inserted into the rendered page (never into the inert <x-dc> template) and are put back into place if they drift.
  function rendered(el) { return !!el && !el.closest('x-dc'); }
  function place(sec) {
    var why = document.getElementById('why');
    if (!rendered(why)) return false;
    var about = document.getElementById('about');
    var anchor = rendered(about) && about.parentNode === why.parentNode ? about : why;
    if (anchor.nextElementSibling !== sec) anchor.parentNode.insertBefore(sec, anchor.nextSibling);
    return true;
  }
  function build() {
    var existing = document.getElementById('projects');
    if (existing && rendered(existing)) return place(existing);
    var list = window.STZ_PROJECTS;
    if (!rendered(document.getElementById('why')) || !list) return false;
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
      '#projects .lp-card{position:relative;display:block;padding:0;border:0;border-radius:18px;overflow:hidden;aspect-ratio:4/3;cursor:pointer;background:#1B1712;font:inherit;text-align:start}' +
      '#projects .lp-card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .5s ease}' +
      '#projects .lp-card:hover img{transform:scale(1.04)}' +
      '#projects .lp-grid.lp-feat{grid-template-columns:repeat(3,1fr);gap:16px}#projects .lp-feat .lp-card{aspect-ratio:3/4;border-radius:22px}#projects .lp-feat .lp-card span{font-size:19px;padding:60px 18px 18px;line-height:1.25}#projects .lp-feat .lp-card em{display:block;margin-top:6px;font-style:normal;font-size:13.5px;font-weight:500;color:#E8C48C;line-height:1.35}#projects .lp-feat .lp-card b{position:absolute;top:12px;inset-inline-start:12px;background:rgba(27,23,18,.78);color:#E8C48C;font-size:12.5px;font-weight:600;padding:4px 12px;border-radius:100px}' +
      '@media (max-width:900px){#projects .lp-grid.lp-feat{grid-template-columns:1fr;gap:14px}#projects .lp-feat .lp-card{aspect-ratio:4/5}#projects .lp-feat .lp-card span{font-size:18px;padding:56px 16px 16px}}' +
      '#projects .lp-card span{position:absolute;inset-inline:0;bottom:0;padding:34px 16px 14px;color:#fff;font-size:15.5px;font-weight:600;line-height:1.3;background:linear-gradient(0deg,rgba(17,14,11,.88),rgba(17,14,11,0))}' +
      '@media (max-width:900px){#projects .lp-grid{grid-template-columns:repeat(2,1fr);gap:10px}#projects .lp-card:nth-child(9){display:none}#projects .lp-card span{font-size:13.5px;padding:26px 12px 11px}}' +
      '#lp-box{position:fixed;inset:0;z-index:2147483100;background:rgba(14,11,8,.9);display:flex;align-items:center;justify-content:center;padding:16px}' +
      '#lp-box .lb-card{position:relative;width:min(980px,100%);max-height:92vh;overflow:auto;background:#F5F0E4;border-radius:20px;display:grid;grid-template-columns:1.3fr 1fr}' +
      '#lp-box .lb-ph{position:relative;background:#1B1712;min-height:320px}' +
      '#lp-box .lb-ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}' +
      '#lp-box .lb-nav{position:absolute;top:50%;transform:translateY(-50%);width:42px;height:42px;border-radius:50%;border:0;background:rgba(27,23,18,.7);color:#F5F0E4;font-size:20px;cursor:pointer}' +
      '#lp-box .lb-count{position:absolute;bottom:10px;inset-inline-start:10px;background:rgba(27,23,18,.75);color:#E8C48C;font-size:12.5px;padding:3px 10px;border-radius:100px}' +
      '#lp-box .lb-txt{padding:26px 24px;display:flex;flex-direction:column;gap:12px;color:#211C16}' +
      '#lp-box .lb-meta{color:#8F6326;font-size:14px;font-weight:600}' +
      '#lp-box .lb-txt p{color:#4B443A;font-size:15.5px;line-height:1.6;margin:0}' +
      '#lp-box .lb-txt ul{margin:0;padding-inline-start:18px;color:#4B443A;font-size:14.5px;line-height:1.55}' +
      '#lp-box .lb-cta{align-self:flex-start;margin-top:6px;display:inline-flex;align-items:center;min-height:48px;padding:0 24px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:15.5px;font-weight:600;text-decoration:none}' +
      '#lp-box .lb-x{position:absolute;top:12px;inset-inline-end:12px;z-index:2;width:44px;height:44px;border-radius:50%;border:0;background:rgba(27,23,18,.75);color:#F5F0E4;font-size:22px;cursor:pointer}' +
      '@media (max-width:760px){#lp-box{padding:0;align-items:flex-end}#lp-box .lb-card{grid-template-columns:1fr;border-radius:20px 20px 0 0;max-height:94vh}#lp-box .lb-ph{min-height:0;aspect-ratio:4/3}#lp-box .lb-txt{padding:20px 18px 26px}}';
    if (!css.parentNode) document.head.appendChild(css);
    var sec = document.createElement('section');
    sec.id = 'projects';
    sec.style.cssText = 'padding-block:0 clamp(3rem,8vh,5.5rem)';
    var html = '<div style="width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto">' +
      '<div style="display:inline-flex;align-items:center;gap:10px;color:#B4813C;font-size:14.5px;font-weight:600;margin-bottom:18px;white-space:nowrap"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>פרויקטים שביצענו</div>' +
      '<h2 style="font-size:clamp(28px,3.6vw,44px);letter-spacing:-0.02em;line-height:1.12;max-width:20ch">כך זה נראה אצל לקוחות</h2>' +
      '<p style="margin:14px 0 clamp(1.25rem,3vh,2rem);color:#4B443A;font-size:17px;max-width:52ch">שלושה פרויקטים, שלושה סגנונות של מעטפת חוץ. לחצו על פרויקט לפרטים ולתמונות נוספות.</p>' +
      '<div class="lp-grid lp-feat">';
    cards.forEach(function (c, i) {
      var tg = ''; Object.keys(TAG).forEach(function (k) { if (c.src.indexOf('/' + k + '.webp') > -1) tg = TAG[k]; });
      html += '<button type="button" class="lp-card" data-i="' + i + '"><img src="' + esc(c.src) + '" alt="' + esc(c.p.title) + '" loading="lazy" decoding="async"><b>0' + (i + 1) + '</b><span>' + esc(c.p.title) + (tg ? '<em>' + esc(tg) + '</em>' : '') + '</span></button>';
    });
    html += '</div>' +
      '<div style="margin-top:clamp(1.5rem,3vh,2.25rem);display:flex;flex-wrap:wrap;gap:12px"><a href="#lead" style="display:inline-flex;align-items:center;min-height:48px;padding:0 26px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:16px;font-weight:600">תאמו שיחת ייעוץ</a>' +
      '<a href="/projects" class="lp-all" style="display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 24px;border-radius:100px;border:1px solid rgba(33,28,22,0.3);color:#211C16;font-size:16px;font-weight:600">לכל ' + list.length + ' הפרויקטים <span aria-hidden="true">←</span></a></div></div>';
    sec.innerHTML = html;
    place(sec);
    realign();
    // (the before / after slider above the grid comes from ba-story.js; the three flagship tiles do not rotate)
    sec.addEventListener('click', function (e) {
      var b = e.target.closest('.lp-card'); if (!b) return;
      // Project details: photos with next / previous, place and client, description and specs, and a consultation button.
      var c = cards[+b.getAttribute('data-i')], p = c.p, ph = c.all, at = Math.max(0, ph.indexOf(c.src));
      var CAT = { shade: 'הצללה וקירוי', glass: 'סגירות', envelope: 'בנייה קלה ומעטפת חוץ', deck: 'דקים ופיתוח', fence: 'גידור וחיפויים' };
      var meta = [p.place, p.client ? 'לקוח ' + p.client : '', CAT[p.cat]].filter(Boolean).join(' · ');
      var box = document.createElement('div'); box.id = 'lp-box'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', p.title);
      box.innerHTML = '<div class="lb-card"><button type="button" class="lb-x" aria-label="סגירה">×</button>' +
        '<div class="lb-ph"><img alt="' + esc(p.title) + '">' +
        (ph.length > 1 ? '<button type="button" class="lb-nav" data-d="-1" aria-label="התמונה הקודמת" style="inset-inline-start:10px">›</button><button type="button" class="lb-nav" data-d="1" aria-label="התמונה הבאה" style="inset-inline-end:10px">‹</button><span class="lb-count"></span>' : '') +
        '</div><div class="lb-txt"><h3 style="font-size:22px;line-height:1.25;margin:0">' + esc(p.title) + '</h3>' +
        (meta ? '<div class="lb-meta">' + esc(meta) + '</div>' : '') +
        (p.desc ? '<p>' + esc(p.desc) + '</p>' : '') +
        (p.specs && p.specs.length ? '<ul>' + p.specs.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ul>' : '') +
        '<a href="#lead" class="lb-cta">רוצים משהו דומה? לשיחת ייעוץ</a></div></div>';
      var img = box.querySelector('.lb-ph img'), cnt = box.querySelector('.lb-count');
      function show() { img.src = ph[at]; if (p.captions && p.captions[at]) img.alt = p.captions[at]; if (cnt) cnt.textContent = (at + 1) + ' / ' + ph.length; }
      function close() { box.remove(); removeEventListener('keydown', key); document.documentElement.style.overflow = ''; }
      function key(ev) { if (ev.key === 'Escape') close(); }
      box.addEventListener('click', function (ev) {
        var nav = ev.target.closest('.lb-nav');
        if (nav) { at = (at + (+nav.getAttribute('data-d')) + ph.length) % ph.length; show(); return; }
        if (ev.target === box || ev.target.closest('.lb-x') || ev.target.closest('.lb-cta')) close();
      });
      addEventListener('keydown', key);
      show();
      document.documentElement.style.overflow = 'hidden';
      document.body.appendChild(box);
      try { box.querySelector('.lb-x').focus(); } catch (x) {}
    });
    return true;
  }
  // Every few seconds one tile fades to another project from the catalog, so the grid shows the range of projects.
  function rotate(sec, cards, list) {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var shown = cards.map(function (c) { return c.p; });
    var pool = list.filter(function (p) { return p.photos && p.photos.length && shown.indexOf(p) < 0; });
    var hover = -1, last = -1;
    sec.addEventListener('pointerover', function (e) { var b = e.target.closest('.lp-card'); hover = b ? +b.getAttribute('data-i') : -1; });
    sec.addEventListener('pointerleave', function () { hover = -1; });
    setInterval(function () {
      if (!pool.length || document.hidden || document.getElementById('lp-box')) return;
      var r = sec.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
      var btns = sec.querySelectorAll('.lp-card'), i;
      do { i = Math.floor(Math.random() * btns.length); } while ((i === hover || i === last || btns[i].offsetParent === null) && btns.length > 2);
      last = i;
      var next = pool.shift(), b = btns[i], img = b.querySelector('img'), lab = b.querySelector('span');
      pool.push(cards[i].p);
      var pre = new Image();
      pre.onload = function () {
        img.style.transition = 'opacity .6s ease'; lab.style.transition = 'opacity .6s ease';
        img.style.opacity = '0'; lab.style.opacity = '0';
        setTimeout(function () {
          img.src = next.photos[0]; img.alt = next.title; lab.textContent = next.title;
          cards[i] = { p: next, src: next.photos[0], all: next.photos };
          img.style.opacity = '1'; lab.style.opacity = '1';
        }, 600);
      };
      pre.src = next.photos[0];
    }, 3200);
  }

  function start() {
    var tries = 0;
    (function tick() { var had = !!document.getElementById('projects'); build(); if (tries < 28 && had) realign(); if (++tries > 80) return; setTimeout(tick, tries < 40 ? 250 : 1000); })();
  }
  if (window.STZ_PROJECTS) start();
  else { var s = document.createElement('script'); s.src = '/projects-data.js?v=3'; s.onload = start; document.head.appendChild(s); }
})();
