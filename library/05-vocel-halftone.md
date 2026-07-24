# Style Spec — 05 vocel-halftone

**Real extraction** from `references/1553695a4bf3e18e2a86756c4cff1041.jpg` ("Vocel").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** vocel-halftone
- **one-line:** Near-black technical minimalism — a monochrome dot-matrix/halftone hero, corner-bracket frames, mono eyebrows, and white-on-black buttons; a single green status dot is the only color.
- **best_for:** AI/voice/infra, developer and engineering products, anything that wants to read precise, fast, and technical without going neon.
- **avoid_for:** warm consumer, wellness, luxury-hospitality, or color-forward brands.

## 1. Palette (named hex + role — never just "black")
- **bg:** #101010   (near-black, primary background)
- **surface:** #171717   (raised cards, the chat/waveform panels)
- **ink:** #F4F4F4   (primary text / headlines)
- **accent:** #34E39B   (green status dot — the ONLY color, used at pinprick size)
- **accent_soft:** #16311F   (rare green-tinted chip)
- **muted:** #868686   (secondary text, mono labels)
- **line:** #262626   (hairline frames, dividers, bracket corners)
- **button_fill:** #FFFFFF   (primary buttons are white with black text)
- **accent_usage_rule:** the page is monochrome. Green appears ONLY as a tiny status dot inside a voice-toggle pill. Emphasis otherwise is white type on black, hairline frames, and the halftone texture — never a colored fill.

## 2. Type
- **display_face:** clean grotesque (Inter Tight / Geist feel) — tight, technical-neutral
- **body_face:** same family, regular; muted for supporting copy
- **mono_face:** a monospace for eyebrow badges and micro-labels
- **h1:** weight 600, size clamp(30px→52px), line-height 1.06, letter-spacing -0.02em
- **h2:** weight 600, size ~30–40px
- **body:** weight 400, size 15–16px, line-height 1.6, muted
- **eyebrow:** mono, 11px, uppercase, letter-spacing 0.14em, inside a bordered pill badge (e.g. "NEW ERA: …")
- **two_tone_headline:** no — single ink white

## 3. Layout skeleton (section order + structure)
1. Nav — inside a corner-bracket frame: mark + mono links + a white "Get Started" button
2. Hero — centered mono pill badge; big white grotesque headline; muted subline; a white primary + a hairline-bordered secondary button; below, a large monochrome HALFTONE dot-matrix graphic (a globe/landscape) with a floating dark chat panel (greeting, quick-action pills, a circular play button, a voice-toggle with a green dot)
3. Logos — a row of grayscale partner marks on black, split by vertical hairline rules; hatched/striped divider bands above and below
4. Feature (voice intelligence) — h2 + two buttons; two dark cards each showing a white waveform visualization + a green-dot voice toggle, with a circular play button between them
5. …continues with more dark bordered sections (pricing/FAQ) in the same system
6. Footer — mono link grid on black, hairline top

## 4. Signature moves (the memorable, must-keep specifics)
- **Monochrome halftone / dot-matrix imagery** (globe, waveforms) as the hero graphic — the defining texture
- **Corner-bracket "⌐ ¬" frames** around the nav and section blocks
- **Mono eyebrow badges** inside bordered pills, uppercase and letter-spaced
- **Hatched/striped divider bands** between sections
- **A single green status dot** as the only color, inside voice-toggle pills
- **White-filled primary buttons** + hairline-bordered secondary buttons
- Circular play buttons; waveform visualizations rendered in white on black

## 5. Shape & spacing rules
- **radius:** cards ~10–12px; buttons ~8px; pill badges fully round
- **section_padding:** ~110px vertical
- **card_padding:** ~24px
- **shadow:** none — depth is hairline borders (#262626) + selective halftone glow, never drop shadows
- **borders:** 1px #262626 everywhere, including the bracket-corner frames

## 6. Imagery
- **style:** monochrome generative/technical — halftone dot fields, waveforms, wireframe globes; no stock people, no color photos
- **treatment:** white-on-black, framed in bordered panels; soft radial fade at the edges
- **source:** generate/render texture locally; use Unsplash/Pexels only for grayscale abstracts (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the single status accent (green → cyan/amber) and the exact near-black temperature — nothing else
- **must NOT change on remix:** the black monochrome base, the halftone imagery, the corner-bracket frames, mono eyebrow badges, the border-not-shadow depth model, and white-on-black buttons
