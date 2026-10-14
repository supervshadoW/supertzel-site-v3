#!/usr/bin/env python3
"""Builds pergola-v2.html: a campaign landing page generated from pergola.html, without touching pergola.html.

pergola.html is only read, never written, so the page the current Google Ads campaign points to stays exactly as it is.
The result is served at pergola.supertzel.co.il/pergola-v2 (not linked from anywhere, noindex).

What the copy changes (see README-PERGOLA-V2.md):
  * one page per ad group, chosen by ?s=  (default = pergolas, ?s=glass, ?s=deck, ?s=awning): headline, sub line, three check lines,
    hero photos, product tab and the scrolling band all match the search;
  * a short form (name + phone) inside the first screen, next to WhatsApp and call buttons, and the Google rating;
  * a proof block right after the first screen (three short points + customer reviews);
  * the product gallery comes before the long "before you choose" explanation;
  * WhatsApp messages say they came from the pergola page, one name for the main button.

Run from the repository root after a new export of pergola.html:  python3 tools/make-pergola-v2.py
Every replacement must match exactly once; if the export changed that text the script says so and writes nothing.
"""
import os, sys
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

# --- head: not indexed, tab title, the preloaded hero photo follows the variant ------------------------------------------
rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 'noindex')
rep('<title>פתרונות הצללה מתקדמים בהתאמה אישית | סופר צל</title>', '<title>פרגולות והצללה בהתאמה אישית | סופר צל</title>', 'title')
PRELOAD = ("<script>(function(){try{var m=/[?&]s=(\\w+)/.exec(location.search),k=m&&m[1],"
           "P={glass:'/img/fast/lp/pg-hero.webp',closure:'/img/fast/lp/pg-hero.webp',deck:'/img/fast/lp/pg-hero-deck.webp',awning:'/img/fast/gallery/new-61-1.webp'},"
           "l=document.createElement('link');l.rel='preload';l.as='image';l.href=P[k]||'/img/fast/w/pg2-black-louver.webp';"
           "l.setAttribute('fetchpriority','high');document.head.appendChild(l);}catch(e){}})();</script>")
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
"""
rep('<script src="/edit-index.js" defer></script>\n</head>', '<style id="stz-v2">' + V2_CSS + '</style>\n<script src="/edit-index.js" defer></script>\n</head>', 'v2 css')

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
    t = t[:j] + reality + '\n\n' + t[j:]

# --- script: variants, slides per variant, rating, gallery tab, chapter list, new bindings ----------------------------------
CONSTS = r'''// pergola-v2: one landing experience per ad group, chosen by ?s= (default: pergolas)
const STZ_VARIANTS = {
  pergola: { cap: 'סופר צל · פרגולות והצללה', h1a: 'פרגולות אלומיניום', h1b: 'בהתאמה אישית.',
    sub: 'תכנון יישומי, ייצור והתקנה — עם נקודת קשר אחת מהמדידה ועד המסירה.',
    checks: ['מדידה בשטח וייעוץ ללא התחייבות', 'פרגולות אלומיניום, תריס חשמלי ועץ', 'מרכז, שפלה ודרום'],
    slides: [2, 4, 0, 3, 5], tab: 'shade', marquee: ['פרגולות אלומיניום', 'פרגולות תריס חשמליות', 'פרגולות עץ', 'סוככים וגגונים', 'רשתות צל מעוצבות'],
    proofH: 'פרגולה שמתאימה לבית שלכם' },
  glass: { cap: 'סופר צל · סגירות זכוכית', h1a: 'סגירות זכוכית', h1b: 'למרפסת.',
    sub: 'מערכות זכוכית והזזה בהתאמה אישית — תכנון יישומי ונקודת קשר אחת מהמדידה ועד ההתקנה.',
    checks: ['מדידה בשטח וייעוץ ללא התחייבות', 'מערכות חלונות הזזה בהתאמה למרפסת', 'מרכז, שפלה ודרום'],
    slides: [1], tab: 'glass', marquee: ['סגירות זכוכית', 'מערכות חלונות הזזה', 'סגירת מרפסת', 'קירוי למרפסת'],
    proofH: 'סגירה שמתאימה למרפסת שלכם' },
  deck: { cap: 'סופר צל · דקים וריצוף חוץ', h1a: 'דקים וריצוף חוץ', h1b: 'בהתאמה אישית.',
    sub: 'דקים מעץ, מעץ מלאכותי ומחומרים מתקדמים — תכנון יישומי ונקודת קשר אחת מהמדידה ועד ההתקנה.',
    checks: ['מדידה בשטח וייעוץ ללא התחייבות', 'דקים, ריצוף וחיפוי חוץ', 'מרכז, שפלה ודרום'],
    slides: [7], tab: 'deck', marquee: ['דקים', 'ריצוף וחיפוי חוץ', 'פרגולות', 'גדרות ותיחום'],
    proofH: 'דק שמתאים למרחב החוץ שלכם' },
  awning: { cap: 'סופר צל · סוככים והצללה', h1a: 'סוככים וגגונים', h1b: 'בהתאמה אישית.',
    sub: 'סוככי זרועות חשמליים, סוככים קבועים ורשתות צל — תכנון יישומי ומדידה בשטח.',
    checks: ['מדידה בשטח וייעוץ ללא התחייבות', 'סוככי זרועות חשמליים וסוככים קבועים', 'מרכז, שפלה ודרום'],
    slides: [6], tab: 'shade', marquee: ['סוככי זרועות חשמליים', 'סוככים קבועים', 'רשתות ומפרשי צל', 'פרגולות'],
    proofH: 'סוכך שמתאים לחזית שלכם' }
};
STZ_VARIANTS.closure = STZ_VARIANTS.glass;
function stzVariant() {
  let k = '';
  try { k = (location.search.match(/[?&]s=(\w+)/) || [])[1] || ''; } catch (e) {}
  return STZ_VARIANTS[k] || STZ_VARIANTS.pergola;
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
        { n: '01', t: 'מדידה בשטח:', d: 'מבינים את כיוון השמש, המידות וצורת השימוש לפני שמתחילים.' },
        { n: '02', t: 'תכנון יישומי והתאמה אישית:', d: 'מידות, גוון וסגנון בהתאמה לבית ולמרחב החוץ.' },
        { n: '03', t: 'נקודת קשר אחת:', d: 'מהמדידה ועד ההתקנה, אדם אחד שמלווה אתכם בפרויקט.' }
      ],
      proofReviews: this.revs.filter(r => !/מושלמ|הכי /.test(r.text)).slice(0, 3).map(r => ({ text: r.text, who: r.meta })),'''
rep("      sent: this.state.sent,", BINDINGS, 'new bindings')

# --- WhatsApp messages say which page they came from ---------------------------------------------------------------------
rep("'היי, הגעתי מהאתר ואשמח לייעוץ קצר לגבי פרגולה והצללה למרחב החוץ שלנו.'",
    "'היי, הגעתי מדף הפרגולות באתר ואשמח לייעוץ קצר לגבי פרגולה והצללה למרחב החוץ שלנו.'", 'WhatsApp text', count=2)
rep("'היי, הגעתי מהאתר ואשמח לשיחת ייעוץ והתאמה של פתרון הצללה.'",
    "'היי, הגעתי מדף הפרגולות באתר ואשמח לשיחת ייעוץ והתאמה של פתרון הצללה.'", 'WhatsApp text (form)')

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
print('pergola-v2.html written (pergola.html untouched)')
