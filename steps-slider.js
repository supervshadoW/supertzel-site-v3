// Work-steps slider: panels open one after another, with a gold timing bar under each step.
(function () {
  var css = '' +
    '[data-stepsl]{display:flex!important;flex-direction:row!important;gap:8px!important;grid-template-columns:none!important;align-items:stretch;overflow:visible!important;margin-inline:0!important;padding:0!important}' +
    '[data-stepsl]>div{position:relative;flex:1 1 0!important;max-width:none!important;min-width:0;min-height:150px;cursor:pointer;display:flex!important;flex-direction:column!important;align-items:flex-start!important;gap:10px!important;padding:16px 14px 20px!important;border:0!important;border-radius:16px!important;background:rgba(245,240,228,0.06)!important;overflow:hidden;transition:flex-grow .7s cubic-bezier(.2,.7,.2,1),background .4s ease}' +
    // all steps stay the same width and always show their title and text (no empty boxes); the active one is only highlighted
    '[data-stepsl]>div[data-on]{background:rgba(245,240,228,0.13)!important}' +
    '[data-stepsl]>div>div{min-width:0;opacity:.72;transition:opacity .35s ease}' +
    '[data-stepsl]>div[data-on]>div{opacity:1}' +
    '[data-stepsl]>div::after{content:"";position:absolute;inset-inline:14px;bottom:10px;height:3px;border-radius:100px;background:rgba(245,240,228,0.18)}' +
    '[data-stepsl]>div::before{content:"";position:absolute;inset-inline-start:14px;bottom:10px;height:3px;width:0;border-radius:100px;background:#C99752;z-index:1}' +
    '[data-stepsl]>div[data-done]::before{width:calc(100% - 28px)}' +
    '[data-stepsl][data-run]>div[data-on]::before{animation:stzStepFill 4.2s linear forwards}' +
    '[data-stepsl]:hover>div[data-on]::before{animation-play-state:paused}' +
    '@keyframes stzStepFill{from{width:0}to{width:calc(100% - 28px)}}' +
    '@media (max-width:760px){[data-stepsl]{flex-direction:column!important;gap:8px!important}'+
    '[data-stepsl]>div{flex:none!important;min-height:0!important;flex-direction:row!important;align-items:baseline!important;gap:14px!important;padding:14px 16px 20px!important}'+
    '[data-stepsl]>div>div{min-width:0!important;opacity:1!important;transform:none!important}'+
    '[data-stepsl]>div:not([data-on])>div p{display:none}'+
    '[data-stepsl]>div[data-on]{background:rgba(245,240,228,0.13)!important}}' +
    '@media (prefers-reduced-motion:reduce){[data-stepsl]>div,[data-stepsl]>div>div{transition:none}[data-stepsl][data-run]>div[data-on]::before{animation:none;width:calc(100% - 28px)}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  function init(c) {
    if (c._sl) return; var kids = [].slice.call(c.children); if (kids.length < 2) return; c._sl = true;
    var cur = 0;
    function go(i) { cur = (i + kids.length) % kids.length; kids.forEach(function (k, j) { if (j === cur) k.setAttribute('data-on', ''); else k.removeAttribute('data-on'); if (j < cur) k.setAttribute('data-done', ''); else k.removeAttribute('data-done'); }); }
    kids.forEach(function (k, j) { k.setAttribute('role', 'button'); k.tabIndex = 0; k.addEventListener('click', function () { go(j); }); k.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(j); } }); });
    c.addEventListener('animationend', function (e) { if (e.animationName === 'stzStepFill') go(cur + 1); });
    go(0);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) c.setAttribute('data-run', ''); else c.removeAttribute('data-run'); }); }, { threshold: 0.4 }).observe(c);
    else c.setAttribute('data-run', '');
  }
  function scan() { [].forEach.call(document.querySelectorAll('[data-stepsl]'), init); }
  setInterval(scan, 800); addEventListener('load', scan);
})();
