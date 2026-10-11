// Section index ("פרקים") docked at the top of the side scroll rail. Visible to visitors.
(function () {
  function labelOf(sec) {
    if (sec.id === 'hero') return 'פתיחה';
    var kick = [].slice.call(sec.querySelectorAll('div,span')).find(function (el) { var t = el.textContent || ''; return /^\s*\d\d · /.test(t) && t.length < 60; });
    var k = sec.querySelector('h2, h1');
    var t = (kick ? kick.textContent : (k ? k.textContent : sec.id)) || sec.id;
    return t.replace(/\s+/g, ' ').trim().slice(0, 42);
  }
  function build() {
    var secs = [].slice.call(document.querySelectorAll('main section[id], section[id]'))
      .filter(function (s, i, a) { return a.indexOf(s) === i && s.offsetHeight > 40; });
    if (!secs.length) return;
    var root = document.createElement('div');
    root.setAttribute('data-stz-chapters', '');
    root.style.cssText = 'position:fixed;left:10px;top:76px;z-index:2147483000;font:500 13px/1.3 system-ui,sans-serif;color:#F5F0E4;display:flex;flex-direction:column;align-items:flex-start;gap:6px;direction:ltr;transition:opacity .3s';
    var tab = document.createElement('button');
    tab.type = 'button'; tab.setAttribute('aria-label', 'רשימת הפרקים'); tab.setAttribute('aria-expanded', 'false');
    tab.style.cssText = 'all:unset;cursor:pointer;display:flex;align-items:center;gap:7px;height:32px;padding:0 11px;border-radius:100px;background:#1B1712;border:1px solid #C99752;color:#F5F0E4;font:600 12.5px/1 system-ui,sans-serif;box-shadow:0 4px 14px rgba(0,0,0,0.25)';
    tab.innerHTML = '<span aria-hidden="true" style="display:flex;flex-direction:column;gap:3px"><i style="display:block;width:12px;height:1.5px;background:#C99752"></i><i style="display:block;width:12px;height:1.5px;background:#C99752"></i><i style="display:block;width:8px;height:1.5px;background:#C99752"></i></span><span dir="rtl">פרקים</span>';
    var panel = document.createElement('div');
    panel.setAttribute('dir', 'rtl');
    panel.style.cssText = 'display:none;flex-direction:column;max-height:60vh;overflow:auto;min-width:220px;max-width:min(78vw,290px);background:rgba(27,23,18,0.96);border:1px solid rgba(201,151,82,0.5);border-radius:14px;padding:6px;box-shadow:0 12px 30px rgba(0,0,0,0.35)';
    var rows = secs.map(function (s, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.style.cssText = 'all:unset;cursor:pointer;display:flex;gap:10px;align-items:center;padding:9px 10px;border-radius:9px;min-height:26px';
      b.innerHTML = '<span style="color:#C99752;font-weight:700;min-width:18px"></span><span></span>';
      b.children[0].textContent = i + 1;
      b.children[1].textContent = labelOf(s);
      b.onclick = function () { go(i); };
      panel.appendChild(b);
      return b;
    });
    function setOpen(o) { panel.style.display = o ? 'flex' : 'none'; tab.setAttribute('aria-expanded', o ? 'true' : 'false'); }
    tab.onclick = function () { setOpen(panel.style.display === 'none'); };
    document.addEventListener('click', function (e) { if (!root.contains(e.target)) setOpen(false); });
    root.appendChild(tab); root.appendChild(panel);
    document.body.appendChild(root);
    function go(i) { var y = secs[i].getBoundingClientRect().top + window.scrollY - 64; window.scrollTo({ top: y, behavior: 'smooth' }); setOpen(false); }
    function idx() { var best = 0; secs.forEach(function (s, i) { if (s.getBoundingClientRect().top - 90 <= 0) best = i; }); return best; }
    function upd() { var i = idx(); rows.forEach(function (r, j) { r.style.background = j === i ? 'rgba(201,151,82,0.22)' : 'transparent'; }); }
    function dock() {
      var rail = document.querySelector('nav[aria-label="גלילה מהירה בין פרקים"]');
      var r = rail && rail.getBoundingClientRect();
      var cs = rail && getComputedStyle(rail);
      if (r && r.height > 40 && cs.display !== 'none') {
        root.style.left = Math.max(4, Math.round(r.left + r.width / 2 - 16)) + 'px';
        root.style.top = Math.max(72, Math.round(r.top - 42)) + 'px';
        var op = +cs.opacity; root.style.opacity = String(op); root.style.pointerEvents = op > 0.1 ? 'auto' : 'none';
        if (op <= 0.1) setOpen(false);
      } else { root.style.opacity = '0'; root.style.pointerEvents = 'none'; setOpen(false); }
    }
    addEventListener('scroll', function () { upd(); dock(); }, { passive: true });
    addEventListener('resize', dock); setInterval(dock, 800); upd(); dock();
  }
  function ready() { setTimeout(build, 900); }
  if (document.readyState === 'complete') ready(); else addEventListener('load', ready);
})();
