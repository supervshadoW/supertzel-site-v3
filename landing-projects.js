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
  var PICK = ['pergola-modern-lighting-1', 'pergola-white-wood', 'balcony-electric-pergola-window', 'winter-1', 'project-deck-view', 'pergola-cream-louvers', 'glass-1', 'pergola-lighting-rishon', 'awning-jaffa-1'];
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
      '<p style="margin:14px 0 clamp(1.25rem,3vh,2rem);color:#4B443A;font-size:17px;max-width:52ch">פרגולות, סגירות והצללה מפרויקטים שבוצעו. לחצו על פרויקט לפרטים ולתמונות נוספות.</p>' +
      '<div class="lp-grid">';
    cards.forEach(function (c, i) {
      html += '<button type="button" class="lp-card" data-i="' + i + '"><img src="' + esc(c.src) + '" alt="' + esc(c.p.title) + '" loading="lazy" decoding="async"><span>' + esc(c.p.title) + '</span></button>';
    });
    html += '</div>' +
      '<div style="margin-top:clamp(1.5rem,3vh,2.25rem);display:flex;flex-wrap:wrap;gap:12px"><a href="#lead" style="display:inline-flex;align-items:center;min-height:48px;padding:0 26px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:16px;font-weight:600">תאמו שיחת ייעוץ</a>' +
      '<a href="/projects" class="lp-all" style="display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 24px;border-radius:100px;border:1px solid rgba(33,28,22,0.3);color:#211C16;font-size:16px;font-weight:600">לכל ' + list.length + ' הפרויקטים <span aria-hidden="true">←</span></a></div></div>';
    sec.innerHTML = html;
    place(sec);
    realign();
    rotate(sec, cards, list);
    beforeAfter(sec);
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

  // Before / after of the Kfar Saba driveway: drag the handle (or use the arrow keys) to compare.
  function beforeAfter(sec) {
    var grid = sec.querySelector('.lp-grid');
    if (!grid || sec.querySelector('.ba')) return;
    var css = document.createElement('style');
    css.textContent =
      '#projects .ba{position:relative;aspect-ratio:2.14/1;border-radius:18px;overflow:hidden;margin-bottom:14px;background:#1B1712;touch-action:pan-y;user-select:none;cursor:ew-resize}' +
      '#projects .ba img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none}' +
      '#projects .ba .ba-top{clip-path:inset(0 0 0 var(--x,50%))}' +
      // zoom the after photo slightly from its left edge so the third-party street sign at the far right stays out of frame
      '#projects .ba .ba-top{transform:scale(1.16);transform-origin:0 55%;clip-path:inset(0 0 0 calc(var(--x,50%) / 1.16))}' +
      '#projects .ba .ba-bar{position:absolute;top:0;bottom:0;left:var(--x,50%);width:3px;margin-left:-1.5px;background:#E8C48C;box-shadow:0 0 12px rgba(0,0,0,.5)}' +
      '#projects .ba .ba-knob{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:46px;height:46px;border-radius:50%;background:#E8C48C;color:#1B1712;display:grid;place-items:center;font-size:18px;font-weight:700;box-shadow:0 4px 18px rgba(0,0,0,.45)}' +
      '#projects .ba .ba-l{position:absolute;top:12px;padding:5px 12px;border-radius:100px;background:rgba(27,23,18,.78);color:#F5F0E4;font-size:13.5px;font-weight:600}' +
      '#projects .ba-cap{margin:0 0 clamp(1.5rem,3vh,2rem);color:#4B443A;font-size:15px}' +
      '@media (max-width:760px){#projects .ba{aspect-ratio:4/3}}';
    document.head.appendChild(css);
    var ba = document.createElement('div');
    ba.className = 'ba'; ba.setAttribute('role', 'slider'); ba.setAttribute('tabindex', '0');
    ba.setAttribute('aria-label', 'לפני ואחרי: גררו כדי להשוות'); ba.setAttribute('aria-valuemin', '0'); ba.setAttribute('aria-valuemax', '100');
    ba.innerHTML = '<img src="/img/fast/gallery/before-46-1.jpg" alt="לפני: חניה בשלבי פירוק ועבודות עפר" loading="lazy" decoding="async">' +
      '<img class="ba-top" src="/img/fast/gallery/new-46-3.webp" alt="אחרי: יציקת בטון, פרגולת אלומיניום ושער חשמלי" loading="lazy" decoding="async">' +
      '<span class="ba-l" style="left:12px">לפני</span><span class="ba-l" style="right:12px">אחרי</span>' +
      '<div class="ba-bar"><span class="ba-knob" aria-hidden="true">⇆</span></div>';
    var cap = document.createElement('p');
    cap.className = 'ba-cap';
    cap.textContent = 'לפני ואחרי · כפר סבא: יציקת בטון, פרגולת אלומיניום עם תאורה ושער חשמלי. גררו את הפס כדי להשוות.';
    grid.parentNode.insertBefore(ba, grid);
    grid.parentNode.insertBefore(cap, grid);
    function set(p) { p = Math.max(0, Math.min(100, p)); ba.style.setProperty('--x', p + '%'); ba.setAttribute('aria-valuenow', Math.round(p)); }
    function at(e) { var r = ba.getBoundingClientRect(); set((e.clientX - r.left) / r.width * 100); }
    var drag = false;
    ba.addEventListener('pointerdown', function (e) { drag = true; try { ba.setPointerCapture(e.pointerId); } catch (x) {} at(e); });
    ba.addEventListener('pointermove', function (e) { if (drag) at(e); });
    ba.addEventListener('pointerup', function () { drag = false; });
    ba.addEventListener('pointercancel', function () { drag = false; });
    ba.addEventListener('keydown', function (e) {
      var v = parseFloat(ba.style.getPropertyValue('--x')) || 50;
      if (e.key === 'ArrowLeft') { set(v - 5); e.preventDefault(); } else if (e.key === 'ArrowRight') { set(v + 5); e.preventDefault(); }
    });
    set(50);
  }

  function start() {
    var tries = 0;
    (function tick() { var had = !!document.getElementById('projects'); build(); if (tries < 28 && had) realign(); if (++tries > 80) return; setTimeout(tick, tries < 40 ? 250 : 1000); })();
  }
  if (window.STZ_PROJECTS) start();
  else { var s = document.createElement('script'); s.src = '/projects-data.js?v=3'; s.onload = start; document.head.appendChild(s); }
})();
