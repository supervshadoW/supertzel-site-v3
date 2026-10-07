/* Campaign landing mode: on pergola.supertzel.co.il (or with ?landing=1 for testing) the page stands alone.
   No links out to the rest of the site (logo, "projects"), no section menu in the header, kept out of search results. */
(function () {
  var on = location.hostname.indexOf('pergola.') === 0 || /[?&]landing=1(&|$)/.test(location.search);
  if (!on) return;
  document.documentElement.classList.add('stz-landing');

  var css = document.createElement('style');
  css.textContent =
    '.stz-landing header nav[aria-label="ניווט מהיר"]{display:none!important}' +
    '.stz-landing a[href="/projects"]{display:none!important}';
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
