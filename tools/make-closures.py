#!/usr/bin/env python3
"""Builds closures.html: category page "סגירות זכוכית ומערכות הזזה" (glass only), generated from index.html. index.html is only read.

Same technique as make-about.py: the home page's header, "למי זה מתאים" card (rotating sentence + quick form) and contact form stay,
everything else is hidden by CSS and replaced by: hero, an article, the catalogue, numbered pins on real projects, the process and FAQ.
Copy follows the IL voice (short, quiet, no emoji), the category name is the official one, glass projects only (never fabric).
Not indexed until the owner approves. Run from the repository root:  python tools/make-closures.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST = os.path.join(ROOT, 'index.html'), os.path.join(ROOT, 'closures.html')
t = open(SRC, encoding='utf-8', newline='').read()
problems = []


def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        problems.append('"%s": expected 1 match, found %d' % (label, n))
        return
    t = t.replace(old, new)


def esc(x):
    return x.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 'noindex')
rep('<title>IL Projects | סופר צל — מעטפת מקצועית לבית ולמרחב החוץ</title>', '<title>סגירות זכוכית ומערכות הזזה | IL Projects</title>', 'title')
rep('<span>מי אנחנו · IL Projects | סופר צל</span>', '<span>מי אנחנו · IL Projects</span>', 'eyebrow')
rep('alt="מרחב חוץ גמור של סופר צל"', 'alt="מרחב חוץ גמור של IL Projects"', 'alt')
rep('IL Projects, הידועה גם כסופר צל, מרכזת', 'IL Projects מרכזת', 'brand text')

WA = 'https://wa.me/972559958231?text=' + 'היי, הגעתי מדף סגירות המרפסת באתר ואשמח לתאם שיחת ייעוץ'
GOLD = '#C99752'
LBL = 'display:inline-flex;align-items:center;gap:10px;color:%s;font-size:14.5px;font-weight:600;margin-bottom:16px'
H2 = 'font-size:clamp(28px,3.6vw,44px);letter-spacing:-0.025em;line-height:1.12;text-wrap:balance'
W = 'width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto'

hero = ('<section id="chero" style="position:relative;background:#1B1712;color:#F5F0E4;overflow:hidden;display:flex;align-items:flex-end;min-height:min(80vh,680px)">'
        '<img src="/img/fast/hero/hero-glass-balcony.webp" alt="מרפסת בסגירת זכוכית עם קירוי שקוף מעל הקורות" fetchpriority="high" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
        '<span aria-hidden="true" style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(14,11,8,.92) 0%,rgba(14,11,8,.6) 45%,rgba(14,11,8,.25) 100%)"></span>'
        '<div style="position:relative;' + W + ';padding-block:clamp(6.5rem,17vh,9.5rem) clamp(2.25rem,6vh,3.75rem)">'
        '<div style="display:inline-flex;align-items:center;gap:12px;color:#E8C48C;font-size:15px;font-weight:600;margin-bottom:18px;text-shadow:0 1px 12px rgba(14,11,8,.8)"><span style="display:block;width:34px;height:1px;background:#C99752"></span>סגירות זכוכית ומערכות הזזה</div>'
        '<h1 style="font-size:clamp(34px,5vw,64px);line-height:1.08;font-weight:600;letter-spacing:-0.03em;color:#F5F0E4;max-width:16ch;text-shadow:0 2px 24px rgba(14,11,8,.6)">מרפסת לשימוש כל השנה.</h1>'
        '<p style="margin-top:16px;color:rgba(245,240,228,.9);font-size:clamp(17px,1.6vw,20px);max-width:40ch;line-height:1.55">סגירות זכוכית ומערכות הזזה בהתאמה אישית למידות המרפסת. האור והנוף נשארים, והמרחב נשאר שלכם.</p>'
        '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:26px">'
        '<a href="#quick" style="display:inline-flex;align-items:center;justify-content:center;min-height:54px;padding:0 34px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:16.5px;font-weight:600;white-space:nowrap">לתיאום שיחת ייעוץ</a>'
        '<a href="' + esc(WA) + '" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;min-height:54px;padding:0 28px;border-radius:100px;border:1px solid rgba(245,240,228,.5);color:#F5F0E4;font-size:16.5px;white-space:nowrap;backdrop-filter:blur(6px)">שיחת וואטסאפ מהירה</a>'
        '</div></div></section>\n')

article = ('<section id="cart" style="background:#F5F0E4;color:#211C16;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
           '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:clamp(1.5rem,4vw,3.5rem);align-items:start">'
           '<div><div style="' + LBL % '#80561E' + '"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>על הסגירה</div>'
           '<h2 style="' + H2 + ';max-width:14ch">לא כל סגירה אותו דבר.</h2></div>'
           '<div style="color:#4B443A;font-size:17px;line-height:1.75;max-width:56ch">'
           '<p style="margin-bottom:14px">מרפסת היא החלק הפתוח של הבית. סגירה מוקפדת לא סוגרת אותה, אלא מרחיבה את השימוש בה: אור טבעי, נוף פתוח וחלל שאפשר לשבת בו לאורך השנה.</p>'
           '<p style="margin-bottom:14px">אנחנו מבצעים סגירות זכוכית ומערכות הזזה, כולל פנורמיות, ויטרינות וחלונות הזזה. מסגרת האלומיניום נבחרת בגוון ובפרופיל שמשתלבים בקו של הבניין.</p>'
           '<p>לפני שבוחרים בודקים כיווני שמש, רוח, מידות והאופן שבו משתמשים במרפסת. לכן כל פרויקט מתחיל בפגישה במקום ובמדידה, וההצעה נכתבת אחריהן. אישורים וליווי הנדסי, ככל שנדרשים, מתואמים מול בעלי מקצוע מוסמכים.</p>'
           '</div></div></div></section>\n')

cards = [
    ('01', 'סגירת זכוכית בהזזה', 'מערכת הזזה בזכוכית, בגוון ובפרופיל שנבחרים לפי הבית.', '/img/fast/hero/hero-glass-balcony.webp', 'מרפסת בסגירת זכוכית בהזזה'),
    ('02', 'סגירה פנורמית בשילוב פרגולה', 'זכוכית רחבה שמשאירה את הנוף פתוח, יחד עם פרגולת תריס, כמתחם אחד.', '/img/fast/hero/hero-panoramic-balcony.webp', 'מרפסת פנורמית עם פרגולת תריס חשמלית'),
    ('03', 'חדר שמש', 'תוספת חוץ מזכוכית ואלומיניום, כחלק מהבית ומהגינה.', '/img/fast/hero/hero-sunroom.webp', 'חדר שמש עם דלתות הזזה לגינה'),
]
cardhtml = ''.join(
    '<div style="position:relative;border-radius:20px;overflow:hidden;background:#1B1712;aspect-ratio:4/5;color:#F5F0E4"><img src="%s" alt="%s" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover">'
    '<span aria-hidden="true" style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(17,14,11,.92) 0%%,rgba(17,14,11,.55) 40%%,rgba(17,14,11,0) 70%%)"></span>'
    '<div style="position:absolute;inset-inline:0;bottom:0;padding:clamp(16px,2vw,24px)"><span style="font-size:13px;font-weight:600;color:#E8C48C;letter-spacing:.06em">%s</span>'
    '<h3 style="margin:6px 0;font-size:clamp(21px,2vw,25px);line-height:1.2;color:#fff">%s</h3><p style="font-size:15.5px;line-height:1.5;color:rgba(245,240,228,.92)">%s</p></div></div>'
    % (img, esc(alt), n, esc(ti), esc(tx)) for n, ti, tx, img, alt in cards)
catalog = ('<section id="ccat" style="background:#ECE4D2;color:#211C16;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
           '<div style="' + LBL % '#80561E' + '"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>סוגי פתרונות</div>'
           '<h2 style="' + H2 + ';max-width:20ch;margin-bottom:clamp(1.5rem,4vh,2.5rem)">קו נקי, ביצוע מדויק.</h2>'
           '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:16px">' + cardhtml + '</div>'
           '<p style="margin-top:22px;color:#4B443A;font-size:16.5px;max-width:60ch">וגם ויטרינות, חלונות הזזה, זכוכית מתקפלת ומחיצות זכוכית. הגוון, הפרופיל והחלוקה נקבעים לפי הבית והשימוש.</p>'
           '<p style="margin-top:14px;padding:16px 20px;border-radius:14px;background:rgba(33,28,22,.06);color:#4B443A;font-size:16px;line-height:1.65;max-width:60ch">דף זה עוסק בסגירות זכוכית. סגירות בד ו-PVC, כמו סגירת חורף, הן פתרון נפרד עם חומר ומערכת אחרים. נסביר את ההבדל בשיחת ייעוץ.</p>'
           '</div></section>\n')

# numbered pins on two real glass projects
PINS = [
    ('סגירת מרפסת וקירוי', '/img/fast/hero/hero-glass-balcony.webp', 'מרפסת בסגירת זכוכית עם קירוי שקוף מעל הקורות',
     [('סגירת זכוכית בהזזה', 70, 24), ('קירוי עליון, סנטף BH', 30, 8), ('חלון בקצה המרפסת', 27, 40)]),
    ('סגירת מרפסת ופרגולת תריס', '/img/fast/hero/hero-panoramic-balcony.webp', 'מרפסת בסגירת זכוכית עם פרגולת תריס חשמלית ונוף פתוח',
     [('פרגולת תריס חשמלית', 45, 10), ('סגירת זכוכית בהזזה', 32, 40), ('מעקה זכוכית לנוף פנורמי', 40, 72), ('דלתות הזזה ליציאה למרפסת', 74, 45)]),
]
tabs = ''.join('<button type="button" role="tab" data-pj="%d" aria-selected="%s" style="font:inherit;cursor:pointer;min-height:44px;padding:0 18px;border-radius:100px;border:1px solid rgba(245,240,228,.3);background:%s;color:%s;font-size:15px;font-weight:600;white-space:nowrap">%s</button>'
               % (i, 'true' if i == 0 else 'false', GOLD if i == 0 else 'transparent', '#1B1712' if i == 0 else '#F5F0E4', esc(p[0])) for i, p in enumerate(PINS))
panels = ''
for i, (name, src, alt, pins) in enumerate(PINS):
    dots = ''.join('<button type="button" data-pin="%d" aria-label="%s" style="position:absolute;left:%d%%;top:%d%%;transform:translate(-50%%,-50%%);width:34px;height:34px;border-radius:50%%;border:2px solid #fff;background:#B4813C;color:#fff;font:inherit;font-size:14px;font-weight:700;cursor:pointer;box-shadow:0 2px 14px rgba(0,0,0,.45)">%d</button>' % (k, esc(l), x, y, k + 1) for k, (l, x, y) in enumerate(pins))
    items = ''.join('<li data-item="%d" style="display:flex;gap:14px;align-items:center;padding:13px 0;border-top:1px solid rgba(245,240,228,.14);font-size:16.5px;line-height:1.4;color:rgba(245,240,228,.92)"><span style="flex:none;display:grid;place-items:center;width:30px;height:30px;border-radius:50%%;background:#B4813C;color:#1B1712;font-size:14px;font-weight:700">%d</span><span>%s</span></li>' % (k, k + 1, esc(l)) for k, (l, x, y) in enumerate(pins))
    panels += ('<div data-pjp="%d" role="tabpanel" style="display:%s;grid-template-columns:repeat(auto-fit,minmax(min(100%%,340px),1fr));gap:clamp(1.25rem,3vw,2.5rem);align-items:center">'
               '<div style="position:relative;border-radius:20px;overflow:hidden;aspect-ratio:2064/960;min-height:230px;background:#1B1712"><img src="%s" alt="%s" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover">%s</div>'
               '<div><h3 style="font-size:clamp(22px,2.4vw,30px);line-height:1.25;color:#F5F0E4;margin-bottom:8px">מה ביצענו בפרויקט</h3><ul style="list-style:none;margin:0;padding:0">%s</ul></div></div>'
               % (i, 'grid' if i == 0 else 'none', src, esc(alt), dots, items))
done = ('<section id="cdone" style="position:relative;z-index:2;background:#1B1712;color:#F5F0E4;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
        '<div style="' + LBL % GOLD + '"><span style="display:block;width:24px;height:1px;background:#C99752"></span>מהשטח</div>'
        '<h2 style="' + H2 + ';color:#F5F0E4;max-width:20ch">אמון מקצועי נבנה דרך תוצאות.</h2>'
        '<p style="margin:14px 0 22px;color:rgba(245,240,228,.78);font-size:17px;max-width:46ch">לחצו על מספר בתמונה ותראו מה בדיוק ביצענו.</p>'
        '<div role="tablist" aria-label="פרויקטים" style="display:flex;gap:10px;overflow-x:auto;scrollbar-width:none;padding-bottom:6px;margin-bottom:clamp(1.25rem,3vh,2rem)">' + tabs + '</div>' + panels + '</div></section>\n')

# every glass project on the projects page (glass only: fabric entries are skipped), copy and photo taken from projects-data.js
data = open(os.path.join(ROOT, 'projects-data.js'), encoding='utf-8').read()
A, P = '/img/fast/gallery/', '/img/fast/projects/'
glass = []
for m in re.finditer(r"\{ title: '([^']+)',[^{}]*?cat: 'glass',([^{}]*?)\}\s*[,\]]", data, re.S):
    body = m.group(0)
    if 'fabric: true' in body:
        continue
    d = re.search(r"desc: '([^']+)'", body)
    ph = re.search(r"photos: \[(A|P) \+ '([^']+)'", body)
    cl = re.search(r"client: '([^']+)'", body)
    if d and ph:
        glass.append((m.group(1), d.group(1), (A if ph.group(1) == 'A' else P) + ph.group(2), cl.group(1) if cl else ''))
if not glass:
    problems.append('no glass projects parsed from projects-data.js')
glass.sort(key=lambda g: g[3] == 'עסקי')
pcards = ''.join(
    '<div style="border-radius:18px;overflow:hidden;background:#FBF7EE;box-shadow:0 1px 0 rgba(33,28,22,.06),0 14px 32px rgba(33,28,22,.1);display:flex;flex-direction:column"><div style="aspect-ratio:4/3;background:#ECE4D2"><img src="%s" alt="%s" loading="lazy" decoding="async" style="display:block;width:100%%;height:100%%;object-fit:cover"></div>'
    '<div style="padding:18px 20px 22px"><span style="font-size:12.5px;font-weight:600;color:#80561E;letter-spacing:.04em">%s</span><h3 style="margin:6px 0 8px;font-size:19px;line-height:1.3">%s</h3><p style="font-size:15.5px;line-height:1.6;color:#4B443A">%s</p></div></div>'
    % (img, esc(ti), esc(cl), esc(ti), esc(de)) for ti, de, img, cl in glass)
more = ('<section id="cmore" style="background:#F5F0E4;color:#211C16;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
        '<div style="' + LBL % '#80561E' + '"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>פרויקטים שביצענו</div>'
        '<h2 style="' + H2 + ';max-width:20ch;margin-bottom:clamp(1.5rem,4vh,2.5rem)">סגירות זכוכית ומערכות הזזה.</h2>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:18px">' + pcards + '</div>'
        '<div style="margin-top:clamp(1.5rem,4vh,2.5rem)"><a href="/projects" style="display:inline-flex;align-items:center;gap:10px;min-height:50px;padding:0 26px;border-radius:100px;border:1px solid #211C16;color:#211C16;font-size:16px;font-weight:600">לכל הפרויקטים <span aria-hidden="true">←</span></a></div>'
        '</div></section>\n')

steps = [('01', 'פגישה במקום ומדידה', 'מדידה, כיווני שמש וצורת השימוש.'), ('02', 'תכנון יישומי והצעה', 'חומרים, גוונים והיקף, בכתב.'), ('03', 'ייצור והתקנה', 'לפי המידות של המקום, ומסירה מסודרת.')]
stephtml = ''.join('<div style="display:flex;gap:16px;align-items:baseline;border-top:1px solid rgba(33,28,22,.16);padding-block:18px"><span style="font-size:26px;font-weight:300;color:#B4813C;line-height:1;flex:none">%s</span><div><h3 style="font-size:19px;font-weight:600">%s</h3><p style="margin-top:4px;color:#4B443A;font-size:16px">%s</p></div></div>' % s for s in steps)
faq = [('האם סגירת זכוכית דורשת היתר או אישורים?', 'זה תלוי בפרויקט ובמצב המבנה. בודקים זאת בכל פרויקט לגופו, ואישורים וליווי הנדסי, ככל שנדרשים, מתואמים מול בעלי מקצוע מוסמכים.'),
       ('אפשר לשלב פרגולה עם הסגירה?', 'כן. סגירת זכוכית ופרגולה יכולות להיות פרויקט אחד, באותה שפה עיצובית ועם נקודת קשר אחת.'),
       ('מה בודקים בפגישה במקום?', 'כיווני שמש, רוח, מידות המרפסת והאופן שבו אתם משתמשים בה. על בסיס זה נכתבת ההצעה.')]
faqhtml = ''.join('<details style="border-top:1px solid rgba(33,28,22,.16);padding:16px 0"><summary style="cursor:pointer;font-size:18px;font-weight:600;list-style:none">%s</summary><p style="margin-top:10px;color:#4B443A;font-size:16.5px;line-height:1.7;max-width:62ch">%s</p></details>' % (esc(q), esc(a)) for q, a in faq)
process = ('<section id="cproc" style="background:#F5F0E4;color:#211C16;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
           '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:clamp(2rem,5vw,4rem)">'
           '<div><div style="' + LBL % '#80561E' + '"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>איך זה עובד</div>'
           '<h2 style="' + H2 + ';margin-bottom:18px">נקודת קשר אחת, מהמדידה ועד ההתקנה.</h2>' + stephtml + '</div>'
           '<div><div style="' + LBL % '#80561E' + '"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>שאלות נפוצות</div>'
           '<h2 style="' + H2 + ';margin-bottom:18px">לפני שמתחילים.</h2>' + faqhtml + '<div style="border-top:1px solid rgba(33,28,22,.16)"></div></div>'
           '</div></div></section>\n')

JS = ('<script>/* closures.html: numbered pins on real projects */\n(function(){\n'
      'function sel(root,i){root.querySelectorAll("[data-pin]").forEach(function(b){var on=+b.getAttribute("data-pin")===i;b.style.background=on?"#fff":"#B4813C";b.style.color=on?"#1B1712":"#fff";b.style.transform="translate(-50%,-50%) scale("+(on?1.18:1)+")"});'
      'root.querySelectorAll("[data-item]").forEach(function(li){li.style.background=+li.getAttribute("data-item")===i?"rgba(201,151,82,0.14)":"transparent"})}\n'
      'document.addEventListener("click",function(e){var tb=e.target.closest&&e.target.closest("[data-pj]");if(tb){var n=tb.getAttribute("data-pj");document.querySelectorAll("[data-pj]").forEach(function(b){var on=b===tb;b.setAttribute("aria-selected",on);b.style.background=on?"#C99752":"transparent";b.style.color=on?"#1B1712":"#F5F0E4"});'
      'document.querySelectorAll("[data-pjp]").forEach(function(p){p.style.display=p.getAttribute("data-pjp")===n?"grid":"none"});return}'
      'var pb=e.target.closest&&e.target.closest("[data-pin]");if(pb){sel(pb.closest("[data-pjp]"),+pb.getAttribute("data-pin"))}});\n'
      '})();</script>')

rep('<section id="why"', hero + article + catalog + done + more + process + '<section id="why"', 'insert sections')
rep('</body>', JS + '</body>', 'js')
CSS = ('<style id="stz-closures">html body #hero,html body #why,html body #projects,html body #social,html body #scope,html body #services,html body #build,html body #reviews,html body #faq{display:none !important}'
       'html body header{background:rgba(27,23,18,0.94) !important;border-bottom-color:rgba(245,240,228,0.14) !important}'
       'html body div[style*="z-index: 900"],html body div[style*="z-index:900"]{display:none !important}'
       'summary::-webkit-details-marker{display:none}</style>')
rep('</head>', CSS + '</head>', 'css')

if problems:
    print('closures.html NOT written:\n  ' + '\n  '.join(problems))
    sys.exit(1)
t = t.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- GENERATED by tools/make-closures.py from index.html: do not edit, run the script -->', 1)
open(DST, 'w', encoding='utf-8', newline='').write(t)
print('wrote', os.path.relpath(DST, ROOT), len(t))
