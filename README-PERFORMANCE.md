# Performance, measurement and accessibility fixes (keep these when pages are re-exported)

A new export of the pages (from Claude Design) overwrites `index.html`, `pergola.html`, `projects.html`, `legal.html`,
`analytics.js`, `vercel.json` and the logo / hero images with older versions, which silently removes the fixes below.
After copying a new export into the repo, run once from the repository root:

    python3 tools/perf/apply.py

The script is safe to run repeatedly. It does the following, with no visual change:

1. **React / ReactDOM and the Rubik font are served from this site** (`/vendor`, `/fonts`) instead of unpkg.com and Google
   Fonts, and are preloaded from the static `<head>`. The React files are byte-identical to the unpkg builds pinned by the
   SRI hashes in `support.js`.
2. **`window.__resources`** (inline script before `support.js`) tells the page runtime to use those files. It also stops the
   runtime from downloading and re-rendering the whole page a second time.
3. **`analytics.js` runs once.** The page runtime executes `<helmet>` scripts a second time, which used to count every
   WhatsApp / phone click and every returning visitor's page view twice. gtag.js and Clarity now load after the page has loaded.
4. **Smaller images:** logos at 3x their displayed size, the landing hero re-encoded, the simulation image below the fold lazy-loaded.
5. **`vercel.json`:** immutable caching for `/vendor` and `/fonts`.

6. **Accessibility / SEO / Google Ads policy:** `lang="he"` on every page, meta descriptions, the business name as visible text
   in the first screen of the landing page on phones (hero caption "סופר צל · פרגולות והצללה", for the Google Ads
   "business name prominence" policy), an accessible name for the phone fields (the country-code select that
   `phone-cc.js` inserts took over the label), a left-to-right page counter on the home page ("1 / 2" was drawn as
   "2 / 1" in the right-to-left page), `loading="lazy"` on the template placeholder images (the browser used to request
   `/{{ pMain }}` and got 404s), `robots.txt`, and the privacy policy no longer lists Google Fonts.

7. **Home page and projects page only (the landing page structure is never touched here):** gold kicker lines on the cream
   background and a few grey hints darkened to meet WCAG AA contrast, accessible names that contain the visible text
   (logo link, numbered hero hotspots, project cards, call button), `canonical` + `LocalBusiness` structured data (no rating,
   no price, not typed as a contractor) on the home page, and Escape closes the mobile menu (`home-a11y.js`).

8. **Social links:** the export links the Facebook / Instagram icons to the generic front pages (`facebook.com/`,
   `instagram.com/`). `apply.py` sets the real Super Tzel profiles (`FB_URL`, `IG_URL` at the top of section 8; taken from the
   footer of the previous Lovable site). On the landing page only the two `href` values change. The home page keeps its
   reviews section (with the icons) hidden, as requested.

The "who we are" and "projects" sections of the pergola landing page are inserted by `landing-about.js` and
`landing-projects.js` right after `#why` (in that order). They only insert into the rendered page and put themselves back in
place if the page re-renders, so the order is the same on every load.
