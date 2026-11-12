#!/usr/bin/env python3
"""Builds about.html ("מי אנחנו ואיך זה עובד") from index.html. index.html is only read.

The page keeps the home page's design, header, form and scripts. It shows, in this order:
  1. the "פרויקט חוץ שלם, מעטפת אחת" section with the full explanation and the process (the pages that used to open inside the home page),
  2. a new section with numbered pins on real projects: what was done in each, plus one line of context,
  3. the "למי זה מתאים" card with the rotating sentence and the quick lead form, the FAQ and the contact form.
Everything else of the home page (hero, scope picker, components, projects, Instagram strip, reviews) is hidden here by CSS.
Not indexed until the owner approves it. Run from the repository root after any change to index.html:  python tools/make-about.py
"""
import os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST = os.path.join(ROOT, 'index.html'), os.path.join(ROOT, 'about.html')
t = open(SRC, encoding='utf-8', newline='').read()
problems = []


def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        problems.append('"%s": expected 1 match, found %d' % (label, n))
        return
    t = t.replace(old, new)


rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 'noindex')
rep('<title>IL Projects | סופר צל — מעטפת מקצועית לבית ולמרחב החוץ</title>', '<title>מי אנחנו ואיך זה עובד | IL Projects</title>', 'title')

# the explanation opens by default, no expand row, top of page clears the fixed header
rep('<div data-more-row=""', '<div data-more-row="" hidden style="display:none"', 'hide more row') if False else None
t = re.sub(r'<div data-more-row="".*?</div>\s*', '', t, count=1, flags=re.S)
t = t.replace('<div id="tracks" data-reveal=""', '<div id="tracks" class="stz-open" data-reveal=""', 1)

PINS = [
    ('מטבחי חוץ ואירוח', 'פרגולה, מטבח חוץ, שולחן בר וכסאות', '/img/fast/hero/hero-pergola-kitchen-bar.webp',
     'פרגולת אלומיניום שחורה עם פרופילי הצללה בגוון דמוי עץ, מעל מטבח חוץ ושולחן בר',
     [('פרופילי הצללה בגוון דמוי עץ, סנטף BH שקוף', 34, 18), ('קורות אלומיניום שחורות', 14, 42), ('מטבח חוץ', 29, 68), ('שולחן בר וכסאות', 53, 64)]),
    ('סגירת מרפסת', 'סגירת מרפסת ופרגולת תריס', '/img/fast/hero/hero-panoramic-balcony.webp',
     'מרפסת בסגירת זכוכית עם פרגולת תריס חשמלית ונוף פתוח',
     [('פרגולת תריס חשמלית', 45, 10), ('סגירת זכוכית בהזזה', 32, 40), ('מעקה זכוכית לנוף פנורמי', 40, 72), ('דלתות הזזה ליציאה למרפסת', 74, 45)]),
    ('סגירת זכוכית', 'סגירת מרפסת וקירוי', '/img/fast/hero/hero-glass-balcony.webp',
     'מרפסת בסגירת זכוכית עם קירוי שקוף מעל הקורות',
     [('סגירת זכוכית בהזזה', 70, 24), ('קירוי עליון, סנטף BH', 30, 8), ('חלון בקצה המרפסת', 27, 40)]),
    ('בנייה קלה', 'תוספת חוץ בגינה', '/img/fast/hero/hero-sunroom.webp',
     'חדר שמש בבנייה קלה עם דלתות הזזה לגינה',
     [('מבנה פאנל מבודד', 36, 9), ('חלונות פנורמיים אל הגינה', 62, 30), ('מערכת דלתות הזזה', 42, 48), ('ריצוף קרמיקה ברצף אחד עם הבית', 50, 64)]),
    ('דקים ופיתוח', 'פיתוח חוץ בעץ', '/img/fast/hero/hero-deck-wood.webp',
     'דק עץ בגינה עם פרגולת תריס, חיפוי עץ וגדר',
     [('פרגולה צפה', 40, 16), ('דק עץ', 50, 72), ('חיפוי עץ לקיר', 82, 55), ('גדר ותיחום', 42, 34), ('צמחייה ופיתוח גינה', 52, 49)]),
]


def esc(x):
    return x.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


tabs = ''.join('<button type="button" role="tab" data-pj="%d" aria-selected="%s" style="font:inherit;cursor:pointer;min-height:44px;padding:0 18px;border-radius:100px;border:1px solid rgba(245,240,228,0.3);background:%s;color:%s;font-size:15px;font-weight:600;white-space:nowrap">%s</button>'
               % (i, 'true' if i == 0 else 'false', '#C99752' if i == 0 else 'transparent', '#1B1712' if i == 0 else '#F5F0E4', esc(p[0])) for i, p in enumerate(PINS))
panels = ''
for i, (name, cap, src, alt, pins) in enumerate(PINS):
    dots = ''.join('<button type="button" data-pin="%d" aria-label="%s" style="position:absolute;left:%d%%;top:%d%%;transform:translate(-50%%,-50%%);width:34px;height:34px;border-radius:50%%;border:2px solid #fff;background:#B4813C;color:#fff;font:inherit;font-size:14px;font-weight:700;cursor:pointer;box-shadow:0 2px 14px rgba(0,0,0,.45)">%d</button>' % (k, esc(l), x, y, k + 1) for k, (l, x, y) in enumerate(pins))
    items = ''.join('<li data-item="%d" style="display:flex;gap:14px;align-items:center;padding:13px 0;border-top:1px solid rgba(245,240,228,0.14);font-size:16.5px;line-height:1.4;color:rgba(245,240,228,0.92)"><span style="flex:none;display:grid;place-items:center;width:30px;height:30px;border-radius:50%%;background:#B4813C;color:#1B1712;font-size:14px;font-weight:700">%d</span><span>%s</span></li>' % (k, k + 1, esc(l)) for k, (l, x, y) in enumerate(pins))
    panels += ('<div data-pjp="%d" role="tabpanel" style="display:%s;grid-template-columns:repeat(auto-fit,minmax(min(100%%,340px),1fr));gap:clamp(1.25rem,3vw,2.5rem);align-items:center">'
               '<div style="position:relative;border-radius:20px;overflow:hidden;aspect-ratio:2064/960;min-height:230px;background:#1B1712"><img src="%s" alt="%s" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover">%s</div>'
               '<div><p style="margin:0 0 6px;color:#C99752;font-size:13px;font-weight:600;letter-spacing:.06em">%s</p><h3 style="font-size:clamp(22px,2.4vw,30px);line-height:1.25;color:#F5F0E4;margin-bottom:8px">מה ביצענו בפרויקט</h3><ul style="list-style:none;margin:0;padding:0">%s</ul></div></div>'
               % (i, 'grid' if i == 0 else 'none', src, esc(alt), dots, esc(cap), items))

SECTION = ('<section id="done" style="position:relative;z-index:2;background:#1B1712;color:#F5F0E4;padding-block:clamp(3rem,9vh,6rem)"><div style="width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto">'
           '<div style="display:inline-flex;align-items:center;gap:10px;color:#C99752;font-size:14.5px;font-weight:600;margin-bottom:16px"><span style="display:block;width:24px;height:1px;background:#C99752"></span>הבידול שלנו</div>'
           '<h2 style="font-size:clamp(30px,3.9vw,48px);letter-spacing:-0.025em;line-height:1.1;color:#F5F0E4;max-width:20ch;text-wrap:balance">כל פרט בפרויקט מתוכנן מראש.</h2>'
           '<p style="margin:14px 0 22px;color:rgba(245,240,228,0.78);font-size:17px;max-width:48ch">לחצו על מספר בתמונה ותראו מה בדיוק ביצענו. כך נראה פרויקט שבו הכול מחובר.</p>'
           '<div role="tablist" aria-label="פרויקטים" style="display:flex;gap:10px;overflow-x:auto;scrollbar-width:none;padding-bottom:6px;margin-bottom:clamp(1.25rem,3vh,2rem)">' + tabs + '</div>'
           + panels +
           '<div style="margin-top:clamp(1.5rem,4vh,2.5rem)"><a href="#quick" style="display:inline-flex;align-items:center;gap:10px;min-height:54px;padding:0 32px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:16.5px;font-weight:600">תאמו שיחת ייעוץ <span aria-hidden="true">←</span></a></div>'
           '</div></section>\n')
JS = ('<script>/* about.html: numbered pins on real projects */\n(function(){\n'
      'function sel(root,i){root.querySelectorAll("[data-pin]").forEach(function(b){var on=+b.getAttribute("data-pin")===i;b.style.background=on?"#fff":"#B4813C";b.style.color=on?"#1B1712":"#fff";b.style.transform="translate(-50%,-50%) scale("+(on?1.18:1)+")"});'
      'root.querySelectorAll("[data-item]").forEach(function(li){li.style.background=+li.getAttribute("data-item")===i?"rgba(201,151,82,0.14)":"transparent"})}\n'
      'document.addEventListener("click",function(e){var tb=e.target.closest&&e.target.closest("[data-pj]");if(tb){var n=tb.getAttribute("data-pj");document.querySelectorAll("[data-pj]").forEach(function(b){var on=b===tb;b.setAttribute("aria-selected",on);b.style.background=on?"#C99752":"transparent";b.style.color=on?"#1B1712":"#F5F0E4"});'
      'document.querySelectorAll("[data-pjp]").forEach(function(p){p.style.display=p.getAttribute("data-pjp")===n?"grid":"none"});return}'
      'var pb=e.target.closest&&e.target.closest("[data-pin]");if(pb){sel(pb.closest("[data-pjp]"),+pb.getAttribute("data-pin"))}});\n'
      '})();</script>')
rep('<section id="fit"', SECTION + '<section id="fit"', 'insert pins section')
rep('</body>', JS + '</body>', 'js')

CSS = ('<style id="stz-about">html body #hero,html body #projects,html body #social,html body #scope,html body #services,html body #build,html body #reviews{display:none !important}'
       'html body #why{margin-top:0 !important;border-radius:0 !important;box-shadow:none !important;padding-top:clamp(5.5rem,14vh,8rem) !important}'
       'html body #why > span:first-child{display:none !important}'
       'html body header{background:rgba(27,23,18,0.94) !important;border-bottom-color:rgba(245,240,228,0.14) !important}'
       'html body div[style*="z-index: 900"],html body div[style*="z-index:900"]{display:none !important}</style>')
rep('<span>מי אנחנו · IL Projects | סופר צל</span>', '<span>מי אנחנו · IL Projects</span>', 'about eyebrow')
rep('alt="מרחב חוץ גמור של סופר צל"', 'alt="מרחב חוץ גמור של IL Projects"', 'about photo alt')
rep('IL Projects, הידועה גם כסופר צל, מרכזת', 'IL Projects מרכזת', 'about text')
rep('</head>', CSS + '</head>', 'css')

if problems:
    print('about.html NOT written:\n  ' + '\n  '.join(problems))
    sys.exit(1)
t = t.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- GENERATED by tools/make-about.py from index.html: do not edit, run the script -->', 1)
open(DST, 'w', encoding='utf-8', newline='').write(t)
print('wrote', os.path.relpath(DST, ROOT), len(t))
