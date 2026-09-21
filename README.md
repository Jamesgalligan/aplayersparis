# A Players Paris — 23–25 October 2026

Landing page for the three-day AI, Ads & Branding workshop mastermind.
Adapted from the A Players Dublin build.

## Files

| Path | What it is |
|---|---|
| `index.html` | **The deployable file.** Self-contained, ~1.8 MB, no build step at runtime. Drop it on any static host. |
| `src/page.html` | Editable source. Same as `index.html` but with a `/*IMAGES*/` marker instead of the base64 photos. **Edit this, not `index.html`.** |
| `assets/images.css` | The 34 embedded photographs, extracted from the Dublin build. Workshop, roundtable, working-session and dinner shots only — gala / black-tie / afterparty imagery is deliberately excluded. |
| `assets/people.css` | All three advisor portraits, 720px wide and colour-matched. Christian Schuette from aplayersmarbella.com; Marius Bulai and James Galligan cropped and graded from supplied stage photographs. |
| `build.py` | Inlines the photos into `src/page.html` → `index.html`. Only embeds images the page actually references. |
| `favicon.svg` | The A Players arch mark. |

## Build

```sh
python3 build.py     # src/page.html + assets/images.css -> index.html
```

## Pricing

`src/page.html` has a single `PRICING` block driving every price, flag, meter and
seat count on the page:

```js
var PRICING = { seats: 15, sold: 0, earlyCount: 10, earlyPrice: 4000, fullPrice: 5000 };
```

Update `sold` as seats are taken and redeploy. The first 10 seats show €4,000;
from the 10th sale onward the page flips to €5,000 on its own. At `sold: 15`
every CTA becomes "Join the waitlist".

Note this is a static count, not live inventory — it does not read from Whop.

## Before launch

1. **Check the Whop plan price.** `CFG.checkout` points at
   `https://whop.com/checkout/plan_P1FjwOpo09JN8`. The page charges EUR 4,000
   for the first ten seats and EUR 5,000 after, so the Whop plan has to be
   changed by hand when the price steps up - nothing syncs it automatically.
   Blanking `CFG.checkout` reverts the form to capture-only, showing
   "we'll be in touch within 24 hours" instead of redirecting.
2. **Replace a portrait** by dropping new base64 into `assets/people.css` under
   the same `--p-*` name. Framing and exposure are per-card in `src/page.html`
   via `--photo-pos` (vertical position) and `--photo-grade` (a CSS filter), so
   a new photo may need those retuned. The serif-monogram fallback still works:
   remove the `has-photo` class and the inline `--photo` to go back to it.
3. **Confirm the advisor bio claims.** Christian's copy is taken verbatim from
   aplayersmarbella.com. Marius's and James's are written from public sources
   and carry no revenue figures — see the note below.
4. **Confirm the venue**, then update the "Where in Paris is it?" FAQ answer.

## A note on the advisor copy

An early draft of this page carried figures for Marius Bulai (€65M ad spend,
€300M client revenue) and James Galligan ($2M/year at 22, 180+ founders, 25+
masterminds) that came from an unreliable automated read of aplayersmarbella.com.
None of those numbers appear anywhere in that site's actual source. They have
been removed. The bios now claim only what could be verified:

- **Christian Schuette** — verbatim from the Marbella site's "Meet the Host" block.
- **Marius Bulai** — "Founder — Altitude, coolest Meta Ads agency for Online
  Businesses" is legible on his own stage slide. The three figures on that slide
  ($20M+, $7fig, $0) are on the page nowhere, because their captions are too
  low-resolution to read and an uncaptioned figure means nothing.
- **James Galligan** — role and the €50k–€500k/m room size, which is the
  Marbella site's own phrasing.

The testimonial stats (23+ / 700+ / 16+) are the figures published on
aplayersdublin.com. Replace any of this with your own confirmed numbers.

## Differences from Dublin

- Steel (`--steel: #B6BEC6`) replaces the pink accent throughout.
- Speaker-led hero: three advisor cards above the city, no iOS smart-stack carousel.
- One ticket tier (€3,000, 15 seats) instead of GA / VIP / VVIP.
- All gala, black-tie, awards and afterparty content and imagery removed.
- Analytics endpoints (Supabase, Trakyo, n8n, Meta pixel) are unchanged and shared
  with the other tour sites; only `city` / `purchase_tier_name` differ.
