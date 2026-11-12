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
        h1a='מרפסת לשימוש כל השנה,',
        sub='סגירת זכוכית, סגירת חורף, פרגולה חשמלית ודק למרפסת או לפנטהאוז. מהמדידה ועד המסירה, עם נקודת קשר אחת.',
        why_h2='פרויקט חוץ שלם,<br>מעטפת אחת.',
        why_p='',
        # slot k4 is the eager, preloaded photo; the other slots are lazy
        slots={4: H + 'hero-glass-balcony.webp', 0: H + 'hero-panoramic-balcony.webp', 1: '/img/fast/gallery/project-lake-terrace.webp',
               2: '/img/fast/gallery/project-deck-view.webp', 3: '/img/fast/gallery/project-black-glass-balcony.webp'},
        slides=[
            dict(k=4, word='בסגירת זכוכית', caption='סגירת מרפסת וקירוי', alt='מרפסת בסגירת זכוכית עם קירוי שקוף מעל הקורות',
                 pins=[('סגירת זכוכית בהזזה', '70%', '24%'), ('קירוי עליון — סנטף BH', '30%', '8%'), ('חלון בקצה המרפסת', '27%', '40%')]),
            dict(k=0, word='עם פרגולת תריס חשמלית', caption='סגירת מרפסת ופרגולת תריס', alt='מרפסת בסגירת זכוכית עם פרגולת תריס חשמלית ונוף פתוח',
                 pins=[('פרגולת תריס חשמלית', '45%', '10%'), ('סגירת זכוכית בהזזה', '32%', '40%'), ('מעקה זכוכית לנוף פנורמי', '40%', '72%'), ('דלתות הזזה ליציאה למרפסת', '74%', '45%')]),
            dict(k=3, word='בפרופיל אלומיניום שחור', caption='סגירת זכוכית בפרופיל שחור', alt='מרפסת בסגירת זכוכית בהזזה בפרופיל אלומיניום שחור',
                 pins=[('פרופיל אלומיניום שחור', '46%', '28%'), ('סגירת זכוכית בהזזה', '62%', '62%')]),
            dict(k=2, word='עם דק ופרגולה', caption='מרפסת נוף עם דק', alt='מרפסת נוף עם דק, פרגולה בגמר עץ ופינת ישיבה',
                 pins=[('פרגולה בגמר עץ', '55%', '8%'), ('דק', '30%', '84%'), ('מעקה לנוף פתוח', '78%', '47%')]),
            dict(k=1, word='גם בפנטהאוז', caption='מרפסת נוף עם דק ומעקה זכוכית', alt='מרפסת נוף גדולה עם דק עץ ומעקה זכוכית',
                 pins=[('דק', '40%', '45%'), ('מעקה זכוכית', '62%', '33%')]),
        ],
        env_opt='מעטפת מלאה למרפסת', env_back='סגירת זכוכית למרפסת',   # chosen full-envelope track fills this option; leaving it restores the fallback
        style=3,   # white and minimal: has the glass closure pin
        path='add',
        proj_order=[6, 10, 4, 3, 2, 9, 1],
        proj_line='סגירות זכוכית, סגירות חורף, פרגולות ודקים במרפסות.',
        ch_order=[1, 0, 5, 2, 3, 4, 6],   # glass, shade, deck, light building | kitchens, fences, garden
        opts=['סגירת זכוכית למרפסת', 'סגירת חורף', 'פרגולה חשמלית למרפסת', 'סגירת פרגולה קיימת', 'מעטפת מלאה למרפסת', 'עדיין בודקים אפשרויות'],
        pick_map={'סגירת זכוכית': 'סגירת זכוכית למרפסת', 'הצללה וקירוי': 'פרגולה חשמלית למרפסת'}, pick_default='מעטפת מלאה למרפסת',
        wa='היי, הגעתי מדף סגירות המרפסת באתר',
    ),
    'garden': dict(
        title='הגינה של הבית הפרטי | IL Projects',
        h1a='הגינה של הבית הפרטי,',
        sub='מטבח חוץ, פרגולה, דק, שער וגדר, חיפוי חזית וחדר שמש. הכול בפרויקט אחד, מהמדידה ועד המסירה, עם נקודת קשר אחת.',
        why_h2='פרויקט חוץ שלם,<br>מעטפת אחת.',
        why_p='',
        slots={4: H + 'hero-pergola-kitchen-bar.webp', 3: H + 'hero-deck-wood.webp', 0: '/img/fast/gallery/fence-grey-aluminum.webp',
               1: H + 'hero-sunroom.webp', 2: '/img/fast/gallery/project-black-louvered-pergola.webp'},
        slides=[
            dict(k=4, word='מתוכננת כפרויקט אחד', caption='פרויקט לדוגמה · פרגולה, מטבח חוץ, שולחן בר וכסאות',
                 alt='פרגולת אלומיניום שחורה עם פרופילי הצללה בגוון דמוי עץ וסנטף BH, מעל מטבח חוץ, שולחן בר וכסאות בגינה',
                 pins=[('פרופילי הצללה בגוון דמוי עץ · סנטף BH שקוף של פלרם', '34%', '18%'), ('קורות אלומיניום שחורות', '14%', '42%'), ('מטבח חוץ', '29%', '68%'), ('שולחן בר וכסאות', '53%', '64%')]),
            dict(k=3, word='עם דק, פרגולה וחיפוי עץ', caption='פיתוח חוץ בעץ', alt='דק עץ בגינה עם פרגולת תריס, חיפוי עץ וגדר',
                 pins=[('פרגולה צפה', '40%', '16%'), ('דק עץ', '50%', '72%'), ('חיפוי עץ לקיר', '82%', '55%'), ('גדר ותיחום', '42%', '34%'), ('צמחייה ופיתוח גינה', '52%', '49%')]),
            dict(k=0, word='עם שער וגדר אלומיניום', caption='גדר אלומיניום לבית פרטי', alt='גדר אלומיניום אפורה בפסים אופקיים בחזית בית פרטי',
                 pins=[('גדר אלומיניום בפסים אופקיים', '62%', '50%')]),
            dict(k=1, word='עם חדר שמש בבנייה קלה', caption='תוספת חוץ בגינה', alt='חדר שמש בבנייה קלה עם דלתות הזזה לגינה',
                 pins=[('מבנה פאנל מבודד', '36%', '9%'), ('חלונות פנורמיים אל הגינה', '62%', '30%'), ('מערכת דלתות הזזה', '42%', '48%'), ('ריצוף קרמיקה ברצף אחד עם הבית', '50%', '64%')]),
            dict(k=2, word='עם פרגולת אלומיניום', caption='פרגולת אלומיניום שחורה בגינה', alt='פרגולת אלומיניום שחורה עם רפפות מעל גינה של בית פרטי',
                 pins=[('רפפות אלומיניום', '45%', '22%')]),
        ],
        env_opt='מעטפת חוץ מלאה לבית', env_back='',   # chosen full-envelope track fills this option; leaving it restores the fallback
        style=3,   # same illustration and legend as /balcony so "who we are" is identical on both pages
        path='full',
        proj_order=[1, 5, 11, 2, 0, 9, 12],
        proj_line='מטבחי חוץ, פרגולות, דקים וגדרות בבתים פרטיים.',
        ch_order=[3, 4, 0, 5, 2, 6, 1],   # kitchens, fences, shade, deck | light building, garden, glass
        opts=['מעטפת חוץ מלאה לבית', 'מטבח חוץ ופינת אירוח', 'פרגולה לגינה', 'שער וגדר', 'דק, ריצוף וחיפוי', 'חדר שמש ותוספת בנייה', 'עדיין בודקים אפשרויות'],
        pick_map={'מטבח חוץ ואירוח': 'מטבח חוץ ופינת אירוח', 'הצללה וקירוי': 'פרגולה לגינה', 'דק, ריצוף וחיפוי': 'דק, ריצוף וחיפוי', 'בנייה קלה / חדר שמש': 'חדר שמש ותוספת בנייה'},
        pick_default='מעטפת חוץ מלאה לבית',
        wa='היי, הגעתי מדף הגינה והבית הפרטי באתר',
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
    rep('letter-spacing:-0.03em;text-shadow:0 2px 30px rgba(14,11,8,0.45);animation:stz-up 1.1s 0.35s both">כשמדויק,<br><span style="display:block;min-height:1.1em;color:#C99752;font-weight:300">זה מרגיש אחרת.</span></h1>',
        'letter-spacing:-0.03em;text-shadow:0 2px 30px rgba(14,11,8,0.45);animation:stz-up 1.1s 0.35s both">' + P['h1a'] + '<br><span style="display:block;min-height:1.1em;color:#C99752;font-weight:300">{{ heroRotEl }}</span></h1>', 'hero headline')
    rep('מרחב חוץ שמתוכנן סביב החיים שלכם בבית. שפה עיצובית אחת ונקודת קשר אחת, מהמדידה ועד ההתקנה.', P['sub'], 'hero sub line')
    slides = ',\n      '.join(
        '{ k: %d, word: %s, caption: %s, src: %s, alt: %s,\n        pins: [%s] }' % (
            s['k'], js(s['word']), js(s['caption']), js(P['slots'][s['k']]), js(s['alt']),
            ', '.join('{ label: %s, x: %s, y: %s }' % (js(a), js(x), js(y)) for a, x, y in s['pins']))
        for s in P['slides'])
    rep("pinKey = 'stz-home-hero-pins-v1';", "pinKey = 'stz-" + key + "-hero-pins-v1';", 'pin storage key')

    # --- first section ----------------------------------------------------------------------------------------------------
    rep('text-wrap:balance">פרויקט חוץ שלם,<br>מעטפת אחת.</h2>', 'text-wrap:balance">' + P['why_h2'] + '</h2>', 'first section headline')
    if P['why_p']:
        rep('מרחב החוץ שלכם, מתוכנן כמו הבית עצמו. שפה עיצובית אחת, קו נקי ונקודת קשר אחת, מהפגישה הראשונה ועד המסירה.', P['why_p'], 'first section text')
    else:
        rep('<p style="margin:0;flex:1 1 320px;color:#4B443A;font-size:18px;max-width:38ch">מרחב החוץ שלכם, מתוכנן כמו הבית עצמו. שפה עיצובית אחת, קו נקי ונקודת קשר אחת, מהפגישה הראשונה ועד המסירה.</p>', '', 'first section text removed')

    # --- path picker: opens on the ad group's path; that path shows the ad group's projects first -----------------------------
    rep("p = ['full', 'add', 'focus'].indexOf(q) > -1 ? q : sessionStorage.getItem('stz-path');",
        "p = ['full', 'add', 'focus'].indexOf(q) > -1 ? q : '" + P['path'] + "';", 'default path')
    old_orders = {'full': "proj: 'פרויקטים שבהם כל המרחב תוכנן יחד, בשפה עיצובית אחת.', order: [0, 1, 3, 5, 4, 6, 2] }",
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
    rep('white-space:nowrap">המבוקש ביותר</span>', 'white-space:nowrap">מומלץ לפרויקט שלם</span>', 'badge')
    rep("'סוככי זרועות, רשתות וגגונים'", "'גגונים וקירוי בהתאמה לקו הבית'", 'components list')

    # --- first card: the numbered envelope illustration (AI render, "הדמיה") with pins and a legend, instead of the generic photo -----------------
    old_img = '<div style="border-radius:14px;overflow:hidden;aspect-ratio:21/9;background:#ECE4D2;margin-bottom:16px" data-ab0img=""><img src="/img/fast/slots/ab-hero.webp" alt="מרחב חוץ גמור של IL Projects" loading="lazy" decoding="async" style="display:block;width:100%;height:100%;object-fit:cover"></div>'
    new_img = ('<div style="display:flex;flex-direction:column;flex:1 1 auto;margin-bottom:16px" data-envfig="">'
        '<div style="position:relative;border-radius:14px;overflow:hidden;aspect-ratio:16/9;flex:none;background:#2A241D">'
        '<img src="{{ styleSrc }}" alt="{{ styleAlt }}" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
        '<sc-for list="{{ worldPins }}" as="w" hint-placeholder-count="5">'
        '<button type="button" aria-label="{{ w.aria }}" aria-pressed="{{ w.pressed }}" title="{{ w.aria }}" onPointerDown="{{ stopEv }}" onClick="{{ w.onTap }}" style="pointer-events:auto;position:absolute;left:{{ w.x }};top:{{ w.y }};transform:translate(-50%,-50%) scale({{ w.scale }});display:flex;align-items:center;justify-content:center;width:44px;height:44px;padding:0;border:0;background:transparent;cursor:pointer;transition:transform 0.2s">'
        '<span style="display:flex;align-items:center;justify-content:center;width:{{ pinSz }};height:{{ pinSz }};border-radius:50%;border:2px solid #FFFFFF;background:{{ w.bg }};color:{{ w.fg }};font-size:13px;font-weight:700;box-shadow:0 2px 12px rgba(0,0,0,0.4)">{{ w.mark }}</span></button></sc-for>'
        '<span style="position:absolute;bottom:8px;right:12px;color:#F2C230;font-size:12.5px;font-weight:500;letter-spacing:0.04em;text-shadow:0 1px 3px rgba(0,0,0,0.6);pointer-events:none">הדמיה</span></div>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));grid-auto-rows:minmax(46px,1fr);flex:1 1 auto;gap:0 22px;margin-top:6px">'
        '<sc-for list="{{ legendL }}" as="g" hint-placeholder-count="5">'
        '<button type="button" aria-pressed="{{ g.pressed }}" onPointerDown="{{ stopEv }}" onClick="{{ g.onTap }}" style="font:inherit;color:inherit;text-align:start;width:100%;display:flex;align-items:center;gap:10px;min-height:44px;padding:6px 0;background:transparent;border:0;border-bottom:1px solid rgba(33,28,22,0.1);font-size:14.5px;cursor:pointer">'
        '<span style="flex:0 0 auto;display:flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:{{ g.dot }};color:{{ g.fg }};font-size:11.5px;font-weight:700;border:2px solid #FFFFFF;box-shadow:0 0 0 1px #B4813C">{{ g.mark }}</span>'
        '<span style="flex:1">{{ g.label }}</span><span style="font-size:12.5px;font-weight:600;color:#8A5F24">{{ g.cta }}</span></button></sc-for></div></div>')
    rep(old_img, new_img, 'about image to numbered illustration')
    rep("const sty = this.styles()[this.state.style ?? 0];", "const sty = this.styles()[this.state.style ?? " + str(P['style']) + "];", 'default legend style')
    rep("const si = this.state.style ?? 0, S = STY[si], P = S.P;", "const si = this.state.style ?? " + str(P['style']) + ", S = STY[si], P = S.P;", 'default illustration style')
    # --- catalogue page 2: choosing a service track also selects the same track in the next section ("איזה מרחב חוץ אתם מתכננים?") ---------------
    rep("onTap: () => this.setState(s => ({ trackTab: (s.trackTab ?? (this.state.narrow ? -1 : 2)) === i ? -1 : i })) }; }),",
        "onTap: () => { const wasOpen = (this.state.trackTab ?? (this.state.narrow ? -1 : 2)) === i; this.setState(s => ({ trackTab: wasOpen ? -1 : i })); { const pk = ['focus', 'add', 'full'][i]; this.setState({ path: pk, openFq: 0 }); this.syncCat(pk); try { sessionStorage.setItem('stz-path', pk); } catch (e) {} try { window.stzTrack && window.stzTrack('select_scope', { scope: pk }); } catch (e) {} } } }; }),",
        'track click selects the matching path')
    # --- the opened track offers "להשאיר פנייה" right away, to catch a visitor who just chose a track --------------------------------------------
    cta = ('</ul><div style="padding:2px 0 18px"><a href="#quick" style="display:inline-flex;align-items:center;gap:10px;min-height:46px;padding:0 24px;border-radius:100px;background:#B4813C;color:#1B1712;font-size:15.5px;font-weight:600;white-space:nowrap" '
           'style-hover="background:#C99752;color:#1B1712">להשאיר פנייה <span aria-hidden="true">←</span></a></div>')
    t, n = re.subn(r'(color:#211C16;font-size:14\.5px">(?:(?!</ul>).){0,260}?\{\{ it \}\}</span></li>\s*</sc-for>\s*)</ul>', lambda m: m.group(1) + cta, t, count=1, flags=re.S)
    if n != 1:
        problems.append(f'{key}: "leave an inquiry button": not found')
    rep("revealH: o ? '260px' : '0px'", "revealH: o ? '330px' : '0px'", 'track reveal height')
    # --- the long form follows the chosen track: "מעטפת מלאה" fills the envelope option, the visitor can still change it ----------------------------
    sync = ("  syncCat(pk) { const ENV = " + js(P['env_opt']) + ", DEF = " + js(P['env_back']) + "; this.setState(s => { const c = s.form.category; const n = pk === 'full' ? ENV : (c === ENV ? DEF : c); return n === c ? null : { form: Object.assign({}, s.form, { category: n }) }; }); }\n"
            "  initPath() {")
    rep("  initPath() {", sync, 'syncCat method')
    rep("    if (['full', 'add', 'focus'].indexOf(p) > -1) this.setState({ path: p });", "    if (['full', 'add', 'focus'].indexOf(p) > -1) { this.setState({ path: p, trackTab: ['focus', 'add', 'full'].indexOf(p) }); this.syncCat(p); }", 'syncCat on arrival')
    rep("    this.setState({ path: k, openFq: 0 });", "    this.setState({ path: k, openFq: 0 }); this.syncCat(k);", 'syncCat on card pick')
    # lead-modal.js opens the contact window for any button whose text has "תיאום"; the full-envelope track must select itself like the other two
    # the home page hides the who-we-are pages behind a link to /about and shows an Instagram strip; a landing page keeps them open and has no outbound strip
    t, n_more = re.subn(r'<div data-more-row="".*?</div>\s*', '', t, count=1, flags=re.S)
    if n_more != 1:
        problems.append(f'{key}: "more row": not found')
    rep('<div id="tracks" data-reveal=""', '<div id="tracks" class="stz-open" data-reveal=""', 'tracks open')
    rep('</head>', '<style id="stz-lp-nosocial">html body #social{display:none !important}</style></head>', 'no social strip')
    # --- no book flipping: three cards in one view (illustration | text + steps | tracks), stacked on phones ---------------------------------------
    m = re.search(r'(<h3 style="font-size:clamp\(22px,2\.4vw,28px\)[^>]*>בית אחד לכל מעטפת החוץ</h3>.*?</p>)(\s*)(<button type="button" aria-label="לעמוד הבא" onClick="\{\{ bookNext \}\}" data-flip-anim)', t, flags=re.S)
    ms = re.search(r'(<div style="margin-top:18px;display:flex;flex-direction:column;gap:10px">.*?</div>\s*</div>)(?=\s*</div>\s*</div>\s*<div data-bkctl)', t, flags=re.S)
    hdr = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;color:#8A5F24;font-size:12.5px;font-weight:600;letter-spacing:0.08em"><span>מסלולי שירות · איך אנחנו עוזרים</span><span>02</span></div>'
    p2 = '<div data-bkpage="" data-bkp2=""'
    if not m or not ms or t.count(hdr) != 1 or t.count(p2) != 1:
        problems.append(f'{key}: "split about card": markers not found')
    else:
        text_html, steps_html = m.group(1), ms.group(1)
        # take the steps out first (they come later in the file), then the text block
        t = t[:ms.start()] + t[ms.end():]
        m = re.search(r'(<h3 style="font-size:clamp\(22px,2\.4vw,28px\)[^>]*>בית אחד לכל מעטפת החוץ</h3>.*?</p>)(\s*)(<button type="button" aria-label="לעמוד הבא" onClick="\{\{ bookNext \}\}" data-flip-anim)', t, flags=re.S)
        t = t[:m.start()] + m.group(2) + m.group(3) + t[m.end():]
        head2 = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;color:#8A5F24;font-size:12.5px;font-weight:600;letter-spacing:0.08em"><span>בית אחד · איך זה עובד</span><span>02</span></div>'
        card = ('<div data-bkcard="" style="background:#FBF7EE;border-radius:20px;box-shadow:0 1px 0 rgba(33,28,22,0.06),0 18px 40px rgba(33,28,22,0.12);padding:clamp(1.25rem,3vw,2.25rem);box-sizing:border-box">'
                + head2 + text_html + steps_html.replace('margin-top:18px', 'margin-top:8px', 1) + '</div>\n        ')
        t = t.replace(p2, card + p2, 1)
        t = t.replace(hdr, hdr.replace('<span>02</span>', '<span>03</span>'), 1)
        rep('aria-hidden="{{ bookP0Hidden }}"', 'aria-hidden="false"', 'page 1 visible to readers')
        rep('aria-hidden="{{ bookP2Hidden }}"', 'aria-hidden="false"', 'page 3 visible to readers')
        PG = 'html body [data-bkwrap] > [data-bkpage], html body [data-bkwrap] > [data-bkpage]:first-child, html body [data-bkwrap] > [data-bkpage]:last-child, html body [data-bkwrap] > [data-bkpage]:nth-child(n)'
        CSS = ('<style id="stz-nobook">html body [data-bkwrap]{display:grid !important;grid-template-columns:minmax(0,1fr) !important;gap:18px !important;perspective:none !important;align-items:stretch !important}'
               + PG + '{grid-area:auto !important;position:relative !important;top:auto !important;inset-inline:auto !important;height:auto !important;transform:none !important;transition:none !important;opacity:1 !important;overflow:visible !important;border-radius:20px !important;box-shadow:0 1px 0 rgba(33,28,22,0.06),0 18px 40px rgba(33,28,22,0.12) !important}'
               'html body [data-bkwrap] [data-flip-anim],html body [data-bkctl]{display:none !important}'
               'html body [data-bkwrap] > [data-bkpage][data-ab0]{padding-bottom:clamp(1.25rem,3vw,2.25rem) !important}'
               'html body [data-bkcard] [data-stepsl]{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr)) !important;gap:8px !important}html body [data-bkcard] [data-stepsl] > div{display:flex !important;flex-direction:column !important;align-items:flex-start !important;gap:2px !important;width:auto !important;height:auto !important;min-height:0 !important;padding:9px 14px !important;border-radius:12px !important}html body [data-bkcard] [data-stepsl] p{display:none !important}html body [data-bkcard] [data-stepsl] h4{font-size:16px !important}html body [data-bkcard] [data-stepsl] > div::after,html body [data-bkcard] [data-stepsl] > div::before{display:none !important}'
               '@media (min-width:1000px){html body [data-bkwrap]{grid-template-columns:repeat(2,minmax(0,1fr)) !important}html body [data-bkwrap] > [data-bkpage][data-ab0]:nth-child(n){grid-column:1 / -1 !important;grid-area:auto / 1 / auto / -1 !important}html body [data-ab0] [data-envfig]{display:grid !important;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr) !important;gap:30px !important;align-items:stretch !important;margin-bottom:0 !important}html body [data-bkp2]{display:flex !important;flex-direction:column !important}html body [data-bkp2] [role=list]{flex:1 1 auto !important;display:flex !important;flex-direction:column !important}html body [data-bkp2] [role=listitem]{flex:1 1 auto !important;display:flex !important;flex-direction:column !important;justify-content:center !important}html body [data-ab0] [data-envfig] > div:first-child{align-self:start !important}html body [data-ab0] [data-envfig] > div:last-child{grid-template-columns:minmax(0,1fr) !important;margin-top:0 !important;grid-auto-rows:minmax(48px,1fr) !important}}</style>')
        rep('</head>', CSS + '</head>', 'no-book css')
        SLIDE_CSS = ('<style id="stz-slide">html body [data-bkwrap].stz-slide{display:grid !important;grid-template-columns:minmax(0,1fr) !important}'
                     'html body [data-bkwrap].stz-slide > [data-bkpage]:nth-child(n),html body [data-bkwrap].stz-slide > [data-bkcard]{grid-area:1 / 1 !important;opacity:0 !important;visibility:hidden !important;transition:opacity .55s ease,visibility .55s !important}'
                     'html body [data-bkwrap].stz-slide > .stz-on.stz-on:nth-child(n){opacity:1 !important;visibility:visible !important}'
                     'html body [data-bkwrap].stz-slide > [data-ab0]{display:flex !important;flex-direction:column !important;justify-content:center !important}'
                     '.stz-pgbar{display:none;justify-content:center;align-items:center;gap:14px;margin-top:14px}'
                     '.stz-pgbar button{font:inherit;cursor:pointer}'
                     '.stz-pgbar [data-prev],.stz-pgbar [data-next]{width:44px;height:44px;border-radius:50%;border:1px solid #211C16;background:#211C16;color:#F5F0E4;font-size:17px}'
                     '.stz-pgbar [data-dot]{width:10px;height:10px;padding:0;border-radius:50%;border:0;background:rgba(33,28,22,0.25);margin:0 4px;transition:background .3s,width .3s}'
                     '.stz-pgbar [data-dot][aria-current="true"]{background:#B4813C;width:26px;border-radius:6px}'
                     '.stz-pgbar [data-dots]{display:flex;align-items:center;min-height:44px}'
                     # desktop: the page already reads --stz-max (container) and --stz-hz/--stz-bz (text scale): widen the container with the screen
                     # instead of scaling a mobile column (no zoom hack)
                     + ''.join('@media (min-width:%dpx){:root{--stz-max:%s !important;--stz-hz:%s;--stz-bz:%s}}' % (w, mx, hz, bz)
                               for w, mx, hz, bz in ((1500, 'min(86vw,1440px)', '1.05', '1.05'), (1800, 'min(84vw,1640px)', '1.12', '1.1'),
                                                     (2200, 'min(82vw,1960px)', '1.3', '1.25'), (2800, 'min(82vw,2480px)', '1.6', '1.5'),
                                                     (3400, 'min(82vw,3000px)', '1.9', '1.75'), (4000, 'min(82vw,3500px)', '2.2', '2.0')))
                     + '@media (min-width:1500px){html body #tracks{max-width:none !important}}'
                     # hero gold line was washed out over bright photos: lighter gold, heavier weight, dark halo
                     + 'html body #hero h1 > span{color:#EBBF72 !important;font-weight:500 !important;text-shadow:0 2px 16px rgba(14,11,8,.92),0 0 3px rgba(14,11,8,.75),0 1px 1px rgba(14,11,8,.6) !important}'
                     + '</style>')
        SLIDE_JS = r"""<script>/* stz-slide: on narrow screens the three catalogue pages turn by themselves; touch, tap or focus stops it */
(function(){
  var mq = window.matchMedia('(max-width:999px)'), rm = window.matchMedia('(prefers-reduced-motion: reduce)');
  var tries = 0;
  function init(){
    var wrap = document.querySelector('[data-bkwrap]');
    var pages = wrap ? [].filter.call(wrap.children, function(c){ return c.hasAttribute('data-bkpage') || c.hasAttribute('data-bkcard'); }) : [];
    if (pages.length < 3) { if (tries++ < 40) setTimeout(init, 300); return; }
    var i = 0, timer = null, stopped = false, seen = true;
    var bar = document.createElement('div'); bar.className = 'stz-pgbar';
    bar.innerHTML = '<button type="button" data-prev aria-label="לעמוד הקודם">→</button><span data-dots></span><button type="button" data-next aria-label="לעמוד הבא">←</button>';
    var dots = bar.querySelector('[data-dots]');
    pages.forEach(function(p, k){ var d = document.createElement('button'); d.type = 'button'; d.setAttribute('data-dot', ''); d.setAttribute('aria-label', 'עמוד ' + (k + 1)); d.addEventListener('click', function(){ stop(); show(k); }); dots.appendChild(d); });
    wrap.parentNode.insertBefore(bar, wrap.nextSibling);
    function show(n){
      i = (n + pages.length) % pages.length;
      pages.forEach(function(p, k){ p.classList.toggle('stz-on', k === i); if (mq.matches) p.setAttribute('aria-hidden', k === i ? 'false' : 'true'); });
      [].forEach.call(dots.children, function(d, k){ d.setAttribute('aria-current', k === i ? 'true' : 'false'); });
    }
    function stop(){ stopped = true; if (timer) { clearInterval(timer); timer = null; } }
    function start(){ if (timer || stopped || rm.matches || !mq.matches) return; timer = setInterval(function(){ if (seen) show(i + 1); }, 6500); }
    function apply(){
      var on = mq.matches;
      wrap.classList.toggle('stz-slide', on); bar.style.display = on ? 'flex' : 'none';
      if (on) { show(i); start(); } else { if (timer) { clearInterval(timer); timer = null; } pages.forEach(function(p){ p.classList.remove('stz-on'); p.setAttribute('aria-hidden', 'false'); }); }
    }
    bar.querySelector('[data-prev]').addEventListener('click', function(){ stop(); show(i - 1); });
    bar.querySelector('[data-next]').addEventListener('click', function(){ stop(); show(i + 1); });
    ['pointerdown', 'focusin', 'touchstart'].forEach(function(ev){ wrap.addEventListener(ev, stop, { passive: true }); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function(es){ seen = es[0].isIntersecting; }, { threshold: 0.4 }).observe(wrap);
    (mq.addEventListener ? mq.addEventListener('change', apply) : mq.addListener(apply));
    apply();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
</script>"""
        rep('</head>', SLIDE_CSS + '</head>', 'slider css')
        rep('</body>', SLIDE_JS + '</body>', 'slider script')
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
