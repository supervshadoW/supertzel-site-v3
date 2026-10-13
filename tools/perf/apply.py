#!/usr/bin/env python3
"""Re-applies the site's performance, measurement, accessibility and policy fixes. Safe to run more than once.

Run it from the repository root after copying a fresh export of the pages over the repo
(a new export overwrites index.html, pergola.html, projects.html, legal.html, analytics.js,
vercel.json and the logo / hero images with the older versions):

    python3 tools/perf/apply.py

What it does (no visual change):
  1. React and ReactDOM are served from /vendor (byte-identical to the unpkg builds pinned by support.js) and the
     Rubik font from /fonts, instead of unpkg.com and Google Fonts. Both are preloaded from the static <head>.
  2. window.__resources makes support.js use those files. As a side effect it skips the second download and
     re-render of the page that support.js does when __resources is not defined.
  3. analytics.js runs only once (the page runtime executes <helmet> scripts twice, which counted every
     WhatsApp / phone click and every page view twice) and loads gtag.js and Clarity after the page has loaded.
  4. Logos are shipped at 3x their displayed size (112KB -> 15KB), the landing hero is re-encoded (-30%), and the
     simulation image below the fold is lazy-loaded.
  5. vercel.json: immutable caching for /vendor and /fonts.
  6. Accessibility / SEO / Google Ads policy: lang="he", meta descriptions, the business name as text in the first screen
     of the landing page (Google Ads "business name prominence"), a name for the phone fields, a left-to-right page
     counter ("1 / 2" instead of "2 / 1"), no bogus requests for template placeholders, robots.txt, and the privacy
     policy no longer lists Google Fonts (fonts are served from this site).
"""
import json, os, re, shutil, sys

ROOT = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')

def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f: return f.read()
def write(p, s):
    with open(os.path.join(ROOT, p), 'w', encoding='utf-8') as f: f.write(s)

for need in ('vendor/react-18.3.1.production.min.js', 'vendor/react-dom-18.3.1.production.min.js',
             'fonts/rubik-hebrew-wght-normal.woff2', 'fonts/rubik-latin-wght-normal.woff2'):
    if not os.path.exists(os.path.join(ROOT, need)):
        sys.exit(f'missing {need} - run from the repo root')

# 4) optimised images (same file names as before)
shutil.copy(f'{ASSETS}/logo-light-bg.png', f'{ROOT}/img/logo-light-bg.png')
shutil.copy(f'{ASSETS}/logo-dark-bg.png', f'{ROOT}/img/logo-dark-bg.png')
shutil.copy(f'{ASSETS}/pg-hero.webp', f'{ROOT}/img/fast/lp/pg-hero.webp')

HEAD = '''<link rel="preload" href="/vendor/react-18.3.1.production.min.js" as="script">
<link rel="preload" href="/vendor/react-dom-18.3.1.production.min.js" as="script">
<link rel="preload" href="/fonts/rubik-hebrew-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/rubik-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<style id="stz-fonts">@font-face{font-family:'Rubik';font-style:normal;font-weight:300 700;font-display:swap;src:url(/fonts/rubik-hebrew-wght-normal.woff2) format('woff2');unicode-range:U+0307-0308,U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}@font-face{font-family:'Rubik';font-style:normal;font-weight:300 700;font-display:swap;src:url(/fonts/rubik-latin-wght-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}</style>
<script>window.__resources={"https://unpkg.com/react@18.3.1/umd/react.production.min.js":"/vendor/react-18.3.1.production.min.js","https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js":"/vendor/react-dom-18.3.1.production.min.js"};</script>
'''
SUP = '<script src="/support.js"></script>'
for name in ('index.html', 'pergola.html', 'projects.html', 'legal.html'):
    s = read(name)
    if 'stz-fonts' not in s:
        assert SUP in s, f'{name}: support.js tag not found'
        s = s.replace(SUP, HEAD + SUP, 1)
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\s*', '', s)
    s = re.sub(r'<link href="https://fonts\.googleapis\.com/css2[^>]*rel="stylesheet">\s*', '', s)
    assert 'fonts.googleapis' not in s, f'{name}: Google Fonts reference left'
    if name == 'pergola.html':
        tag = '<img src="/img/fast/w/envelope-render-pins.webp"'
        if tag in s: s = s.replace(tag, '<img loading="lazy" src="/img/fast/w/envelope-render-pins.webp"', 1)
    write(name, s)

# 3) analytics.js
a = read('analytics.js')
if '__stzAnalytics' not in a:
    a = a.replace("(function () {\n", "(function () {\n  // The page runtime re-runs <helmet> scripts after the browser already ran them; run only once so events and page views are not counted twice.\n  if (window.__stzAnalytics) return;\n  window.__stzAnalytics = true;\n", 1)
    old = """  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
"""
    new = """  // gtag.js is loaded after the page has loaded so it does not compete with the page itself; dataLayer queues everything until then.
  var gtagLoaded = false;
  function loadGtag() {
    if (gtagLoaded) return;
    gtagLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }
  if (document.readyState === 'complete') setTimeout(loadGtag, 0);
  else { addEventListener('load', function () { setTimeout(loadGtag, 0); }); setTimeout(loadGtag, 6000); }
"""
    assert old in a, 'analytics.js: gtag loader not found'
    a = a.replace(old, new, 1)
if 'stz-clarity-later' not in a:
    old = """    clarityOn = true;
    (function (c, l, a, r, i, t, y) {"""
    new = """    clarityOn = true;
    // stz-clarity-later: inject the script after the page has loaded (calls made before that are queued by the stub below)
    var later = function (fn) { if (document.readyState === 'complete') setTimeout(fn, 0); else addEventListener('load', function () { setTimeout(fn, 0); }); };
    (function (c, l, a, r, i, t, y) {"""
    assert old in a, 'analytics.js: clarity loader not found'
    a = a.replace(old, new, 1)
    old2 = """      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);"""
    new2 = """      later(function () {
        t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
        y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
      });"""
    assert old2 in a, 'analytics.js: clarity injection not found'
    a = a.replace(old2, new2, 1)
write('analytics.js', a)
for name in ('index.html', 'pergola.html', 'projects.html', 'legal.html'):
    s = read(name)
    s2 = re.sub(r'analytics\.js\?v=(\d+)', lambda m: 'analytics.js?v=%d' % max(int(m.group(1)), 10), s)
    if s2 != s: write(name, s2)

# 5) caching (text edit so the rest of vercel.json keeps its formatting).
# Later header rules win over earlier ones, so /vendor goes after the generic "*.js" rule (max-age=300).
raw = read('vercel.json')
def rule(src):
    return ('                    {\n'
            f'                        "source":  "{src}",\n'
            '                        "headers":  [\n'
            '                                        {\n'
            '                                            "key":  "Cache-Control",\n'
            '                                            "value":  "public, max-age=31536000, immutable"\n'
            '                                        }\n'
            '                                    ]\n'
            '                    },\n')
js_rule = ('                    {\n'
           '                        "source":  "/(.*)\\\\.js",\n'
           '                        "headers":  [\n'
           '                                        {\n'
           '                                            "key":  "Cache-Control",\n'
           '                                            "value":  "public, max-age=300, must-revalidate"\n'
           '                                        }\n'
           '                                    ]\n'
           '                    },\n')
for src in ('/fonts/(.*)', '/vendor/(.*)'):
    if f'"source":  "{src}"' in raw: continue
    assert js_rule in raw, 'vercel.json: expected "*.js" cache rule not found'
    raw = raw.replace(js_rule, js_rule + rule(src), 1)
json.loads(raw)
write('vercel.json', raw)

# 6) accessibility / SEO / policy fixes. patch() skips quietly when already applied and warns when the text it expects is gone.
changed_js = set()
def patch(name, old, new, label, count=1):
    s = read(name)
    if new in s:
        return False
    if old not in s:
        print(f'WARNING: {name}: "{label}" not applied (expected text not found)')
        return False
    write(name, s.replace(old, new, count))
    if name.endswith('.js'): changed_js.add(name)
    return True

PAGES = ('index.html', 'pergola.html', 'projects.html', 'legal.html')
for name in PAGES:
    patch(name, '<html>', '<html lang="he">', 'lang')
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'
DESC = {
    'pergola.html': 'פרגולות והצללה בהתאמה אישית: פרגולות אלומיניום, תריס חשמלי ועץ, סוככים ורשתות צל. מדידה בשטח, תכנון יישומי ונקודת קשר אחת מהמדידה ועד המסירה. סופר צל — מרכז, שפלה ודרום. תאמו שיחת ייעוץ.',
    'projects.html': 'פרויקטים שביצענו — פרגולות, סגירות זכוכית, מטבחי חוץ, דקים וגידור. תמונות מפרויקטים של סופר צל.',
    'legal.html': 'תקנון, מדיניות פרטיות והצהרת נגישות של סופר צל.',
}
for name, text in DESC.items():
    if 'name="description"' not in read(name):
        patch(name, VIEWPORT, VIEWPORT + '\n<meta name="description" content="' + text + '">', 'meta description')
# Google Ads "business name prominence": the name must be visible as text in the first screen on phones
patch('pergola.html', "heroCapShow: n ? 'פרגולות והצללה' : S[cs].caption,", "heroCapShow: n ? 'סופר צל · פרגולות והצללה' : S[cs].caption,", 'business name in the hero caption')
# page counters in a right-to-left page: "1 / 2" was drawn as "2 / 1"
patch('index.html', '<span style="font-size:14px;font-weight:600;color:#211C16;min-width:44px;text-align:center">{{ bookNum }} / {{ bookTotal }}</span>', '<span dir="ltr" style="font-size:14px;font-weight:600;color:#211C16;min-width:44px;text-align:center">{{ bookNum }} / {{ bookTotal }}</span>', 'page counter')
patch('index.html', '<span style="font-size:14px;font-weight:600;color:#F5F0E4;min-width:44px;text-align:center">{{ b2Num }} / 2</span>', '<span dir="ltr" style="font-size:14px;font-weight:600;color:#F5F0E4;min-width:44px;text-align:center">{{ b2Num }} / 2</span>', 'page counter 2')
# the raw template made the browser request "/{{ pMain }}" etc. (404s); lazy images inside hidden markup are not requested
for name, srcs in (('pergola.html', ('{{ pMain }}', '{{ t.src }}')), ('projects.html', ('{{ mSrc }}', '{{ t.src }}'))):
    for src in srcs:
        patch(name, f'<img src="{src}"', f'<img loading="lazy" src="{src}"', f'lazy {src}')
# phone fields: the country-code select is inserted into the label, which left the number field without a name
patch('phone-cc.js', "    input.parentNode.insertBefore(sel, input);\n", "    input.parentNode.insertBefore(sel, input);\n    if (!input.getAttribute('aria-label')) input.setAttribute('aria-label', 'טלפון');\n", 'phone field name')
patch('lead-modal.js', "telI.required = true;", "telI.required = true; telI.setAttribute('aria-label', 'טלפון');", 'modal phone field name')
# cache-busting for the scripts changed above
for js in sorted(changed_js):
    for name in PAGES:
        t = read(name)
        t2 = re.sub(re.escape(js) + r'\?v=(\d+)', lambda m: '%s?v=%d' % (js, int(m.group(1)) + 1), t)
        if t2 != t: write(name, t2)
# privacy policy: Google Fonts is no longer used
lg = read('legal.html')
lg2 = re.sub(r'\s*<tr[^>]*><td[^>]*>Google Fonts</td>.*?</tr>', '', lg, count=1, flags=re.S)
if lg2 != lg: write('legal.html', lg2)
# robots.txt (explicitly lets the Google Ads crawlers in)
if not os.path.exists(os.path.join(ROOT, 'robots.txt')):
    write('robots.txt', 'User-agent: *\nAllow: /\n\nUser-agent: AdsBot-Google\nAllow: /\n\nUser-agent: AdsBot-Google-Mobile\nAllow: /\n')

print('performance fixes applied')
