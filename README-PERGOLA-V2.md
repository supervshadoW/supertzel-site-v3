# pergola-v2: a separate copy of the campaign landing page

`pergola.html` is the page the Google Ads campaign points to. It is **not modified** by anything in this folder.
`pergola-v2.html` is a generated copy with a few conversion changes, served at `https://pergola.supertzel.co.il/pergola-v2`.
Nothing links to it, it has `<meta name="robots" content="noindex, nofollow">` (and the pergola host already sends `X-Robots-Tag: noindex`).

## What differs from `/pergola`

| | `/pergola` (live campaign page) | `/pergola-v2` |
|---|---|---|
| First screen | glass-closure photo, headline "…וגם סגירות זכוכית למרפסת." | black louvered pergola photo (95 KB, preloaded), headline "…פרגולות אלומיניום ועץ." |
| WhatsApp message | "הגעתי מהאתר" | "הגעתי מדף הפרגולות באתר", so a WhatsApp chat shows which page it came from |
| Main button names | "תאמו שיחת ייעוץ" in the hero, "תיאום פגישת ייעוץ" in the floating bar and below | "תאמו שיחת ייעוץ" everywhere |
| `?s=awning` | headline changes but the hero has **no photo** (the slide has no image element) | the awnings photo is shown |
| Tab title | "פתרונות הצללה מתקדמים בהתאמה אישית \| סופר צל" | "פרגולות והצללה בהתאמה אישית \| סופר צל" |

Everything else is identical: same sections in the same order, same scripts, same tracking. Leads from the copy carry
`עמוד: /pergola-v2` in the message and GA4 events carry `source: /pergola-v2`.

Measured against `/pergola` (simulated phone network): same page height, same element ids, no new accessibility findings, first screen
not slower (LCP 3.29 s vs 3.40 s on a slow connection), `generate_lead` / `whatsapp_click` / `contact_call` and both Google Ads conversions
fire once per action on `pergola.supertzel.co.il/pergola-v2`.

## Using it

- Final URL of an ad group: `https://pergola.supertzel.co.il/pergola-v2`. Use the `pergola.` host: the direct Ads conversions for WhatsApp and
  calls are only sent on that host, on `/pergola` paths of any host, or with `?landing=1` (so `supertzel.co.il/pergola-v2` would not send them).
- Sitelink anchors work the same (`?sl=contact#contact` etc.).
- The glass-closure ad group should keep pointing at `/pergola`, which still opens on the glass-closure photo.
- To stop: point the ads back to `/pergola` and delete `pergola-v2.html`.

## Rebuilding

After a new export overwrites `pergola.html` (and `tools/perf/apply.py` has been run), rebuild the copy:

    python3 tools/make-pergola-v2.py

Each change in the script must match the exact text of `pergola.html` once; if the export changed that text the script says which one
and writes nothing.
