// Before / after slider (deck renovation, same camera angle) in the projects section, and a "from the field" photo
// panel next to the work-steps slider that follows the active step. Used on the home page and the pergola landing page.
(function () {
  if (window.__stzBaStory) return;
  window.__stzBaStory = true;
  var G = '/img/fast/gallery/';
  var PROC = [
    { src: G + 'deck-proc-1.jpg', cap: 'החומרים מגיעים לשטח' },
    { src: G + 'deck-proc-2.jpg', cap: 'שלד מפולס לפי המידות' },
    { src: G + 'deck-proc-3.jpg', cap: 'טיפול בשלד לפני הדק' },
    { src: G + 'deck-proc-4.jpg', cap: 'הדק המוגמר' }
  ];
  function rendered(el) { return !!el && !el.closest('x-dc'); }

  var css = document.createElement('style');
  css.textContent =
    '.stz-ba{position:relative;aspect-ratio:2.14/1;border-radius:18px;overflow:hidden;background:#1B1712;touch-action:pan-y;user-select:none;cursor:ew-resize}' +
    '.stz-ba img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none}' +
    '.stz-ba .ba-top{clip-path:inset(0 0 0 var(--x,50%))}' +
    '.stz-ba .ba-bar{position:absolute;top:0;bottom:0;left:var(--x,50%);width:3px;margin-left:-1.5px;background:#E8C48C;box-shadow:0 0 12px rgba(0,0,0,.5)}' +
    '.stz-ba .ba-knob{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:46px;height:46px;border-radius:50%;background:#E8C48C;color:#1B1712;display:grid;place-items:center;font-size:18px;font-weight:700;box-shadow:0 4px 18px rgba(0,0,0,.45)}' +
    '.stz-ba .ba-l{position:absolute;top:12px;padding:5px 12px;border-radius:100px;background:rgba(27,23,18,.78);color:#F5F0E4;font-size:13.5px;font-weight:600}' +
    '.stz-ba-cap{margin:10px 0 clamp(1.5rem,3vh,2rem);color:#4B443A;font-size:15px}' +
    '@media (max-width:760px){.stz-ba{aspect-ratio:4/3}}' +
    '.stz-proc{display:flex;gap:10px;margin-top:clamp(1.25rem,3vh,1.75rem)}' +
    '.stz-proc figure{position:relative;flex:1 1 0;margin:0;border-radius:14px;overflow:hidden;aspect-ratio:3/4;max-height:340px;opacity:.45;filter:grayscale(.5);transition:flex-grow .7s cubic-bezier(.2,.7,.2,1),opacity .5s ease,filter .5s ease;cursor:pointer}' +
    '.stz-proc figure[data-on]{flex-grow:2.2;opacity:1;filter:none}' +
    '.stz-proc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}' +
    '.stz-proc figcaption{position:absolute;inset-inline:0;bottom:0;padding:26px 12px 10px;color:#F5F0E4;font-size:13.5px;font-weight:600;background:linear-gradient(0deg,rgba(17,14,11,.85),rgba(17,14,11,0))}' +
    '.stz-proc-t{margin-top:clamp(1.5rem,3vh,2rem);font-size:13px;font-weight:600;letter-spacing:.06em;opacity:.8}' +
    '@media (max-width:760px){.stz-proc figure{aspect-ratio:auto;height:220px}.stz-proc figure:not([data-on]) figcaption{display:none}}' +
    '@media (prefers-reduced-motion:reduce){.stz-proc figure{transition:none}}';
  document.head.appendChild(css);

  function makeBA() {
    var wrap = document.createElement('div');
    wrap.className = 'stz-ba-wrap';
    var ba = document.createElement('div');
    ba.className = 'stz-ba'; ba.setAttribute('role', 'slider'); ba.setAttribute('tabindex', '0');
    ba.setAttribute('aria-label', 'לפני ואחרי: גררו כדי להשוות'); ba.setAttribute('aria-valuemin', '0'); ba.setAttribute('aria-valuemax', '100');
    ba.innerHTML = '<img src="' + G + 'deck-before.jpg" alt="לפני: דק עץ ישן ושחוק במרפסת" loading="lazy" decoding="async">' +
      '<img class="ba-top" src="' + G + 'deck-after.jpg" alt="אחרי: דק חדש ומעקה עץ מתחת לפרגולה" loading="lazy" decoding="async">' +
      '<span class="ba-l" style="left:12px">לפני</span><span class="ba-l" style="right:12px">אחרי</span>' +
      '<div class="ba-bar"><span class="ba-knob" aria-hidden="true">⇆</span></div>';
    var cap = document.createElement('p');
    cap.className = 'stz-ba-cap';
    cap.textContent = 'לפני ואחרי · חידוש דק ומעקה במרפסת, מאותה נקודת צילום. גררו את הפס כדי להשוות.';
    wrap.appendChild(ba); wrap.appendChild(cap);
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
    // a short hint movement the first time the slider comes into view
    if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
      var io = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting) return; io.disconnect();
        var t0 = performance.now();
        (function step(t) { var k = Math.min(1, (t - t0) / 1600); if (drag) return; set(50 + Math.sin(k * Math.PI * 2) * 18); if (k < 1) requestAnimationFrame(step); })(t0);
      }, { threshold: 0.6 });
      io.observe(ba);
    }
    return wrap;
  }

  function placeBA() {
    var sec = document.getElementById('projects');
    if (!rendered(sec) || sec.querySelector('.stz-ba')) return;
    var grid = sec.querySelector('.lp-grid'); // landing page
    if (grid) { grid.parentNode.insertBefore(makeBA(), grid); return; }
    var head = sec.querySelector('[data-reveal]'); // home page: right after the section heading
    if (head && head.parentNode) head.parentNode.insertBefore(makeBA(), head.nextSibling);
  }

  function placeProc() {
    var sl = [].filter.call(document.querySelectorAll('[data-stepsl]'), rendered)[0];
    if (!sl || (sl.nextElementSibling && sl.nextElementSibling.classList.contains('stz-proc-box'))) return;
    var steps = [].slice.call(sl.children);
    if (steps.length < 2) return;
    var box = document.createElement('div');
    box.className = 'stz-proc-box';
    box.innerHTML = '<div class="stz-proc-t">מהשטח · דק בבית פרטי, שלב אחרי שלב</div><div class="stz-proc">' +
      PROC.map(function (p, i) { return '<figure data-i="' + i + '"><img src="' + p.src + '" alt="' + p.cap + '" loading="lazy" decoding="async"><figcaption>' + p.cap + '</figcaption></figure>'; }).join('') + '</div>';
    sl.parentNode.insertBefore(box, sl.nextSibling);
    var figs = [].slice.call(box.querySelectorAll('figure'));
    function sync() {
      var on = 0; steps.forEach(function (s, j) { if (s.hasAttribute('data-on')) on = j; });
      var k = Math.round(on * (figs.length - 1) / Math.max(1, steps.length - 1));
      figs.forEach(function (f, j) { if (j === k) f.setAttribute('data-on', ''); else f.removeAttribute('data-on'); });
    }
    new MutationObserver(sync).observe(sl, { attributes: true, subtree: true, attributeFilter: ['data-on'] });
    figs.forEach(function (f, j) {
      f.addEventListener('click', function () { var s = steps[Math.round(j * (steps.length - 1) / (figs.length - 1))]; if (s) s.click(); });
    });
    sync();
  }

  var tries = 0;
  (function tick() { placeBA(); placeProc(); if (++tries > 80) return; setTimeout(tick, tries < 40 ? 300 : 1000); })();
})();
