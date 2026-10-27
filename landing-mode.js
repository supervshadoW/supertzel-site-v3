// Anchor safety (campaign sitelinks / old links): removed or hidden targets map to the right section, #lead opens the form.
(function () {
  var MAP = { why: 'about', reality: 'catalog' };
  function go() {
    var h = decodeURIComponent((location.hash || '').slice(1)); if (!h) return;
    if ((h === 'lead' || h === 'quick') && window.stzOpenLead) { window.stzOpenLead('pergola'); return; }
    var id = MAP[h]; if (!id) return;
    var el = document.getElementById(id); if (el && el.offsetHeight) el.scrollIntoView();
  }
  var n = 0; (function t() { go(); if (++n < 6) setTimeout(t, 700); })();
  addEventListener('hashchange', go);
})();
/* Campaign landing mode: on pergola.supertzel.co.il (or with ?landing=1 for testing) the page stands alone.
   No links out to the rest of the site (logo, "projects"), no section menu in the header, kept out of search results. */
(function () {
  var on = location.hostname.indexOf('pergola.') === 0 || /[?&]landing=1(&|$)/.test(location.search);
  if (!on) return;
  document.documentElement.classList.add('stz-landing');

  var css = document.createElement('style');
  css.textContent =
    '.stz-landing header nav[aria-label="ניווט מהיר"]{display:none!important}' +
    '.stz-landing footer a[href="/projects"]{display:none!important}';
  document.head.appendChild(css);

  var m = document.createElement('meta');
  m.name = 'robots'; m.content = 'noindex, nofollow';
  document.head.appendChild(m);

  // The logo stays on the page: it scrolls to the top instead of opening the home page.
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href="/"]');
    if (!a) return;
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, true);
})();
