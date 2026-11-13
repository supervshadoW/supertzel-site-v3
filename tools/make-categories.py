#!/usr/bin/env python3
"""Builds the category pages (all except glass closures, which has tools/make-closures.py) from index.html. index.html is only read.

Same template as closures.html: hero, short article, catalogue cards, numbered pins on a real project, project cards taken from
projects-data.js, process + FAQ, then the home page's "למי זה מתאים" card and contact form. Category names are the official ones.
Copy rules: IL voice, no comma before 'ו', "תכנון יישומי", approvals only "ככל שנדרש". Pages are noindex until the owner approves.
Run from the repository root after any change to index.html:  python tools/make-categories.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = open(os.path.join(ROOT, 'index.html'), encoding='utf-8', newline='').read()
DATA = open(os.path.join(ROOT, 'projects-data.js'), encoding='utf-8').read()
G, PR, HE = '/img/fast/gallery/', '/img/fast/projects/', '/img/fast/hero/'
PERMIT = 'זה תלוי בפרויקט ובמבנה. בודקים כל פרויקט לגופו. אישורים וליווי הנדסי, ככל שנדרשים, מתואמים מול בעלי מקצוע מוסמכים.'

PIN_KITCHEN = ('פרגולה, מטבח חוץ, שולחן בר וכסאות', HE + 'hero-pergola-kitchen-bar.webp', 'פרגולת אלומיניום שחורה עם פרופילי הצללה בגוון דמוי עץ, מעל מטבח חוץ ושולחן בר',
               [('פרופילי הצללה בגוון דמוי עץ, סנטף BH שקוף', 34, 18), ('קורות אלומיניום שחורות', 14, 42), ('מטבח חוץ', 29, 68), ('שולחן בר וכסאות', 53, 64)])
PIN_DECK = ('פיתוח חוץ בעץ', HE + 'hero-deck-wood.webp', 'דק עץ בגינה עם פרגולת תריס, חיפוי עץ וגדר',
            [('פרגולה צפה', 40, 16), ('דק עץ', 50, 72), ('חיפוי עץ לקיר', 82, 55), ('גדר ותיחום', 42, 34), ('צמחייה ופיתוח גינה', 52, 49)])
PIN_SUN = ('תוספת חוץ בגינה', HE + 'hero-sunroom.webp', 'חדר שמש בבנייה קלה עם דלתות הזזה לגינה',
           [('מבנה פאנל מבודד', 36, 9), ('חלונות פנורמיים אל הגינה', 62, 30), ('מערכת דלתות הזזה', 42, 48), ('ריצוף קרמיקה ברצף אחד עם הבית', 50, 64)])

PAGES = {
    'shade': dict(
        name='פתרונות קירוי והצללה בהתאמה אישית', hero=G + 'project-black-louvered-pergola.webp', hero_alt='פרגולת אלומיניום שחורה עם פרופילי הצללה בגינה',
        h1='כל מרחב והפתרון שמותאם לו.', sub='הצללה שמתוכננת לפי המידות, השמש והקו של הבית שלכם. כך היא מתאימה בדיוק לשימוש ולמראה.',
        art_h='לא כל פתרון זהה.',
        art=['פתרון טוב מתחיל בהתאמה מדויקת לשטח, לכיווני השמש, לאופי השימוש ולקו של הבית. אחרי בדיקה במקום אנחנו מתאימים את הפתרון שנכון לכם.',
             'כך נולד פתרון שמרגיש חלק מהבית: פרגולת אלומיניום קבועה או מתכווננת, פרגולת עץ, סוכך זרועות או מפרש צל. כל אחד נבחר ונבנה למקום שלו.',
             'הקירוי, הגוון והפרופיל נקבעים יחד איתכם. כל פרויקט מתחיל בפגישה במקום ובמדידה. ההצעה נכתבת אחריהן.'],
        cards=[('פרגולות אלומיניום', 'קונסטרוקציה קבועה או פרופילים מתכווננים, בגוון ובקירוי שנבחרים לפי הבית.', G + 'project-black-hightech-pergola.webp'),
               ('פרגולות עץ', 'מראה חם וטבעי שמשתלב בבית ובגינה.', PR + 'wood-pergola-rustic.webp'),
               ('סוככים, רשתות ומפרשי צל', 'הצללה קלה לחזיתות, למרפסות ולמרחבים פתוחים.', G + 'awning-leumi.webp')],
        more='וגם קירוי לכניסות ולחניה. הפתרון נבחר בפגישה במקום, לפי המרחב.', pins=PIN_KITCHEN,
        projects=['project-black-hightech-pergola.webp', 'wood-pergola-rustic.webp', 'project-black-louvered-pergola.webp', 'pergola-white-wood.webp', 'pergola-parking-rehovot.webp', 'awning-leumi.webp'],
        faq=[('איך בוחרים בין פרגולה קבועה למתכווננת?', 'בודקים את כיווני השמש, את שעות השימוש ואת האופן שבו אתם רוצים לשלוט באור ובצל. בפגישה נעבור יחד על האפשרויות.'),
             ('אפשר לשלב תאורה או מאוורר?', 'כן. משלבים אותם כבר בשלב התכנון היישומי. הכנות החשמל מתואמות מול בעלי מקצוע מוסמכים.'),
             ('האם נדרש היתר?', PERMIT)]),
    'decks': dict(
        name='ריצוף, דקים וחיפויים', hero=HE + 'hero-deck-wood.webp', hero_alt='דק עץ בגינה עם חיפוי עץ וצמחייה',
        h1='דק חמים, בקו אחד עם הבית.', sub='דקים, ריצוף חוץ וחיפויים שמתוכננים לפי המקום. כך המרחב כולו נראה כהמשך של הבית.',
        art_h='המשטח קובע את התחושה.',
        art=['המשטח הוא הדבר הראשון שמרגישים במרחב החוץ. החומר, הגוון והכיוון שלו קובעים את האופי של המקום כולו.',
             'אנחנו מבצעים דקים מעץ טבעי או מחומר מרוכב, ריצוף חוץ באבן או בגרניט פורצלן, שבילים, משטחי ישיבה וחיפויי קיר.',
             'בפגישה במקום בודקים מפלסים, ניקוז ושימוש. עבודות משלימות מתואמות ככל שנדרש.'],
        cards=[('דקים', 'עץ טבעי או חומר מרוכב, בהתאמה למידות המקום.', G + 'project-deck-wood-pergola.webp'),
               ('מרפסות נוף', 'דק שמשאיר את הנוף במרכז.', G + 'project-lake-terrace.webp'),
               ('חיפויי קיר', 'עץ, אבן או חומר מרוכב, באותה שפה עיצובית.', G + 'cladding-1.webp')],
        more='וגם ריצוף חוץ, שבילים ומשטחי ישיבה.', pins=PIN_DECK,
        projects=['project-lake-terrace.webp', 'project-deck-view.webp', 'project-deck-wood-pergola.webp', 'project-deck-black-frame.webp', 'cladding-1.webp'],
        faq=[('עץ טבעי או חומר מרוכב?', 'לכל חומר מראה ותחזוקה אחרים. בפגישה נראה לכם דוגמאות ונבחר לפי השימוש והסגנון.'),
             ('אפשר להתאים את הדק לריצוף הקיים?', 'כן. בתכנון היישומי בודקים גבהים וגוונים כדי ליצור רצף אחד עם הבית.'),
             ('מה בודקים בפגישה במקום?', 'מפלסים, ניקוז, מידות והאופן שבו אתם משתמשים במקום.')]),
    'landscape': dict(
        name='גינה ופיתוח נוף', hero=G + 'kitchen-1.webp', hero_alt='פרגולה מקורה בצמחייה מטפסת בגינה',
        h1='גינה שמשלימה את הבית.', sub='צמחייה, שבילים ותאורה שמתוכננים יחד עם שאר מרחב החוץ. כך הכול מתחבר לשפה עיצובית אחת.',
        art_h='הגינה היא חלק מהתמונה.',
        art=['גינה טובה מתוכננת יחד עם הפרגולה, הדק והתאורה. כך כל פרט מוצא את מקומו.',
             'אנחנו מקימים ומשדרגים גינות בסגנונות שונים: טרופי, מדברי, מינימליסטי או ירוק ועוטף. הצמחייה נבחרת לפי האור, המקום והתחזוקה שמתאימה לכם.',
             'התכנון היישומי כולל גם השקיה ותאורת גינה. מטפסים יכולים להשתלב בפרגולה עצמה.'],
        cards=[('צמחייה ושתילה', 'בחירת צמחייה לפי האור, המקום והסגנון.', None),
               ('שבילים ומשטחים', 'חצץ, אבני נוי ושבילים שמחברים בין חלקי הגינה.', None),
               ('השקיה ותאורה', 'תכנון יישומי והתקנה, לאווירה נעימה גם בערב.', None)],
        more='', pins=PIN_DECK, projects=[],
        faq=[('אפשר לשלב גינה בפרויקט של פרגולה או דק?', 'כן. כשמתכננים יחד, הצמחייה, ההשקיה והתאורה מתחברות לשאר המרחב.'),
             ('איך בוחרים צמחייה?', 'לפי כיווני האור, גודל המקום והתחזוקה שמתאימה לכם.'),
             ('מה כולל התכנון היישומי?', 'צמחייה, שבילים, השקיה ותאורה, לפי המקום.')]),
    'fences': dict(
        name='גידור ותיחום', hero=G + 'fence-grey-aluminum.webp', hero_alt='גדר אלומיניום בגוון אפור כהה בחזית בית',
        h1='פרטיות, בקו של הבית.', sub='גדרות, שערים ומעקות שמתוכננים כחלק מחזית הבית. הגוון והפרופיל נבחרים לפי הקו שלו.',
        art_h='התיחום הוא חלק מהחזית.',
        art=['גדר ושער הם הדבר הראשון שרואים מהרחוב. כשהם מתוכננים בקו של הבית, הם משלימים אותו.',
             'אנחנו מבצעים גדרות אלומיניום, שערי כניסה וחניה בהפעלה ידנית או חשמלית, מעקות אלומיניום וזכוכית ומסכי פרטיות.',
             'מעקות נבדקים בכל פרויקט לגופו, בהתאם לדרישות שחלות עליו. הכנות החשמל לשער מתואמות מול בעלי מקצוע מוסמכים.'],
        cards=[('גדרות אלומיניום', 'בגוון ובפרופיל שמתאימים לחזית.', G + 'fence-grey-aluminum.webp'),
               ('גוונים ופרופילים', 'התאמה של הגוון והפרופיל לקו של הבית.', G + 'fence-white-rishon.webp'),
               ('שערים', 'שערי כניסה וחניה, בהפעלה ידנית או חשמלית.', G + 'new-46-1.webp')],
        more='וגם מעקות אלומיניום וזכוכית ומסכי פרטיות, בהתאם לפרויקט.', pins=None,
        projects=['fence-grey-aluminum.webp', 'fence-white-rishon.webp', 'new-46-1.webp'],
        faq=[('אפשר להתאים את הגדר לגוון הבית?', 'כן. הגוון והפרופיל נבחרים לפי החזית.'),
             ('שער ידני או חשמלי?', 'שתי האפשרויות קיימות. הכנות החשמל מתואמות מול בעלי מקצוע מוסמכים.'),
             ('מה לגבי מעקות?', 'מעקות נבדקים בכל פרויקט לגופו, בהתאם לדרישות שחלות עליו.')]),
    'kitchens': dict(
        name='מטבחי חוץ ונגרות', hero=HE + 'hero-pergola-kitchen-bar.webp', hero_alt='מטבח חוץ ושולחן בר תחת פרגולת אלומיניום שחורה',
        h1='לארח בחוץ, כמו בבית.', sub='מטבח חוץ, בר ופינת ישיבה שמתוכננים יחד עם ההצללה. כך האירוח זורם בין בישול לישיבה.',
        art_h='מטבח חוץ הוא לב האירוח.',
        art=['מטבח חוץ טוב מתוכנן סביב הדרך שבה אתם מארחים. המיקום, הגובה ומשטחי העבודה נקבעים לפי המקום.',
             'אנחנו מבצעים מטבחי חוץ בהתאמה אישית, דלפקי בר, איים, משטחי הגשה ונגרות חוץ לאחסון.',
             'הכנות מים, חשמל, גז, ניקוז ואוורור מתואמות מול בעלי מקצוע מוסמכים, בהתאם להיקף הפרויקט.'],
        cards=[('מטבח חוץ ובר', 'מטבח ושולחן בר תחת פרגולה, כמתחם אחד.', PR + 'pergola-kitchen-bar-side.webp'),
               ('אירוח בגינה', 'מטבח חוץ ובר אירוח בין הצמחייה.', G + 'kitchen-1.webp')],
        more='וגם איים, משטחי הגשה ונגרות חוץ לאחסון.', pins=PIN_KITCHEN,
        projects=['pergola-kitchen-bar-side.webp', 'kitchen-1.webp'],
        faq=[('אפשר לשלב מטבח חוץ עם פרגולה?', 'כן. כשמתכננים יחד, ההצללה, התאורה והמטבח הופכים למתחם אחד.'),
             ('מי מטפל בהכנות למים, לחשמל ולגז?', 'ההכנות מתואמות מול בעלי מקצוע מוסמכים, בהתאם להיקף הפרויקט.'),
             ('מה בודקים בפגישה במקום?', 'מיקום, מידות, כיווני שמש והאופן שבו אתם מארחים.')]),
    'light-build': dict(
        name='בנייה קלה ותוספות חוץ', hero=HE + 'hero-sunroom.webp', hero_alt='חדר שמש בבנייה קלה עם דלתות הזזה לגינה',
        h1='תוספת שנראית כאילו תמיד הייתה חלק מהבית.', sub='משרד, קליניקה או חדר אירוח בגינה, בתכנון יישומי שממשיך את הקו של הבית.',
        art_h='עוד חדר, באותה שפה.',
        art=['תוספת טובה ממשיכה את הבית. הגבהים, הריצוף והגוונים נבחרים כך שהמעבר ירגיש טבעי.',
             'אנחנו מבצעים משרדי חוץ, קליניקות, חדרי שמש, חדרי אירוח, מבני שירות ומחסנים.',
             'אישורים, תשתיות וליווי הנדסי, ככל שנדרשים, מתואמים מול בעלי מקצוע מוסמכים. כך גם הכנות חשמל, תקשורת ואוורור.'],
        cards=[('חדר שמש', 'תוספת מוארת שנפתחת לגינה.', HE + 'hero-sunroom.webp'),
               ('תוספת בנייה קלה', 'מבנה מבודד עם רצף ריצוף אחד לבית.', PR + 'light-sunroom-out.webp')],
        more='וגם משרדי חוץ, קליניקות, חדרי אירוח ומחסנים.', pins=PIN_SUN,
        projects=['light-sunroom-out.webp', 'glass-1.webp', 'court-consulott.webp'],
        faq=[('האם תוספת כזו דורשת היתר?', PERMIT),
             ('איך התוספת מתחברת לבית הקיים?', 'בתכנון היישומי בודקים גבהים, ריצוף וגוונים. כך התוספת ממשיכה את הבית.'),
             ('למה משמשת תוספת כזו?', 'משרד, קליניקה, חדר אירוח או חדר שמש, לפי הצורך שלכם.')]),
}

LBL = 'display:inline-flex;align-items:center;gap:10px;color:%s;font-size:14.5px;font-weight:600;margin-bottom:16px'
H2 = 'font-size:clamp(28px,3.6vw,44px);letter-spacing:-0.025em;line-height:1.12;text-wrap:balance'
W = 'width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto'
BAR = '<span style="display:block;width:24px;height:1px;background:%s"></span>'


def esc(x):
    return x.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def project(photo):
    for m in re.finditer(r"\{ title: '([^']+)',[^{}]*?\}", DATA, re.S):
        b = m.group(0)
        ph = re.search(r"photos: \[(A|P) \+ '([^']+)'", b)
        if ph and ph.group(2) == photo and 'fabric: true' not in b:
            d = re.search(r"desc: '([^']+)'", b)
            c = re.search(r"client: '([^']+)'", b)
            return m.group(1), (d.group(1) if d else ''), (G if ph.group(1) == 'A' else PR) + photo, (c.group(1) if c else '')
    return None


def build(slug, P):
    t, problems = BASE, []

    def rep(old, new, label):
        nonlocal t
        if t.count(old) != 1:
            problems.append('%s: "%s": expected 1 match, found %d' % (slug, label, t.count(old)))
            return
        t = t.replace(old, new)

    texts = [P['h1'], P['sub'], P['art_h'], P['more']] + P['art'] + [x for c in P['cards'] for x in c[:2]] + [x for f in P['faq'] for x in f]
    for x in texts:
        if re.search(r'[א-ת], ו(?!יטר)[א-ת]', x):
            problems.append('%s: comma before vav in: %s' % (slug, x[:50]))

    rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 'noindex')
    rep('<title>IL Projects | סופר צל — מעטפת מקצועית לבית ולמרחב החוץ</title>', '<title>' + P['name'] + ' | IL Projects</title>', 'title')
    wa = 'https://wa.me/972559958231?text=' + 'היי, הגעתי מדף ' + P['name'] + ' באתר ואשמח לתאם שיחת ייעוץ'

    hero = ('<section id="chero" style="position:relative;background:#1B1712;color:#F5F0E4;overflow:hidden;display:flex;align-items:flex-end;min-height:min(80vh,680px)">'
            '<img src="' + P['hero'] + '" alt="' + esc(P['hero_alt']) + '" fetchpriority="high" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
            '<span aria-hidden="true" style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(14,11,8,.92) 0%,rgba(14,11,8,.6) 45%,rgba(14,11,8,.25) 100%)"></span>'
            '<div style="position:relative;' + W + ';padding-block:clamp(6.5rem,17vh,9.5rem) clamp(2.25rem,6vh,3.75rem)">'
            '<div style="display:inline-flex;align-items:center;gap:12px;color:#E8C48C;font-size:15px;font-weight:600;margin-bottom:18px;text-shadow:0 1px 12px rgba(14,11,8,.8)"><span style="display:block;width:34px;height:1px;background:#C99752"></span>' + esc(P['name']) + '</div>'
            '<h1 style="font-size:clamp(32px,4.8vw,60px);line-height:1.1;font-weight:600;letter-spacing:-0.03em;color:#F5F0E4;max-width:18ch;text-wrap:balance;text-shadow:0 2px 24px rgba(14,11,8,.6)">' + esc(P['h1']) + '</h1>'
            '<p style="margin-top:16px;color:rgba(245,240,228,.9);font-size:clamp(17px,1.6vw,20px);max-width:42ch;line-height:1.55">' + esc(P['sub']) + '</p>'
            '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:26px">'
            '<a href="#quick" style="display:inline-flex;align-items:center;justify-content:center;min-height:54px;padding:0 34px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:16.5px;font-weight:600;white-space:nowrap">לתיאום שיחת ייעוץ</a>'
            '<a href="' + esc(wa) + '" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;justify-content:center;min-height:54px;padding:0 28px;border-radius:100px;border:1px solid rgba(245,240,228,.5);color:#F5F0E4;font-size:16.5px;white-space:nowrap;backdrop-filter:blur(6px)">שיחת וואטסאפ מהירה</a>'
            '</div></div></section>\n')

    paras = ''.join('<p style="margin-bottom:14px">%s</p>' % esc(x) for x in P['art'])
    article = ('<section id="cart" style="background:#F5F0E4;color:#211C16;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
               '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:clamp(1.5rem,4vw,3.5rem);align-items:start">'
               '<div><div style="' + LBL % '#80561E' + '">' + BAR % '#B4813C' + 'על התחום</div><h2 style="' + H2 + ';max-width:14ch">' + esc(P['art_h']) + '</h2></div>'
               '<div style="color:#4B443A;font-size:17px;line-height:1.75;max-width:56ch">' + paras + '</div></div></div></section>\n')

    def card(i, ti, tx, img):
        pic = ('<img src="%s" alt="%s" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover">'
               '<span aria-hidden="true" style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(17,14,11,.92) 0%%,rgba(17,14,11,.55) 40%%,rgba(17,14,11,0) 70%%)"></span>' % (img, esc(ti))) if img else ''
        ar = '4/5' if img else 'auto'
        pos = 'position:absolute;inset-inline:0;bottom:0;' if img else ''
        return ('<div style="position:relative;border-radius:20px;overflow:hidden;background:#1B1712;aspect-ratio:%s;color:#F5F0E4">%s<div style="%spadding:clamp(18px,2vw,26px)">'
                '<span style="font-size:13px;font-weight:600;color:#E8C48C;letter-spacing:.06em">0%d</span><h3 style="margin:6px 0;font-size:clamp(21px,2vw,25px);line-height:1.2;color:#fff">%s</h3>'
                '<p style="font-size:15.5px;line-height:1.5;color:rgba(245,240,228,.92)">%s</p></div></div>' % (ar, pic, pos, i + 1, esc(ti), esc(tx)))
    more = ('<p style="margin-top:22px;color:#4B443A;font-size:16.5px;max-width:60ch">' + esc(P['more']) + '</p>') if P['more'] else ''
    catalog = ('<section id="ccat" style="background:#ECE4D2;color:#211C16;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
               '<div style="' + LBL % '#80561E' + '">' + BAR % '#B4813C' + 'סוגי פתרונות</div>'
               '<h2 style="' + H2 + ';max-width:20ch;margin-bottom:clamp(1.5rem,4vh,2.5rem)">קו נקי, ביצוע מדויק.</h2>'
               '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:16px">' + ''.join(card(i, *c) for i, c in enumerate(P['cards'])) + '</div>' + more + '</div></section>\n')

    done = ''
    if P['pins']:
        cap, src, alt, pins = P['pins']
        dots = ''.join('<button type="button" data-pin="%d" aria-label="%s" style="position:absolute;left:%d%%;top:%d%%;transform:translate(-50%%,-50%%);width:34px;height:34px;border-radius:50%%;border:2px solid #fff;background:#B4813C;color:#fff;font:inherit;font-size:14px;font-weight:700;cursor:pointer;box-shadow:0 2px 14px rgba(0,0,0,.45)">%d</button>' % (k, esc(l), x, y, k + 1) for k, (l, x, y) in enumerate(pins))
        items = ''.join('<li data-item="%d" style="display:flex;gap:14px;align-items:center;padding:13px 0;border-top:1px solid rgba(245,240,228,.14);font-size:16.5px;line-height:1.4;color:rgba(245,240,228,.92)"><span style="flex:none;display:grid;place-items:center;width:30px;height:30px;border-radius:50%%;background:#B4813C;color:#1B1712;font-size:14px;font-weight:700">%d</span><span>%s</span></li>' % (k, k + 1, esc(l)) for k, (l, x, y) in enumerate(pins))
        done = ('<section id="cdone" style="position:relative;z-index:2;background:#1B1712;color:#F5F0E4;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
                '<div style="' + LBL % '#C99752' + '">' + BAR % '#C99752' + 'מהשטח</div>'
                '<h2 style="' + H2 + ';color:#F5F0E4;max-width:20ch">אמון מקצועי נבנה דרך תוצאות.</h2>'
                '<p style="margin:14px 0 22px;color:rgba(245,240,228,.78);font-size:17px;max-width:46ch">לחצו על מספר בתמונה ותראו מה בדיוק ביצענו.</p>'
                '<div data-pjp="0" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:clamp(1.25rem,3vw,2.5rem);align-items:center">'
                '<div style="position:relative;border-radius:20px;overflow:hidden;aspect-ratio:2064/960;min-height:230px;background:#1B1712"><img src="' + src + '" alt="' + esc(alt) + '" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">' + dots + '</div>'
                '<div><p style="margin:0 0 6px;color:#C99752;font-size:13px;font-weight:600;letter-spacing:.06em">' + esc(cap) + '</p><h3 style="font-size:clamp(22px,2.4vw,30px);line-height:1.25;color:#F5F0E4;margin-bottom:8px">מה ביצענו בפרויקט</h3><ul style="list-style:none;margin:0;padding:0">' + items + '</ul></div></div></div></section>\n')

    more_sec = ''
    found = []
    for ph in P['projects']:
        pr = project(ph)
        if pr is None:
            problems.append('%s: project photo not in projects-data.js: %s' % (slug, ph))
        else:
            found.append(pr)
    if found:
        pcards = ''.join(
            '<div style="border-radius:18px;overflow:hidden;background:#FBF7EE;box-shadow:0 1px 0 rgba(33,28,22,.06),0 14px 32px rgba(33,28,22,.1);display:flex;flex-direction:column"><div style="aspect-ratio:4/3;background:#ECE4D2"><img src="%s" alt="%s" loading="lazy" decoding="async" style="display:block;width:100%%;height:100%%;object-fit:cover"></div>'
            '<div style="padding:18px 20px 22px"><span style="font-size:12.5px;font-weight:600;color:#80561E;letter-spacing:.04em">%s</span><h3 style="margin:6px 0 8px;font-size:19px;line-height:1.3">%s</h3><p style="font-size:15.5px;line-height:1.6;color:#4B443A">%s</p></div></div>'
            % (img, esc(ti), esc(cl), esc(ti), esc(de)) for ti, de, img, cl in found)
        more_sec = ('<section id="cmore" style="background:#F5F0E4;color:#211C16;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
                    '<div style="' + LBL % '#80561E' + '">' + BAR % '#B4813C' + 'פרויקטים שביצענו</div>'
                    '<h2 style="' + H2 + ';max-width:22ch;margin-bottom:clamp(1.5rem,4vh,2.5rem)">' + esc(P['name']) + '.</h2>'
                    '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:18px">' + pcards + '</div>'
                    '<div style="margin-top:clamp(1.5rem,4vh,2.5rem)"><a href="/projects" style="display:inline-flex;align-items:center;gap:10px;min-height:50px;padding:0 26px;border-radius:100px;border:1px solid #211C16;color:#211C16;font-size:16px;font-weight:600">לכל הפרויקטים <span aria-hidden="true">←</span></a></div>'
                    '</div></section>\n')

    steps = [('01', 'פגישה במקום ומדידה', 'מדידה, כיווני שמש וצורת השימוש.'), ('02', 'תכנון יישומי והצעה', 'חומרים, גוונים והיקף, בכתב.'), ('03', 'ייצור והתקנה', 'לפי המידות של המקום ומסירה מסודרת.')]
    stephtml = ''.join('<div style="display:flex;gap:16px;align-items:baseline;border-top:1px solid rgba(33,28,22,.16);padding-block:18px"><span style="font-size:26px;font-weight:300;color:#B4813C;line-height:1;flex:none">%s</span><div><h3 style="font-size:19px;font-weight:600">%s</h3><p style="margin-top:4px;color:#4B443A;font-size:16px">%s</p></div></div>' % s for s in steps)
    faqhtml = ''.join('<details style="border-top:1px solid rgba(33,28,22,.16);padding:16px 0"><summary style="cursor:pointer;font-size:18px;font-weight:600;list-style:none">%s</summary><p style="margin-top:10px;color:#4B443A;font-size:16.5px;line-height:1.7;max-width:62ch">%s</p></details>' % (esc(q), esc(a)) for q, a in P['faq'])
    process = ('<section id="cproc" style="background:#ECE4D2;color:#211C16;padding-block:clamp(3rem,9vh,6rem)"><div style="' + W + '">'
               '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:clamp(2rem,5vw,4rem)">'
               '<div><div style="' + LBL % '#80561E' + '">' + BAR % '#B4813C' + 'איך זה עובד</div><h2 style="' + H2 + ';margin-bottom:18px">נקודת קשר אחת, מהמדידה ועד ההתקנה.</h2>' + stephtml + '</div>'
               '<div><div style="' + LBL % '#80561E' + '">' + BAR % '#B4813C' + 'שאלות נפוצות</div><h2 style="' + H2 + ';margin-bottom:18px">לפני שמתחילים.</h2>' + faqhtml + '<div style="border-top:1px solid rgba(33,28,22,.16)"></div></div>'
               '</div></div></section>\n')

    js = ('<script>/* category page: numbered pins */\n(function(){document.addEventListener("click",function(e){var pb=e.target.closest&&e.target.closest("[data-pin]");if(!pb)return;var root=pb.closest("[data-pjp]"),i=+pb.getAttribute("data-pin");'
          'root.querySelectorAll("[data-pin]").forEach(function(b){var on=+b.getAttribute("data-pin")===i;b.style.background=on?"#fff":"#B4813C";b.style.color=on?"#1B1712":"#fff";b.style.transform="translate(-50%,-50%) scale("+(on?1.18:1)+")"});'
          'root.querySelectorAll("[data-item]").forEach(function(li){li.style.background=+li.getAttribute("data-item")===i?"rgba(201,151,82,0.14)":"transparent"})});})();</script>')
    rep('<section id="why"', hero + article + catalog + done + more_sec + process + '<section id="why"', 'insert sections')
    rep('</body>', js + '</body>', 'js')
    css = ('<style id="stz-category">html body #hero,html body #why,html body #projects,html body #social,html body #scope,html body #services,html body #build,html body #reviews,html body #faq{display:none !important}'
           'html body header{background:rgba(27,23,18,0.94) !important;border-bottom-color:rgba(245,240,228,0.14) !important}'
           'html body div[style*="z-index: 900"],html body div[style*="z-index:900"]{display:none !important}summary::-webkit-details-marker{display:none}</style>')
    rep('</head>', css + '</head>', 'css')
    return t, problems


out, allp = {}, []
for slug, P in PAGES.items():
    t, pr = build(slug, P)
    out[slug] = t
    allp += pr
if allp:
    print('nothing written:\n  ' + '\n  '.join(allp))
    sys.exit(1)
for slug, t in out.items():
    t = t.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- GENERATED by tools/make-categories.py from index.html: do not edit, run the script -->', 1)
    open(os.path.join(ROOT, slug + '.html'), 'w', encoding='utf-8', newline='').write(t)
    print('wrote', slug + '.html', len(t))
