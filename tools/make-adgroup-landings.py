#!/usr/bin/env python3
"""Builds one Google Ads landing page per ad group of the "מעטפת חוץ" campaign, generated from index.html (the home page):

  balcony.html -> /balcony   ad group "פנטהאוזים ומרפסות גדולות"
  garden.html  -> /garden    ad group "בתים פרטיים וחזיתות"

index.html is only read, never written; envelope.html (tools/make-envelope.py) is not touched. Each copy keeps the home page's
design, sections, section order, components and scripts. What changes (see README-ADGROUP-LANDINGS.md):
  * noindex, own tab title, landing=1 added to the address when missing (Google Ads conversions; analytics.js unchanged);
  * hero: headline, sub line, slide photos (existing photos of the repo), slide order, captions, photo pins;
  * the first section's headline and paragraph speak to the ad group;
  * the "components" puzzle shows the ad group's components first; the projects grid shows the ad group's projects first;
  * the page opens on the matching path of the "which outdoor space" picker;
  * the long form's "what would you like to do" options are the ad group's list (first one preselected);
  * leads, WhatsApp text and the GA4 form name say which page they came from;
  * the same word fixes as /envelope (old brand name in body copy, a superlative badge, awnings in the components list).

Run from the repository root after any change to index.html:  python3 tools/make-adgroup-landings.py
Every replacement must match exactly once; if index.html changed that text the script says which one and writes nothing.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
BASE = open(SRC, encoding='utf-8').read()
H = '/img/fast/hero/'

PAGES = {
    'balcony': dict(
        title='סגירת מרפסת ופנטהאוז | IL Projects',
        h1a='סגירת מרפסת,',
        sub='סגירות זכוכית, סגירות חורף, פרגולות חשמליות ודקים למרפסת ולפנטהאוז. מהמדידה ועד המסירה, עם נקודת קשר אחת לאורך כל הדרך.',
        why_h2='סגירה, קירוי ודק — <br>בתכנון אחד.',
        why_p='במרפסת ובפנטהאוז כל רכיב משפיע על האחר: הסגירה, הקירוי, הדק והחיבור לבית. אצלנו הם מתוכננים יחד, בשפה חומרית אחת — מהמדידה ועד המסירה.',
        # slot k4 is the eager, preloaded photo; the other slots are lazy
        slots={4: H + 'hero-glass-balcony.webp', 0: H + 'hero-panoramic-balcony.webp', 1: '/img/fast/gallery/project-lake-terrace.webp',
               2: '/img/fast/gallery/project-deck-view.webp', 3: '/img/fast/gallery/project-black-glass-balcony.webp'},
        slides=[
            dict(k=4, word='לשימוש כל השנה', caption='סגירת מרפסת וקירוי', alt='מרפסת בסגירת זכוכית עם קירוי שקוף מעל הקורות',
                 pins=[('סגירת זכוכית בהזזה', '70%', '24%'), ('קירוי עליון — סנטף BH', '30%', '8%'), ('חלון בקצה המרפסת', '27%', '40%')]),
            dict(k=0, word='ופרגולה חשמלית', caption='סגירת מרפסת ופרגולת תריס', alt='מרפסת בסגירת זכוכית עם פרגולת תריס חשמלית ונוף פתוח',
                 pins=[('פרגולת תריס חשמלית', '45%', '10%'), ('סגירת זכוכית בהזזה', '32%', '40%'), ('מעקה זכוכית לנוף פנורמי', '40%', '72%'), ('דלתות הזזה ליציאה למרפסת', '74%', '45%')]),
            dict(k=3, word='בזכוכית בהזזה', caption='סגירת זכוכית בפרופיל שחור', alt='מרפסת בסגירת זכוכית בהזזה בפרופיל אלומיניום שחור',
                 pins=[('פרופיל אלומיניום שחור', '46%', '28%'), ('סגירת זכוכית בהזזה', '62%', '62%')]),
            dict(k=2, word='דק ופרגולה', caption='מרפסת נוף עם דק', alt='מרפסת נוף עם דק, פרגולה בגמר עץ ופינת ישיבה',
                 pins=[('פרגולה בגמר עץ', '55%', '8%'), ('דק', '30%', '84%'), ('מעקה לנוף פתוח', '78%', '47%')]),
            dict(k=1, word='גם לפנטהאוז', caption='מרפסת נוף עם דק ומעקה זכוכית', alt='מרפסת נוף גדולה עם דק עץ ומעקה זכוכית',
                 pins=[('דק', '40%', '45%'), ('מעקה זכוכית', '62%', '33%')]),
        ],
        path='add',
        proj_order=[6, 10, 4, 3, 2, 9, 1],
        proj_line='סגירות זכוכית, סגירות חורף, פרגולות ודקים במרפסות.',
        ch_order=[1, 0, 5, 2, 3, 4, 6],   # glass, shade, deck, light building | kitchens, fences, garden
        opts=['סגירת זכוכית למרפסת', 'סגירת חורף', 'פרגולה חשמלית למרפסת', 'סגירת פרגולה קיימת', 'מעטפת מלאה למרפסת', 'עדיין בודקים אפשרויות'],
        pick_map={'סגירת זכוכית': 'סגירת זכוכית למרפסת', 'הצללה וקירוי': 'פרגולה חשמלית למרפסת'}, pick_default='מעטפת מלאה למרפסת',
        wa='היי, הגעתי מדף סגירות המרפסת באתר',
    ),
    'garden': dict(
        title='החצר של הבית הפרטי | IL Projects',
        h1a='החצר של הבית הפרטי,',
        sub='מטבח חוץ, פרגולה לגינה, דק וריצוף, שער וגדר, חיפוי חזית וחדר שמש. תכנון אחד לכל החצר, מהמדידה ועד המסירה, עם נקודת קשר אחת.',
        why_h2='כל החצר — <br>בתכנון אחד.',
        why_p='מטבח חוץ, פרגולה, דק, גדר וחזית אפשר לבנות בשלבים, אבל כדאי לתכנן אותם יחד. כך החומרים, הגבהים והגוונים ממשיכים זה את זה — מהמדידה ועד המסירה.',
        slots={4: H + 'hero-pergola-kitchen-bar.webp', 3: H + 'hero-deck-wood.webp', 0: '/img/fast/gallery/fence-grey-aluminum.webp',
               1: H + 'hero-sunroom.webp', 2: '/img/fast/gallery/project-black-louvered-pergola.webp'},
        slides=[
            dict(k=4, word='מתוכננת כפרויקט אחד', caption='פרויקט לדוגמה · פרגולה, מטבח חוץ, שולחן בר וכסאות',
                 alt='פרגולת אלומיניום שחורה עם פרופילי הצללה בגוון דמוי עץ וסנטף BH, מעל מטבח חוץ, שולחן בר וכסאות בגינה',
                 pins=[('פרופילי הצללה בגוון דמוי עץ · סנטף BH שקוף של פלרם', '34%', '18%'), ('קורות אלומיניום שחורות', '14%', '42%'), ('מטבח חוץ', '29%', '68%'), ('שולחן בר וכסאות', '53%', '64%')]),
            dict(k=3, word='דק, פרגולה וחיפוי עץ', caption='פיתוח חוץ בעץ', alt='דק עץ בגינה עם פרגולת תריס, חיפוי עץ וגדר',
                 pins=[('פרגולה צפה', '40%', '16%'), ('דק עץ', '50%', '72%'), ('חיפוי עץ לקיר', '82%', '55%'), ('גדר ותיחום', '42%', '34%'), ('צמחייה ופיתוח גינה', '52%', '49%')]),
            dict(k=0, word='שער וגדר אלומיניום', caption='גדר אלומיניום לבית פרטי', alt='גדר אלומיניום אפורה בפסים אופקיים בחזית בית פרטי',
                 pins=[('גדר אלומיניום בפסים אופקיים', '62%', '50%')]),
            dict(k=1, word='חדר שמש ובנייה קלה', caption='תוספת חוץ בגינה', alt='חדר שמש בבנייה קלה עם דלתות הזזה לגינה',
                 pins=[('מבנה פאנל מבודד', '36%', '9%'), ('חלונות פנורמיים אל הגינה', '62%', '30%'), ('מערכת דלתות הזזה', '42%', '48%'), ('ריצוף קרמיקה ברצף אחד עם הבית', '50%', '64%')]),
            dict(k=2, word='ופרגולה לגינה', caption='פרגולת אלומיניום שחורה בגינה', alt='פרגולת אלומיניום שחורה עם רפפות מעל גינה של בית פרטי',
                 pins=[('רפפות אלומיניום', '45%', '22%')]),
        ],
        path='full',
        proj_order=[1, 5, 11, 2, 0, 9, 12],
        proj_line='מטבחי חוץ, פרגולות, דקים וגדרות בבתים פרטיים.',
        ch_order=[3, 4, 0, 5, 2, 6, 1],   # kitchens, fences, shade, deck | light building, garden, glass
        opts=['מעטפת חוץ מלאה לבית', 'מטבח חוץ ופינת אירוח', 'פרגולה לגינה', 'שער וגדר', 'דק, ריצוף וחיפוי', 'חדר שמש ותוספת בנייה', 'עדיין בודקים אפשרויות'],
        pick_map={'מטבח חוץ ואירוח': 'מטבח חוץ ופינת אירוח', 'הצללה וקירוי': 'פרגולה לגינה', 'דק, ריצוף וחיפוי': 'דק, ריצוף וחיפוי', 'בנייה קלה / חדר שמש': 'חדר שמש ותוספת בנייה'},
        pick_default='מעטפת חוץ מלאה לבית',
        wa='היי, הגעתי מדף החצר והגינה באתר',
    ),
}

js = lambda v: json.dumps(v, ensure_ascii=False)


def build(key, P):
    t = BASE
    problems = []

    def rep(old, new, label, count=1):
        nonlocal t
        n = t.count(old)
        if n != count:
            problems.append(f'{key}: "{label}": expected {count} match(es), found {n}')
            return
        t = t.replace(old, new)

    def slot(k, src):
        nonlocal t
        t2, n = re.subn(r'<img src="[^"]+"(?= alt="\{\{ sl\.alt \}\}"[^>]*display:\{\{ sl\.show' + str(k) + r' \}\})', '<img src="' + src + '"', t, count=1)
        if n != 1:
            problems.append(f'{key}: "hero slot {k}": not found')
            return
        t = t2

    # --- head: not indexed, title, landing=1 always present, preload the first hero photo ---------------------------------
    LANDING = ("<script>/* " + key + ".html: campaign landing page. analytics.js counts Google Ads conversions only when the address has landing=1; "
               "make sure it does, without reloading */(function(){try{if(!/[?&]landing=1(&|$)/.test(location.search)){"
               "var q=location.search?location.search+'&landing=1':'?landing=1';history.replaceState(history.state,'',location.pathname+q+location.hash);}}catch(e){}})();</script>")
    rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">\n' + LANDING, 'noindex + landing')
    rep('<title>IL Projects | סופר צל — מעטפת מקצועית לבית ולמרחב החוץ</title>', '<title>' + P['title'] + '</title>', 'title')
    rep('<link rel="preload" as="image" href="/img/fast/hero/hero-pergola-kitchen-bar.webp" fetchpriority="high">',
        '<link rel="preload" as="image" href="' + P['slots'][4] + '" fetchpriority="high">', 'hero preload')

    # --- hero photos: the five photo slots of the template get the ad group's photos ----------------------------------------
    for k, src in P['slots'].items():
        slot(k, src)

    # --- hero text --------------------------------------------------------------------------------------------------------
    rep('letter-spacing:-0.03em;text-shadow:0 2px 30px rgba(14,11,8,0.45);animation:stz-up 1.1s 0.35s both">מרחב חוץ שלם,<br>',
        'letter-spacing:-0.03em;text-shadow:0 2px 30px rgba(14,11,8,0.45);animation:stz-up 1.1s 0.35s both">' + P['h1a'] + '<br>', 'hero headline')
    rep('פתרונות חוץ מלאים לבית ולעסק — מהמדידה ועד המסירה, עם נקודת קשר אחת לאורך כל הדרך.', P['sub'], 'hero sub line')
    slides = ',\n      '.join(
        '{ k: %d, word: %s, caption: %s, src: %s, alt: %s,\n        pins: [%s] }' % (
            s['k'], js(s['word']), js(s['caption']), js(P['slots'][s['k']]), js(s['alt']),
            ', '.join('{ label: %s, x: %s, y: %s }' % (js(a), js(x), js(y)) for a, x, y in s['pins']))
        for s in P['slides'])
    rep("pinKey = 'stz-home-hero-pins-v1';", "pinKey = 'stz-" + key + "-hero-pins-v1';", 'pin storage key')

    # --- first section ----------------------------------------------------------------------------------------------------
    rep('text-wrap:balance">פרויקט חוץ שלם — <br>נקודת קשר אחת.</h2>', 'text-wrap:balance">' + P['why_h2'] + '</h2>', 'first section headline')
    rep('מרחב חוץ אחד נבנה מכמה שכבות. אצלנו כולן מתוכננות יחד, בשפה חומרית אחת — מהקונספט ועד המסירה.', P['why_p'], 'first section text')

    # --- path picker: opens on the ad group's path; that path shows the ad group's projects first -----------------------------
    rep("p = ['full', 'add', 'focus'].indexOf(q) > -1 ? q : sessionStorage.getItem('stz-path');",
        "p = ['full', 'add', 'focus'].indexOf(q) > -1 ? q : '" + P['path'] + "';", 'default path')
    old_orders = {'full': "proj: 'מרחבי חוץ שלמים, מכמה רכיבים שתוכננו יחד.', order: [0, 1, 3, 5, 4, 6, 2] }",
                  'add': "proj: 'תוספות לבית קיים: חדרי שמש, סגירות ומרפסות.', order: [2, 7, 4, 6, 11, 1, 8] }"}
    rep(old_orders[P['path']], "proj: " + js(P['proj_line']).replace('"', "'") + ", order: [" + ', '.join(map(str, P['proj_order'])) + "] }", 'projects order')

    # --- components puzzle and list: the ad group's components first (layout of each position unchanged) ---------------------
    ORD = P['ch_order']
    REORDER = ("\n    const __ORD = " + js(ORD) + ";\n"
               "    { const _c = chapters.map(c => Object.assign({}, c)); __ORD.forEach((j, i) => { chapters[i] = Object.assign({}, _c[j], { num: _c[i].num, span: _c[i].span, titleSize: _c[i].titleSize, tone: _c[i].tone }); }); }\n"
               "    const a11y = this.state.a11y")
    rep("\n    const a11y = this.state.a11y", REORDER, 'components reorder', count=1)
    W7 = ['קירוי והצללה', 'סגירות זכוכית', 'בנייה קלה ותוספות', 'מטבחי חוץ ואירוח', 'גידור ושערים', 'דקים, ריצוף וחיפויים', 'פיתוח חוץ וגינה']
    rep("const W7 = " + js(W7).replace('"', "'").replace("', '", "','") + ";", "const W7 = " + js([W7[j] for j in ORD]).replace('"', "'").replace("', '", "','") + ";", 'puzzle labels')
    rep("const c = chapters[p.ch];", "const c = chapters[__ORD.indexOf(p.ch)];", 'anatomy pins chapter')
    rep("openCh: p.ch", "openCh: __ORD.indexOf(p.ch)", 'anatomy pins open chapter')
    rep("hasLp: !!dc.hasLp || li === 0", "hasLp: !!dc.hasLp || dc.slotId === 'lp-cat-1'", 'pergola link stays on the shade tile')

    # --- long form ----------------------------------------------------------------------------------------------------------
    rep("const cats = ['הצללה, קירוי וחיפויים', 'הקמת גינה ופיתוח נוף', 'פתרונות אלומיניום ועץ בהתאמה אישית', 'בנייה קלה, תוספות חוץ וחדרי שמש'];",
        'const cats = ' + js(P['opts']).replace('"', "'").replace("','", "', '") + ';', 'form options')
    rep("form: { name: '', phone: '', city: '', scope: '', notes: '', category: '', stage: '' }",
        "form: { name: '', phone: '', city: '', scope: '', notes: '', category: '" + P['opts'][0] + "', stage: '' }", 'first option preselected')
    rep('<sc-for list="{{ catOpts }}" as="o" hint-placeholder-count="4">', '<sc-for list="{{ catOpts }}" as="o" hint-placeholder-count="%d">' % len(P['opts']), 'options placeholder count')
    rep("const map = { 'הצללה וקירוי': 'הצללה, קירוי וחיפויים', 'סגירת זכוכית': 'הצללה, קירוי וחיפויים', 'דק, ריצוף וחיפוי': 'הצללה, קירוי וחיפויים', 'מטבח חוץ ואירוח': 'פתרונות אלומיניום ועץ בהתאמה אישית', 'גינה ופיתוח נוף': 'הקמת גינה ופיתוח נוף', 'בנייה קלה / חדר שמש': 'בנייה קלה, תוספות חוץ וחדרי שמש' }",
        "const map = " + js(P['pick_map']).replace('"', "'").replace("':'", "': '").replace("','", "', '").replace('{', '{ ').replace('}', ' }'), 'picker map')
    rep("const cat = picked.length ? map[picked[0]] : null;",
        "const cat = picked.length ? (picked.length === 1 && map[picked[0]] ? map[picked[0]] : '" + P['pick_default'] + "') : null;", 'picker to form')

    # --- leads say where they came from -------------------------------------------------------------------------------------------
    rep("source: 'home_long'", "source: '" + key + "_long'", 'long form source')
    rep("source: 'home_quick'", "source: '" + key + "_quick'", 'quick form source')
    rep("encodeURIComponent('היי, הגעתי מהאתר ואשמח לתאם שיחת ייעוץ')", "encodeURIComponent('" + P['wa'] + " ואשמח לתאם שיחת ייעוץ')", 'WhatsApp text')
    rep("'היי, הגעתי מהאתר ואשמח שתחזרו אליי לשיחת ייעוץ.'", "'" + P['wa'] + " ואשמח שתחזרו אליי לשיחת ייעוץ.'", 'quick lead text')
    rep("'היי, הגעתי מהאתר ואשמח לתאם שיחת ייעוץ.',", "'" + P['wa'] + " ואשמח לתאם שיחת ייעוץ.',", 'long lead text')

    # --- copy that breaks the ad rules (same fixes as /envelope) -------------------------------------------------------------------
    rep('<span>מי אנחנו · IL Projects | סופר צל</span>', '<span>מי אנחנו · IL Projects</span>', 'about eyebrow')
    rep('alt="מרחב חוץ גמור של סופר צל"', 'alt="מרחב חוץ גמור של IL Projects"', 'about photo alt')
    rep('IL Projects, הידועה גם כסופר צל, מרכזת', 'IL Projects מרכזת', 'about text')
    rep('בפרויקטים הכוללים כמה תחומי שירות, סופר צל מסייעת', 'בפרויקטים הכוללים כמה תחומי שירות, IL Projects מסייעת', 'disclosure')
    rep('white-space:nowrap">המבוקש ביותר</span>', 'white-space:nowrap">מומלץ לפרויקט שלם</span>', 'badge')
    rep("'סוככי זרועות, רשתות וגגונים'", "'גגונים וקירוי בהתאמה לקו הבית'", 'components list')

    # hero slides (done last: plain string surgery between two fixed markers)
    a = t.find('  heroSlideData() {\n    return [\n')
    b = t.find('\n    ].map((s, i) => { const ov', a)
    if a < 0 or b < 0:
        problems.append(f'{key}: "hero slides": markers not found')
    else:
        t = t[:a] + '  heroSlideData() {\n    return [\n      ' + slides + t[b:]
    return t, problems


all_problems, out = [], {}
for key, P in PAGES.items():
    # every photo the page uses must exist
    for src in set(P['slots'].values()):
        if not os.path.exists(os.path.join(ROOT, src.lstrip('/'))):
            all_problems.append(f'{key}: photo missing: {src}')
    html, pr = build(key, P)
    all_problems += pr
    out[key] = html
if all_problems:
    print('nothing written:\n  ' + '\n  '.join(all_problems))
    sys.exit(1)
for key, html in out.items():
    html = html.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- GENERATED by tools/make-adgroup-landings.py from index.html: do not edit, run the script -->', 1)
    open(os.path.join(ROOT, key + '.html'), 'w', encoding='utf-8').write(html)
    print('wrote', key + '.html')
