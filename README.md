# A Players Paris — 23–25 October 2026

Landing page for the three-day AI, Ads & Branding workshop mastermind.
Adapted from the A Players Dublin build.

## Files

| Path | What it is |
|---|---|
| `index.html` | **The deployable file.** Self-contained, ~1.8 MB, no build step at runtime. Drop it on any static host. |
| `src/page.html` | Editable source. Same as `index.html` but with a `/*IMAGES*/` marker instead of the base64 photos. **Edit this, not `index.html`.** |
| `assets/images.css` | The 34 embedded photographs, extracted from the Dublin build. Workshop, roundtable, working-session and dinner shots only — gala / black-tie / afterparty imagery is deliberately excluded. |
| `assets/people.css` | Advisor portraits. Christian Schuette (from aplayersmarbella.com) and Marius Bulai (cropped and graded from a supplied stage photo). James Galligan pending. |
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

1. **Paste the Whop checkout URL.** In `src/page.html`, find `CFG.checkout` (it is
   empty and marked with a TODO) and set it to the Paris plan URL. While it is
   empty the reserve form still captures the lead to Supabase + Trakyo, then shows
   "we'll be in touch within 24 hours" instead of redirecting.
2. **Add James Galligan's headshot.** Christian and Marius are in;
   James still falls back to a serif monogram. To add him: base64 the image into
   `assets/people.css` as `--p-james`, then put the `has-photo` class and
   `style="--photo: var(--p-james)"` on his `.adv-card` and `.bio-card`.
   Each portrait can be tuned independently with `--photo-grade` (a CSS filter)
   and `--photo-pos` (vertical framing), as Marius's cards do.
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
