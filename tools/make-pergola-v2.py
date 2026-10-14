#!/usr/bin/env python3
"""Builds pergola-v2.html: a campaign landing page generated from pergola.html, without touching pergola.html.

pergola.html is only read, never written, so the page the current Google Ads campaign points to stays exactly as it is.
The result is served at pergola.supertzel.co.il/pergola-v2 (not linked from anywhere, noindex).

What the copy changes (see README-PERGOLA-V2.md):
  * one page per ad group, chosen by ?s=  (default = pergolas, ?s=glass, ?s=deck, ?s=awning): headline, sub line, three check lines,
    hero photos, product tab and the scrolling band all match the search;
  * the rest of the page follows the ad group too, so nothing on a deck page talks about pergola shade: the sun simulator and
    "before you choose a shading solution" block only exist on the pergola page (and leave the menu and the side rail with it),
    the proof points, the first process step, the FAQ questions, the contact text and the "what interests you" list are written
    per ad group, the awning page lists awnings first;
  * the four questions of the questions section are written per ad group (glass, deck, awning) from reading up on each solution; the
    sources are listed in README-PERGOLA-V2.md; the projects grid shows real projects of the ad group's solution (landing-projects-v2.js is
    derived from landing-projects.js); the deck before/after slider and deck story are hidden on the glass and awning pages;
  * leads and WhatsApp messages say which ad group's page they came from (text, lead "solution" label, GA4 form name);
  * a short form (name + phone) inside the first screen, next to WhatsApp and call buttons, and the Google rating;
  * a proof block right after the first screen (three short points + customer reviews);
  * the product gallery comes before the long "before you choose" explanation;
  * one name for the main button.

Run from the repository root after a new export of pergola.html:  python3 tools/make-pergola-v2.py
Every replacement must match exactly once; if the export changed that text the script says so and writes nothing.
"""
import json, os, re, sys
from PIL import Image

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


# --- light hero photo for the deck variant (the original is 336 KB) --------------------------------------------------
DECK_SRC, DECK_OUT = os.path.join(ROOT, 'img/fast/hero/hero-deck-wood.webp'), os.path.join(ROOT, 'img/fast/lp/pg-hero-deck.webp')
if not os.path.exists(DECK_OUT):
    im = Image.open(DECK_SRC).convert('RGB')
    im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS).save(DECK_OUT, 'WEBP', quality=64, method=6)

# --- projects grid per ad group: the photos of real projects from projects-data.js, most relevant first ---------------------------
# landing-projects.js (shared, untouched) shows nine fixed projects and rotates the grid through the rest; the copy gets a derived
# script that takes the list from window.STZ_PICK and does not rotate when it is given, so a deck page shows deck projects.
PICKS = {
    'glass': ['glass-1', 'balcony-electric-pergola-window', 'project-balcony-glass-louver', 'new-49-1', 'roller-screens-balcony', 'light-sunroom-out'],
    'deck': ['project-deck-view', 'project-deck-wood-pergola', 'project-deck-black-frame', 'project-lake-terrace', 'project-sukkah-suite-pvc', 'new-55-1'],
    'awning': ['awning-jaffa-1', 'awning-leumi', 'designer-wave-awning', 'new-56-1', 'new-61-1', 'new-47-1'],
}
PICKS['closure'] = PICKS['glass']
PROJ_SUB = {'glass': 'סגירות זכוכית, חדרי שמש ופתרונות למרפסת מפרויקטים שבוצעו.', 'deck': 'דקים, פרגולות ומרחבי חוץ מפרויקטים שבוצעו.',
            'awning': 'סוככים, מפרשי צל ופתרונות הצללה מפרויקטים שבוצעו.'}
PROJ_SUB['closure'] = PROJ_SUB['glass']
_pdata = open(os.path.join(ROOT, 'projects-data.js'), encoding='utf-8').read()
for _k, _keys in PICKS.items():
    for _key in _keys:
        if "'" + _key + ".webp'" not in _pdata:   # photo paths are written as A + 'name.webp' / P + 'name.webp'
            problems.append(f'"projects picks": {_key} is not in projects-data.js')

# --- head: not indexed, tab title, the preloaded hero photo follows the variant ------------------------------------------
rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 'noindex')
rep('<title>פתרונות הצללה מתקדמים בהתאמה אישית | סופר צל</title>', '<title>פרגולות והצללה בהתאמה אישית | סופר צל</title>', 'title')
PRELOAD = ("<script>(function(){try{var m=/[?&]s=(\\w+)/.exec(location.search),k=m&&m[1],"
           "P={glass:'/img/fast/lp/pg-hero.webp',closure:'/img/fast/lp/pg-hero.webp',deck:'/img/fast/lp/pg-hero-deck.webp',awning:'/img/fast/gallery/new-61-1.webp'},"
           "T={glass:'סגירות זכוכית למרפסת בהתאמה אישית | סופר צל',closure:'סגירות זכוכית למרפסת בהתאמה אישית | סופר צל',"
           "deck:'דקים וריצוף חוץ בהתאמה אישית | סופר צל',awning:'סוככים וגגונים בהתאמה אישית | סופר צל'},"
           "l=document.createElement('link');l.rel='preload';l.as='image';l.href=P[k]||'/img/fast/w/pg2-black-louver.webp';"
           "l.setAttribute('fetchpriority','high');document.head.appendChild(l);if(T[k])document.title=T[k];"
           "var K=json_picks[k];if(K){window.STZ_PICK=K;window.STZ_PROJ_SUB=json_sub[k];}"
           "document.documentElement.setAttribute('data-stz-v',k==='closure'?'glass':(P[k]?k:'pergola'));}catch(e){}})();</script>"
           ).replace('json_picks', json.dumps(PICKS, ensure_ascii=False, separators=(',', ':'))).replace('json_sub', json.dumps(PROJ_SUB, ensure_ascii=False, separators=(',', ':')))
rep('<link rel="preload" as="image" href="/img/fast/lp/pg-hero.webp" fetchpriority="high">', PRELOAD, 'hero preload')

V2_CSS = """
/* pergola-v2: campaign hero (static headline, short form), proof block */
.stz-hero h1.stz-h1v { font-size: clamp(34px,4.6vw,46px); }
.stz-hero h1.stz-h1v > span { min-height: 0 !important; }
.stz-hform { flex: 1 1 100%; min-width: 0; background: rgba(27,23,18,0.8); border: 1px solid rgba(245,240,228,0.28); border-radius: 22px; padding: 14px; }
.stz-hform input { width: 100%; box-sizing: border-box; padding: 12px 14px; border: 1px solid rgba(245,240,228,0.32); background: rgba(245,240,228,0.09); border-radius: 14px; color: #F5F0E4; font: inherit; font-size: 16px; }
.stz-hform input::placeholder { color: rgba(245,240,228,0.62); }
.stz-hform input:focus { outline: none; border-color: #C99752; background: rgba(245,240,228,0.14); }
.stz-hform button { width: 100%; background: #B4813C; color: #1B1712; border: 0; padding: 14px; font: inherit; font-size: 17px; font-weight: 600; border-radius: 100px; cursor: pointer; }
.stz-hform button:hover { background: #C99752; }
.stz-hform small { display: block; font-size: 11.5px; line-height: 1.45; color: rgba(245,240,228,0.68); text-align: center; }
.stz-hphone { display: flex; flex-wrap: wrap; gap: 8px; }
.stz-hphone > select { flex: 0 0 116px !important; width: 116px !important; padding: 12px 8px !important; font-size: 14px !important; }
.stz-hphone > input { flex: 1 1 0 !important; min-width: 0 !important; width: auto !important; }
.stz-hphone > div[role="alert"] { flex: 1 1 100%; }
.stz-hrow > a { flex: 1 1 calc(50% - 5px) !important; box-sizing: border-box; padding: 13px 12px !important; font-size: 15px !important; white-space: normal !important; }
.stz-hchecks { list-style: none; margin: 0; padding: 0; display: grid; gap: 3px; font-size: 13.5px; color: rgba(245,240,228,0.82); }
.stz-hrate { display: inline-flex; align-items: center; gap: 6px; color: #F5F0E4; font-size: 14px; font-weight: 600; text-decoration: none; }
.stz-hrate b { color: #E8C48C; font-weight: 600; }
.stz-hrate-slot { min-height: 22px; }
.stz-proof-revs figure { margin: 0; background: #F5F0E4; border: 1px solid rgba(33,28,22,0.12); border-radius: 20px; padding: 18px; }
@media (max-width: 760px) {
  .stz-hero h1.stz-h1v { font-size: 31px !important; }
  .stz-hero h1.stz-h1v > span { font-size: 31px !important; margin-top: 0 !important; }
  .stz-hero p.stz-hsub { font-size: 15.5px !important; }
  .stz-hero-cap { min-height: 0 !important; }
  .stz-hero .stz-hero-body { padding-top: 78px !important; }
  .stz-proof-revs { display: flex !important; overflow-x: auto; scroll-snap-type: x mandatory; gap: 12px; padding-bottom: 6px; scrollbar-width: none; }
  .stz-proof-revs::-webkit-scrollbar { display: none; }
  .stz-proof-revs > figure { flex: 0 0 84%; scroll-snap-align: start; }
}
@media (max-width: 760px) and (max-height: 720px) { .stz-hchecks { display: none; } }
/* the deck before/after slider and the deck work story (ba-story.js) are about decks: glass and awning pages do not show them */
html[data-stz-v="glass"] .stz-ba-wrap, html[data-stz-v="glass"] .stz-proc-box, html[data-stz-v="awning"] .stz-ba-wrap, html[data-stz-v="awning"] .stz-proc-box { display: none !important; }
"""
rep('<script src="/edit-index.js" defer></script>\n</head>', '<style id="stz-v2">' + V2_CSS + '</style>\n<script src="/edit-index.js" defer></script>\n</head>', 'v2 css')

# --- projects script derived from the shared one (the shared file is read, never written) ---------------------------------------------
LP_SRC, LP_DST = os.path.join(ROOT, 'landing-projects.js'), os.path.join(ROOT, 'landing-projects-v2.js')
lp = open(LP_SRC, encoding='utf-8').read()


def lprep(old, new, label):
    global lp
    if lp.count(old) != 1:
        problems.append(f'"landing-projects.js / {label}": expected 1 match, found {lp.count(old)}')
        return
    lp = lp.replace(old, new)


m_pick = re.search(r"var PICK = (\[[^\n]*\]);", lp)
if not m_pick:
    problems.append('"landing-projects.js / PICK list": not found')
else:
    lp = lp.replace(m_pick.group(0), 'var PICK = window.STZ_PICK && window.STZ_PICK.length ? window.STZ_PICK : ' + m_pick.group(1) + ';', 1)
lprep("var pool = list.filter(function (p) { return p.photos && p.photos.length && shown.indexOf(p) < 0; });",
      "var pool = window.STZ_PICK ? [] : list.filter(function (p) { return p.photos && p.photos.length && shown.indexOf(p) < 0; });", 'rotation pool')
lprep(">פרגולות, סגירות והצללה מפרויקטים שבוצעו. לחצו על פרויקט",
      ">' + (window.STZ_PROJ_SUB || 'פרגולות, סגירות והצללה מפרויקטים שבוצעו.') + ' לחצו על פרויקט", 'sub line')
lp = ('// GENERATED by tools/make-pergola-v2.py from landing-projects.js for pergola-v2.html: do not edit. Differences: the project list comes from\n'
      '// window.STZ_PICK when the page sets it, the grid then does not rotate, and the sub line comes from window.STZ_PROJ_SUB.\n') + lp
import hashlib
LP_VER = hashlib.md5(lp.encode('utf-8')).hexdigest()[:8]
t, _n_lp = re.subn(r'<script src="/landing-projects\.js\?v=\d+" defer></script>', '<script src="/landing-projects-v2.js?v=' + LP_VER + '" defer></script>', t)
if _n_lp != 1:
    problems.append(f'"projects script tag": expected 1 match, found {_n_lp}')

# --- hero photos: all lazy (the variant's photo is preloaded in the head); awnings and deck slides get a photo element --
rep('<img src="/img/fast/lp/pg-hero.webp" alt="{{ sl.alt }}" fetchpriority="high" decoding="async"',
    '<img src="/img/fast/lp/pg-hero.webp" alt="{{ sl.alt }}" loading="lazy" decoding="async"', 'closure hero image lazy')
K5 = '<img src="/img/fast/projects/wood-pergola-rustic.webp" alt="{{ sl.alt }}" loading="lazy" decoding="async" style="display:{{ sl.s5 }};width:100%;height:100%;object-fit:cover;object-position:{{ sl.pos }};animation:stz-kb 14s ease-in-out infinite alternate">'
IMG_STYLE = 'width:100%;height:100%;object-fit:cover;object-position:{{ sl.pos }};animation:stz-kb 14s ease-in-out infinite alternate'
rep(K5, K5 + '\n          <img src="/img/fast/gallery/new-61-1.webp" alt="{{ sl.alt }}" loading="lazy" decoding="async" style="display:{{ sl.s6 }};' + IMG_STYLE + '">'
    '\n          <img src="/img/fast/lp/pg-hero-deck.webp" alt="{{ sl.alt }}" loading="lazy" decoding="async" style="display:{{ sl.s7 }};' + IMG_STYLE + '">', 'awning and deck slide images')
rep("s5: sl.k === 5 ? 'block' : 'none',", "s5: sl.k === 5 ? 'block' : 'none', s6: sl.k === 6 ? 'block' : 'none', s7: sl.k === 7 ? 'block' : 'none',", 'slide flags')

# --- hero text: static headline per variant, short form, rating, check lines -----------------------------------------------
rep('<h1 style="font-size: clamp(34px,4.8vw,47px); line-height: 1.06; font-weight: 600; color: #F5F0E4; letter-spacing: -0.03em; text-shadow: 0 2px 30px rgba(14,11,8,0.45)">פתרונות הצללה וחוץ,<br><span style="display:block;min-height:1.1em;font-weight:300;color:rgb(201, 151, 82);">{{ heroWordEl }}</span></h1>',
    '<h1 class="stz-h1v" style="font-size: clamp(34px,4.8vw,47px); line-height: 1.06; font-weight: 600; color: #F5F0E4; letter-spacing: -0.03em; text-shadow: 0 2px 30px rgba(14,11,8,0.45)">{{ heroH1a }}<span style="display:block;min-height:0;font-weight:300;color:rgb(201, 151, 82);">{{ heroH1b }}</span></h1>', 'hero headline')
rep('<p style="color:rgba(245,240,228,0.86);font-size:clamp(16px,1.5vw,17.5px);max-width:46ch">מפרגולה אחת ועד פרויקט חוץ שלם — תחת מעטפת אחת.</p>',
    '<p class="stz-hsub" style="color:rgba(245,240,228,0.86);font-size:clamp(16px,1.5vw,17.5px);max-width:46ch">{{ heroSub }}</p>', 'hero sub line')
HERO_FORM = '''<div class="stz-hrow" style="display:flex;gap:10px;flex-wrap:wrap">
          <div class="stz-hform">
            <sc-if value="{{ quickSent }}" hint-placeholder-val="{{ false }}">
              <div role="status" style="display:grid;gap:6px;padding:6px 4px">
                <strong style="font-size:19px;color:#F5F0E4">תודה, קיבלנו</strong>
                <span style="font-size:15px;color:rgba(245,240,228,0.84)">נחזור אליכם לתיאום שיחת ייעוץ קצרה.</span>
              </div>
            </sc-if>
            <sc-if value="{{ quickOpen }}" hint-placeholder-val="{{ true }}">
              <div style="display:grid;gap:8px">
                <input type="text" aria-label="שם מלא" placeholder="שם מלא" autocomplete="name" value="{{ fName }}" onChange="{{ onName }}">
                <div class="stz-hphone"><input type="tel" aria-label="טלפון" placeholder="טלפון" autocomplete="tel" inputmode="tel" value="{{ fPhone }}" onChange="{{ onPhone }}"></div>
                <sc-if value="{{ pgErr }}" hint-placeholder-val="{{ false }}"><span role="alert" style="display:block;font-size:13.5px;color:#E8C48C;text-align:center">נא למלא שם ומספר טלפון תקין</span></sc-if>
                <button type="button" onClick="{{ onQuickSubmit }}">תאמו שיחת ייעוץ</button>
                <small>השארת פרטים מהווה הסכמה ליצירת קשר לצורך טיפול בפנייה זו בלבד. <a href="/legal#privacy" style="color:#E8C48C;text-decoration:underline">מדיניות פרטיות</a></small>
              </div>
            </sc-if>
          </div>'''
rep('<div style="display:flex;gap:12px;flex-wrap:wrap">\n          <button onClick="{{ openModal }}" style="flex:{{ procBtnFlex }};background:#B4813C;color:#1B1712;border:0;padding:17px 40px;font-size:17px;font-weight:600;border-radius:100px;cursor:pointer;white-space:nowrap" style-hover="background:#C99752">תאמו שיחת ייעוץ</button>',
    HERO_FORM, 'hero form')
HERO_TAIL = '''וואטסאפ</a>
          <a href="tel:0553100154" aria-label="חיוג עכשיו לסופר צל" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;color:#F5F0E4;border:1px solid rgba(245,240,228,0.55);border-radius:100px;background:rgba(27,23,18,0.25);font-weight:500" style-hover="background:rgba(245,240,228,0.1)">חיוג עכשיו</a>
        </div>
        <div style="display:grid;gap:8px">
          <div class="stz-hrate-slot"><sc-if value="{{ hasRating }}" hint-placeholder-val="{{ false }}"><a class="stz-hrate" href="{{ reviewsHref }}" target="_blank" rel="noopener" aria-label="{{ ratingLabel }}"><b aria-hidden="true">★</b><span>{{ ratingText }} · {{ ratingCountText }}</span></a></sc-if></div>
          <ul class="stz-hchecks"><sc-for list="{{ heroChecks }}" as="c" hint-placeholder-count="3"><li>✓ {{ c.t }}</li></sc-for></ul>
        </div>'''
rep('שיחת וואטסאפ מהירה</a>\n        </div>\n        <p style="margin-top:-2px;font-size:13px;color:rgba(245,240,228,0.65)">✓ שיחת ייעוץ ומדידה ללא התחייבות · מרכז, שפלה ודרום</p>',
    HERO_TAIL, 'hero actions, rating and checks')

# --- scrolling band per variant, proof block, product gallery before the long explanation ----------------------------------
i_band = t.find('  <div style="background:#211C16;color:#F5F0E4;padding:16px 0;overflow:hidden;white-space:nowrap">')
i_real = t.find('  <section id="reality"')
i_real_end = t.find('</section>', i_real) + len('</section>')
i_env = t.find('  <section id="envelope"')
ok = min(i_band, i_real, i_real_end, i_env) >= 0 and i_band < i_real < i_real_end < i_env
if ok:
    band_old, reality = t[i_band:i_real], t[i_real:i_real_end]
    ok = band_old.count('<section') == 0 and reality.count('<section') == 1 and band_old.strip().endswith('</div>') and t.count('  <section id="reality"') == 1
if not ok:
    problems.append('"band / reality / envelope": the structure around the scrolling band changed')
else:
    ITEM = '<span style="display:inline-flex;align-items:center;gap:34px"><span>{{ m.t }}</span><span style="color:#C99752">•</span></span>'
    BAND = f'''  <div style="background:#211C16;color:#F5F0E4;padding:16px 0;overflow:hidden;white-space:nowrap">
    <div style="display:inline-flex;animation:stz-marquee 34s linear infinite">
      <span style="display:inline-flex;align-items:center;gap:34px;padding:0 17px;font-size:20px;font-weight:500">
        <sc-for list="{{{{ marqueeItems }}}}" as="m" hint-placeholder-count="5">{ITEM}</sc-for>
      </span>
      <span style="display:inline-flex;align-items:center;gap:34px;padding:0 17px;font-size:20px;font-weight:500" aria-hidden="true">
        <sc-for list="{{{{ marqueeItems }}}}" as="m" hint-placeholder-count="5">{ITEM}</sc-for>
      </span>
    </div>
  </div>

'''
    PROOF = '''  <section id="proof" style="position:relative;background:#ECE4D2;color:#211C16;border-block:1px solid rgba(33,28,22,0.1);padding-block:clamp(2.5rem,7vh,4.5rem)">
    <div style="width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto;display:grid;gap:clamp(1.5rem,4vw,2.5rem)">
      <div>
        <div style="display:inline-flex;align-items:center;gap:10px;color:#80561E;font-size:14.5px;font-weight:600;margin-bottom:14px;white-space:nowrap"><span style="display:block;width:24px;height:1px;background:#B4813C"></span>בקצרה</div>
        <h2 style="font-size:clamp(28px,3.6vw,44px);line-height:1.12;letter-spacing:-0.02em;color:#211C16;text-wrap:balance">{{ proofH }} <span style="font-weight:300;color:#80561E">— מהמדידה ועד ההתקנה</span></h2>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:clamp(0.75rem,2vw,1.5rem)">
        <sc-for list="{{ proofTiles }}" as="p" hint-placeholder-count="3">
          <div style="border-top:1px solid rgba(33,28,22,0.18);padding-top:14px;display:flex;gap:14px;align-items:baseline">
            <span style="font-size:13px;letter-spacing:0.12em;color:#80561E;flex:none">{{ p.n }}</span>
            <p style="font-size:16.5px;line-height:1.5;color:#211C16"><b>{{ p.t }}</b> {{ p.d }}</p>
          </div>
        </sc-for>
      </div>
      <div class="stz-proof-revs" tabindex="0" role="region" aria-label="ביקורות לקוחות" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px">
        <sc-for list="{{ proofReviews }}" as="r" hint-placeholder-count="3">
          <figure>
            <p style="font-size:16px;line-height:1.55;color:#211C16">{{ r.text }}</p>
            <figcaption style="margin-top:10px;font-size:14px;color:#6E4D1E">{{ r.who }} · ביקורת בגוגל</figcaption>
          </figure>
        </sc-for>
      </div>
    </div>
  </section>

'''
    t = t[:i_band] + BAND + PROOF + t[i_real_end:]
    j = t.find('  <section id="envelope"')
    # the "before you choose a shading solution" block and the sun simulator only make sense on the pergola page
    t = t[:j] + '  <sc-if value="{{ showSim }}" hint-placeholder-val="{{ true }}">\n' + reality + '\n  </sc-if>\n\n' + t[j:]

# --- ad-group variants: every piece of copy that depends on what the visitor searched for lives in this table ----------------------
# The pergola entry is the live page's own wording, read from pergola.html (so it cannot drift); the other entries are written in the same
# register. The product facts in the FAQ answers were read up on and are listed with their sources in README-PERGOLA-V2.md; whatever could
# not be backed by a source was left out.

# the four questions of the questions section as pergola.html words them (static markup)
i_el = t.find('<section id="elephant"')
i_el_end = t.find('</section>', i_el)
el_html = t[i_el:i_el_end] if i_el >= 0 and i_el_end > i_el else ''
LIVE_Q = re.findall(r'font-weight:600;line-height:1.3">"([^"<]+)"</span>', el_html)
LIVE_A = re.findall(r'max-width:58ch">([^<]+)</p>', el_html)
if len(LIVE_Q) != 4 or len(LIVE_A) != 4:
    problems.append('"questions section": expected 4 questions and 4 answers')
    LIVE_Q, LIVE_A = [''] * 4, [''] * 4
LIVE_FAQ = [[q, a] for q, a in zip(LIVE_Q, LIVE_A)]
ASK = ' בואו נשב יחד על כוס קפה (או בטלפון), נבין את הצרכים והסגנון שלכם, ונציע פתרון שמתאים לכם.'
CHECK1, AREA = 'מדידה בשטח וייעוץ ללא התחייבות', 'מרכז, שפלה ודרום'
MORE_OPTS = ['מעטפת חוץ רחבה יותר', 'עדיין בודקים אפשרויות']

# None = the live page's own question and answer at that position (installation, permit)
RESEARCHED_FAQ = {
    'glass': [
        ['איזו זכוכית ואיזו מערכת מתאימות לסגירת מרפסת?',
         'בסגירות למרפסת משתמשים בדרך כלל במערכות הזזה בפרופיל אלומיניום, עם זכוכית שכבתית (טריפלקס) או מחוסמת, ולעיתים בזכוכית בידודית. '
         'יש גם מערכות מתקפלות. סוג הזכוכית, העובי ופרופיל האלומיניום משפיעים על המראה ועל הבידוד, ונבחרים לפי גודל הפתח, '
         'כיוון החשיפה ואופן השימוש. את ההתאמה בודקים בשטח, בשיחת הייעוץ.'],
        ['איך סגירת זכוכית מתמודדת עם גשם ורוח?',
         'הסגירה מפחיתה את החשיפה לרוח ולגשם, אבל איננו מתחייבים לחסימה מלאה. במערכות הזזה יש בדרך כלל אטמים (מברשות) '
         'ומסילה תחתונה עם שיפוע לניקוז, שמפחיתים חדירת מים, אבק ורוח — ובכל זאת בגשם חזק או ברוח אלכסונית עלולים להיכנס מעט מים. '
         'סוג המסילה והפרופיל משפיעים על כך, ולכן כדאי לשאול על המערכת הספציפית ולא להסתמך על הבטחה כללית.'],
        None,
        ['האם סגירת מרפסת דורשת היתר או הסכמת שכנים?',
         'סגירה קבועה של מרפסת עשויה להיחשב תוספת בנייה הדורשת היתר, והתשובה משתנה לפי הרשות המקומית ומאפייני המרפסת. '
         'בבית משותף ייתכן שגם תקנון הבית דורש הסכמה לשינוי בחזית. אנחנו לא מפזרים הבטחות ריקות ש"יהיה בסדר" — '
         'נבדוק יחד איתכם את הנתונים בשטח, ואת נושא האישורים נתאם מול בעלי מקצוע מוסמכים.'],
    ],
    'deck': [
        ['דק עץ או דק קומפוזיט — מה ההבדל?',
         'דק עץ טבעי נותן מראה ותחושה של עץ אמיתי, אבל הוא חומר חי: הוא סופג מים, עלול להתנפח ולהשתנות עם הזמן, '
         'ודורש תחזוקה תקופתית — שימון או צביעה, לפי סוג העץ והחשיפה לשמש. דק קומפוזיט (עץ מלאכותי) סופג פחות מים, '
         'לרוב אינו נרקב ודורש תחזוקה מועטה, אבל המרקם שלו שונה מעץ אמיתי, ושריטה או נזק לא תמיד אפשר לתקן — לפעמים מחליפים את הלוח. '
         'הבחירה נעשית לפי המראה שאתם רוצים ולפי התחזוקה שנוח לכם לבצע.'],
        ['האם דק מתחמם בשמש, והאם הוא חלק כשהוא רטוב?',
         'דק בגוון כהה מתחמם יותר בשמש ישירה — בקומפוזיט וגם בעץ כהה. גוונים בהירים מתחממים פחות, וצל, למשל מעל פרגולה, עוזר. '
         'לגבי החלקה: גם עץ וגם קומפוזיט עלולים להיות חלקים כשהם רטובים, וההבדל תלוי במוצר ובמרקם שלו '
         '(למשל לוחות עם חריצים או מרקם), ולכן כדאי לבדוק את נתוני ההחלקה של הדגם שנבחר.'],
        ['מה חשוב בהתקנה של דק?',
         'הדק יושב על שלד (תשתית) שצריך להיות מפולס, יציב ומחובר היטב למשטח. בין הלוחות משאירים מרווחים, ובקומפוזיט גם מרווח '
         'מקירות ומרכיבים קבועים, לפי הנחיות יצרן הלוחות, כי החומר מתרחב ומתכווץ עם החום. חשוב גם לאפשר אוורור וניקוז מתחת לדק, '
         'כדי שמים לא יישארו לכודים: ריקבון בדק עץ נובע לרוב מהתקנה לקויה, למשל קורות שלא טופלו כראוי או מרווח קטן מדי מעל הקרקע. '
         'את הפרטים קובעים לפי השטח והחומר שנבחר.'],
        None,
    ],
    'awning': [
        ['סוכך זרועות חשמלי או ידני — מה כדאי?',
         'סוכך חשמלי הוא סוכך רגיל שמצויד במנוע שפותח וסוגר אותו, למשל בשלט, ובסוכך ידני אין מנוע. אפשר להוסיף גם חיישן רוח שמקפל '
         'את הסוכך אוטומטית — מתקינים רבים ממליצים עליו — אבל הוא תוספת נוחות ואינו תחליף לקיפול הסוכך כשהרוח חזקה.'],
        ['מה קורה לסוכך ברוח ובגשם?',
         'סוכך זרועות נועד להצללה מהשמש ואינו גג. יצרנים ממליצים לקפל אותו כשהרוח מתחזקת ולא להשאיר אותו פתוח בסערה. '
         'בגשם ההתנהגות תלויה בדגם ובשיפוע: בשיפוע מספיק המים יורדים, ובסוכך שטוח עלולות להיווצר שלוליות על הבד. '
         'חיישני רוח וגשם יכולים לקפל את הסוכך אוטומטית, אבל הם תוספת נוחות ולא הבטחה. לכן בוחרים דגם, שיפוע וחיישנים לפי המיקום והחשיפה, '
         'ובודקים בהוראות היצרן מה הדגם מסוגל לשאת.'],
        ['מאיזה בד הסוכך עשוי, ואיך מתחזקים אותו?',
         'בסוככי זרועות נפוצים בדי אקריליק, ולפי יצרנים יש להם ציפויים שמתמודדים עם דהייה והתעפשות. עם השנים בד סוכך עלול לדהות או להישחק '
         'בחשיפה לשמש. כדי למנוע עובש מומלץ לנקות את הבד מדי פעם, בלי שטיפה בלחץ גבוה, ולוודא שהוא יבש לפני שמקפלים את הסוכך לתקופה ארוכה. '
         'סוג הבד והגוון נבחרים לפי המראה והחשיפה.'],
        None,
    ],
}


VARIANTS = {
    'pergola': dict(
        key='pergola', label='פרגולות והצללה', cap='סופר צל · פרגולות והצללה', h1a='פרגולות אלומיניום', h1b='בהתאמה אישית.',
        sub='תכנון יישומי, ייצור והתקנה — עם נקודת קשר אחת מהמדידה ועד המסירה.',
        checks=[CHECK1, 'פרגולות אלומיניום, תריס חשמלי ועץ', AREA],
        slides=[2, 4, 0, 3, 5], tab='shade',
        marquee=['פרגולות אלומיניום', 'פרגולות תריס חשמליות', 'פרגולות עץ', 'סוככים וגגונים', 'רשתות צל מעוצבות'],
        proofH='פרגולה שמתאימה לבית שלכם', proofD1='מבינים את כיוון השמש, המידות וצורת השימוש לפני שמתחילים.',
        sim=True, step1='מדידה, כיווני שמש וצורת השימוש.', reason1=None, deckNote=None,
        waShort='היי, הגעתי מדף הפרגולות באתר ואשמח לייעוץ קצר לגבי פרגולה והצללה למרחב החוץ שלנו.',
        waLong='היי, הגעתי מדף הפרגולות באתר ואשמח לשיחת ייעוץ והתאמה של פתרון הצללה.',
        faqH='4 שאלות שחובה לשאול לפני שבוחרים פתרון הצללה',
        contactH='נדבר על ההצללה שלכם', contactP='חושבים על פתרון הצללה לגינה או למרפסת?' + ASK),
    'glass': dict(
        key='glass', label='סגירות זכוכית', cap='סופר צל · סגירות זכוכית', h1a='סגירות זכוכית', h1b='למרפסת.',
        sub='מערכות זכוכית והזזה בהתאמה אישית — תכנון יישומי ונקודת קשר אחת מהמדידה ועד ההתקנה.',
        checks=[CHECK1, 'מערכות חלונות הזזה בהתאמה למרפסת', AREA],
        slides=[1], tab='glass', marquee=['סגירות זכוכית', 'מערכות חלונות הזזה', 'סגירת מרפסת', 'קירוי למרפסת'],
        proofH='סגירה שמתאימה למרפסת שלכם', proofD1='מבינים את מידות המרפסת וצורת השימוש לפני שמתחילים.',
        sim=False, step1='מדידה, מידות המרפסת וצורת השימוש.', reason1=None, deckNote=None,
        waShort='היי, הגעתי מדף סגירות הזכוכית באתר ואשמח לייעוץ קצר לגבי סגירת זכוכית למרפסת שלנו.',
        waLong='היי, הגעתי מדף סגירות הזכוכית באתר ואשמח לשיחת ייעוץ והתאמה של סגירת זכוכית למרפסת.',
        faqH='4 שאלות שחובה לשאול לפני שבוחרים סגירת זכוכית',
        contactH='נדבר על סגירת הזכוכית שלכם', contactP='חושבים על סגירת זכוכית למרפסת?' + ASK),
    'deck': dict(
        key='deck', label='דקים וריצוף חוץ', cap='סופר צל · דקים וריצוף חוץ', h1a='דקים וריצוף חוץ', h1b='בהתאמה אישית.',
        sub='דקים מעץ, מעץ מלאכותי ומחומרים מתקדמים — תכנון יישומי ונקודת קשר אחת מהמדידה ועד ההתקנה.',
        checks=[CHECK1, 'דקים, ריצוף וחיפוי חוץ', AREA],
        slides=[7], tab='deck', marquee=['דקים', 'ריצוף וחיפוי חוץ', 'פרגולות', 'גדרות ותיחום'],
        proofH='דק שמתאים למרחב החוץ שלכם', proofD1='מבינים את המידות, המשטח וצורת השימוש לפני שמתחילים.',
        sim=False, step1='מדידה, מצב המשטח וצורת השימוש.',
        reason1=dict(title='חומרים, מחברים וגמר', body='סוג החומר, איכות המחברים והגמר — רשומים במפרט בכתב, רכיב אחרי רכיב, כדי שתוכלו להשוות.'),
        deckNote='דק, ריצוף וחיפוי בהתאמה לשפה החומרית של הבית.',
        envDeck='דק עץ טבעי או קומפוזיט, ריצוף אבן ופורצלן לחוץ וחיפויי קיר — בהתאמה לשפה החומרית של הבית.',
        waShort='היי, הגעתי מדף הדקים באתר ואשמח לייעוץ קצר לגבי דק וריצוף למרחב החוץ שלנו.',
        waLong='היי, הגעתי מדף הדקים באתר ואשמח לשיחת ייעוץ והתאמה של דק וריצוף חוץ.',
        faqH='4 שאלות שחובה לשאול לפני שבוחרים דק',
        contactH='נדבר על הדק שלכם', contactP='חושבים על דק או ריצוף למרפסת או לגינה?' + ASK),
    'awning': dict(
        key='awning', label='סוככים והצללה', cap='סופר צל · סוככים והצללה', h1a='סוככים וגגונים', h1b='בהתאמה אישית.',
        sub='סוככי זרועות חשמליים, סוככים קבועים ורשתות צל — תכנון יישומי ומדידה בשטח.',
        checks=[CHECK1, 'סוככי זרועות חשמליים וסוככים קבועים', AREA],
        slides=[6], tab='shade', marquee=['סוככי זרועות חשמליים', 'סוככים קבועים', 'רשתות ומפרשי צל', 'פרגולות'],
        proofH='סוכך שמתאים לחזית שלכם', proofD1='מבינים את כיוון השמש, המידות וצורת השימוש לפני שמתחילים.',
        sim=False, step1='מדידה, כיווני שמש וצורת השימוש.', reason1=None, deckNote=None,
        waShort='היי, הגעתי מדף הסוככים באתר ואשמח לייעוץ קצר לגבי סוכך או גגון למרחב החוץ שלנו.',
        waLong='היי, הגעתי מדף הסוככים באתר ואשמח לשיחת ייעוץ והתאמה של סוכך או גגון.',
        faqH='4 שאלות שחובה לשאול לפני שבוחרים סוכך',
        contactH='נדבר על ההצללה שלכם', contactP='חושבים על סוכך או גגון לגינה, למרפסת או לחזית?' + ASK),
}
for _k, _v in VARIANTS.items():
    _spec = RESEARCHED_FAQ.get(_k)
    _v['faq'] = [list(LIVE_FAQ[i]) if (_spec is None or _spec[i] is None) else list(_spec[i]) for i in range(4)]
# "what interests you" list of the long contact form; the values are the Hebrew labels, so a lead reads "דק עץ" and not a code
OPTS = {
    'pergola': ['פרגולת אלומיניום', 'פרגולת תריס חשמלית', 'פרגולת עץ', 'סוכך, גגון או רשת צל'] + MORE_OPTS,
    'glass': ['סגירת זכוכית למרפסת', 'מערכת חלונות הזזה', 'קירוי למרפסת'] + MORE_OPTS,
    'deck': ['דק עץ', 'דק קומפוזיט (עץ מלאכותי)', 'ריצוף וחיפוי חוץ'] + MORE_OPTS,
    'awning': ['סוכך זרועות חשמלי', 'סוכך קבוע או גגון', 'רשת או מפרש צל', 'פרגולה'] + MORE_OPTS,
}
P = VARIANTS['pergola']

# --- script: variants, slides per variant, rating, gallery tab, chapter list, new bindings ----------------------------------
CONSTS = ('// pergola-v2: one landing experience per ad group, chosen by ?s= (default: pergolas); the copy of every variant is in this table\n'
          'const STZ_VARIANTS = ' + json.dumps(VARIANTS, ensure_ascii=False, separators=(',', ':')) + ';\n') + r'''STZ_VARIANTS.closure = STZ_VARIANTS.glass;
function stzVariant() {
  let k = '';
  try { k = (location.search.match(/[?&]s=(\w+)/) || [])[1] || ''; } catch (e) {}
  return STZ_VARIANTS[k] || STZ_VARIANTS.pergola;
}
// deck page: the gallery note about "the base the pergola sits on" says what the deck tab is
function stzGalNote(n) { const V = stzVariant(); return V.deckNote && /הבסיס שעליו יושבת הפרגולה/.test(n) ? V.deckNote : n; }
// awning page: awnings first in the shade gallery (same six-column grid, card numbers follow the new order)
function stzAwningOrder(types, narrow) {
  if (stzVariant().key !== 'awning') return;
  const by = {}; types.forEach(x => { by[x.num] = x; });
  if (['01', '02', '03', '04', '05', '06', '07'].some(k => !by[k])) return;
  const big = x => narrow ? x : Object.assign(x, { span: 'span 3', minH: '340px', titleSize: '27px' });
  const small = x => narrow ? x : Object.assign(x, { span: 'span 2', minH: '280px', titleSize: '22px' });
  const order = [big(by['05']), big(by['06']), small(by['01']), small(by['02']), small(by['07']), big(by['03']), big(by['04'])];
  order.forEach((x, i) => { x.num = String(i + 1).padStart(2, '0'); });
  types.splice(0, types.length, ...order);
}
// leads say which ad group's page they came from (solution label, floating-form text, GA4 form name); lead.js / lead-modal.js stay untouched.
// The page runs its body scripts a second time after it has rendered (lead.js assigns window.stzSendLead again), so the wrapper is kept
// in a property that wraps whatever function is assigned to it.
function stzLeadLabels() {
  const V = stzVariant();
  if (V.key === 'pergola') return;
  const wrap = orig => {
    if (typeof orig !== 'function' || orig.__stzV2) return orig;
    const w = function (p) {
      try {
        p = Object.assign({}, p);
        if (p.solution === 'פרגולות והצללה') p.solution = V.label;
        if (typeof p.message === 'string') p.message = p.message.replace('פנייה מהטופס הצף · פרגולות והצללה', 'פנייה מהטופס הצף · ' + V.label);
        if (typeof p.source === 'string') p.source = /^pergola_(quick|long)$/.test(p.source) ? p.source + '_' + V.key : p.source.replace('פרגולות והצללה', V.label);
      } catch (e) {}
      return orig.call(this, p);
    };
    w.__stzV2 = true;
    return w;
  };
  let cur = wrap(window.stzSendLead);
  try { Object.defineProperty(window, 'stzSendLead', { configurable: true, get: () => cur, set: fn => { cur = wrap(fn); } }); }
  catch (e) { window.stzSendLead = cur; }
}
'''
rep('class Component extends DCLogic {\n  revsFallback = [', CONSTS + 'class Component extends DCLogic {\n  revsFallback = [', 'variant table')

SLIDES = r'''    // pergola-v2: the deck slide, then only the slides of this ad group's variant, in its order
    if (sv === 'deck') S.unshift({ k: 7, word: 'דקים וריצוף חוץ.', caption: 'פיתוח חוץ בעץ', src: '/img/fast/lp/pg-hero-deck.webp', pos: '50% 50%', alt: 'דק עץ בגינה עם פרגולת תריס, חיפוי עץ וגדר', pins: [] });
    const ordered = stzVariant().slides.map(k => S.find(s => s.k === k)).filter(Boolean);
    if (ordered.length) S.splice(0, S.length, ...ordered);
    S.forEach(s => { s.pins = []; });
    const ov = (this.state && this.state.pinOv) || {};
    return S.map((s, i) => ov[i] ? Object.assign({}, s, { pins: ov[i] }) : s);'''
rep("    const ov = (this.state && this.state.pinOv) || {};\n    return S.map((s, i) => ov[i] ? Object.assign({}, s, { pins: ov[i] }) : s);", SLIDES, 'slides per variant')

rep("        if (typeof d.googleMapsUri === 'string' && d.googleMapsUri) this.setState({ reviewsUrl: d.googleMapsUri });",
    "        if (typeof d.googleMapsUri === 'string' && d.googleMapsUri) this.setState({ reviewsUrl: d.googleMapsUri });\n"
    "        if (typeof d.rating === 'number' && d.rating > 0) this.setState({ rating: d.rating, ratingCount: typeof d.userRatingCount === 'number' ? d.userRatingCount : null });",
    'rating from the reviews function')

rep("    try { if (location.hash === '#glass' || new URLSearchParams(location.search).get('s') === 'glass') this.setState({ galTab: 'glass' }); } catch (e) {}",
    "    try { const vt = stzVariant().tab; if (location.hash === '#glass' || vt === 'glass') this.setState({ galTab: 'glass' }); else if (vt === 'deck') this.setState({ galTab: 'deck' }); } catch (e) {}",
    'gallery tab per variant')
rep("        const q = new URLSearchParams(location.search).get('s') || location.hash.slice(1);",
    "        const sq = new URLSearchParams(location.search).get('s'); const q = (sq && !STZ_VARIANTS[sq] ? sq : '') || location.hash.slice(1);",
    'variants do not scroll')

rep("      { id: 'hero', n: '01', label: 'פתיחה' },\n      { id: 'reality', n: '02', label: 'השמש במרחב' },\n      { id: 'catalog', n: '03', label: 'גלריה לפי רכיב' },\n      { id: 'why', n: '04', label: 'למה סופר צל' },\n      { id: 'process', n: '05', label: 'איך זה עובד' },\n      { id: 'envelope', n: '06', label: 'מעבר להצללה' },\n      { id: 'reviews', n: '07', label: 'ביקורות' },\n      { id: 'elephant', n: '08', label: 'שאלות' },\n      { id: 'contact', n: '09', label: 'צור קשר' }",
    "      { id: 'hero', n: '01', label: 'פתיחה' },\n      { id: 'proof', n: '02', label: 'בקצרה' },\n      { id: 'catalog', n: '03', label: 'גלריה לפי רכיב' },\n      { id: 'why', n: '04', label: 'למה סופר צל' },\n      { id: 'process', n: '05', label: 'איך זה עובד' },\n      { id: 'reality', n: '06', label: 'השמש במרחב' },\n      { id: 'envelope', n: '07', label: 'מעבר להצללה' },\n      { id: 'reviews', n: '08', label: 'ביקורות' },\n      { id: 'elephant', n: '09', label: 'שאלות' },\n      { id: 'contact', n: '10', label: 'צור קשר' }",
    'chapter list order')
rep("      { id: 'contact', n: '10', label: 'צור קשר' }\n    ];",
    "      { id: 'contact', n: '10', label: 'צור קשר' }\n    ].filter(c => c.id !== 'reality' || stzVariant().sim).map((c, i) => Object.assign({}, c, { n: String(i + 1).padStart(2, '0') }));",
    'chapters follow the variant')

rep("      heroDots: S.map((sl, si) =>", "      heroDots: S.length < 2 ? [] : S.map((sl, si) =>", 'no dots for a single slide')
rep("      heroCapShow: n ? 'סופר צל · פרגולות והצללה' : S[cs].caption,", "      heroCapShow: n ? stzVariant().cap : S[cs].caption,", 'hero caption per variant')

BINDINGS = r'''      sent: this.state.sent,
      heroH1a: stzVariant().h1a, heroH1b: stzVariant().h1b, heroSub: stzVariant().sub,
      heroChecks: stzVariant().checks.map(c => ({ t: c })),
      marqueeItems: stzVariant().marquee.map(m => ({ t: m })),
      hasRating: typeof this.state.rating === 'number' && this.state.rating > 0,
      ratingText: typeof this.state.rating === 'number' ? this.state.rating.toFixed(1) : '',
      ratingCountText: this.state.ratingCount ? this.state.ratingCount + ' ביקורות בגוגל' : 'דירוג בגוגל',
      ratingLabel: typeof this.state.rating === 'number' ? 'דירוג ' + this.state.rating.toFixed(1) + ' בגוגל' + (this.state.ratingCount ? ', ' + this.state.ratingCount + ' ביקורות' : '') : '',
      proofH: stzVariant().proofH,
      proofTiles: [
        { n: '01', t: 'מדידה בשטח:', d: stzVariant().proofD1 },
        { n: '02', t: 'תכנון יישומי והתאמה אישית:', d: 'מידות, גוון וסגנון בהתאמה לבית ולמרחב החוץ.' },
        { n: '03', t: 'נקודת קשר אחת:', d: 'מהמדידה ועד ההתקנה, אדם אחד שמלווה אתכם בפרויקט.' }
      ],
      proofReviews: this.revs.filter(r => !/מושלמ|הכי /.test(r.text)).slice(0, 3).map(r => ({ text: r.text, who: r.meta })),
      showSim: stzVariant().sim,
      isPergola: stzVariant().key === 'pergola', isGlass: stzVariant().key === 'glass', isDeck: stzVariant().key === 'deck', isAwning: stzVariant().key === 'awning',
      mn: Object.fromEntries(this.chapList().map(c => [c.id, c.n])),
      faqH: stzVariant().faqH,
      faqQ1: stzVariant().faq[0][0], faqA1: stzVariant().faq[0][1], faqQ2: stzVariant().faq[1][0], faqA2: stzVariant().faq[1][1],
      faqQ3: stzVariant().faq[2][0], faqA3: stzVariant().faq[2][1], faqQ4: stzVariant().faq[3][0], faqA4: stzVariant().faq[3][1],
      contactH: stzVariant().contactH, contactP: stzVariant().contactP,'''
rep("      sent: this.state.sent,", BINDINGS, 'new bindings')

# --- WhatsApp messages and lead texts say which ad group's page they came from ---------------------------------------------------
rep("'היי, הגעתי מהאתר ואשמח לייעוץ קצר לגבי פרגולה והצללה למרחב החוץ שלנו.'", "stzVariant().waShort", 'WhatsApp text', count=2)
rep("'היי, הגעתי מהאתר ואשמח לשיחת ייעוץ והתאמה של פתרון הצללה.'", "stzVariant().waLong", 'WhatsApp text (form)')
rep("  componentDidMount() {\n    this.applyLook();", "  componentDidMount() {\n    try { stzLeadLabels(); } catch (e) {}\n    this.applyLook();", 'lead labels per variant')

# --- the rest of the page follows the ad group ----------------------------------------------------------------------------------
rep("body: 'מדידה, כיווני שמש וצורת השימוש.' }", "body: stzVariant().step1 }", 'first process step per variant')
REASON1 = "{ title: 'פרופילים, מחברים וצביעה', body: 'עובי הפרופילים, איכות המחברים ושיטת הצביעה — רשומים במפרט בכתב, רכיב אחרי רכיב, כדי שתוכלו להשוות.' },"
rep(REASON1, "stzVariant().reason1 || " + REASON1, 'first reason per variant')
ENV_DECK = "body: 'דק עץ טבעי או קומפוזיט, ריצוף אבן ופורצלן לחוץ וחיפויי קיר — הבסיס שעליו יושבת הפרגולה.' }"
rep(ENV_DECK, "body: stzVariant().envDeck || 'דק עץ טבעי או קומפוזיט, ריצוף אבן ופורצלן לחוץ וחיפויי קיר — הבסיס שעליו יושבת הפרגולה.' }", 'deck line of the overview')
rep("      galNote: (GAL_TABS.find(t => t.id === (this.state.galTab || 'shade')) || GAL_TABS[0]).note,",
    "      galNote: stzGalNote((GAL_TABS.find(t => t.id === (this.state.galTab || 'shade')) || GAL_TABS[0]).note),", 'gallery note per variant')
rep("    ];\n    const galPick = this.state.galTab || 'shade';", "    ];\n    stzAwningOrder(types, n);\n    const galPick = this.state.galTab || 'shade';", 'awnings first on the awning page')

# questions block (static markup in pergola.html): heading, the four questions and the four answers become bindings; the live text is cut out verbatim
rep('>' + P['faqH'] + '</h2>', '>{{ faqH }}</h2>', 'FAQ heading')
for _i in range(4):
    rep('>"' + LIVE_FAQ[_i][0] + '"</span>', '>"{{ faqQ%d }}"</span>' % (_i + 1), 'FAQ question %d' % (_i + 1))
    rep('>' + LIVE_FAQ[_i][1] + '</p>', '>{{ faqA%d }}</p>' % (_i + 1), 'FAQ answer %d' % (_i + 1))
# contact block: heading, sentence under it, and the "what interests you" list (one list per ad group; the values are the Hebrew labels)
rep('>' + P['contactH'] + '</h2>', '>{{ contactH }}</h2>', 'contact heading')
rep('>' + P['contactP'] + '</p>', '>{{ contactP }}</p>', 'contact sentence')
mark = '<span style="font-size:14px;color:rgba(245,240,228,0.65)">סוג הפתרון שמעניין אתכם</span>'
i_m = t.find(mark)
i_l = t.rfind('<label style="display:grid;gap:8px">', 0, i_m)
i_le = t.find('</label>', i_m) + len('</label>')
sel = t[i_l:i_le] if min(i_m, i_l, i_le) >= 0 and t.count(mark) == 1 else ''
m_sel = re.search(r'(<select [^>]*>)(.*?)(</select>)', sel, re.S)
if not m_sel or sel.count('<select') != 1 or sel.count('<option') != 6:
    problems.append('"contact interest list": the select block changed')
else:
    blocks = []
    for k in ('pergola', 'glass', 'deck', 'awning'):
        opts = '\n'.join(f'              <option value="{o}" style="color:#211C16">{o}</option>' for o in OPTS[k])
        body = sel[:m_sel.start(2)] + '\n' + opts + '\n            ' + sel[m_sel.end(2):]
        blocks.append(f'<sc-if value="{{{{ is{k.capitalize()} }}}}" hint-placeholder-val="{{{{ {str(k == "pergola").lower()} }}}}">{body}</sc-if>')
    t = t[:i_l] + '\n          '.join(blocks) + t[i_le:]

# mobile menu: the sun link follows the chapter order and leaves with its section; the numbers follow the chapter list
i_nav = t.find('<nav style="display:flex;flex-direction:column;margin-top:28px">')
i_nav_end = t.find('</nav>', i_nav)
nav = t[i_nav:i_nav_end] if i_nav >= 0 and i_nav_end > i_nav else ''
NUM = r'<span style="color:#C99752;font-size:13px;letter-spacing:0\.14em">\d\d</span>'


def menu_num(m):
    if m.group(2) == 'glass':      # "סגירות" opens a gallery tab, it is not a chapter
        return m.group(1)
    return m.group(1) + '<span style="color:#C99752;font-size:13px;letter-spacing:0.14em">{{ mn.' + m.group(2) + ' }}</span>'


nav2, n_num = re.subn(r'(<a href="#(\w+)"[^>]*>[^<]*?)' + NUM, menu_num, nav)
m_r = re.search(r'\n *<a href="#reality"[^\n]*</a>', nav2)
m_p = re.search(r'\n *<a href="#process"[^\n]*</a>', nav2)
if not nav or n_num != 9 or not m_r or not m_p or m_r.start() > m_p.start():
    problems.append('"mobile menu": the menu markup changed')
else:
    a_real = m_r.group(0).strip()
    nav2 = nav2.replace(m_r.group(0), '', 1)
    m_p = re.search(r'\n *<a href="#process"[^\n]*</a>', nav2)
    nav2 = nav2[:m_p.end()] + '\n    <sc-if value="{{ showSim }}" hint-placeholder-val="{{ true }}">' + a_real + '</sc-if>' + nav2[m_p.end():]
    t = t[:i_nav] + nav2 + t[i_nav_end:]

# --- one name for the main button: "תאמו שיחת ייעוץ" ------------------------------------------------------------------------
rep('border-radius:100px" style-hover="background:#C99752;color:#1B1712">לתיאום פגישת ייעוץ</a>',
    'border-radius:100px" style-hover="background:#C99752;color:#1B1712">תאמו שיחת ייעוץ</a>', 'inline button label')
rep('aria-label="פתיחת טופס לתיאום פגישת ייעוץ"', 'aria-label="פתיחת טופס: תאמו שיחת ייעוץ"', 'floating button aria-label')
rep('  <span>תיאום פגישת ייעוץ</span>', '  <span>תאמו שיחת ייעוץ</span>', 'floating button label')
rep('<section id="lead" aria-label="תיאום פגישת ייעוץ"', '<section id="lead" aria-label="תאמו שיחת ייעוץ"', 'lead section label')

if problems:
    print('pergola-v2.html NOT written:\n  ' + '\n  '.join(problems))
    sys.exit(1)
open(DST, 'w', encoding='utf-8').write(t)
open(LP_DST, 'w', encoding='utf-8').write(lp)
print('pergola-v2.html written (pergola.html untouched)')
