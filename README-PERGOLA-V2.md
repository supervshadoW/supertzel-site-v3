# pergola-v2: the campaign landing page

`pergola.html` is the page the current Google Ads campaign points to. It is **not modified** by anything in this folder.
`pergola-v2.html` is generated from it by `tools/make-pergola-v2.py` and served at `https://pergola.supertzel.co.il/pergola-v2`.
Nothing links to it and it has `<meta name="robots" content="noindex, nofollow">` (the pergola host also sends `X-Robots-Tag: noindex`).

## One page per ad group

The address decides what the visitor sees. Everything that talks about a product follows the ad group, so a deck page never talks about
pergola shade and a glass page never offers a sun simulator.

| Ad group | Final URL | Headline | Photo | Gallery opens on |
|---|---|---|---|---|
| Aluminium pergolas (default) | `https://pergola.supertzel.co.il/pergola-v2` | פרגולות אלומיניום בהתאמה אישית | pergolas (5 photos) | הצללה וקירוי |
| Glass closures | `…/pergola-v2?s=glass` | סגירות זכוכית למרפסת | glass balcony | סגירות |
| Decks | `…/pergola-v2?s=deck` | דקים וריצוף חוץ בהתאמה אישית | deck and garden (117 KB version) | דקים וריצוף |
| Awnings | `…/pergola-v2?s=awning` | סוככים וגגונים בהתאמה אישית | awnings | הצללה וקירוי, awnings first |

Parameters such as `utm_source` and `gclid` can follow (`…/pergola-v2?s=glass&utm_source=google`). Sitelinks keep working (`?sl=contact#contact`).

### What follows the ad group (all texts are in the `VARIANTS` table of `tools/make-pergola-v2.py`)

| Part of the page | pergolas | glass | decks | awnings |
|---|---|---|---|---|
| Browser tab title | as before | סגירות זכוכית… | דקים וריצוף חוץ… | סוככים וגגונים… |
| First screen: headline, sub line, 3 check lines, photo | ✓ | ✓ | ✓ | ✓ |
| Scrolling band | ✓ | ✓ | ✓ | ✓ |
| "בקצרה" block: heading and first point (measuring) | sun direction, size, use | balcony size, use | size, surface, use | sun direction, size, use |
| Gallery tab that opens, and its note | shade | closures | decks (note without "the base the pergola sits on") | shade, awnings listed first |
| "למה סופר צל": first reason | profiles, connectors, paint | same | material, connectors, finish | same as pergolas |
| "איך זה עובד": first step | sun directions | balcony size | surface condition | sun directions |
| "לפני שבוחרים פתרון הצללה" + sun simulator | shown | **not on the page** | **not on the page** | **not on the page** |
| Side rail ("פרקים") and mobile menu | with "השמש במרחב" | without it, numbers continue | without it | without it |
| Questions section: heading, questions 1 and 2, answer 1 | pergola | glass systems | decks | awnings |
| Contact: heading, sentence, "what interests you" list | pergola list | closures list | deck list | awning list |
| WhatsApp text | "הגעתי מדף הפרגולות באתר…" | "…מדף סגירות הזכוכית…" | "…מדף הדקים…" | "…מדף הסוככים…" |
| Lead label (`solution`), floating-form text, GA4 `form` | פרגולות והצללה | סגירות זכוכית | דקים וריצוף חוץ | סוככים והצללה |

The sun simulator, the "company overview", the portfolio, the reviews, the footer and the multi-discipline disclosure are the same everywhere.

## What else is different from `/pergola`

- **First screen:** static headline that repeats the search, one sentence of what we do, a two-field form (name, phone, country code) with the
  button "תאמו שיחת ייעוץ", WhatsApp and call buttons next to it, the Google rating and review count (read from the same reviews function the
  page already uses; hidden if it cannot be loaded) and three check lines. On `/pergola` the first screen is a rotating headline, two buttons
  and no rating.
- **Right after it:** a short block with three points and three customer reviews (swipeable on phones). Reviews that contain absolute claims
  ("מושלם", "הכי") are left out of this block; they stay in the reviews section lower on the page, as before.
- **Order:** the product gallery comes before the long "before you choose" explanation and the sun simulator (pergola page only), which moved
  down to after "איך זה עובד". The left rail lists the chapters in the new order.
- **No photo pins** on the hero photo (they sat on top of the form on wide screens).
- **Leads say where they came from.** The text of the WhatsApp message and of the quick form names the ad group's page; the label in the
  lead (`solution`) is the ad group, not "פרגולות והצללה"; leads from the forms carry `עמוד: /pergola-v2` and the UTM/gclid as before;
  GA4 `generate_lead` carries `form` = `pergola_quick_deck`, `pergola_long_glass`, `modal_דקים וריצוף חוץ`…
  (done by a small wrapper inside the page: `lead.js` and `lead-modal.js` are shared and untouched).
- **The long contact form sends readable values.** On `/pergola` the "what interests you" choice reaches the lead as a code (`alu`, `louver`…);
  here it is the Hebrew label.
- **One name for the main button,** "תאמו שיחת ייעוץ" (the floating bar and an inline button said "תיאום פגישת ייעוץ").
- `?s=awning` shows a photo (on `/pergola` that slide has no image element).
- **Faster first screen:** the photo of the chosen variant is preloaded and the others are lazy.

Everything else is the same: same sections and texts, same scripts, same consent banner, same tracking.

## Checked against `/pergola` (headless browser, simulated phone network)

- Rendered text of the default page differs from `/pergola` only in the parts listed above; all section ids and sitelink anchors that exist
  are present (they land below the header).
- First screen not slower in any variant: LCP about 3.0–3.2 s against about 3.2–3.4 s for `/pergola` (150 ms RTT, 1.6 Mbps, 4x CPU, run to
  run noise about ±0.2 s). Layout shift ≈ 0 on phone and desktop.
- Accessibility (axe, WCAG A/AA): the same findings as `/pergola` on a phone (same elements), fewer on desktop; none from the new parts.
- On `pergola.supertzel.co.il/pergola-v2?s=…&utm…&gclid…` (host emulated), for all four variants: the hero form, the contact form, the floating form,
  the call and the WhatsApp buttons each fire once, both Google Ads conversions fire, `generate_lead` fires once per submitted form, the lead
  carries the ad group's label, the page, UTM and gclid; no JavaScript errors.
- Not testable from the build environment: the live Supabase functions (reviews, lead delivery) and the live domains.

## Using it

- Use the `pergola.` host: the direct Ads conversions for WhatsApp and calls are only sent on that host, on `/pergola` paths of any host, or with
  `?landing=1` (so `supertzel.co.il/pergola-v2` would not send them).
- To compare with the current page, run it as a separate ad group or ad and judge after about 100 clicks each.
- To stop: point the ads back to `/pergola` and delete `pergola-v2.html` (and `img/fast/lp/pg-hero-deck.webp` if the deck variant is not used).

## Rebuilding

After a new export overwrites `pergola.html` (and `tools/perf/apply.py` has been run), rebuild the copy:

    python3 tools/make-pergola-v2.py

Each change in the script must match the exact text of `pergola.html` once; if the export changed that text the script says which one
and writes nothing. The pergola entry of the `VARIANTS` table repeats the live page's own wording and is used as the text that is cut out,
so it only matches while `pergola.html` still says exactly that.
