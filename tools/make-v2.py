#!/usr/bin/env python3
"""Builds balcony-v2.html and garden-v2.html from the generated balcony.html / garden.html (run make-adgroup-landings.py first).

The existing pages are never touched. v2 = the brand-book version (BRAND-BOOK.md): short "who we are" card with the text, "how it works" with
real step lines, "why work with us" instead of the duplicated service tracks, reading-order sections (01 envelope, 02 components, 03 projects,
04 fit, 05 questions), a one-line legal note with the full wording behind a toggle, shorter FAQ answers, tighter hero lines.
Every replacement must match exactly once; if not, nothing is written.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ABOUT_H = "פרויקטי חוץ בוטיק, מא' ועד ת'."
ABOUT_P1 = ("IL Projects היא חברת ביצוע לפרויקטי חוץ בוטיק. אנחנו לוקחים את %s כפרויקט אחד שלם, מהפגישה הראשונה ועד המסירה בשטח, "
            "מול כתובת אחת שמכירה כל פרט. כחברת ביצוע אנחנו רואים את כל הרכיבים יחד ושומרים על האינטרס שלכם: מה שמתוכנן הוא מה שנבנה, "
            "בתקציב ובלוח הזמנים שסוכמו.")
ABOUT_P2 = ("הדרך מתחילה אצלכם בשטח: מודדים, בודקים את כיווני השמש ואת הקו של הבית ומקשיבים לאיך אתם חיים במקום. "
            "מתוך זה נבנה תכנון יישומי והצעה בכתב. רק אז מבצעים. התוצאה היא שקט, גימור ברמה גבוהה ופרויקטים שאפשר לראות כאן באתר.")

WHY = [
    ("תוכנית אחת, גורם אחד.", "כל הרכיבים מתוכננים ומבוצעים יחד, מול נקודת קשר אחת, גם כשמתחילים מפרגולה אחת."),
    ("תכנון יישומי שנולד מהביצוע.", "מה שמצויר בהצעה הוא מה שנבנה בשטח, בחומרים, בגבהים ובלוח הזמנים שסוכמו."),
    ("גימור ברמה גבוהה.", "חומרים איכותיים והתקנה לפי הוראות היצרן, עם ניסיון מוכח בשטח."),
    ("הצעה מפורטת בכתב.", "היקף, חומרים, שלבים ולוח זמנים מוגדרים מראש, כך שאתם יודעים בדיוק מה מקבלים."),
    ("פתרון שנבחר בשבילכם.", "לפי %s ולפי איך שאתם חיים %s."),
]

PAGES = {
    'balcony': dict(
        about_obj='המרפסת או הפנטהאוז שלכם', why5=('המרפסת', 'בה'),
        proj_old='סגירות זכוכית, סגירות חורף, פרגולות ודקים במרפסות.',
        proj_new='מרפסות ופנטהאוזים שהפכו לחלק מהבית. כל פרויקט כאן בוצע על ידי הצוות שלנו.',
        hero=[("מרפסת שיושבים בה כל השנה גם כשיורד גשם בחוץ, בזכות מדידה מדויקת וסגירה שמתאימה בדיוק למרפסת שלכם.",
               "מרפסת שיושבים בה כל השנה, גם כשיורד גשם בחוץ, בזכות מדידה מדויקת וסגירה שמתאימה בדיוק למרפסת שלכם."),
              ("שנפתחת וסוגרת בלחיצה אחת", "שנפתחת ונסגרת בלחיצה אחת"),
              ("קווים נקיים בפרופיל שחור וסגירת זכוכית שמחברת בין הבית לנוף, בלי להרגיש שיש שם קיר.",
               "קווים נקיים בפרופיל שחור וסגירת זכוכית שמשאירה את הנוף פתוח גם כשהמרפסת סגורה."),
              ("גם במרפסת פנטהאוז גדולה, כל פרט נבחר כך שהנוף נשאר הכוכב — לא המעקה ולא הקירוי.",
               "גם במרפסת פנטהאוז גדולה, כל פרט נבחר כך שהנוף נשאר במרכז.")]),
    'garden': dict(
        about_obj='הגינה והבית הפרטי שלכם', why5=('הבית', 'בו'),
        proj_old='מטבחי חוץ, פרגולות, דקים וגדרות בבתים פרטיים.',
        proj_new='בתים פרטיים וגינות שהפכו למרחב חיים שלם. כל פרויקט כאן בוצע על ידי הצוות שלנו.',
        hero=[("דק עץ וחיפוי שמביאים חמימות לגינה ועומדים בשמש ובשימוש היומיומי לאורך שנים.",
               "דק עץ וחיפוי שמביאים חמימות לגינה ונבחרים לעמוד בשמש ובשימוש היומיומי.")]),
}

COMMON = [
    # faq: shorter, no dashes, no slogans
    ("כשכל המרחב מתוכנן יחד, הכול מתחבר לשפה עיצובית אחת. לכם יש נקודת קשר אחת, מהפגישה הראשונה ועד המסירה.",
     "כשכל הרכיבים מתוכננים יחד, הגבהים, החומרים והגימורים מתחברים לתוצאה אחת. לכם יש נקודת קשר אחת, מהפגישה הראשונה ועד המסירה."),
    ("בתכנון היישומי בודקים את מה שכבר קיים — גבהים, ריצוף, פתחים וגוונים — ובוחרים פרופילים וחומרים שממשיכים אותו, כך שהתוספת תיראה כחלק מהבית.",
     "בתכנון היישומי בודקים את מה שכבר קיים: גבהים, ריצוף, פתחים וגוונים. לפי זה בוחרים פרופילים וחומרים שממשיכים את הקו של הבית, כך שהתוספת נראית כחלק ממנו מהיום הראשון."),
    ("אלומיניום, עץ, פוליקרבונט ובד — לכל חומר יתרונות אחרים במראה, בתחזוקה ובהתנהגות בשמש ובגשם. בשיחת הייעוץ נעבור על האפשרויות שמתאימות למקום שלכם.",
     "לכל חומר יתרונות אחרים במראה, בתחזוקה ובהתנהגות בשמש ובגשם: אלומיניום, עץ, פוליקרבונט ובד. בשיחת הייעוץ נעבור על האפשרויות שמתאימות למקום שלכם."),
    ("נשמח שתביאו אותן לשיחה. נעבור עליהן יחד ונבדוק מה כלול בכל אחת: חומרים, גימור, היקף ותנאי ההתקשרות. מאיתנו תקבלו הצעה מפורטת בכתב, כדי שתוכלו להשוות בביטחון.",
     "מצוין, נשמח שתביאו אותן לשיחה. נעבור יחד על מה שכלול בכל אחת: חומרים, רמת גימור, היקף ותנאי התקשרות. מאיתנו תקבלו הצעה מפורטת בכתב, כך שתוכלו להשוות בביטחון ולבחור את מה שנכון לכם."),
    # steps
    ("<h4 style=\"font-size:17.5px;font-weight:600\">פגישת ייעוץ ומדידה</h4><p style=\"margin-top:4px;color:#4B443A;font-size:14.5px\">מדידה, כיווני שמש וצורת השימוש.</p>",
     "<h4 style=\"font-size:17.5px;font-weight:600\">פגישה ומדידה בשטח</h4><p style=\"margin-top:4px;color:#4B443A;font-size:14.5px\">מגיעים אליכם, מודדים ומבינים איך אתם חיים במקום.</p>"),
    ("<p style=\"margin-top:4px;color:#4B443A;font-size:14.5px\">הצעה מפורטת בכתב.</p>",
     "<p style=\"margin-top:4px;color:#4B443A;font-size:14.5px\">פתרון מותאם בחומרים ובגוונים הנכונים, והצעה מפורטת בכתב.</p>"),
    ("<p style=\"margin-top:4px;color:#4B443A;font-size:14.5px\">לפי המידות של המקום.</p>",
     "<p style=\"margin-top:4px;color:#4B443A;font-size:14.5px\">הצוות שלנו מבצע בשטח, לפי התוכנית ולפי לוח זמנים מוגדר.</p>"),
    ("<p style=\"margin-top:4px;color:#4B443A;font-size:14.5px\">בהתאם לתנאי ההתקשרות שנקבעו בכתב.</p>",
     "<p style=\"margin-top:4px;color:#4B443A;font-size:14.5px\">עוברים יחד על הכול ומשאירים לכם מקום מוכן לשימוש.</p>"),
    # card 2 header; the small label under the heading repeated it
    ("<span>בית אחד · איך זה עובד</span><span>02</span>", "<span>איך זה עובד</span><span>02</span>"),
    ("<div style=\"color:#8A5F24;font-size:12.5px;font-weight:600;letter-spacing:0.08em\">איך זה עובד · תהליך מסודר, פתרון מדויק</div>", ""),
    # numbering
    ("</span>03 · למי זה מתאים</div>", "</span>04 · למי זה מתאים</div>"),
    ("{ id: 'fit', n: '03', label: 'למי זה מתאים' },\n      { id: 'projects', n: '04', label: 'מהשטח' },",
     "{ id: 'projects', n: '03', label: 'מהשטח' },\n      { id: 'fit', n: '04', label: 'למי זה מתאים' },"),
    # legal note: one line, full wording behind a toggle
    ("<p style=\"font-size:14.5px;color:rgba(245,240,228,0.74);line-height:1.8;max-width:62ch\">בפרויקטים הכוללים כמה תחומי שירות, IL Projects מסייעת בבניית רצף ביצוע מתואם ובחיבור בין מרכיבי הפרויקט. שירותים מקצועיים ייעודיים, אישורים, תשתיות וליווי הנדסי — ככל שנדרשים — מתואמים מול בעלי מקצוע מוסמכים, בהתאם להיקף הפרויקט ולתנאי ההתקשרות שנקבעו מראש ובכתב.</p>",
     "<details style=\"font-size:14.5px;color:rgba(245,240,228,0.74);line-height:1.8;max-width:62ch\"><summary style=\"cursor:pointer\">אישורים, תשתיות וליווי הנדסי, ככל שנדרשים, מתואמים מול בעלי מקצוע מוסמכים. <span style=\"color:#C99752;border-bottom:1px solid rgba(201,151,82,0.5)\">לנוסח המלא</span></summary>"
     "<p style=\"margin-top:8px\">בפרויקטים הכוללים כמה תחומי שירות, IL Projects מסייעת בבניית רצף ביצוע מתואם ובחיבור בין מרכיבי הפרויקט. שירותים מקצועיים ייעודיים, אישורים, תשתיות וליווי הנדסי, ככל שנדרשים, מתואמים מול בעלי מקצוע מוסמכים, בהתאם להיקף הפרויקט ולתנאי ההתקשרות שנקבעו מראש ובכתב.</p></details>"),
]

CSS = ('<style id="stz-v2">@media (min-width:1000px){'
       'html body [data-bkwrap]{grid-template-columns:repeat(3,minmax(0,1fr)) !important}'
       'html body [data-bkwrap] > [data-bkpage][data-ab0]:nth-child(n){grid-column:auto !important;grid-area:auto !important}'
       'html body [data-bkcard] [data-stepsl]{grid-template-columns:minmax(0,1fr) !important;align-content:start !important;grid-auto-rows:auto !important;gap:10px !important}'
       'html body [data-bkcard] [data-stepsl] p{display:block !important;margin-top:2px !important}'
       'html body [data-bkcard] [data-stepsl] > div{flex-direction:row !important;align-items:baseline !important;gap:14px !important;padding:12px 16px !important}'
       'html body [data-bkcard] [data-stepsl] > div > div{min-width:0}'
       'html body [data-bkwrap] > [data-bkpage][data-ab0]{padding-bottom:clamp(1.25rem,3vw,2.25rem) !important;justify-content:flex-start !important}}'
       '</style>')

CTA = ('<div style="margin-top:auto;padding-top:20px"><a href="#quick" style="display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 26px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:16px;font-weight:600;white-space:nowrap" '
       'style-hover="background:#C99752;color:#1B1712">תאמו שיחת ייעוץ <span aria-hidden="true">←</span></a></div>')


def build(key, P):
    t = open(os.path.join(ROOT, key + '.html'), encoding='utf-8').read()
    problems = []

    def rep(old, new, label):
        nonlocal t
        n = t.count(old)
        if n != 1:
            problems.append(f'{key}: "{label}": expected 1 match, found {n}')
            return
        t = t.replace(old, new)

    for i, (old, new) in enumerate(COMMON):
        rep(old, new, 'common %d: %s' % (i, old[:40]))
    for i, (old, new) in enumerate(P['hero']):
        rep(old, new, 'hero line %d' % i)
    rep(P['proj_old'], P['proj_new'], 'projects subtitle')

    # card 1: the illustration and its category legend go; the about text comes in
    about = ('<h3 style="font-size:clamp(22px,2.4vw,28px);line-height:1.2;letter-spacing:-0.02em;margin-bottom:10px">' + ABOUT_H + '</h3>'
             '<p style="color:#4B443A;font-size:15.5px;line-height:1.7;max-width:60ch;margin-bottom:10px">' + ABOUT_P1 % P['about_obj'] + '</p>'
             '<p style="color:#4B443A;font-size:15.5px;line-height:1.7;max-width:60ch;margin-bottom:10px">' + ABOUT_P2 + '</p>' + CTA)
    t, n = re.subn(r'<div style="display:flex;flex-direction:column;flex:1 1 auto;margin-bottom:16px" data-envfig="">.*?(?=\s*<button type="button" aria-label="לעמוד הבא" onClick="\{\{ bookNext \}\}" data-flip-anim="")',
                   lambda m: about, t, count=1, flags=re.S)
    if n != 1:
        problems.append(f'{key}: "card 1 illustration": not found')

    # card 2: heading and the three old paragraphs become one short line
    t, n = re.subn(r'<h3 style="font-size:clamp\(22px,2\.4vw,28px\)[^>]*>בית אחד לכל מעטפת החוץ</h3>\s*(?:<p[^>]*>.*?</p>\s*){3}',
                   lambda m: '<h3 style="font-size:clamp(22px,2.4vw,28px);line-height:1.2;letter-spacing:-0.02em;margin-bottom:10px">ארבעה שלבים, נקודת קשר אחת.</h3>'
                             '<p style="color:#4B443A;font-size:15.5px;line-height:1.65;max-width:60ch;margin-bottom:10px">מהפגישה הראשונה ועד המסירה, בסדר קבוע וברור.</p>',
                   t, count=1, flags=re.S)
    if n != 1:
        problems.append(f'{key}: "card 2 text": not found')

    # card 3: "service tracks" (repeated later in the picker) becomes "why work with us"
    obj, rel = P['why5']
    items = ''.join(
        '<div role="listitem" style="border-top:1px solid rgba(33,28,22,0.14);padding:13px 0"><div style="font-size:17px;font-weight:600;line-height:1.3">%s</div>'
        '<div style="margin-top:3px;color:#4B443A;font-size:14.5px;line-height:1.55">%s</div></div>'
        % (h, (d % (obj, rel)) if '%s' in d else d) for h, d in WHY)
    m = re.search(r'(<div data-bkpage="" data-bkp2=""[^>]*>)(.*?)(\n        </div>\n\s*<div data-bkctl="")', t, flags=re.S)
    if not m:
        problems.append(f'{key}: "card 3": not found')
    else:
        head = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;color:#8A5F24;font-size:12.5px;font-weight:600;letter-spacing:0.08em"><span>למה איתנו</span><span>03</span></div>'
        body = (head + '<h3 style="font-size:clamp(22px,2.4vw,28px);line-height:1.2;letter-spacing:-0.02em;margin:0 0 10px">למה לעבוד איתנו</h3>'
                '<div role="list" aria-label="למה לעבוד איתנו" style="display:flex;flex-direction:column">' + items + '</div>')
        t = t[:m.start(2)] + body + t[m.end(2):]

    # reading order: components (02) before projects (03)
    ms = re.search(r'\n  <section id="services".*?\n  </section>\n', t, flags=re.S)
    mp = t.find('\n  <section id="projects"')
    if not ms or mp < 0 or ms.start() < mp:
        problems.append(f'{key}: "services/projects order": markers not found or already moved')
    else:
        block = ms.group(0)
        t = t[:ms.start()] + t[ms.end():]
        mp = t.find('\n  <section id="projects"')
        t = t[:mp] + block + t[mp:]

    # mobile menu: same numbers and order as the page
    mm = re.search(r'(    <a href="#fit"[^\n]*?>למי זה מתאים <span[^>]*>)03(</span></a>\n)(    <a href="#projects"[^\n]*?>פרויקטים <span[^>]*>)04(</span></a>\n)', t)
    if not mm:
        problems.append(f'{key}: "menu order": not found')
    else:
        t = t[:mm.start()] + mm.group(3) + '03' + mm.group(4) + mm.group(1) + '04' + mm.group(2) + t[mm.end():]

    t = t.replace('</head>', CSS + '</head>', 1)
    t = t.replace('<!-- GENERATED by tools/make-adgroup-landings.py from index.html: do not edit, run the script -->',
                  '<!-- GENERATED by tools/make-v2.py from ' + key + '.html: do not edit, run tools/make-adgroup-landings.py then tools/make-v2.py -->', 1)
    t = t.replace('<meta name="robots" content="noindex, nofollow">', '<meta name="robots" content="noindex, nofollow">', 1)
    return t, problems


out, allp = {}, []
for key, P in PAGES.items():
    html, pr = build(key, P)
    allp += pr
    out[key] = html
if allp:
    print('nothing written:\n  ' + '\n  '.join(allp))
    sys.exit(1)
for key, html in out.items():
    open(os.path.join(ROOT, key + '-v2.html'), 'w', encoding='utf-8').write(html)
    print('wrote', key + '-v2.html')
