/* Mobile only (<= 760px): turns the long stacks of cards into swipeable carousels with dots and a gentle auto-advance.
   Desktop is not touched. Respects "reduce motion". */
(function () {
  var mq = window.matchMedia('(max-width: 760px)');
  if (!mq.matches) return;
  // header blur strip is shown only after the page has moved (see pergola.html)
  function onScroll() { document.documentElement.classList.toggle('stz-scrolled', (window.scrollY || 0) > 40); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function glide(el, to) {
    var from = el.scrollLeft, t0 = null, dur = 650;
    var snap = el.style.scrollSnapType;
    el.style.scrollSnapType = 'none'; // snapping would fight the animation
    function step(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur), e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      el.scrollLeft = from + (to - from) * e;
      if (p < 1) requestAnimationFrame(step); else el.style.scrollSnapType = snap;
    }
    requestAnimationFrame(step);
  }

  function setup(car) {
    if (car.__stzCar) return;
    var cards = [].slice.call(car.children).filter(function (c) { return c.offsetWidth > 0; });
    if (cards.length < 2) return;
    car.__stzCar = true;
    // horizontally hidden cards must not wait for lazy-loading: load their photos right away
    car.querySelectorAll('img').forEach(function (im) { im.loading = 'eager'; im.decoding = 'async'; });

    var dots = document.createElement('div');
    dots.setAttribute('aria-hidden', 'true');
    dots.__stzFor = car;
    dots.style.cssText = 'display:flex;justify-content:center;gap:7px;margin:2px 0 6px';
    var dotEls = cards.map(function () {
      var d = document.createElement('span');
      d.style.cssText = 'width:7px;height:7px;border-radius:50%;background:rgba(33,28,22,.22);transition:background .25s,width .25s';
      dots.appendChild(d);
      return d;
    });
    car.parentNode.insertBefore(dots, car.nextSibling);

    function current() {
      var cr = car.getBoundingClientRect(), best = 0, bd = 1e9;
      cards.forEach(function (c, i) {
        var r = c.getBoundingClientRect();
        var d = Math.abs((r.right) - (cr.right - 14)); // RTL: cards start at the right edge
        if (d < bd) { bd = d; best = i; }
      });
      return best;
    }
    function paint() {
      var i = current();
      dotEls.forEach(function (d, k) {
        d.style.background = k === i ? '#B4813C' : 'rgba(33,28,22,.22)';
        d.style.width = k === i ? '20px' : '7px';
        d.style.borderRadius = k === i ? '8px' : '50%';
      });
      return i;
    }
    car.addEventListener('scroll', function () { paint(); }, { passive: true });
    paint();

    var stopped = reduce || car.classList.contains('stz-noauto'), timer = null, visible = false;
    function stop() { stopped = true; if (timer) { clearInterval(timer); timer = null; } }
    ['pointerdown', 'touchstart', 'wheel', 'keydown'].forEach(function (ev) { car.addEventListener(ev, stop, { passive: true }); });
    function tick() {
      if (stopped || !visible) return;
      var i = paint();
      var next = cards[(i + 1) % cards.length]; // loops; a touch stops it for good
      var cr = car.getBoundingClientRect(), nr = next.getBoundingClientRect();
      // scroll the container only (never the page); own easing so it also works where native smooth scroll is off
      glide(car, car.scrollLeft + (nr.right - (cr.right - 14)));
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting;
        if (visible && !stopped && !timer) timer = setInterval(tick, 4200);
        if (!visible && timer) { clearInterval(timer); timer = null; }
      }, { threshold: 0.6 }).observe(car);
    }
  }

  function scan() { document.querySelectorAll('.stz-carousel').forEach(setup); }
  scan();
  var t;
  new MutationObserver(function () { clearTimeout(t); t = setTimeout(scan, 120); }).observe(document.body, { childList: true, subtree: true });
})();
