/* Google Analytics 4 (G-573EPTRPVM) with Consent Mode v2 + cookie banner.
   Same behaviour as the previous site: everything is denied by default and
   GA is configured only after the visitor actively accepts analytics. */
(function () {
  var GA_ID = 'G-573EPTRPVM';
  var STORAGE_KEY = 'supertzel_cookie_consent_v2';

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  gtag('consent', 'default', {
    ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
    analytics_storage: 'denied', functionality_storage: 'denied', personalization_storage: 'denied',
    security_storage: 'granted', wait_for_update: 500
  });
  gtag('js', new Date());

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);

  function apply(state) {
    gtag('consent', 'update', {
      analytics_storage: state.analytics ? 'granted' : 'denied',
      functionality_storage: state.analytics ? 'granted' : 'denied',
      ad_storage: state.ads ? 'granted' : 'denied',
      ad_user_data: state.ads ? 'granted' : 'denied',
      ad_personalization: state.ads ? 'granted' : 'denied',
      personalization_storage: 'denied'
    });
    if (state.analytics) { gtag('config', GA_ID, { anonymize_ip: true }); clarity(); }
  }

  // Microsoft Clarity (heatmaps / recordings): loaded only after analytics consent.
  var CLARITY_ID = 'yty9r0kcag', clarityOn = false;
  function clarity() {
    if (clarityOn) return;
    clarityOn = true;
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
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

  function track(name, params) { try { gtag('event', name, params || {}); } catch (e) {} }
  window.stzTrack = track;

  // Click tracking: WhatsApp, phone call.
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('wa.me') > -1 || h.indexOf('api.whatsapp.com') > -1) track('contact_whatsapp', { source: location.pathname });
    else if (h.indexOf('tel:') === 0) track('contact_call', { source: location.pathname });
  }, true);

  function banner() {
    if (document.getElementById('stz-consent')) return;
    var d = document.createElement('div');
    d.id = 'stz-consent';
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-labelledby', 'stz-consent-t');
    d.dir = 'rtl';
    d.style.cssText = 'position:fixed;inset-inline:12px;bottom:12px;z-index:2147483000;max-width:560px;margin-inline:auto;background:#1B1712;color:#F5F0E4;border:1px solid rgba(201,151,82,.45);border-radius:18px;padding:18px 20px;box-shadow:0 18px 50px rgba(0,0,0,.45);font:14px/1.6 inherit;font-family:inherit';
    d.innerHTML =
      '<div id="stz-consent-t" style="font-weight:700;font-size:16px;margin-bottom:6px">אנחנו מכבדים את הפרטיות שלך</div>' +
      '<p style="margin:0 0 14px;opacity:.9">האתר משתמש בעוגיות (Cookies) כדי לתפעל שירותים בסיסיים, וכן — אם תסכים/י — כדי לנתח ביקורים באמצעות Google Analytics. חלק מהמידע מעובד בשרתי ספקים בחו״ל. באפשרותך לקבל, לדחות או להתאים אישית. <a href="/legal#privacy" style="color:#C99752;white-space:nowrap">למידע מלא — מדיניות הפרטיות</a></p>' +
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

  var saved = load();
  if (saved) apply(saved);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(banner, 400); });
  else setTimeout(banner, 400);
})();
