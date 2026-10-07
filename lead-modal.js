// Floating lead form — opens from every "שיחת ייעוץ" CTA (links to #quick / #contact / #lead, or window.stzOpenLead()).
// Sends through window.stzSendLead (lead.js). Phone field has an international country-code picker with auto-detect.
(function () {
  if (window.stzOpenLead) return;
  var C = [
    ['ישראל', '972', '54-123-4567'], ['ארה״ב / קנדה', '1', '201-555-0123'], ['בריטניה', '44', '7400 123456'],
    ['צרפת', '33', '6 12 34 56 78'], ['גרמניה', '49', '1512 3456789'], ['רוסיה', '7', '912 345-67-89'],
    ['אוקראינה', '380', '50 123 4567'], ['בלארוס', '375', '29 123-45-67'], ['מולדובה', '373', '621 12 345'],
    ['גאורגיה', '995', '555 12 34 56'], ['אזרבייג׳ן', '994', '50 123 45 67'], ['ספרד', '34', '612 34 56 78'],
    ['איטליה', '39', '312 345 6789'], ['הולנד', '31', '6 12345678'], ['בלגיה', '32', '470 12 34 56'],
    ['שווייץ', '41', '78 123 45 67'], ['אוסטריה', '43', '664 123456'], ['פולין', '48', '512 345 678'],
    ['רומניה', '40', '712 345 678'], ['הונגריה', '36', '20 123 4567'], ['צ׳כיה', '420', '601 123 456'],
    ['יוון', '30', '691 234 5678'], ['קפריסין', '357', '96 123456'], ['טורקיה', '90', '501 234 56 78'],
    ['פורטוגל', '351', '912 345 678'], ['אירלנד', '353', '85 012 3456'], ['שוודיה', '46', '70 123 45 67'],
    ['נורווגיה', '47', '406 12 345'], ['דנמרק', '45', '20 12 34 56'], ['פינלנד', '358', '41 2345678'],
    ['אוסטרליה', '61', '412 345 678'], ['דרום אפריקה', '27', '71 123 4567'], ['ארגנטינה', '54', '9 11 2345-6789'],
    ['ברזיל', '55', '11 91234-5678'], ['מקסיקו', '52', '1 55 1234 5678'], ['איחוד האמירויות', '971', '50 123 4567'],
    ['ירדן', '962', '7 9012 3456'], ['מצרים', '20', '100 123 4567'], ['מרוקו', '212', '650-123456'],
    ['אתיופיה', '251', '91 123 4567'], ['הודו', '91', '81234 56789'], ['סין', '86', '131 2345 6789'], ['יפן', '81', '90-1234-5678']
  ];
  window.stzCountries = C;
  // Phone length check to prevent typos. national = digits after the country code (leading 0 allowed).
  window.stzPhoneValid = function (code, national) {
    var n = String(national || '').replace(/\D/g, '').replace(/^0+/, '');
    if (code === '972') return n.length === 9 || n.length === 8; // mobile 5X-XXXXXXX / landline X-XXXXXXX
    return n.length >= 6 && (code.length + n.length) <= 15;
  };
  var codes = C.map(function (c) { return c[1]; }).sort(function (a, b) { return b.length - a.length; });
  var root, form, done, nameI, telI, sel, err, btn, last, source = 'site';
  var S = {
    back: 'position:fixed;inset:0;z-index:2147483000;background:rgba(17,14,11,0.72);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);display:none;align-items:center;justify-content:center;padding:20px;font-family:Rubik,system-ui,sans-serif;direction:rtl',
    card: 'position:relative;width:min(100%,440px);max-height:92vh;overflow:auto;background:#211C16;color:#F5F0E4;border:1px solid rgba(245,240,228,0.2);border-radius:26px;padding:clamp(1.5rem,4vw,2.1rem);box-shadow:0 30px 80px rgba(0,0,0,0.5);display:grid;gap:14px',
    x: 'position:absolute;top:14px;left:14px;width:40px;height:40px;border-radius:50%;border:1px solid rgba(245,240,228,0.25);background:transparent;color:#F5F0E4;font-size:20px;line-height:1;cursor:pointer;display:grid;place-items:center',
    lab: 'display:grid;gap:6px;font-size:13.5px;color:rgba(245,240,228,0.72)',
    inp: 'width:100%;box-sizing:border-box;min-height:52px;padding:0 18px;border:1px solid rgba(245,240,228,0.26);background:rgba(245,240,228,0.06);border-radius:14px;color:#F5F0E4;font:inherit;font-size:16px;outline:none',
    sel: 'flex:0 0 auto;max-width:46%;min-height:52px;padding:0 10px;border:1px solid rgba(245,240,228,0.26);background:#2A241D;border-radius:14px;color:#F5F0E4;font:inherit;font-size:15px;direction:rtl',
    btn: 'width:100%;min-height:54px;border:0;border-radius:100px;background:#B4813C;color:#1B1712;font:inherit;font-size:16.5px;font-weight:600;cursor:pointer'
  };
  function el(tag, style, html) { var e = document.createElement(tag); if (style) e.style.cssText = style; if (html != null) e.innerHTML = html; return e; }
  function cur() { return C[sel.selectedIndex] || C[0]; }
  function setPh() { telI.placeholder = cur()[2]; }
  function detect() {
    var v = telI.value.replace(/[^\d+]/g, '');
    if (v.indexOf('00') === 0) v = '+' + v.slice(2);
    if (v.charAt(0) !== '+') return;
    var d = v.slice(1);
    for (var i = 0; i < codes.length; i++) {
      if (d.indexOf(codes[i]) === 0) {
        for (var j = 0; j < C.length; j++) if (C[j][1] === codes[i]) { sel.selectedIndex = j; break; }
        telI.value = telI.value.replace(/^\s*(\+|00)\s*/, '').replace(new RegExp('^' + codes[i].split('').join('[\\s-]*')), '').replace(/^[\s-]+/, '');
        setPh(); return;
      }
    }
  }
  function e164() {
    var n = telI.value.replace(/\D/g, '');
    if (cur()[1] === '972' || n.charAt(0) === '0') n = n.replace(/^0+/, '');
    return '+' + cur()[1] + n;
  }
  function build() {
    root = el('div', S.back); root.id = 'stz-lead-root'; root.setAttribute('role', 'dialog'); root.setAttribute('aria-modal', 'true'); root.setAttribute('aria-label', 'תיאום שיחת ייעוץ');
    var card = el('div', S.card);
    var x = el('button', S.x, '&times;'); x.type = 'button'; x.setAttribute('aria-label', 'סגירה'); x.onclick = close;
    form = el('form', 'display:grid;gap:14px'); form.noValidate = true;
    form.appendChild(el('div', 'display:grid;gap:8px;padding-left:44px',
      '<span style="font-size:13.5px;font-weight:600;color:#C99752">שיחת ייעוץ ללא עלות וללא התחייבות</span>' +
      '<h3 style="margin:0;font-size:clamp(22px,5vw,26px);line-height:1.2;letter-spacing:-0.02em;color:#F5F0E4">השאירו שם וטלפון — ונחזור אליכם</h3>'));
    var l1 = el('label', S.lab, '<span>שם מלא</span>'); nameI = el('input', S.inp); nameI.type = 'text'; nameI.autocomplete = 'name'; nameI.required = true; l1.appendChild(nameI);
    var l2 = el('label', S.lab, '<span>טלפון</span>');
    var row = el('div', 'display:flex;gap:8px;direction:ltr');
    sel = el('select', S.sel); sel.setAttribute('aria-label', 'קידומת מדינה'); sel.autocomplete = 'tel-country-code';
    C.forEach(function (c) { var o = document.createElement('option'); o.value = c[1]; o.textContent = '+' + c[1] + ' ' + c[0]; o.style.color = '#211C16'; sel.appendChild(o); });
    sel.onchange = setPh;
    telI = el('input', S.inp + ';direction:ltr;text-align:left'); telI.type = 'tel'; telI.inputMode = 'tel'; telI.autocomplete = 'tel-national'; telI.required = true;
    telI.addEventListener('input', detect);
    row.appendChild(sel); row.appendChild(telI); l2.appendChild(row);
    err = el('p', 'margin:0;font-size:13.5px;color:#E8C48C;text-align:center;display:none', 'נא למלא שם ומספר טלפון תקין'); err.setAttribute('role', 'alert');
    btn = el('button', S.btn, 'תאמו שיחת ייעוץ'); btn.type = 'submit';
    form.appendChild(l1); form.appendChild(l2); form.appendChild(err); form.appendChild(btn);
    form.appendChild(el('p', 'margin:0;font-size:12.5px;color:rgba(245,240,228,0.6);text-align:center;line-height:1.5', 'השארת פרטים מהווה הסכמה ליצירת קשר לצורך טיפול בפנייה זו בלבד. <a href="/privacy-policy" target="_blank" rel="noopener" style="color:#C99752">מדיניות הפרטיות</a>'));
    form.onsubmit = submit;
    done = el('div', 'display:none;gap:10px;text-align:center;padding:12px 0',
      '<h3 style="margin:0;font-size:22px;color:#F5F0E4">תודה, קיבלנו</h3><p style="margin:0;font-size:15.5px;color:rgba(245,240,228,0.78)">נחזור אליכם בהקדם לתיאום שיחת ייעוץ.</p>');
    card.appendChild(x); card.appendChild(form); card.appendChild(done); root.appendChild(card);
    root.addEventListener('click', function (e) { if (e.target === root) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && root.style.display !== 'none') close(); });
    setPh(); document.body.appendChild(root);
  }
  function submit(e) {
    e.preventDefault();
    var nm = nameI.value.trim(), digits = telI.value.replace(/\D/g, '');
    if (nm.length < 2 || !window.stzPhoneValid(cur()[1], digits)) { err.textContent = nm.length < 2 ? 'נא למלא שם מלא' : 'מספר הטלפון לא נראה תקין, נא לבדוק את מספר הספרות'; err.style.display = 'block'; return; }
    err.style.display = 'none';
    var phone = e164();
    var msg = 'פנייה מהטופס הצף · ' + document.title + ' · ' + source;
    form.style.display = 'none'; done.style.display = 'grid';
    var send = window.stzSendLead ? window.stzSendLead({ name: nm, phone: phone, solution: source, message: msg, source: 'modal_' + source }) : Promise.reject();
    send.catch(function () {
      location.href = 'https://wa.me/972547752697?text=' + encodeURIComponent('היי, אשמח לתאם שיחת ייעוץ.\nשם: ' + nm + '\nטלפון: ' + phone);
    });
  }
  function open(src) {
    if (!root) build();
    source = src || source;
    last = document.activeElement;
    form.style.display = 'grid'; done.style.display = 'none'; err.style.display = 'none';
    root.style.display = 'flex'; document.documentElement.style.overflow = 'hidden';
    setTimeout(function () { nameI.focus(); }, 30);
  }
  function close() {
    root.style.display = 'none'; document.documentElement.style.overflow = '';
    if (last && last.focus) try { last.focus(); } catch (e) {}
  }
  window.stzOpenLead = open;
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href$="#quick"],a[href$="#contact"],a[href$="#lead"],[data-lead-open]');
    if (!a || (root && root.contains(a))) return;
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) !== '#' && href.indexOf(location.pathname) === -1 && !a.hasAttribute('data-lead-open')) return;
    e.preventDefault();
    open((location.pathname.replace(/\//g, '') || 'home'));
  }, true);

  // Plain <button> CTAs (including the floating bottom bar) open the same window.
  // Form submit buttons are left alone: they have an input/textarea within a few levels above them.
  var CTA = /ייעוץ|השארת פרטים|מילוי פרטים|השאירו פרטים|תיאום|צרו קשר|צור קשר/;
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button');
    if (!b || (root && root.contains(b)) || b.type === 'submit' && b.form) return;
    if (!CTA.test(b.innerText || '')) return;
    var p = b, i;
    for (i = 0; i < 4 && p; i++, p = p.parentElement) {
      if (p.querySelector && p.querySelector('input,textarea,select')) return;
    }
    e.preventDefault(); e.stopPropagation();
    open((location.pathname.replace(/\//g, '') || 'home'));
  }, true);
})();
