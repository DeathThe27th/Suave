# Style Spec — Library Entry Format (blank template)

Every style in `/library/` is one file in this exact shape. An extraction fills every
field by reading a reference image. **No field is optional.** "Vibe words" are banned as
the *only* description of anything — every choice must be concrete (hex, px, weight, order).

A worked example lives in `style-spec-template.md` and in `library/01-swiftlogix-warm.md`.
Copy this file, rename it `NN-<id>.md`, and fill every `<...>` slot.

---

## 0. Identity
- **id:** <kebab-case-unique-id>
- **one-line:** <one sentence naming the single most memorable thing about the style>
- **best_for:** <product kinds this fits; Suave uses this to auto-pick a style>
- **avoid_for:** <briefs where this style actively hurts>

## 1. Palette (named hex + role — never just "orange")
- **bg:** <#hex>   (<role>)
- **surface:** <#hex>   (cards, panels)
- **ink:** <#hex>   (primary text / headlines)
- **accent:** <#hex>   (the ONE accent)
- **accent_soft:** <#hex>   (accent tint)
- **muted:** <#hex>   (secondary text)
- **line:** <#hex>   (dividers, hairlines)
- **accent_usage_rule:** <exactly where the accent may touch — and where it may NOT>

## 2. Type
- **display_face:** <face + why>
- **body_face:** <face>
- **h1:** weight <n>, size clamp(<min>→<max>), line-height <n>, letter-spacing <n>em
- **h2:** weight <n>, size <n>, letter-spacing <n>em
- **body:** weight <n>, size <n>, line-height <n>
- **eyebrow:** weight <n>, <n>px, <prefix?>, <color>
- **two_tone_headline:** <yes/no — how>

## 3. Layout skeleton (numbered section order + structure)
1. <Nav — structure>
2. <Hero — structure>
3. <...>
9. <Footer — structure>

## 4. Signature moves (the memorable, must-keep specifics)
- <the field that decides quality — list the concrete, reproducible moves>

## 5. Shape & spacing rules
- **radius:** <cards / tiles / pills>
- **section_padding:** <n>px vertical
- **card_padding:** <n>px
- **shadow:** <exact character, e.g. 0 40px 80px -30px rgba(...)>
- **borders:** <weight + color, or "none">

## 6. Imagery
- **style:** <photo style>
- **treatment:** <how images are framed / overlaid>
- **source:** Unsplash/Pexels API server-side (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** <the coordinated set that may shift>
- **must NOT change on remix:** the layout skeleton, the signature moves, the spacing/shape rules
