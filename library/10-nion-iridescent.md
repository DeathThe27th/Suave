# Style Spec — 10 nion-iridescent

**Real extraction** from `references/2301012fb81b042750c73b2a0b2d25c9.jpg` ("nion").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** nion-iridescent
- **one-line:** Soft iridescent wellness-tech — a pearlescent mint→lavender gradient behind a light panel, thin airy grotesque headlines, fluted-glass photo cards, and one acid-lime accent.
- **best_for:** health-tech, AI wellness, beauty/skincare, calm premium consumer products that want to feel clinical-yet-soft and a little futuristic.
- **avoid_for:** bold/loud brands, dev tools, dense dashboards, or high-contrast utilitarian UIs.

## 1. Palette (named hex + role — never just "green")
- **bg:** #EAF0EC   (pearlescent mint base for the iridescent gradient behind everything)
- **panel:** #F6F6F6   (the light rounded panel the content sits on)
- **surface:** #FFFFFF   (inner cards/pills)
- **ink:** #16181A   (near-black — thin headlines, body)
- **accent:** #DBF269   (acid lime — THE accent: one pill, dots, small highlights)
- **accent_soft:** #F1F7D3   (pale lime wash)
- **muted:** #838686   (secondary text)
- **line:** #E7EAE8   (hairlines, pill borders)
- **accent_usage_rule:** lime touches ONLY one CTA pill, a highlight behind a QR/detail, and small dots. The iridescent gradient supplies the color mood; type stays ink; secondary pills are neutral gray. Never a large lime fill.

## 2. Type
- **display_face:** a LIGHT-weight grotesque (thin, airy — Neue Montreal / Suisse feel)
- **body_face:** same family, regular; muted
- **h1:** weight 300–400 (deliberately thin), size clamp(30px→56px), line-height 1.04, letter-spacing -0.02em
- **h2:** weight 400, ~26–34px
- **body:** weight 400, size 14.5–16px, line-height 1.6, muted
- **eyebrow:** "•" dot prefix, 12px, letter-spaced (e.g. "• AI-Infused")
- **nav labels:** carry small superscript badges — "Healthcare (New)", "Doctors (298)"
- **two_tone_headline:** no — single ink; the gradient and glass carry the interest

## 3. Layout skeleton (section order + structure)
1. Nav (on the light panel) — wordmark left; links with superscript badges; a hamburger right
2. Hero — a "• AI-Infused" dot eyebrow; a large THIN grotesque headline on the left; on the right a short paragraph + a pill row: a neutral-gray pill ("Got any questions?") + a lime pill ("Contact us") + two circular arrow buttons (down/up)
3. Gallery row — 4 fluted/frosted-glass photo cards (faces, a wellness chair) with small overlays: a QR code on a lime highlight, a "▶ TAKE A LOOK" caption, BPM/metric chips, a lime dot
4. …continues in the same system (features, doctors, solutions) on the light panel over the iridescent ground
5. Footer — quiet, on the panel

## 4. Signature moves (the memorable, must-keep specifics)
- **Iridescent pearlescent gradient** (mint → lavender → peach) as the page ground — the defining atmosphere
- **Fluted / frosted-glass photo cards** (vertical ridged-glass effect over portraits)
- **A single acid-lime accent** on one pill / dots / a highlight — the only saturated color
- **Deliberately THIN grotesque headlines**
- **Superscript nav badges** — "(New)", "(298)"
- **"•" dot eyebrows** and **circular arrow buttons**
- **A QR-code motif** on a lime highlight

## 5. Shape & spacing rules
- **radius:** the main panel ~28–32px; cards ~16–20px; pills fully round
- **section_padding:** ~72–96px vertical (airy)
- **card_padding:** ~20px
- **shadow:** very soft and diffuse; the glass cards use blur/translucency more than shadow
- **borders:** hairline #E7EAE8; glass cards have a faint light edge

## 6. Imagery
- **style:** soft-focus portraits and clinical-calm product shots, viewed through fluted/frosted glass; pearlescent color casts
- **treatment:** vertical ridged-glass overlay, gentle blur, small metric/QR overlays; rounded cards
- **source:** Unsplash/Pexels API server-side, prefer soft-portrait / wellness queries; the glass treatment is applied in CSS (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the iridescent gradient hues (mint/lavender/peach can rotate together) and the single lime accent (→ another acid pop)
- **must NOT change on remix:** the iridescent-gradient ground, the fluted-glass cards, the single-acid-accent discipline, the thin grotesque headlines, superscript nav badges, and the airy rounded panel
