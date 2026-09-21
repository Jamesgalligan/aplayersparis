# A Players Paris — 23–25 October 2026

Landing page for the three-day AI, Ads & Branding workshop mastermind.
Adapted from the A Players Dublin build.

## Files

| Path | What it is |
|---|---|
| `index.html` | **The deployable file.** Self-contained, ~1.8 MB, no build step at runtime. Drop it on any static host. |
| `src/page.html` | Editable source. Same as `index.html` but with a `/*IMAGES*/` marker instead of the base64 photos. **Edit this, not `index.html`.** |
| `assets/images.css` | The 34 embedded photographs, extracted from the Dublin build. Workshop, roundtable, working-session and dinner shots only — gala / black-tie / afterparty imagery is deliberately excluded. |
| `build.py` | Inlines the photos into `src/page.html` → `index.html`. Only embeds images the page actually references. |
| `favicon.svg` | The A Players arch mark. |

## Build

```sh
python3 build.py     # src/page.html + assets/images.css -> index.html
```

## Before launch

1. **Paste the Whop checkout URL.** In `src/page.html`, find `CFG.checkout` (it is
   empty and marked with a TODO) and set it to the Paris plan URL. While it is
   empty the reserve form still captures the lead to Supabase + Trakyo, then shows
   "we'll be in touch within 24 hours" instead of redirecting.
2. **Swap in the advisor headshots.** The three hero cards and three bio cards use
   serif monograms (`CS` / `MB` / `JG`). To use photos, add the image to
   `assets/images.css` as a custom property and set `--photo` plus the
   `has-photo` class on `.adv-card` / `.bio-card`.
3. **Confirm the venue**, then update the "Where in Paris is it?" FAQ answer.

## Differences from Dublin

- Steel (`--steel: #B6BEC6`) replaces the pink accent throughout.
- Speaker-led hero: three advisor cards above the city, no iOS smart-stack carousel.
- One ticket tier (€3,000, 15 seats) instead of GA / VIP / VVIP.
- All gala, black-tie, awards and afterparty content and imagery removed.
- Analytics endpoints (Supabase, Trakyo, n8n, Meta pixel) are unchanged and shared
  with the other tour sites; only `city` / `purchase_tier_name` differ.
