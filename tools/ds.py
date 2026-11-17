"""Design system helpers shared by make-closures.py and make-categories.py (see DESIGN-SYSTEM.md).

The home page numbers its sections ("01 · ..."), puts a huge faint number behind each one, alternates its sides, and ends a section with
a small numbered link to the next one ("03 למי זה מתאים ←"). Every generated inner page gets the same treatment from here, so it cannot be
forgotten when a section is added or removed: pass the sections in order and the numbers, watermarks and next links follow.
"""
import re

KICKER = re.compile(r'(<div style="display:inline-flex;align-items:center;gap:1[02]px;color:[^"]*"><span[^>]*></span>)([^<]+)(</div>)')


GRID = re.compile(r'display:grid;grid-template-columns:repeat\(auto-fit,minmax\(min\(100%,(\d+)px\),1fr\)\);gap:')
# No empty holes: rows are flex, so the items of an incomplete last row stretch to fill it (a lone last card spans the whole row).
FILL_CSS = ('<style id="stz-fill">[data-fill]>*{flex:1 1 var(--b);min-width:min(100%,var(--b));box-sizing:border-box}'
            '[data-fill]>[style*="aspect-ratio:4/5"]{aspect-ratio:auto!important;height:clamp(320px,34vw,440px)}'
            '[data-fill]>[style*="aspect-ratio:4/3"]{aspect-ratio:auto!important;height:clamp(250px,25vw,330px)}'
            '[data-fill]>[style*="aspect-ratio:auto"]{min-height:150px}</style>')


def fill(html):
    """Turns every auto-fit grid of a section into a filling flex row."""
    return GRID.sub(lambda m: '--b:%spx;display:flex;flex-wrap:wrap;gap:' % m.group(1), html).replace('<div style="--b:', '<div data-fill="" style="--b:')


def apply(sections, last_href='#fit', last_label='למי זה מתאים'):
    """sections: list of (id, html). Empty html is skipped. Returns the numbered, watermarked and linked html."""
    live = [(i, h) for i, h in sections if h]
    out = []
    for n, (sid, html) in enumerate(live, 1):
        num = '%02d' % n
        dark = 'background:#1B1712' in html.split('>', 1)[0] or 'background: #1B1712' in html.split('>', 1)[0]
        # 1. number in the section's first kicker
        html = KICKER.sub(lambda m: m.group(1) + num + ' · ' + m.group(2) + m.group(3), html, count=1)
        # 2. watermark number behind the section, alternating sides like the home page
        side = 'inset-inline-end' if n % 2 else 'inset-inline-start'
        wm = ('<span aria-hidden="true" style="position:absolute;top:-30px;%s:-16px;font-size:clamp(150px,24vw,300px);font-weight:600;color:%s;opacity:%s;line-height:1;pointer-events:none;user-select:none">%s</span>'
              % (side, '#F5F0E4' if dark else '#211C16', '0.05' if dark else '0.04', num))
        m = re.match(r'<section id="([^"]+)" style="([^"]*)">', html)
        style = m.group(2)
        if 'position:relative' not in style:
            style = 'position:relative;' + style
        if 'overflow-x' not in style:
            style += ';overflow-x:clip'
        html = '<section id="%s" style="%s">%s' % (m.group(1), style, wm) + html[m.end():]
        # the inner width wrapper must sit above the watermark
        html = html.replace('<div style="width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto', '<div style="position:relative;z-index:1;width:min(var(--stz-side,92%),var(--stz-max,1180px));margin-inline:auto', 1)
        out.append([sid, html, num, KICKER.search(html).group(2).split(' · ', 1)[-1] if KICKER.search(html) else ''])
    # 3. numbered link to the next section, at the end of each one
    for k, (sid, html, num, title) in enumerate(out):
        if k + 1 < len(out):
            nsid, _, nnum, ntitle = out[k + 1]
            href, label, nn = '#' + nsid, ntitle, nnum
        else:
            href, label, nn = last_href, last_label, ''   # the form card keeps its own numbering
        link = ('<div style="margin-top:clamp(2rem,5vh,3rem);display:flex;justify-content:flex-end"><a href="%s" style="display:inline-flex;white-space:nowrap;align-items:center;gap:10px;font-size:15.5px;font-weight:500;color:%s;border-bottom:1px solid %s;padding-bottom:3px">%s%s <span aria-hidden="true">←</span></a></div>'
                % (href, '#E8C48C' if 'background:#1B1712' in html.split('>', 1)[0] else '#6E4D1E', 'rgba(232,196,140,.5)' if 'background:#1B1712' in html.split('>', 1)[0] else 'rgba(180,129,60,.5)', ('<span style="opacity:.9">' + nn + '</span> ') if nn else '', label))
        idx = html.rfind('</div></section>')
        out[k][1] = html[:idx] + link + html[idx:]
    return FILL_CSS + ''.join(fill(h) for _, h, _, _ in out)
