# A Players Paris — 23–25 October 2026

Landing page for the three-day AI, Ads & Branding workshop mastermind.
Adapted from the A Players Dublin build.

## Files

| Path | What it is |
|---|---|
| `index.html` | **The deployable file.** Self-contained, ~1.8 MB, no build step at runtime. Drop it on any static host. |
| `src/page.html` | Editable source. Same as `index.html` but with a `/*IMAGES*/` marker instead of the base64 photos. **Edit this, not `index.html`.** |
| `assets/images.css` | The 34 embedded photographs, extracted from the Dublin build. Workshop, roundtable, working-session and dinner shots only — gala / black-tie / afterparty imagery is deliberately excluded. |
| `assets/people.css` | All four advisor portraits, 720px wide and colour-matched. Christian Schuette from aplayersmarbella.com; Marius Bulai and James Galligan cropped and graded from supplied stage photographs. |
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
var PRICING = { seats: 15, sold: 3, earlyCount: 10, earlyPrice: 4000,
                fullPrice: 5000, memberOff: 0.25 };
```

`memberOff` in the same block is the A Players Club member discount (0.25).
Both the percentage and the amount shown in the capsule and the FAQ derive
from it, so changing that one number updates every mention and every figure.
At 25% the member price is EUR 3,000 while early seats last, EUR 3,750 after.

**Pricing is no longer shown on the page.** The figures still drive the tier
flag and the Meta pixel value, but nothing renders them. The form captures the
lead and shows a "we'll be in touch" panel instead of redirecting to Whop, so
nobody lands on a priced checkout after being told pricing comes later.

To put the price back on the page and restore checkout, set `CFG.checkout` to
the Whop plan URL (kept in a comment beside it) and re-add the `[data-price]`
elements. The 25% member discount still needs a matching promo code on Whop.

`sold` is the single number to update as seats go. It drives the progress bar,
the "% sold" line, the seats-left counts and the tier flag. The first 10 seats
are the €4,000 **early bird**; from the 10th sale the page flips to €5,000 on
its own. At `sold: 15` every CTA becomes "Join the waitlist".

It currently reads `sold: 3`, which is what puts the bar at 20% sold. That is a
public claim about how many seats have gone, so keep it truthful.

Note this is a static count, not live inventory — it does not read from Whop.

## Phone validation

`window.APCPhone` in `src/page.html` is the whole thing: `check(input, country)`
returns `{ isValid, e164, reason }`, and `mount(root, opts)` wires up the field.

Validity comes from libphonenumber-js (vendored in `vendor/`, inlined at build
time), then four anti-fake checks run on top of it:

- national number of at least 7 digits
- no all-identical runs (1111111111)
- no sequential runs, ascending or descending (1234567890, 0987654321)
- no reserved drama ranges: US/CA `555-01xx`, UK `+44 7700 900xxx`

That last one is the reason the heuristics exist at all: `+1 212 555 0123`
passes libphonenumber's own validity check. Valid input is normalised to
E.164 before it is sent anywhere.

The field is a searchable selector over all 245 countries (names from
`Intl.DisplayNames`, flags from regional-indicator codepoints), a 16px input
so iOS does not zoom on focus, and live green/red states. It exposes the
`onChange(e164, isValid)` contract both as an option and as a bubbling
`phone:change` event.

If the library fails to load the field degrades to digits-only checks rather
than blocking the form.

## The reserve form

Collects first name, last name, email, industry, average monthly revenue,
team size, Instagram handle and phone. Everything except Instagram is
required. Revenue and team size are dropdowns so the answers stay
comparable; industry is free text.

The Instagram field accepts `@handle`, `handle`, or a full profile URL and
normalises all three to the bare handle before sending.

Where the answers go:

| Destination | Carries the new fields? |
|---|---|
| `submit-lead` edge function (`payload`) | yes |
| `gt-event-capture` (see below) | yes |
| Trakyo webhook | yes |
| n8n touchpoint webhook (`profile` object) | yes |
| n8n `gt-event-capture` webhook | yes |
| Supabase `leads` table (direct REST insert) | **no** - still name/email/phone only |

`gt-event-capture` follows a fixed contract: fire-and-forget (never awaited,
never blocks a redirect), fired exactly once per submit, every key present on
every send, and `null` rather than `""` for anything missing. Phone is E.164.

**`purchase_tier_name` sends "The Paris Mastermind".** The integration spec
said `"General Admission"`, which is a Dublin tier name; Paris has one tier and
that is what it is called. If the n8n workflow branches on that string, tell me
and I will switch it.

The direct `leads` insert is deliberately left alone: posting columns that
do not exist on that table would fail the request. If you want industry,
revenue, team size and Instagram in `leads` directly, add those columns
first, then extend that one `JSON.stringify` call.

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
- **Jake Trinder** — agency positioning and the Gary Vee / Ali Abdaal /
  80+ client claims were supplied directly by James.
- **Marius Bulai** — "Founder — Altitude, coolest Meta Ads agency for Online
  Businesses" is legible on his own stage slide. The $400M ad spend figure and
  the client names (Kiyosaki, Cardone, Sapp) were supplied directly by James.
  The three figures printed on the slide in his photograph ($20M+, $7fig, $0)
  are deliberately not quoted anywhere, because their captions are unreadable
  at that resolution.
- **James Galligan** — role and the €50k–€500k/m room size, which is the
  Marbella site's own phrasing.

The testimonial stats (23+ / 700+ / 16+) are the figures published on
aplayersdublin.com. Replace any of this with your own confirmed numbers.

## Differences from Dublin

- Steel (`--steel: #B6BEC6`) replaces the pink accent throughout.
- An Eiffel base arch, drawn as inline SVG line work, sits behind the city name
  in the hero (`.arc`). It deliberately echoes the arch in the A Players mark.
  It is pure vector, adds no weight, and respects prefers-reduced-motion.
- Speaker-led hero: three advisor cards above the city, no iOS smart-stack carousel.
- One ticket tier (€3,000, 15 seats) instead of GA / VIP / VVIP.
- All gala, black-tie, awards and afterparty content and imagery removed.
- Analytics endpoints (Supabase, Trakyo, n8n, Meta pixel) are unchanged and shared
  with the other tour sites; only `city` / `purchase_tier_name` differ.
