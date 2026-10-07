/* Lead delivery: posts the form to the existing Supabase `send-email` function.
   Runs in addition to the WhatsApp redirect; never blocks or throws. */
(function () {
  var URL = 'https://ehhdkoetsmectiyxsjeb.supabase.co/functions/v1/send-email';
  var KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVoaGRrb2V0c21lY3RpeXhzamViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3MzQzOTcsImV4cCI6MjA3NzMxMDM5N30.taMFBuO-L6XoRmXPaDO510HOeFS-LnpAKtwS3xcEmas';
  var PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid'];
  var STORE = 'stz_attribution';

  function readStore() {
    try { return JSON.parse(sessionStorage.getItem(STORE) || '{}'); } catch (e) { return {}; }
  }

  // Remember UTM / gclid from the landing URL for the rest of the visit.
  try {
    var q = new URLSearchParams(location.search), saved = readStore(), changed = false;
    PARAMS.forEach(function (k) { if (q.get(k)) { saved[k] = q.get(k); changed = true; } });
    if (changed) sessionStorage.setItem(STORE, JSON.stringify(saved));
  } catch (e) {}

  window.stzSendLead = function (lead) {
    try {
      var attr = readStore();
      var tail = PARAMS.filter(function (k) { return attr[k]; }).map(function (k) { return k + '=' + attr[k]; }).join(' | ');
      var message = [lead.page ? 'עמוד: ' + lead.page : '', lead.message || '', tail ? 'מקור: ' + tail : '']
        .filter(Boolean).join(' | ').slice(0, 1900);
      var body = { type: 'contact', name: String(lead.name || '').trim(), phone: String(lead.phone || '').trim(), message: message };
      if (lead.city) body.city = String(lead.city).slice(0, 100);
      if (lead.solution) body.solution = String(lead.solution).slice(0, 200);
      fetch(URL, {
        method: 'POST',
        keepalive: true,
        headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + KEY, apikey: KEY },
        body: JSON.stringify(body)
      }).catch(function () {});
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'form_submit', { event_category: 'contact', form_location: lead.page || '' });
        window.gtag('event', 'generate_lead', { form_location: lead.page || '', solution: lead.solution || '' });
      }
    } catch (e) {}
  };
})();
