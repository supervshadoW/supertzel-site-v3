/* Google Analytics 4 (G-573EPTRPVM) with Consent Mode v2 + cookie banner.
   Same behaviour as the previous site: everything is denied by default and
   GA is configured only after the visitor actively accepts analytics. */
(function () {
  // The page runtime re-runs <helmet> scripts after the browser already ran them; run only once so events and page views are not counted twice.
  if (window.__stzAnalytics) return;
  window.__stzAnalytics = true;
  var GA_ID = 'G-573EPTRPVM';
  var ADS_ID = 'AW-18302540762';
  // Direct Google Ads conversion "WhatsApp - דף נחיתה פרגולות" (account 626-713-5003). Sent only on the campaign landing page.
  var WA_CONVERSION = ADS_ID + '/0egZCPPEq5odENq3qpdE';
  // Direct Google Ads conversion "קליק לחיוג - דף נחיתה פרגולות". Values rank the leads: form 3 (set in Google Ads), WhatsApp 2, call 1.
  var CALL_CONVERSION = ADS_ID + '/LAvhCM7wr5odENq3qpdE';
  function isLanding() { return location.hostname.indexOf('pergola.') === 0 || /^\/pergola(\/|$)/.test(location.pathname) || /[?&]landing=1(&|$)/.test(location.search); }
  // Conversion labels from Google Ads (Tag setup). Fill in to send direct Ads conversions, e.g. lead: 'AbC-D_efG-h12345'.
  var ADS_LABELS = { lead: '', whatsapp: '', call: '' };
  var STORAGE_KEY = 'supertzel_cookie_consent_v2';

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  gtag('consent', 'default', {
    ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
    analytics_storage: 'denied', functionality_storage: 'denied', personalization_storage: 'denied',
    security_storage: 'granted', wait_for_update: 500
  });
  gtag('js', new Date());
  // Advanced consent mode: the Google tags run for every visitor, but until the visitor agrees no cookies are
  // stored and Google receives only cookieless pings (used by Google Ads / GA4 to model conversions).
  gtag('set', 'ads_data_redaction', true);
  gtag('set', 'url_passthrough', true);
  gtag('config', GA_ID, { anonymize_ip: true });
  gtag('config', ADS_ID);

  // gtag.js is loaded after the page has loaded so it does not compete with the page itself; dataLayer queues everything until then.
  var gtagLoaded = false;
  function loadGtag() {
    if (gtagLoaded) return;
    gtagLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }
  if (document.readyState === 'complete') setTimeout(loadGtag, 0);
  else { addEventListener('load', function () { setTimeout(loadGtag, 0); }); setTimeout(loadGtag, 6000); }

  function apply(state) {
    gtag('consent', 'update', {
      analytics_storage: state.analytics ? 'granted' : 'denied',
      functionality_storage: state.analytics ? 'granted' : 'denied',
      ad_storage: state.ads ? 'granted' : 'denied',
      ad_user_data: state.ads ? 'granted' : 'denied',
      ad_personalization: state.ads ? 'granted' : 'denied',
      personalization_storage: 'denied'
    });
    if (state.analytics) clarity();
  }

  // Microsoft Clarity (heatmaps / recordings): loaded only after analytics consent.
  var CLARITY_ID = 'yty9r0kcag', clarityOn = false;
  function clarity() {
    if (clarityOn) return;
    clarityOn = true;
    // stz-clarity-later: inject the script after the page has loaded (calls made before that are queued by the stub below)
    var later = function (fn) { if (document.readyState === 'complete') setTimeout(fn, 0); else addEventListener('load', function () { setTimeout(fn, 0); }); };
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      later(function () {
        t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
        y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
      });
    })(window, document, 'clarity', 'script', CLARITY_ID);
    try { window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: 'granted' }); } catch (e) {}
  }

  function load() {
    try { var p = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'); return p && p.version === 2 ? p : null; } catch (e) { return null; }
  }
  function save(analytics, ads) {
    var st = { version: 2, timestamp: Date.now(), necessary: true, analytics: !!analytics, ads: !!ads, functionality: !!analytics };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(st)); } catch (e) {}
    apply(st);
  }

  function track(name, params) {
    try { gtag('event', name, params || {}); } catch (e) {}
    var key = name === 'generate_lead' ? 'lead' : name === 'whatsapp_click' ? 'whatsapp' : name === 'contact_call' ? 'call' : '';
    if (key && ADS_LABELS[key]) { try { gtag('event', 'conversion', { send_to: ADS_ID + '/' + ADS_LABELS[key] }); } catch (e) {} }
  }
  window.stzTrack = track;

  // Click tracking, each kind of click has its own event (no generic "cta_click"):
  //   WhatsApp links      -> whatsapp_click (+ direct Ads conversion on the landing page)
  //   phone links         -> contact_call
  //   book a call / meeting buttons -> book_meeting_click
  //   lead form           -> generate_lead, sent from lead.js only after validation and a successful send
  var MEETING = /ייעוץ|השארת פרטים|מילוי פרטים|השאירו פרטים|תיאום|תאמו|צרו קשר|צור קשר/;
  function isMeetingClick(el) {
    if (!el || el.closest('#stz-lead-root') || el.closest('#stz-consent') || el.closest('form')) return false;
    var href = el.tagName === 'A' ? (el.getAttribute('href') || '') : '';
    if (el.tagName === 'A' && !/#(lead|contact|quick)$/.test(href) && !el.hasAttribute('data-lead-open')) return false;
    if (!el.hasAttribute('data-lead-open') && !MEETING.test(el.innerText || '')) return false;
    if (el.tagName === 'BUTTON') { // a button that sits next to form fields is a form submit, not a "book a call" button
      var p = el;
      for (var i = 0; i < 4 && p; i++, p = p.parentElement) if (p.querySelector && p.querySelector('input,textarea,select')) return false;
    }
    return true;
  }
  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('a[href],button,[data-lead-open]') : null;
    if (!el) return;
    var h = el.tagName === 'A' ? (el.getAttribute('href') || '') : '';
    if (h.indexOf('wa.me') > -1 || h.indexOf('api.whatsapp.com') > -1 || h.indexOf('whatsapp.com/send') > -1) {
      track('whatsapp_click', { source: location.pathname });
      if (isLanding()) { try { gtag('event', 'conversion', { send_to: WA_CONVERSION, value: 2.0, currency: 'ILS' }); } catch (x) {} }
    } else if (h.indexOf('tel:') === 0) {
      track('contact_call', { source: location.pathname });
      if (isLanding()) { try { gtag('event', 'conversion', { send_to: CALL_CONVERSION, value: 1.0, currency: 'ILS' }); } catch (x) {} }
    }
    else if (isMeetingClick(el)) track('book_meeting_click', { source: location.pathname, label: (el.innerText || '').trim().slice(0, 40) });
  }, true);

  function banner() {
    if (document.getElementById('stz-consent')) return;
    var d = document.createElement('div');
    d.id = 'stz-consent';
    if (!document.getElementById('stz-consent-css')) {
      var st = document.createElement('style'); st.id = 'stz-consent-css';
      // phones: same wording, tighter layout so the banner takes about a quarter of the screen instead of 40%
      st.textContent = '@media (max-width:760px){#stz-consent{inset-inline:8px!important;bottom:8px!important;padding:12px 14px!important;border-radius:16px!important;font-size:12.5px!important;line-height:1.45!important}#stz-consent #stz-consent-t{font-size:14px!important;margin-bottom:3px!important}#stz-consent p{margin:0 0 10px!important}#stz-consent #stz-cc-main{flex-wrap:nowrap!important;gap:6px!important}#stz-consent #stz-cc-main button{min-height:44px!important;font-size:13px!important;flex:1 1 0!important;padding:0 6px!important}#stz-consent #stz-cc-main button[data-a=custom]{flex:0 0 auto!important;padding:0 8px!important}}';
      document.head.appendChild(st);
    }
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-labelledby', 'stz-consent-t');
    d.dir = 'rtl';
    d.style.cssText = 'position:fixed;inset-inline:12px;bottom:12px;z-index:2147483000;max-width:560px;margin-inline:auto;background:#1B1712;color:#F5F0E4;border:1px solid rgba(201,151,82,.45);border-radius:18px;padding:18px 20px;box-shadow:0 18px 50px rgba(0,0,0,.45);font:14px/1.6 inherit;font-family:inherit';
    d.innerHTML =
      '<div id="stz-consent-t" style="font-weight:700;font-size:16px;margin-bottom:6px">אנחנו מכבדים את הפרטיות שלך</div>' +
      '<p style="margin:0 0 14px;opacity:.9">האתר משתמש בעוגיות (Cookies) כדי לתפעל שירותים בסיסיים, וכן — אם תסכים/י — כדי לנתח ביקורים באמצעות Google Analytics. ללא הסכמה לא נשמרות עוגיות כאלה, ונשלחים אותות אנונימיים בלבד. חלק מהמידע מעובד בשרתי ספקים בחו״ל. באפשרותך לקבל, לדחות או להתאים אישית. <a href="/legal#privacy" style="color:#C99752;white-space:nowrap">למידע מלא — מדיניות הפרטיות</a></p>' +
      '<div id="stz-cc-custom" style="display:none;margin:0 0 14px;gap:10px;flex-direction:column">' +
      '<label style="display:flex;gap:10px;align-items:flex-start"><input type="checkbox" id="stz-cc-an" style="margin-top:5px"><span><strong>ניתוח ביקורים</strong><br><span style="opacity:.8;font-size:13px">Google Analytics ו-Microsoft Clarity: סטטיסטיקה, מפות חום והקלטות גלישה.</span></span></label>' +
      '<label style="display:flex;gap:10px;align-items:flex-start"><input type="checkbox" id="stz-cc-ad" style="margin-top:5px"><span><strong>פרסום ומדידת קמפיינים</strong><br><span style="opacity:.8;font-size:13px">Google Ads: מדידת פניות שהגיעו ממודעות.</span></span></label>' +
      '<button type="button" data-a="save" style="min-height:44px;border:0;border-radius:100px;background:#B4813C;color:#1B1712;font:inherit;font-weight:700;cursor:pointer">שמירת הבחירה</button>' +
      '</div>' +
      '<div id="stz-cc-main" style="display:flex;gap:8px;flex-wrap:wrap">' +
      '<button type="button" data-a="1" style="flex:1;min-height:44px;border:0;border-radius:100px;background:#B4813C;color:#1B1712;font:inherit;font-weight:700;cursor:pointer">קבל הכל</button>' +
      '<button type="button" data-a="0" style="flex:1;min-height:44px;border:1px solid rgba(245,240,228,.4);border-radius:100px;background:transparent;color:#F5F0E4;font:inherit;cursor:pointer">דחה הכל</button>' +
      '<button type="button" data-a="custom" style="flex:1 1 100%;min-height:40px;border:0;background:transparent;color:#C99752;font:inherit;text-decoration:underline;cursor:pointer">התאמה אישית</button>' +
      '</div>';
    d.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-a]');
      if (!b) return;
      var a = b.getAttribute('data-a');
      if (a === 'custom') {
        var cur = load() || {};
        d.querySelector('#stz-cc-an').checked = !!cur.analytics;
        d.querySelector('#stz-cc-ad').checked = !!cur.ads;
        d.querySelector('#stz-cc-custom').style.display = 'flex';
        d.querySelector('#stz-cc-main').style.display = 'none';
        return;
      }
      if (a === 'save') save(d.querySelector('#stz-cc-an').checked, d.querySelector('#stz-cc-ad').checked);
      else save(a === '1', a === '1');
      d.remove();
    });
    document.body.appendChild(d);
  }
  window.openCookieSettings = banner;

  // Safety net: if the page ever shows raw template text ({{ ... }}) because the page script failed to run, reload once.
  setTimeout(function () {
    try {
      if (document.body && /\{\{\s*[\w.]+\s*\}\}/.test(document.body.innerText) && !sessionStorage.getItem('stz_reloaded')) {
        sessionStorage.setItem('stz_reloaded', '1');
        location.reload();
      }
    } catch (e) {}
  }, 5000);

  var saved = load();
  if (saved) apply(saved);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(banner, 400); });
  else setTimeout(banner, 400);
})();
