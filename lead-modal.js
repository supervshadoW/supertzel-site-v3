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
  // National number length per country (digits after the country code, no leading 0): [min, max]
  var LEN = { '1':[10,10], '44':[9,10], '33':[9,9], '49':[7,11], '7':[10,10], '380':[9,9], '375':[9,9], '373':[8,8],
    '995':[9,9], '994':[9,9], '34':[9,9], '39':[9,11], '31':[9,9], '32':[8,9], '41':[9,9], '43':[7,13], '48':[9,9],
    '40':[9,9], '36':[8,9], '420':[9,9], '30':[10,10], '357':[8,8], '90':[10,10], '351':[9,9], '353':[7,9], '46':[7,10],
    '47':[8,8], '45':[8,8], '358':[7,10], '61':[9,9], '27':[9,9], '54':[10,11], '55':[10,11], '52':[10,11], '971':[8,9],
    '962':[8,9], '20':[9,10], '212':[9,9], '251':[9,9], '91':[10,10], '86':[10,11], '81':[9,10] };
  window.stzPhoneValid = function (code, national) {
    var n = String(national || '').replace(/\D/g, '').replace(/^0+/, '');
    if (code === '972') {
      if (n.length === 9) return /^(5[0-9]|7[0-9])/.test(n);   // נייד 05X / 07X — 10 ספרות עם ה-0
      if (n.length === 8) return /^[23489]/.test(n);            // קווי 02/03/04/08/09 — 9 ספרות עם ה-0
      return false;
    }
    var r = LEN[code];
    if (r) return n.length >= r[0] && n.length <= r[1];
    return n.length >= 6 && (code.length + n.length) <= 15;
  };
  // Short hint shown under the field when the number is wrong
  window.stzPhoneHint = function (code) {
    if (code === '972') return 'מספר ישראלי: נייד 10 ספרות (05X-XXXXXXX) או קווי 9 ספרות (0X-XXXXXXX)';
    var r = LEN[code];
    if (!r) return 'מספר הטלפון לא נראה תקין, נא לבדוק את מספר הספרות';
    return 'מספר הטלפון לא נראה תקין — במדינה שנבחרה ' + (r[0] === r[1] ? r[0] : r[0] + '–' + r[1]) + ' ספרות אחרי הקידומת';
  };
  var codes = C.map(function (c) { return c[1]; }).sort(function (a, b) { return b.length - a.length; });
  var root, form, done, nameI, telI, sel, err, btn, last, picksW, scopeSet, source = 'site';
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function picks() { try { return (window.stzLeadPicks ? window.stzLeadPicks() : []).filter(function (r) { return r && r.v && r.v.length; }); } catch (e) { return []; } }
  function renderPicks() {
    if (!picksW) return; var P = picks();
    if (!P.length) { picksW.style.display = 'none'; return; }
    picksW.style.display = 'grid';
    picksW.innerHTML = '<span style="font-size:13.5px;font-weight:600;color:#E8C48C">הבחירות שלכם · יצורפו לפנייה</span>' + P.map(function (r) {
      return '<div style="display:grid;gap:6px"><span style="font-size:12.5px;color:rgba(245,240,228,0.65)">' + esc(r.k) + '</span><div style="display:flex;flex-wrap:wrap;gap:6px">' + r.v.map(function (v) { return '<span style="padding:4px 10px;border-radius:100px;background:rgba(201,151,82,0.16);border:1px solid rgba(201,151,82,0.55);font-size:13px;color:#F5F0E4">' + esc(v) + '</span>'; }).join('') + '</div></div>';
    }).join('');
  }
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
  var hHead, whenW, callW, scopeW, pDay = '', pTime = '', pCall = '', mode = 'call';
  function build() {
    root = el('div', S.back); root.id = 'stz-lead-root'; root.setAttribute('role', 'dialog'); root.setAttribute('aria-modal', 'true'); root.setAttribute('aria-label', 'תיאום שיחת ייעוץ');
    var card = el('div', S.card);
    var x = el('button', S.x, '&times;'); x.type = 'button'; x.setAttribute('aria-label', 'סגירה'); x.onclick = close;
    form = el('form', 'display:grid;gap:14px'); form.noValidate = true;
    hHead = el('div', 'display:grid;gap:8px;padding-left:44px',
      '<span data-h="k" style="font-size:13.5px;font-weight:600;color:#C99752">שיחת ייעוץ ללא התחייבות</span>' +
      '<h3 data-h="t" style="margin:0;font-size:clamp(22px,5vw,26px);line-height:1.2;letter-spacing:-0.02em;color:#F5F0E4">השאירו שם וטלפון — ונחזור אליכם</h3>' +
      '<p data-h="s" style="margin:0;font-size:14.5px;line-height:1.5;color:rgba(245,240,228,0.78)"></p>');
    form.appendChild(hHead);
    picksW = el('div', 'display:none;gap:10px;padding:12px 14px;border-radius:14px;background:rgba(245,240,228,0.05);border:1px solid rgba(201,151,82,0.35)');
    form.appendChild(picksW);
    var l1 = el('label', S.lab, '<span>שם מלא</span>'); nameI = el('input', S.inp); nameI.type = 'text'; nameI.autocomplete = 'name'; nameI.required = true; l1.appendChild(nameI);
    var l2 = el('label', S.lab, '<span>טלפון</span>');
    var row = el('div', 'display:flex;gap:8px;direction:ltr');
    sel = el('select', S.sel); sel.setAttribute('aria-label', 'קידומת מדינה'); sel.autocomplete = 'tel-country-code';
    C.forEach(function (c) { var o = document.createElement('option'); o.value = c[1]; o.textContent = '+' + c[1] + ' ' + c[0]; o.style.color = '#211C16'; sel.appendChild(o); });
    sel.onchange = setPh;
    telI = el('input', S.inp + ';direction:ltr;text-align:left'); telI.type = 'tel'; telI.inputMode = 'tel'; telI.autocomplete = 'tel-national'; telI.required = true; telI.setAttribute('aria-label', 'טלפון');
    telI.addEventListener('input', detect);
    row.appendChild(sel); row.appendChild(telI); l2.appendChild(row);
    err = el('p', 'margin:0;font-size:13.5px;color:#E8C48C;text-align:center;display:none', 'נא למלא שם ומספר טלפון תקין'); err.setAttribute('role', 'alert');
    btn = el('button', S.btn, 'תאמו שיחת ייעוץ'); btn.type = 'submit';
    var scope = ''; scopeW = el('div', 'display:grid;gap:8px', '<span style="font-size:14px;font-weight:600;color:#F5F0E4">סוג הפרויקט <span style="font-weight:400;color:rgba(245,240,228,0.6)">(לא חובה)</span></span>');
    var scopeR = el('div', 'display:grid;grid-template-columns:1fr 1fr;gap:8px');
    ['רכיב אחד', 'כמה רכיבים יחד', 'מרחב חוץ שלם', 'עוד לא יודעים'].forEach(function (t) {
      var b = el('button', 'min-height:44px;padding:6px 10px;border-radius:12px;border:1px solid rgba(245,240,228,0.25);background:transparent;color:#F5F0E4;font:inherit;font-size:14px;cursor:pointer', t); b.type = 'button'; b.setAttribute('aria-pressed', 'false');
      b.onclick = function () { scopeSet(scope === t ? '' : t); };
      scopeR.appendChild(b);
    });
    scopeSet = function (t) { scope = t; scopeR.querySelectorAll('button').forEach(function (x) { var on = x.textContent === scope; x.setAttribute('aria-pressed', on ? 'true' : 'false'); x.style.background = on ? '#B4813C' : 'transparent'; x.style.color = on ? '#1B1712' : '#F5F0E4'; x.style.borderColor = on ? '#B4813C' : 'rgba(245,240,228,0.25)'; }); try { window.stzLeadScopeChange && window.stzLeadScopeChange(t); } catch (e) {} };
    scopeW.appendChild(scopeR); window.stzLeadScope = function () { return scope; };
    function chipRow(title, items, onPick, cols) {
      var w = el('div', 'display:grid;gap:8px', '<span style="font-size:14px;font-weight:600;color:#F5F0E4">' + title + '</span>');
      var r = el('div', 'display:grid;grid-template-columns:' + (cols || '1fr 1fr') + ';gap:8px');
      items.forEach(function (t) {
        var b = el('button', 'min-height:46px;padding:6px 10px;border-radius:12px;border:1px solid rgba(245,240,228,0.25);background:transparent;color:#F5F0E4;font:inherit;font-size:14px;cursor:pointer', t); b.type = 'button'; b.setAttribute('aria-pressed', 'false');
        b.onclick = function () { var on = b.getAttribute('aria-pressed') !== 'true'; r.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); x.style.background = 'transparent'; x.style.color = '#F5F0E4'; x.style.borderColor = 'rgba(245,240,228,0.25)'; }); if (on) { b.setAttribute('aria-pressed', 'true'); b.style.background = '#B4813C'; b.style.color = '#1B1712'; b.style.borderColor = '#B4813C'; } onPick(on ? t : ''); };
        r.appendChild(b);
      });
      w.appendChild(r); return w;
    }
    var DN = ['א׳', 'ב׳', 'ג׳', 'ד׳', 'ה׳'], days = [], dd = new Date(); dd.setHours(12, 0, 0, 0);
    while (days.length < 6) { dd.setDate(dd.getDate() + 1); if (dd.getDay() <= 4) days.push(DN[dd.getDay()] + ' ' + dd.getDate() + '.' + (dd.getMonth() + 1)); }
    whenW = el('div', 'display:none;gap:14px');
    whenW.appendChild(chipRow('באיזה יום נוח לכם?', days, function (v) { pDay = 'יום ' + v; }, '1fr 1fr 1fr'));
    var TW = { 'בוקר': 'בוקר (8–12)', 'צהריים': 'צהריים (12–16)', 'אחה״צ': 'אחר הצהריים (16–19)' };
    whenW.appendChild(chipRow('באיזו שעה? <span style="font-weight:400;color:rgba(245,240,228,0.6)">בוקר 8–12 · צהריים 12–16 · אחה״צ 16–19</span>', ['בוקר', 'צהריים', 'אחה״צ'], function (v) { pTime = v ? TW[v] : ''; }, '1fr 1fr 1fr'));
    callW = el('div', 'display:none;gap:8px');
    callW.appendChild(chipRow('מתי נוח לדבר? <span style="font-weight:400;color:rgba(245,240,228,0.6)">(לא חובה)</span>', ['בוקר', 'צהריים', 'אחר הצהריים', 'כל שעה'], function (v) { pCall = v; }, '1fr 1fr'));
    form.appendChild(l1); form.appendChild(l2); form.appendChild(whenW); form.appendChild(callW); form.appendChild(scopeW); form.appendChild(err); form.appendChild(btn);
    form.appendChild(el('p', 'margin:0;font-size:12.5px;color:rgba(245,240,228,0.6);text-align:center;line-height:1.5', 'השארת פרטים מהווה הסכמה ליצירת קשר לצורך טיפול בפנייה זו בלבד. <a href="/legal#privacy" target="_blank" rel="noopener" style="color:#C99752">מדיניות הפרטיות</a>'));
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
    if (nm.length < 2 || !window.stzPhoneValid(cur()[1], digits)) { err.textContent = nm.length < 2 ? 'נא למלא שם מלא' : window.stzPhoneHint(C[sel.selectedIndex][1]); err.style.display = 'block'; return; }
    if (mode === 'meeting' && (!pDay || !pTime)) { err.textContent = 'נא לבחור יום ושעה נוחים לפגישה'; err.style.display = 'block'; return; }
    err.style.display = 'none';
    var phone = e164();
    var note = (window.stzLeadNote || '').trim();
    var p = location.pathname.split('/').pop().replace(/\.html$/, '').replace(/^(preview|sim)-/, '');
    var page = /pergola/.test(p) ? 'פרגולות והצללה' : /projects/.test(p) ? 'פרויקטים' : /legal/.test(p) ? 'מידע משפטי' : 'דף הבית';
    var msg = 'פנייה מהטופס הצף · ' + page + (note ? ' | ' + (/^מה מעניין/.test(note) ? '' : 'מה מתאר אותי: ') + note : '');
    var sc = window.stzLeadScope ? window.stzLeadScope() : ''; if (sc && mode !== 'meeting') msg += ' | סוג הפרויקט: ' + sc;
    if (mode === 'meeting') msg = 'בקשת פגישת ייעוץ: ' + pDay + ', ' + pTime + ' | ' + msg; else if (pCall) msg += ' | נוח לדבר: ' + pCall;
    var PK = picks(); if (PK.length) msg += ' | ' + PK.map(function (r) { return r.k + ': ' + r.v.join(', '); }).join(' | ');
    form.style.display = 'none'; done.style.display = 'grid'; try { done.querySelector('p').textContent = mode === 'meeting' ? 'נחזור אליכם בהקדם לאישור הפגישה.' : 'נחזור אליכם בהקדם לתיאום שיחת ייעוץ.'; } catch (x) {}
    var send = window.stzSendLead ? window.stzSendLead({ name: nm, phone: phone, solution: note || page, message: msg, source: (mode === 'meeting' ? 'meeting_' : 'modal_') + page }) : Promise.reject();
    send.catch(function () {
      location.href = 'https://wa.me/972559958231?text=' + encodeURIComponent((mode === 'meeting' ? 'היי, אשמח לתאם פגישת ייעוץ: ' + pDay + ', ' + pTime + '.\nשם: ' : 'היי, אשמח לתאם שיחת ייעוץ.\nשם: ') + nm + '\nטלפון: ' + phone + (note ? '\n' + (/^מה מעניין/.test(note) ? '' : 'מה מתאר אותי: ') + note : ''));
    });
  }
  function setMode(m) {
    mode = m === 'meeting' ? 'meeting' : 'call';
    var T = { k: hHead.querySelector('[data-h=k]'), t: hHead.querySelector('[data-h=t]'), s: hHead.querySelector('[data-h=s]') };
    if (mode === 'meeting') { T.k.textContent = 'פגישת ייעוץ ללא התחייבות'; T.t.textContent = 'בחרו יום ושעה — ונאשר מולכם'; T.s.textContent = 'נחזור אליכם בטלפון לאישור הפגישה והשעה המדויקת.'; btn.textContent = 'בקשת פגישה'; whenW.style.display = 'grid'; callW.style.display = 'none'; }
    else { T.k.textContent = 'שיחת ייעוץ ללא התחייבות'; T.t.textContent = 'השאירו שם וטלפון — ונחזור אליכם'; T.s.textContent = ''; T.s.style.display = 'none'; btn.textContent = 'תאמו שיחת ייעוץ'; whenW.style.display = 'none'; callW.style.display = 'grid'; }
    if (mode === 'meeting') T.s.style.display = 'block';
    scopeW.style.display = mode === 'meeting' ? 'none' : 'grid';
    pDay = ''; pTime = ''; pCall = '';
    [whenW, callW].forEach(function (w) { w.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); x.style.background = 'transparent'; x.style.color = '#F5F0E4'; x.style.borderColor = 'rgba(245,240,228,0.25)'; }); });
  }
  function open(src, m) {
    if (!root) build();
    setMode(m);
    source = src || source;
    last = document.activeElement;
    form.style.display = 'grid'; done.style.display = 'none'; err.style.display = 'none';
    renderPicks();
    try { var pre = window.stzLeadPreset ? window.stzLeadPreset() : ''; if (pre && scopeSet) scopeSet(pre); } catch (e) {}
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
    open((location.pathname.replace(/\//g, '') || 'home'), (a.getAttribute('data-lead-open') === 'meeting' || /פגיש/.test(a.innerText || '')) ? 'meeting' : 'call');
  }, true);

  // Plain <button> CTAs (including the floating bottom bar) open the same window.
  // Form submit buttons are left alone: they have an input/textarea within a few levels above them.
  var CTA = /ייעוץ|פגיש|השארת פרטים|מילוי פרטים|השאירו פרטים|תיאום|צרו קשר|צור קשר/;
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button');
    if (!b || (root && root.contains(b)) || b.type === 'submit' && b.form) return;
    if (!CTA.test(b.innerText || '')) return;
    var p = b, i;
    for (i = 0; i < 4 && p; i++, p = p.parentElement) {
      if (p.querySelector && p.querySelector('input,textarea,select')) return;
    }
    e.preventDefault(); e.stopPropagation();
    open((location.pathname.replace(/\//g, '') || 'home'), (b.getAttribute('data-lead-open') === 'meeting' || /פגיש/.test(b.innerText || '')) ? 'meeting' : 'call');
  }, true);
})();
