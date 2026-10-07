/* Country-code picker for every phone field on the page (not only the floating form).
   The field always ends up holding the full international number (e.g. +972541234567),
   so the email / WhatsApp lead carries the country code. Needs lead-modal.js (country list). */
(function () {
  var C = window.stzCountries;
  if (!C || window.__stzPhoneCC) return;
  window.__stzPhoneCC = true;
  var codes = C.map(function (c) { return c[1]; }).sort(function (a, b) { return b.length - a.length; });

  function setNative(el, v) {
    Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(el, v);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }
  // Split a typed value into { code, local }; code is null when no "+" / "00" prefix was typed.
  function parse(v) {
    var s = String(v || '').replace(/[^\d+]/g, '');
    if (s.indexOf('00') === 0) s = '+' + s.slice(2);
    if (s.charAt(0) !== '+') return { code: null, local: s };
    var d = s.slice(1);
    for (var i = 0; i < codes.length; i++) if (d.indexOf(codes[i]) === 0) return { code: codes[i], local: d.slice(codes[i].length) };
    return { code: null, local: d };
  }
  function indexOfCode(code) { for (var j = 0; j < C.length; j++) if (C[j][1] === code) return j; return 0; }

  function normalize(input, sel, fromSelect) {
    var p = parse(input.value);
    if (!p.local) return;
    if (fromSelect) p.code = null; // the visitor just picked a country: it wins over a previously typed code
    var code = p.code || C[sel.selectedIndex][1];
    var n = p.local;
    if (code === '972' || n.charAt(0) === '0') n = n.replace(/^0+/, '');
    if (p.code) sel.selectedIndex = indexOfCode(p.code);
    var full = '+' + code + n;
    if (input.value !== full) setNative(input, full);
  }

  function enhance(input) {
    if (input.__stzCC || input.closest('#stz-lead-root')) return;
    input.__stzCC = true;
    var sel = document.createElement('select');
    sel.setAttribute('aria-label', 'קידומת מדינה');
    sel.dataset.stzCc = '1';
    sel.style.cssText = 'width:100%;box-sizing:border-box;padding:12px 14px;border:1px solid rgba(245,240,228,0.26);background:#2A241D;border-radius:14px;color:#F5F0E4;font:inherit;font-size:15px;direction:rtl';
    C.forEach(function (c) {
      var o = document.createElement('option');
      o.value = c[1]; o.textContent = '+' + c[1] + ' ' + c[0]; o.style.color = '#211C16';
      sel.appendChild(o);
    });
    var p0 = parse(input.value);
    if (p0.code) sel.selectedIndex = indexOfCode(p0.code);
    input.parentNode.insertBefore(sel, input);
    input.style.direction = 'ltr';
    input.style.textAlign = 'left';
    input.placeholder = input.placeholder || '54-123-4567';
    var msg = document.createElement('div');
    msg.setAttribute('role', 'alert');
    msg.style.cssText = 'display:none;margin-top:2px;font-size:13px;color:#E8A08C;direction:rtl';
    msg.textContent = 'מספר הטלפון לא נראה תקין, נא לבדוק את מספר הספרות';
    input.parentNode.insertBefore(msg, input.nextSibling);
    input.__stzCheck = function (show) {
      var p = parse(input.value);
      var code = p.code || C[sel.selectedIndex][1];
      var ok = !!(p.local && window.stzPhoneValid && window.stzPhoneValid(code, p.local));
      msg.style.display = !ok && show ? 'block' : 'none';
      input.setAttribute('aria-invalid', ok ? 'false' : 'true');
      return ok;
    };
    sel.addEventListener('change', function () { normalize(input, sel, true); input.__stzCheck(!!input.value); });
    input.addEventListener('blur', function () { normalize(input, sel); input.__stzCheck(!!input.value); });
    input.addEventListener('input', function () { var p = parse(input.value); if (p.code) sel.selectedIndex = indexOfCode(p.code); });
    // Enter / programmatic submit paths: normalise just before any click on a button in the same form area.
    document.addEventListener('pointerdown', function () { if (document.activeElement === input) normalize(input, sel); }, true);
  }

  // Block the form's send button while the phone number is empty or the wrong length.
  var SEND = /ייעוץ|שליחה|שלח|פנייה|פניה|תאמו|השאר|תיאום|קבלת/;
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button');
    if (!b || b.closest('#stz-lead-root') || !SEND.test(b.innerText || '')) return;
    var box = b.closest('form'), i, p = b;
    for (i = 0; !box && i < 5 && p; i++, p = p.parentElement) if (p.querySelector && p.querySelector('input[type="tel"]')) box = p;
    if (!box) return;
    var tel = box.querySelector('input[type="tel"]');
    if (!tel || !tel.__stzCheck || tel.offsetWidth === 0) return;
    var sel = tel.previousElementSibling;
    if (sel && sel.dataset && sel.dataset.stzCc) normalize(tel, sel);
    if (!tel.__stzCheck(true)) { e.preventDefault(); e.stopImmediatePropagation(); try { tel.focus(); } catch (x) {} }
  }, true);

  function scan() {
    document.querySelectorAll('input[type="tel"]').forEach(function (i) {
      if (!i.parentNode || (i.previousElementSibling && i.previousElementSibling.dataset && i.previousElementSibling.dataset.stzCc)) return;
      i.__stzCC = false;
      enhance(i);
    });
  }
  scan();
  var t;
  new MutationObserver(function () { clearTimeout(t); t = setTimeout(scan, 80); }).observe(document.body, { childList: true, subtree: true });
})();
