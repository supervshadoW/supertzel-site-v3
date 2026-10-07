// Shared lead sender — same Supabase edge functions the old site used (send-email + send-whatsapp).
(function () {
  var KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVoaGRrb2V0c21lY3RpeXhzamViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3MzQzOTcsImV4cCI6MjA3NzMxMDM5N30.taMFBuO-L6XoRmXPaDO510HOeFS-LnpAKtwS3xcEmas';
  var BASE = 'https://ehhdkoetsmectiyxsjeb.supabase.co/functions/v1/';
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid'];
  try {
    var q = new URLSearchParams(location.search), got = {};
    UTM_KEYS.forEach(function (k) { if (q.get(k)) got[k] = q.get(k); });
    if (Object.keys(got).length) sessionStorage.setItem('stz-utm', JSON.stringify(got));
  } catch (e) {}
  function utmText() {
    try {
      var u = JSON.parse(sessionStorage.getItem('stz-utm') || '{}');
      var parts = Object.keys(u).map(function (k) { return k + '=' + u[k]; });
      return parts.length ? ' | ' + parts.join(', ') : '';
    } catch (e) { return ''; }
  }
  window.stzSendLead = function (p) {
    var body = JSON.stringify({
      name: String(p.name || '').trim(),
      phone: String(p.phone || '').trim(),
      type: 'contact',
      solution: p.solution || '',
      message: (p.message || '') + ' | עמוד: ' + location.pathname + utmText()
    });
    var H = { 'Content-Type': 'application/json', Authorization: 'Bearer ' + KEY, apikey: KEY };
    fetch(BASE + 'send-whatsapp', { method: 'POST', headers: H, body: body }).catch(function () {});
    return fetch(BASE + 'send-email', { method: 'POST', headers: H, body: body }).then(function (r) {
      if (!r.ok) throw new Error('send-email ' + r.status);
      try { if (window.gtag) window.gtag('event', 'generate_lead', { form: p.source || 'site' }); } catch (e) {}
    });
  };
})();
