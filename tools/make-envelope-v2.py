#!/usr/bin/env python3
"""Builds envelope-v2.html: the lean "journey" version of the envelope campaign page, generated from envelope.html (the approved live page).

envelope.html is only read. The design system, header, hero with numbered pins, floating bar, project carousel, footer and scripts stay as they are;
only these differ:
  * H1 "איש קשר אחד, מהמדידה ועד המסירה." and the approved sub line instead of the hero slide description;
  * sections why / social / scope / services / build / fit (flipping book) / reviews / faq are removed;
  * new "choose" section (two photo cards, optional style chips) and a short contact section (name, phone, which space + WhatsApp + phone);
  * header menu, side chapters and the "design inspiration" bar point only at sections that still exist; no email address anywhere.

Run from the repository root after any change to envelope.html:  python3 tools/make-envelope-v2.py
Every replacement must match exactly once; if envelope.html changed that text the script says which one and writes nothing.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST = os.path.join(ROOT, 'envelope.html'), os.path.join(ROOT, 'envelope-v2.html')
t = open(SRC, encoding='utf-8').read()
problems = []


def rep(old, new, label, count=1):
    global t
    n = t.count(old)
    if n != count:
        problems.append(f'"{label}": expected {count} match(es), found {n}')
        return
    t = t.replace(old, new)


def cut_section(sid, label=None):
    """removes <section id="sid" ...> ... </section> (depth aware) and returns the removed text"""
    global t
    m = re.search(r'[ \t]*<section id="%s"' % re.escape(sid), t)
    if not m:
        problems.append(f'section {sid}: not found')
        return ''
    depth, pos = 0, m.start()
    for tag in re.finditer(r'<section\b|</section>', t[m.start():]):
        depth += 1 if tag.group(0).startswith('<section') else -1
        if depth == 0:
            end = m.start() + tag.end()
            removed = t[m.start():end]
            t = t[:m.start()] + '@@' + sid.upper() + '@@' + t[end:]
            return removed
    problems.append(f'section {sid}: no closing tag')
    return ''


# --- head --------------------------------------------------------------------------------------------------------------------
rep('<title>מעטפת חוץ שלמה לבית | IL Projects</title>', '<title>איש קשר אחד, מהמדידה ועד המסירה | IL Projects</title>', 'title')
rep('<meta name="description" content="מעטפת חוץ שלמה לבית: פרגולה, סגירת זכוכית, מטבח חוץ ודק — פרויקט אחד, מעטפת אחת.">',
    '<meta name="description" content="איש קשר אחד, מהמדידה ועד המסירה. חלל חוץ שלם, מעטפת מקצועית אחת.">', 'description')
rep('<meta property="og:title" content="IL Projects — פרויקט חוץ שלם, מעטפת אחת">',
    '<meta property="og:title" content="IL Projects — איש קשר אחד, מהמדידה ועד המסירה">', 'og title')

# --- hero text ---------------------------------------------------------------------------------------------------------------
rep('animation:stz-up 1.1s 0.35s both">פרויקט חוץ שלם,<br><span style="display:block;min-height:1.1em;color:#C99752;font-weight:300">מעטפת אחת.</span></h1>',
    'animation:stz-up 1.1s 0.35s both">איש קשר אחד,<br><span style="display:block;min-height:1.1em;color:#C99752;font-weight:300">מהמדידה ועד המסירה.</span></h1>', 'h1')
rep('margin-bottom:22px">{{ heroDesc }}</p>', 'margin-bottom:22px">חלל חוץ שלם. מעטפת מקצועית אחת.</p>', 'hero sub line')

# --- header and menu: only sections that exist -------------------------------------------------------------------------------
rep('''        <a href="#why" style="font-size:15px;white-space:nowrap">למה מעטפת</a>
        <a href="#services" style="font-size:15px;white-space:nowrap">מה אנחנו עושים</a>
        <a href="#projects" style="font-size:15px;white-space:nowrap">פרויקטים</a>
        <a href="#fit" style="font-size:15px;white-space:nowrap">איך זה עובד</a>
        <a href="#faq" style="font-size:15px;white-space:nowrap">שאלות</a>''',
    '''        <a href="#choose" style="font-size:15px;white-space:nowrap">מה בונים</a>
        <a href="#projects" style="font-size:15px;white-space:nowrap">פרויקטים</a>''', 'desktop nav')
for sid in ('why', 'services', 'fit', 'faq'):
    m = re.search(r'    <a href="#%s" onClick="\{\{ menuClose \}\}"[^\n]*\n' % sid, t)
    if not m:
        problems.append(f'mobile menu link {sid}: not found')
    else:
        t = t[:m.start()] + t[m.end():]
rep('    <a href="#projects" onClick="{{ menuClose }}"', '    <a href="#choose" onClick="{{ menuClose }}" style="display:flex;align-items:center;justify-content:space-between;min-height:54px;border-bottom:1px solid rgba(245,240,228,0.14);font-size:20px;font-weight:500;color:#F5F0E4"><span>מה בונים</span><span aria-hidden="true" style="color:#C99752;font-size:16px">←</span></a>\n    <a href="#projects" onClick="{{ menuClose }}"', 'mobile menu choose')
rep('''      { id: 'why', n: '01', label: 'מעטפת מקצועית לחלל החוץ' },
      { id: 'services', n: '02', label: 'מרכיבי המעטפת' },
      { id: 'fit', n: '03', label: 'למי זה מתאים' },
      { id: 'projects', n: '04', label: 'מהשטח' },
      { id: 'faq', n: '05', label: 'לפני שבוחרים' }''',
    '''      { id: 'choose', n: '01', label: 'מה בונים' },
      { id: 'projects', n: '02', label: 'מהשטח' },
      { id: 'contact', n: '03', label: 'השאירו פרטים' }''', 'chapters')
rep("const el = document.getElementById('scope'); if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 70, behavior: 'smooth' }); },",
    "const el = document.getElementById('choose'); if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 70, behavior: 'smooth' }); },", 'pthSwap target')

# --- remove the long sections ------------------------------------------------------------------------------------------------
contact_old = ''
for sid in ('why', 'social', 'scope', 'services', 'build', 'fit', 'reviews', 'faq'):
    cut_section(sid)
contact_old = cut_section('contact')
for sid in ('why', 'social', 'scope', 'services', 'build', 'fit', 'reviews', 'faq'):
    t = t.replace('@@' + sid.upper() + '@@', '')

# the coordination paragraph is taken from the approved contact section, word for word
m = re.search(r'<p style="font-size:14\.5px;color:rgba\(245,240,228,0\.74\);line-height:1\.8;max-width:62ch">(בפרויקטים הכוללים.*?)</p>', contact_old, re.S)
if not m:
    problems.append('coordination paragraph: not found')
    coord = ''
else:
    coord = m.group(1)

KICK = ('<div style="display:inline-flex;align-items:center;gap:10px;color:%s;font-size:14.5px;font-weight:600;margin-bottom:18px;white-space:nowrap">'
        '<span style="display:block;width:24px;height:1px;background:%s"></span>%s</div>')
WA = 'https://wa.me/972559958231?text=' + 'היי%2C%20הגעתי%20מדף%20המעטפת%20באתר%20ואשמח%20לשמוע%20עוד.'
INP = ('width:100%;padding:14px 18px;border:1px solid rgba(245,240,228,0.22);background:rgba(245,240,228,0.03);border-radius:16px;'
       'color:#F5F0E4;font:inherit;font-size:16px;box-sizing:border-box')

CHOOSE = '''  <section id="choose" style="padding-block:clamp(3rem,9vh,6rem) clamp(1.5rem,4vh,3rem)">
    <div style="width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto">
      ''' + KICK % ('#80561E', '#C99752', 'מה אתם בונים') + '''
      <h2 style="font-size:clamp(30px,3.9vw,48px);letter-spacing:-0.025em;line-height:1.1;margin-bottom:clamp(1.25rem,3vh,2rem)">איפה מתחילים?</h2>
      <div class="env2-cards" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:16px">
        <button type="button" class="env2-card" data-space="גינה ופרויקט חוץ מלא" aria-pressed="false" style="position:relative;display:block;padding:0;border:2px solid transparent;border-radius:20px;overflow:hidden;cursor:pointer;aspect-ratio:4/3;text-align:right;background:#26201A;color:#F5F0E4;font:inherit">
          <img src="/img/fast/gallery/project-wood-pergola-garden.webp" alt="פרגולת עץ בגינה פרטית" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
          <span style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(17,14,11,0) 35%,rgba(17,14,11,0.82) 100%)"></span>
          <span style="position:absolute;inset-inline:0;bottom:0;display:flex;flex-direction:column;gap:4px;padding:24px 22px 22px"><span style="font-size:clamp(22px,2.4vw,28px);font-weight:600;letter-spacing:-0.02em">גינה ופרויקט חוץ מלא</span><span style="font-size:15.5px;color:rgba(245,240,228,0.82)">מרחב אחד, מהתכנון היישומי ועד המסירה.</span></span>
        </button>
        <button type="button" class="env2-card" data-space="סגירת מרפסת" aria-pressed="false" style="position:relative;display:block;padding:0;border:2px solid transparent;border-radius:20px;overflow:hidden;cursor:pointer;aspect-ratio:4/3;text-align:right;background:#26201A;color:#F5F0E4;font:inherit">
          <img src="/img/fast/gallery/project-black-glass-balcony.webp" alt="מרפסת סגורה בזכוכית עם מסגרת שחורה" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
          <span style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(17,14,11,0) 35%,rgba(17,14,11,0.82) 100%)"></span>
          <span style="position:absolute;inset-inline:0;bottom:0;display:flex;flex-direction:column;gap:4px;padding:24px 22px 22px"><span style="font-size:clamp(22px,2.4vw,28px);font-weight:600;letter-spacing:-0.02em">סגירת מרפסת</span><span style="font-size:15.5px;color:rgba(245,240,228,0.82)">סגירה בזכוכית, לפי המרפסת שלכם.</span></span>
        </button>
      </div>
      <div role="group" aria-label="סגנון" style="display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:20px">
        <span style="font-size:15.5px;font-weight:500;margin-inline-end:6px">ואיזה סגנון מדבר אליכם?</span>
        <button type="button" class="env2-chip" data-style="מודרני" aria-pressed="false">מודרני</button>
        <button type="button" class="env2-chip" data-style="עץ חם" aria-pressed="false">עץ חם</button>
        <button type="button" class="env2-chip" data-style="אורבני" aria-pressed="false">אורבני</button>
      </div>
    </div>
  </section>
'''

CONTACT = '''  <section id="contact" style="position:relative;background:#1B1712;color:#F5F0E4;padding-block:clamp(3.25rem,10vh,7.5rem);overflow:hidden">
    <span id="quick" aria-hidden="true" style="position:absolute;top:0;scroll-margin-top:70px"></span>
    <span style="position:absolute;width:600px;height:600px;bottom:-260px;inset-inline-start:-200px;background:radial-gradient(circle,rgba(180,129,60,0.14) 0%,transparent 70%);pointer-events:none"></span>
    <div style="width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto;position:relative;z-index:1;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:clamp(2.5rem,6vw,5rem);align-items:start">
      <div>
        <img src="/img/logo-il-dark-bg.png" alt="IL Projects | סופר צל" style="display:block;height:52px;width:auto;margin-bottom:30px">
        ''' + KICK % ('#C99752', '#C99752', 'השאירו פרטים') + '''
        <h2 style="font-size:clamp(30px,3.9vw,48px);letter-spacing:-0.025em;color:#F5F0E4;margin-bottom:22px">נחזור אליכם</h2>
        <p style="color:rgba(245,240,228,0.72);font-size:17.5px;max-width:40ch;margin-bottom:36px">שם, טלפון ואיזה מרחב. זה הכול.</p>
        <div style="display:flex;flex-direction:column;gap:18px;margin-bottom:36px">
          <div style="display:flex;flex-direction:column;gap:3px;border-top:1px solid rgba(245,240,228,0.16);padding-top:14px"><span style="font-size:12.5px;color:#C99752">טלפון</span><a href="tel:0553100154" style="font-size:17px;color:#F5F0E4">055-310-0154</a></div>
          <div style="display:flex;flex-direction:column;gap:3px;border-top:1px solid rgba(245,240,228,0.16);padding-top:14px"><span style="font-size:12.5px;color:#C99752">וואטסאפ</span><a href="''' + WA + '''" style="font-size:17px;color:#F5F0E4">055-995-8231</a></div>
        </div>
        <p style="font-size:14.5px;color:rgba(245,240,228,0.74);line-height:1.8;max-width:62ch">''' + coord + '''</p>
      </div>
      <div style="background:rgba(245,240,228,0.04);border:1px solid rgba(245,240,228,0.18);border-radius:26px;padding:clamp(1.5rem,3vw,2.75rem)">
        <form id="env2-form" novalidate style="display:grid;gap:18px">
          <label style="display:grid;gap:8px"><span style="font-size:15px;font-weight:600;color:#F5F0E4">שם</span><input id="env2-name" name="name" autocomplete="name" style="''' + INP + '''"></label>
          <label style="display:grid;gap:8px"><span style="font-size:15px;font-weight:600;color:#F5F0E4">טלפון</span><input id="env2-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" style="''' + INP + ''';direction:ltr;text-align:right"></label>
          <label style="display:grid;gap:8px"><span style="font-size:15px;font-weight:600;color:#F5F0E4">איזה מרחב?</span>
            <select id="env2-space" name="space" style="''' + INP + '''"><option>גינה ופרויקט חוץ מלא</option><option>סגירת מרפסת</option><option>פנטהאוז</option><option>עדיין בודקים</option></select></label>
          <p id="env2-err" role="alert" style="min-height:1.2em;font-size:14.5px;color:#F2A99B"></p>
          <button type="submit" id="env2-send" style="display:inline-flex;align-items:center;justify-content:center;min-height:56px;padding:0 34px;border:0;border-radius:100px;background:#B4813C;color:#1B1712;font:inherit;font-size:17px;font-weight:600;cursor:pointer;box-shadow:0 10px 30px rgba(180,129,60,0.28)">השאירו פרטים</button>
          <p style="font-size:13.5px;color:rgba(245,240,228,0.62)">בשליחת הפרטים אתם מאשרים שניצור איתכם קשר. <a href="/legal#privacy" style="color:#E8C48C;text-decoration:underline">מדיניות פרטיות</a></p>
        </form>
        <div id="env2-ok" hidden style="display:none;flex-direction:column;justify-content:center;min-height:240px;gap:16px">
          <h3 style="font-size:26px;color:#F5F0E4">הפנייה נשלחה</h3>
          <p style="color:rgba(245,240,228,0.72);font-size:16px;max-width:34ch">נחזור אליכם בהקדם. אם נוח לכם, אפשר גם לכתוב לנו בוואטסאפ.</p>
          <a href="''' + WA + '''" style="align-self:flex-start;margin-top:8px;background:#B4813C;color:#1B1712;padding:15px 32px;font-size:16px;font-weight:600;border-radius:100px">וואטסאפ</a>
        </div>
        <a href="''' + WA + '''" style="display:flex;align-items:center;justify-content:center;min-height:52px;margin-top:18px;border:1px solid rgba(245,240,228,0.35);border-radius:100px;color:#F5F0E4;font-size:16px;font-weight:500">או ישר בוואטסאפ</a>
      </div>
    </div>
  </section>
'''

SCRIPT = '''<style>
.env2-chip{min-height:44px;padding:0 20px;border-radius:100px;border:1px solid rgba(33,28,22,0.3);background:transparent;color:#211C16;font:inherit;font-size:15.5px;cursor:pointer;transition:background .2s,color .2s}
.env2-chip[aria-pressed="true"]{background:#211C16;color:#F5F0E4;border-color:#211C16}
.env2-card[aria-pressed="true"]{border-color:#B4813C!important}
.env2-card img{transition:transform .6s ease}.env2-card:hover img{transform:scale(1.03)}
.env2-card:focus-visible,.env2-chip:focus-visible,#env2-form input:focus-visible,#env2-form select:focus-visible{outline:3px solid #C99752;outline-offset:2px}
#env2-form input:focus,#env2-form select:focus{outline:none;border-color:#C99752;background:rgba(245,240,228,0.06)}
#env2-form select option{color:#1B1712}
@media (prefers-reduced-motion:reduce){.env2-card img{transition:none}}
</style>
<script>
(function(){
  function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn)}
  ready(function(){
    var space='',style='';
    document.addEventListener('click',function(e){
      var c=e.target.closest&&e.target.closest('.env2-card'),h=e.target.closest&&e.target.closest('.env2-chip');
      if(c){
        space=c.getAttribute('data-space');
        [].forEach.call(document.querySelectorAll('.env2-card'),function(x){x.setAttribute('aria-pressed',x===c?'true':'false')});
        var s=document.getElementById('env2-space');if(s)s.value=space;
        var f=document.getElementById('contact');
        if(f)f.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});
      }
      if(h){
        var on=h.getAttribute('aria-pressed')==='true';
        [].forEach.call(document.querySelectorAll('.env2-chip'),function(x){x.setAttribute('aria-pressed','false')});
        h.setAttribute('aria-pressed',on?'false':'true');style=on?'':h.getAttribute('data-style');
      }
    });
    document.addEventListener('submit',function(e){
      var f=e.target;if(!f||f.id!=='env2-form')return;
      e.preventDefault();
      var err=document.getElementById('env2-err'),btn=document.getElementById('env2-send');
      if(f.dataset.busy)return;
      var name=document.getElementById('env2-name').value.trim();
      var phone=String(document.getElementById('env2-phone').value||'').replace(/[^\\d+]/g,'').replace(/^\\+972/,'0').replace(/^972/,'0');
      var sp=document.getElementById('env2-space').value;
      if(name.length<2){err.textContent='איך לקרוא לכם?';return}
      if(!/^0(5\\d{8}|[2-489]\\d{7})$/.test(phone)){err.textContent='נראה שמספר הטלפון לא מלא. בדקו ונסו שוב.';return}
      err.textContent='';f.dataset.busy='1';btn.disabled=true;btn.textContent='שולחים...';
      window.stzSendLead({name:name,phone:phone,solution:sp,message:'מרחב: '+sp+(style?' | סגנון: '+style:''),source:'envelope_v2'}).then(function(){
        f.style.display='none';var ok=document.getElementById('env2-ok');ok.hidden=false;ok.style.display='flex';
      }).catch(function(){
        delete f.dataset.busy;btn.disabled=false;btn.textContent='השאירו פרטים';
        err.textContent='השליחה לא עברה. אפשר לכתוב לנו בוואטסאפ, או לנסות שוב.';
      });
    },true);
  });
})();
</script>
'''

# no email address in the visible page (the accessibility statement keeps its own contact, as the law asks)
rep('    <a href="mailto:ilprojects.israel@gmail.com" style="color: #F5F0E4" style-hover="color:#C99752">ilprojects.israel@gmail.com</a>\n', '', 'footer email')

# new sections go where the removed ones were: choose before the projects carousel, short contact where the long one was
rep('  <section id="projects"', CHOOSE + '\n  <section id="projects"', 'insert choose')
rep('@@CONTACT@@', CONTACT, 'insert contact')
rep('</body>', SCRIPT + '</body>', 'inline script')

if problems:
    print('NOT WRITTEN:\n  ' + '\n  '.join(problems))
    sys.exit(1)
open(DST, 'w', encoding='utf-8').write(t)
print('wrote', DST, len(t), 'bytes')
