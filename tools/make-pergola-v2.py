#!/usr/bin/env python3
"""Builds pergola-v2.html: a separate copy of the campaign landing page (pergola.html) with conversion changes.

pergola.html is only read, never written, so the page the Google Ads campaign points to stays exactly as it is.
The copy lives at pergola.supertzel.co.il/pergola-v2 (not linked from anywhere, noindex). To use it, change the final URL
of an ad group to that address; to stop using it, point the ads back to /pergola and delete pergola-v2.html.

Run from the repository root after a new export of pergola.html to rebuild the copy:  python3 tools/make-pergola-v2.py
Every replacement must match exactly once; if the export changed that text the script says so and stops.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DST = os.path.join(ROOT, 'pergola.html'), os.path.join(ROOT, 'pergola-v2.html')
t = open(SRC, encoding='utf-8').read()
problems = []


def rep(old, new, label, count=1):
    global t
    n = t.count(old)
    if n != count:
        problems.append(f'"{label}": expected {count} match(es), found {n}')
        return
    t = t.replace(old, new)


# --- not indexed, own tab title that names the product -------------------------------------------------------------
rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 'noindex')
rep('<title>פתרונות הצללה מתקדמים בהתאמה אישית | סופר צל</title>', '<title>פרגולות והצללה בהתאמה אישית | סופר צל</title>', 'title')

# --- 1) message match: the first screen is about pergolas (the copy of the page used for pergola searches) ----------
# The black louvered pergola photo (95 KB, already on the page as slide 3) replaces the glass-closure photo as the first and
# preloaded hero image; the glass-closure image is no longer eager. ?s=awning still opens on the awnings slide.
rep('<link rel="preload" as="image" href="/img/fast/lp/pg-hero.webp" fetchpriority="high">',
    '<link rel="preload" as="image" href="/img/fast/w/pg2-black-louver.webp" fetchpriority="high">', 'hero preload')
rep('<img src="/img/fast/lp/pg-hero.webp" alt="{{ sl.alt }}" fetchpriority="high" decoding="async"',
    '<img src="/img/fast/lp/pg-hero.webp" alt="{{ sl.alt }}" loading="lazy" decoding="async"', 'closure hero image lazy')
rep('<img src="/img/fast/w/pg2-black-louver.webp" alt="{{ sl.alt }}" loading="lazy" decoding="async"',
    '<img src="/img/fast/w/pg2-black-louver.webp" alt="{{ sl.alt }}" fetchpriority="high" decoding="async"', 'pergola hero image eager')
rep("    const ov = (this.state && this.state.pinOv) || {};\n    return S.map((s, i) => ov[i] ? Object.assign({}, s, { pins: ov[i] }) : s);",
    "    // pergola copy: the black louvered pergola slide (k 2) opens the hero, with a headline that names the product\n"
    "    if (sv !== 'awning') { const i2 = S.findIndex(s => s.k === 2); if (i2 > 0) { const s2 = Object.assign({}, S[i2], { word: 'פרגולות אלומיניום ועץ.' }); S.splice(i2, 1); S.unshift(s2); } }\n"
    "    const ov = (this.state && this.state.pinOv) || {};\n    return S.map((s, i) => ov[i] ? Object.assign({}, s, { pins: ov[i] }) : s);", 'slide order')
# the awnings slide (?s=awning) had no photo element on the original page: give it one
rep("s5: sl.k === 5 ? 'block' : 'none',", "s5: sl.k === 5 ? 'block' : 'none', s6: sl.k === 6 ? 'block' : 'none',", 'awning slide flag')
rep('<img src="/img/fast/projects/wood-pergola-rustic.webp" alt="{{ sl.alt }}" loading="lazy" decoding="async" style="display:{{ sl.s5 }};width:100%;height:100%;object-fit:cover;object-position:{{ sl.pos }};animation:stz-kb 14s ease-in-out infinite alternate">',
    '<img src="/img/fast/projects/wood-pergola-rustic.webp" alt="{{ sl.alt }}" loading="lazy" decoding="async" style="display:{{ sl.s5 }};width:100%;height:100%;object-fit:cover;object-position:{{ sl.pos }};animation:stz-kb 14s ease-in-out infinite alternate">\n'
    '          <img src="/img/fast/gallery/new-61-1.webp" alt="{{ sl.alt }}" loading="lazy" decoding="async" style="display:{{ sl.s6 }};width:100%;height:100%;object-fit:cover;object-position:{{ sl.pos }};animation:stz-kb 14s ease-in-out infinite alternate">',
    'awning slide image')

# --- 2) WhatsApp messages say which page they came from ------------------------------------------------------------------
rep("'היי, הגעתי מהאתר ואשמח לייעוץ קצר לגבי פרגולה והצללה למרחב החוץ שלנו.'",
    "'היי, הגעתי מדף הפרגולות באתר ואשמח לייעוץ קצר לגבי פרגולה והצללה למרחב החוץ שלנו.'", 'WhatsApp text', count=2)
rep("'היי, הגעתי מהאתר ואשמח לשיחת ייעוץ והתאמה של פתרון הצללה.'",
    "'היי, הגעתי מדף הפרגולות באתר ואשמח לשיחת ייעוץ והתאמה של פתרון הצללה.'", 'WhatsApp text (form)')

# --- 3) one name for the main button: "תאמו שיחת ייעוץ" (hero and modal already say this) -------------------------------
rep('border-radius:100px" style-hover="background:#C99752;color:#1B1712">לתיאום פגישת ייעוץ</a>',
    'border-radius:100px" style-hover="background:#C99752;color:#1B1712">תאמו שיחת ייעוץ</a>', 'inline button label')
rep('aria-label="פתיחת טופס לתיאום פגישת ייעוץ"', 'aria-label="פתיחת טופס: תאמו שיחת ייעוץ"', 'floating button aria-label')
rep('  <span>תיאום פגישת ייעוץ</span>', '  <span>תאמו שיחת ייעוץ</span>', 'floating button label')
rep('<section id="lead" aria-label="תיאום פגישת ייעוץ"', '<section id="lead" aria-label="תאמו שיחת ייעוץ"', 'lead section label')

if problems:
    print('pergola-v2.html NOT written:\n  ' + '\n  '.join(problems))
    sys.exit(1)
open(DST, 'w', encoding='utf-8').write(t)
print('pergola-v2.html written (pergola.html untouched)')
