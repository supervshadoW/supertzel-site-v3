#!/usr/bin/env python3
"""Re-applies the site's performance and measurement fixes. Safe to run more than once.

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

# 5) caching (text edit so the rest of vercel.json keeps its formatting)
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
marker = '    "headers":  [\n'
for src in ('/fonts/(.*)', '/vendor/(.*)'):
    if f'"source":  "{src}"' not in raw:
        assert marker in raw, 'vercel.json: headers array not found'
        raw = raw.replace(marker, marker + rule(src), 1)
json.loads(raw)
write('vercel.json', raw)
print('performance fixes applied')
