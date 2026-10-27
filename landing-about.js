// "מי אנחנו" section for the pergola landing page. Placed right after #why (the projects section follows it).
(function () {
  if (window.__stzLandingAbout) return;
  window.__stzLandingAbout = true;
  // Sections are inserted after the browser has already jumped to a #anchor, which shifts the layout.
  // Re-align to the anchor after each insert, unless the visitor has already started scrolling.
  var touched = false;
  ['wheel', 'touchmove', 'keydown', 'mousedown'].forEach(function (ev) { addEventListener(ev, function () { touched = true; }, { passive: true, once: true }); });
  function realign() {
    if (touched || !location.hash || location.hash.length < 2) return;
    var t = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (t) t.scrollIntoView();
  }
  // The page runtime re-renders while it boots and can drop or reorder nodes that were inserted by hand. The section is only
  // inserted into the rendered page (never into the inert <x-dc> template) and is put back into place if it drifts.
  function rendered(el) { return !!el && !el.closest('x-dc'); }
  function place(sec) {
    var why = document.getElementById('why');
    if (!rendered(why)) return false;
    if (why.nextElementSibling !== sec) why.parentNode.insertBefore(sec, why.nextSibling);
    return true;
  }
  function build() {
    var existing = document.getElementById('about');
    if (existing && rendered(existing)) return place(existing);
    if (!rendered(document.getElementById('why'))) return false;
    var css = document.getElementById('about-css') || document.createElement('style'); css.id = 'about-css';
    css.textContent =
      '#about .ab-wrap{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,3.5rem);align-items:center}' +
      '#about .ab-img{border-radius:20px;overflow:hidden;aspect-ratio:4/3;background:#ECE4D2}' +
      '#about .ab-img img{display:block;width:100%;height:100%;object-fit:cover}' +
      '#about .ab-pts{display:grid;gap:10px;margin:22px 0 0;padding:0;list-style:none}' +
      '#about .ab-pts li{position:relative;padding:0 26px 0 0;color:#211C16;font-size:16px;font-weight:500;line-height:1.5}#about .ab-pts li::before{content:"";position:absolute;inset-inline-start:0;top:.55em;width:14px;height:1px;background:#B4813C}' +
      '@media (max-width:860px){#about .ab-wrap{grid-template-columns:1fr}}' +
      // slow strip of project photos drifting behind the text
      '#about{position:relative;overflow:hidden}#about>.ab-in{position:relative;z-index:1}' +
      '#about .ab-strip{position:absolute;inset:0;display:flex;align-items:center;pointer-events:none;z-index:0;opacity:.13;filter:grayscale(.35) sepia(.25);-webkit-mask-image:linear-gradient(90deg,transparent,#000 18%,#000 82%,transparent);mask-image:linear-gradient(90deg,transparent,#000 18%,#000 82%,transparent)}' +
      '#about .ab-track{display:flex;gap:16px;width:max-content;animation:ab-drift 90s linear infinite}' +
      '#about .ab-track img{height:clamp(220px,34vh,320px);width:auto;aspect-ratio:4/3;object-fit:cover;border-radius:18px;filter:blur(1.5px)}' +
      '@keyframes ab-drift{from{transform:translateX(0)}to{transform:translateX(50%)}}' +
      '#about .ab-pts li{opacity:0;transform:translateY(10px);transition:opacity .6s ease,transform .6s ease}' +
      '#about.ab-on .ab-pts li{opacity:1;transform:none}' +
      '#about.ab-on .ab-pts li:nth-child(2){transition-delay:.25s}#about.ab-on .ab-pts li:nth-child(3){transition-delay:.5s}' +
      '@media (prefers-reduced-motion:reduce){#about .ab-track{animation:none}#about .ab-pts li{opacity:1;transform:none;transition:none}}';
    if (!css.parentNode) document.head.appendChild(css);
    var sec = document.createElement('section');
    sec.id = 'about';
    sec.style.cssText = 'padding-block:clamp(3rem,8vh,5.5rem)';
    var G = '/img/fast/gallery/', PH = ['new-52-4', 'pergola-modern-lighting-1', 'new-55-1', 'project-deck-view', 'new-58-1', 'glass-1', 'new-60-1', 'awning-jaffa-1', 'new-46-3', 'pergola-white-wood'];
    var strip = PH.concat(PH).map(function (k) { return '<img src="' + G + k + '.webp" alt="" loading="lazy" decoding="async">'; }).join('');
    sec.innerHTML =
      '<div class="ab-strip" aria-hidden="true"><div class="ab-track">' + strip + '</div></div>' +
      '<div class="ab-in" style="width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto"><div class="ab-wrap">' +
      '<div><div style="display:inline-flex;align-items:center;gap:10px;color:#B4813C;font-size:14.5px;font-weight:600;margin-bottom:18px;white-space:nowrap"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>מי אנחנו</div>' +
      '<h2 style="font-size:clamp(28px,3.6vw,44px);letter-spacing:-0.02em;line-height:1.12">בית אחד לכל מעטפת החוץ</h2>' +
      '<p style="margin:18px 0 0;color:#4B443A;font-size:17px;line-height:1.65">סופר צל היא מעטפת מקצועית לתכנון יישומי, ביצוע ותיאום של פרויקטי חוץ. הפעילות שלנו צמחה מתוך שנים של ניסיון מעשי בשטח — ממערכות קירוי, הצללה ואלומיניום, דרך ריצוף ודקים, ועד פיתוח נוף ובנייה קלה.</p>' +
      '<p style="margin:14px 0 0;color:#4B443A;font-size:17px;line-height:1.65">אנחנו קוראים תוכניות ופרטי גמר לעומק, ומסייעים בבניית רצף ביצוע מתואם לפי המפרט שסוכם בכתב — בשפה חומרית אחידה, מול נקודת קשר אחת.</p>' +
      '<ul class="ab-pts"><li>נקודת קשר אחת</li><li>ניסיון בהצללה ובקירוי</li><li>תיאום מול בעלי מקצוע מוסמכים, לפי אופי הפרויקט</li></ul>' +
      '<div style="margin-top:26px"><a href="#contact" style="display:inline-flex;align-items:center;min-height:48px;padding:0 26px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:16px;font-weight:600">תאמו שיחת ייעוץ</a></div></div>' +
      '<div class="ab-img"><img src="/img/fast/slots/ab-hero.webp" alt="מרחב חוץ גמור של סופר צל" loading="lazy" decoding="async"></div>' +
      '</div></div>';
    place(sec);
    realign();
    // the three points light up one after another when the section comes into view
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { sec.classList.add('ab-on'); io.disconnect(); } }, { threshold: 0.3 });
      io.observe(sec);
    } else sec.classList.add('ab-on');
    return true;
  }
  // the page re-renders while it boots and can drop inserted nodes, so keep the section in place for a while
  var tries = 0;
  (function tick() { var had = !!document.getElementById('about'); build(); if (tries < 28 && had) realign(); if (++tries > 80) return; setTimeout(tick, tries < 40 ? 250 : 1000); })();
})();
