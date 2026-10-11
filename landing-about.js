// "מי אנחנו" section for the pergola landing page. Inserted before the projects section (or #why).
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
  function build() {
    if (document.getElementById('about')) return true;
    var anchor = document.getElementById('projects') || document.getElementById('why');
    if (!anchor) return false;
    var css = document.getElementById('about-css') || document.createElement('style'); css.id = 'about-css';
    css.textContent =
      '#about .ab-wrap{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,3.5rem);align-items:center}' +
      '#about .ab-img{border-radius:20px;overflow:hidden;aspect-ratio:4/3;background:#ECE4D2}' +
      '#about .ab-img img{display:block;width:100%;height:100%;object-fit:cover}' +
      '#about .ab-pts{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 0;padding:0;list-style:none}' +
      '#about .ab-pts li{padding:9px 16px;border-radius:100px;border:1px solid rgba(180,129,60,.5);color:#211C16;font-size:15px;font-weight:500}' +
      '@media (max-width:860px){#about .ab-wrap{grid-template-columns:1fr}}';
    if (!css.parentNode) document.head.appendChild(css);
    var sec = document.createElement('section');
    sec.id = 'about';
    sec.style.cssText = 'padding-block:clamp(3rem,8vh,5.5rem)';
    sec.innerHTML =
      '<div style="width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto"><div class="ab-wrap">' +
      '<div><div style="display:inline-flex;align-items:center;gap:10px;color:#B4813C;font-size:14.5px;font-weight:600;margin-bottom:18px;white-space:nowrap"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>מי אנחנו</div>' +
      '<h2 style="font-size:clamp(28px,3.6vw,44px);letter-spacing:-0.02em;line-height:1.12">בית אחד לכל מעטפת החוץ</h2>' +
      '<p style="margin:18px 0 0;color:#4B443A;font-size:17px;line-height:1.65">סופר צל היא מעטפת מקצועית לתכנון יישומי, ביצוע ותיאום של פרויקטי חוץ. הפעילות שלנו צמחה מתוך שנים של ניסיון מעשי בשטח — ממערכות קירוי, הצללה ואלומיניום, דרך ריצוף ודקים, ועד פיתוח נוף ובנייה קלה.</p>' +
      '<p style="margin:14px 0 0;color:#4B443A;font-size:17px;line-height:1.65">אנחנו קוראים תוכניות ופרטי גמר לעומק, ומסייעים בבניית רצף ביצוע מתואם לפי המפרט שסוכם בכתב — בשפה חומרית אחידה, מול נקודת קשר אחת.</p>' +
      '<ul class="ab-pts"><li>נקודת קשר אחת</li><li>ניסיון בהצללה ובקירוי</li><li>תיאום מול בעלי מקצוע מוסמכים, לפי אופי הפרויקט</li></ul>' +
      '<div style="margin-top:26px"><a href="#contact" style="display:inline-flex;align-items:center;min-height:48px;padding:0 26px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:16px;font-weight:600">תאמו שיחת ייעוץ</a></div></div>' +
      '<div class="ab-img"><img src="/img/fast/slots/ab-hero.webp" alt="מרחב חוץ גמור של סופר צל" loading="lazy" decoding="async"></div>' +
      '</div></div>';
    anchor.parentNode.insertBefore(sec, anchor);
    realign();
    return true;
  }
  // the page re-renders while it boots and can drop inserted nodes, so keep the section in place for a while
  var tries = 0;
  (function tick() { build(); if (tries < 14) realign(); if (++tries > 60) return; setTimeout(tick, 500); })();
})();
