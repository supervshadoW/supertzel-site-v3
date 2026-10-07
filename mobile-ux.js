/* Mobile only (<= 760px): turns the long stacks of cards into swipeable carousels with dots and a gentle auto-advance.
   Desktop is not touched. Respects "reduce motion". */
(function () {
  var mq = window.matchMedia('(max-width: 760px)');
  if (!mq.matches) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setup(car) {
    if (car.__stzCar) return;
    var cards = [].slice.call(car.children).filter(function (c) { return c.offsetWidth > 0; });
    if (cards.length < 2) return;
    car.__stzCar = true;
    // horizontally hidden cards must not wait for lazy-loading: load their photos right away
    car.querySelectorAll('img').forEach(function (im) { im.loading = 'eager'; im.decoding = 'async'; });

    var dots = document.createElement('div');
    dots.setAttribute('aria-hidden', 'true');
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
      var loop = car.classList.contains('stz-loop');
      if (i >= cards.length - 1 && !loop) { stop(); return; } // one gentle pass, then leave it to the visitor
      var next = cards[loop ? (i + 1) % cards.length : i + 1];
      var cr = car.getBoundingClientRect(), nr = next.getBoundingClientRect();
      // scroll the container only (never the page)
      car.scrollBy({ left: nr.right - (cr.right - 14), behavior: 'smooth' });
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting;
        if (visible && !stopped && !timer) timer = setInterval(tick, 4200);
        if (!visible && timer) { clearInterval(timer); timer = null; }
      }, { threshold: 0.6 }).observe(car);
    }
  }

  // Numbered photo: attach a legend (מקרא) right under it, built from the circles' labels.
  function legend() {
    var img = document.querySelector('img[src*="envelope-render-pins"]');
    if (!img) return;
    var box = img.parentElement;
    box.style.setProperty('border-radius', '28px 28px 0 0', 'important');
    if (box.__stzLegend) return;
    var pins = [].slice.call(box.querySelectorAll('button[aria-label]'));
    if (!pins.length) return;
    box.__stzLegend = true;
    box.classList.add('stz-envimg');
    var lg = document.createElement('div');
    lg.setAttribute('aria-label', 'מקרא');
    lg.style.cssText = 'display:grid;grid-template-columns:1fr 1fr;gap:10px 12px;padding:16px 16px 18px;background:#211C16;color:#F5F0E4;border-radius:0 0 28px 28px;font-size:14px;line-height:1.3;margin-bottom:6px';
    lg.innerHTML = pins.map(function (p) {
      var m = (p.getAttribute('aria-label') || '').match(/^(\d+)\.\s*(.+)$/);
      return m ? '<div style="display:flex;align-items:center;gap:9px"><span style="flex:none;display:grid;place-items:center;width:24px;height:24px;border-radius:50%;background:#B4813C;border:1.5px solid #fff;font-size:12px;font-weight:600">' + m[1] + '</span><span>' + m[2] + '</span></div>' : '';
    }).join('');
    box.parentNode.insertBefore(lg, box.nextSibling);
  }

  function scan() { document.querySelectorAll('.stz-carousel').forEach(setup); legend(); }
  scan();
  var t;
  new MutationObserver(function () { clearTimeout(t); t = setTimeout(scan, 120); }).observe(document.body, { childList: true, subtree: true });
})();
