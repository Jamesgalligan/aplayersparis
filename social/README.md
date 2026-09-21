# Instagram carousel — A Players Paris

Five 4:5 slides, rendered from `slides.html` in the same fonts, palette,
arch mark and photography as aplayersparis.com.

| File | Slide |
|---|---|
| `out/paris-01.png` | Announcement — PARIS, dates, 15 / 3 / 3 / 1:1 |
| `out/paris-02.png` | The advisors — three portraits |
| `out/paris-03.png` | The format — Day One / Two / Three (light slide) |
| `out/paris-04.png` | What's included |
| `out/paris-05.png` | The ticket — €4,000 early bird, 25% member price, aplayersparis.com |

`paris-0N.png` are 1080x1350, ready to upload. `paris-0N@2x.png` are the
2160x2700 masters if anything needs reworking or printing.

## Re-rendering

The slides pull live from `../assets/images.css` and `../assets/people.css`,
so updated photography flows through automatically. Prices and seat counts
are **hardcoded here** — they do not read the site's `PRICING` block, so
check them against the live card before posting.

1. Serve the repo root (`python3 -m http.server 4173`)
2. Open `http://localhost:4173/social/slides.html`
3. Screenshot each `.slide` at 1080x1350, deviceScaleFactor 2
4. Downscale the 2x files to 1080 wide
