#!/usr/bin/env python3
"""Builds envelope.html: the Google Ads landing page of the "מעטפת חוץ" campaign, generated from index.html (the home page).

index.html is only read, never written. The copy keeps the home page's design, structure, sections and scripts exactly; only these
differ (see README-ENVELOPE.md):
  * not indexed (noindex), own tab title; served at /envelope (vercel.json cleanUrls, no rewrite needed);
  * opens on the "מעטפת מלאה" path (as /?path=full does) unless ?path= says otherwise;
  * always counts as a campaign landing page: if the address has no landing=1, the page adds it (analytics.js isLanding() is unchanged);
  * the long form's "what would you like to do" options are the envelope list, envelope first and preselected;
  * leads say where they came from: GA4 form = envelope_long / envelope_quick, WhatsApp and lead text name the page
    (lead.js adds "עמוד: /envelope" and the UTM/gclid as on every page);
  * a few words that break the ad rules: the old brand name in body copy, a superlative badge, awnings in the components list.

Run from the repository root after any change to index.html:  python3 tools/make-envelope.py
Every replacement must match exactly once; if index.html changed that text the script says which one and writes nothing.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST = os.path.join(ROOT, 'index.html'), os.path.join(ROOT, 'envelope.html')
t = open(SRC, encoding='utf-8').read()
problems = []


def rep(old, new, label, count=1):
    global t
    n = t.count(old)
    if n != count:
        problems.append(f'"{label}": expected {count} match(es), found {n}')
        return
    t = t.replace(old, new)


ENV = 'מעטפת חוץ מלאה לבית'
OPTS = [ENV, 'סגירת זכוכית לפנטהאוז או למרפסת', 'פרגולת אלומיניום', 'פרגולת תריס חשמלית', 'דק, ריצוף וחיפוי', 'עדיין בודקים אפשרויות']

# --- head: not indexed, tab title, landing=1 always present (so leads, WhatsApp and calls count as campaign conversions) -------------
LANDING = ("<script>/* envelope.html: campaign landing page. analytics.js counts Google Ads conversions only when the address has landing=1; "
           "make sure it does, without reloading */(function(){try{if(!/[?&]landing=1(&|$)/.test(location.search)){"
           "var q=location.search?location.search+'&landing=1':'?landing=1';history.replaceState(history.state,'',location.pathname+q+location.hash);}}catch(e){}})();</script>")
rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">\n' + LANDING, 'noindex + landing')
rep('<title>IL Projects | סופר צל — מעטפת מקצועית לבית ולמרחב החוץ</title>', '<title>מעטפת חוץ שלמה לבית | IL Projects</title>', 'title')

# --- opens on the full-envelope path -----------------------------------------------------------------------------------------
rep("p = ['full', 'add', 'focus'].indexOf(q) > -1 ? q : sessionStorage.getItem('stz-path');",
    "p = ['full', 'add', 'focus'].indexOf(q) > -1 ? q : 'full';", 'default path full')

# --- long form: envelope options, envelope first and preselected ------------------------------------------------------------
rep("const cats = ['הצללה, קירוי וחיפויים', 'הקמת גינה ופיתוח נוף', 'פתרונות אלומיניום ועץ בהתאמה אישית', 'בנייה קלה, תוספות חוץ וחדרי שמש'];",
    'const cats = ' + repr(OPTS).replace('"', "'") + ';', 'form options')
rep("form: { name: '', phone: '', city: '', scope: '', notes: '', category: '', stage: '' }",
    "form: { name: '', phone: '', city: '', scope: '', notes: '', category: '" + ENV + "', stage: '' }", 'envelope preselected')
rep('<sc-for list="{{ catOpts }}" as="o" hint-placeholder-count="4">', '<sc-for list="{{ catOpts }}" as="o" hint-placeholder-count="6">', 'options placeholder count')
# the "plan your space" picker hands its choice to the form: one glass or deck pick keeps its option, anything else is the envelope
rep("const map = { 'הצללה וקירוי': 'הצללה, קירוי וחיפויים', 'סגירת זכוכית': 'הצללה, קירוי וחיפויים', 'דק, ריצוף וחיפוי': 'הצללה, קירוי וחיפויים', 'מטבח חוץ ואירוח': 'פתרונות אלומיניום ועץ בהתאמה אישית', 'גינה ופיתוח נוף': 'הקמת גינה ופיתוח נוף', 'בנייה קלה / חדר שמש': 'בנייה קלה, תוספות חוץ וחדרי שמש' }",
    "const map = { 'סגירת זכוכית': 'סגירת זכוכית לפנטהאוז או למרפסת', 'דק, ריצוף וחיפוי': 'דק, ריצוף וחיפוי' }", 'picker map')
rep("const cat = picked.length ? map[picked[0]] : null;",
    "const cat = picked.length ? (picked.length === 1 && map[picked[0]] ? map[picked[0]] : '" + ENV + "') : null;", 'picker to form')

# --- leads say where they came from -----------------------------------------------------------------------------------------
rep("source: 'home_long'", "source: 'envelope_long'", 'long form source')
rep("source: 'home_quick'", "source: 'envelope_quick'", 'quick form source')
rep("encodeURIComponent('היי, הגעתי מהאתר ואשמח לתאם שיחת ייעוץ')", "encodeURIComponent('היי, הגעתי מדף מעטפת החוץ באתר ואשמח לתאם שיחת ייעוץ')", 'WhatsApp text')
rep("'היי, הגעתי מהאתר ואשמח שתחזרו אליי לשיחת ייעוץ.'", "'היי, הגעתי מדף מעטפת החוץ באתר ואשמח שתחזרו אליי לשיחת ייעוץ.'", 'quick lead text')
rep("'היי, הגעתי מהאתר ואשמח לתאם שיחת ייעוץ.',", "'היי, הגעתי מדף מעטפת החוץ באתר ואשמח לתאם שיחת ייעוץ.',", 'long lead text')

# --- copy that breaks the ad rules (old brand name in body copy, superlative, awnings) -------------------------------------------
rep('white-space:nowrap">המבוקש ביותר</span>', 'white-space:nowrap">מומלץ לפרויקט שלם</span>', 'badge')
rep("'סוככי זרועות, רשתות וגגונים'", "'גגונים וקירוי בהתאמה לקו הבית'", 'components list')

if problems:
    print('envelope.html NOT written:\n  ' + '\n  '.join(problems))
    sys.exit(1)
t = t.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- GENERATED by tools/make-envelope.py from index.html: do not edit, run the script -->', 1)
open(DST, 'w', encoding='utf-8').write(t)
print('wrote', os.path.relpath(DST, ROOT))
