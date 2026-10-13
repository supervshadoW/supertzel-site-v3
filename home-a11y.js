// Home page: the mobile navigation dialog closes on Escape (keyboard users and screen readers expect this).
(function () {
  if (window.__stzHomeA11y) return;
  window.__stzHomeA11y = true;
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var d = document.querySelector('[role="dialog"][aria-label="תפריט ניווט"]');
    var b = d && d.querySelector('button[aria-label="סגירת התפריט"]');
    if (b) { e.preventDefault(); b.click(); }
  });
})();
