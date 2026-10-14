# pergola-v2: the campaign landing page

`pergola.html` is the page the current Google Ads campaign points to. It is **not modified** by anything in this folder.
`pergola-v2.html` is generated from it by `tools/make-pergola-v2.py` and served at `https://pergola.supertzel.co.il/pergola-v2`.
Nothing links to it and it has `<meta name="robots" content="noindex, nofollow">` (the pergola host also sends `X-Robots-Tag: noindex`).

## One page per ad group

The address decides what the first screen says, which photos rotate, which product tab opens and what the scrolling band lists.

| Ad group | Final URL | Headline | Photo | Gallery tab |
|---|---|---|---|---|
| Aluminium pergolas (default) | `https://pergola.supertzel.co.il/pergola-v2` | פרגולות אלומיניום בהתאמה אישית | pergolas (5 photos) | הצללה וקירוי |
| Glass closures | `…/pergola-v2?s=glass` | סגירות זכוכית למרפסת | glass balcony | סגירות |
| Decks | `…/pergola-v2?s=deck` | דקים וריצוף חוץ בהתאמה אישית | deck and garden (117 KB version) | דקים וריצוף |
| Awnings | `…/pergola-v2?s=awning` | סוככים וגגונים בהתאמה אישית | awnings | הצללה וקירוי |

Parameters such as `utm_source` and `gclid` can follow (`…/pergola-v2?s=glass&utm_source=google`). Sitelinks keep working (`?sl=contact#contact`).

## What is different from `/pergola`

- **First screen:** static headline that repeats the search, one sentence of what we do, a two-field form (name, phone, country code) with the
  button "תאמו שיחת ייעוץ", WhatsApp and call buttons next to it, the Google rating and review count (read from the same reviews function the
  page already uses; hidden if it cannot be loaded) and three check lines. On `/pergola` the first screen is a rotating headline, two buttons
  and no rating.
- **Right after it:** a short block with three points (measurement on site, applied planning with personal fit, one point of contact) and three customer
  reviews (swipeable on phones). Reviews that contain absolute claims ("מושלם", "הכי") are left out of this block; they stay in the reviews
  section lower on the page, as before.
- **Order:** the product gallery now comes before the long "before you choose" explanation and the sun simulator, which moved down to after
  "איך זה עובד". The left rail lists the chapters in the new order.
- **No photo pins** on the hero photo (they sat on top of the form on wide screens).
- **WhatsApp messages** say "הגעתי מדף הפרגולות באתר" instead of "הגעתי מהאתר", so a WhatsApp chat shows which page it came from; leads from the forms
  carry `עמוד: /pergola-v2` and GA4 events carry `source: /pergola-v2`.
- **One name for the main button,** "תאמו שיחת ייעוץ" (the floating bar and an inline button said "תיאום פגישת ייעוץ").
- `?s=awning` shows a photo (on `/pergola` that slide has no image element).
- **Faster first screen:** the photo of the chosen variant is preloaded and the others are lazy.

Everything else is the same: same sections and texts, same scripts, same consent banner, same tracking.

## Checked against `/pergola` (simulated phone network, headless browser)

- Same text content apart from the changes above; all section ids and sitelink anchors present (they land below the header).
- First screen not slower: LCP 3.04 s vs 3.40 s (150 ms RTT, 1.6 Mbps, 4x CPU); glass 3.21 s, deck 3.10 s, awning 3.36 s. Layout shift ≈ 0.
- Accessibility (axe, WCAG A/AA): the same findings as `/pergola` on a phone, fewer on desktop; none from the new parts.
- On `pergola.supertzel.co.il/pergola-v2?utm…&gclid…` (host emulated): the hero form, the floating form, the call and the WhatsApp buttons each fire
  once, both Google Ads conversions fire, `generate_lead` fires once per submitted form, the lead message carries the page, UTM and gclid.
- Not testable from the build environment: the live Supabase functions and the live domains.

## Using it

- Use the `pergola.` host: the direct Ads conversions for WhatsApp and calls are only sent on that host, on `/pergola` paths of any host, or with
  `?landing=1` (so `supertzel.co.il/pergola-v2` would not send them).
- Keep the closures ad group on `/pergola` until you decide; or point it to `?s=glass`.
- To compare with the current page, run it as a separate ad group or ad and judge after about 100 clicks each.
- To stop: point the ads back to `/pergola` and delete `pergola-v2.html` (and `img/fast/lp/pg-hero-deck.webp` if the deck variant is not used).

## Rebuilding

After a new export overwrites `pergola.html` (and `tools/perf/apply.py` has been run), rebuild the copy:

    python3 tools/make-pergola-v2.py

Each change in the script must match the exact text of `pergola.html` once; if the export changed that text the script says which one
and writes nothing. The ad-group texts are in the `STZ_VARIANTS` table inside the script.
