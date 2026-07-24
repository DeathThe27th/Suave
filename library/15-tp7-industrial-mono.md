# Style Spec — 15 tp7-industrial-mono

**Real extraction** from `references/4a3bbbb99ee8eb35e8b75f373582f061.jpg` ("TP-7" audio device).
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** tp7-industrial-mono
- **one-line:** Teenage-Engineering industrial minimalism — a warm-gray canvas, an oversized ultra-bold black wordmark cut behind a centered product shot, monospace uppercase spec-captions, and a diagonal orange gradient wash, all inside one rounded pill-toolbar frame.
- **best_for:** hardware, audio/synth gear, dev tools, gadgets, physical products, "engineered" premium goods that want a technical, catalog-spec feel.
- **avoid_for:** soft consumer/wellness, luxury-emotional, editorial-serif, or anything photographic-lifestyle; the mono captions and industrial coldness fight warmth.

## 1. Palette (named hex + role — never just "gray")
- **bg:** #E9E7E3   (warm light gray, the outer canvas)
- **surface:** #FFFFFF   (the rounded hero frame / cards, soft-white)
- **ink:** #16130E   (near-black — the oversized display letters, buttons)
- **accent:** #F5872E   (industrial orange — the diagonal gradient wash and one nav segment)
- **accent_soft:** #F9C79A   (pale orange, the far end of the gradient)
- **muted:** #8B8880   (mono caption gray)
- **line:** #D5D2CC   (hairlines, dashed outlines)
- **accent_usage_rule:** orange appears as ONE diagonal corner-to-corner gradient wash behind the product, and ONE filled nav segment ("Features"). It may also tint a status LED on the product. It must NOT color body text, headlines, or more than a single toolbar segment; everything structural stays ink-on-white.

## 2. Type
- **display_face:** an ultra-bold neo-grotesque (Helvetica Now Black / Neue Haas Black feel) — set as huge graphic letters, tight
- **body_face:** a **monospace** (a JetBrains/Space-Mono feel), UPPERCASE, for every caption, spec, and micro-label
- **h1 (display letters):** weight 800–900, size clamp(90px→240px), line-height 0.85, letter-spacing -0.02em, ink; positioned so the product photo overlaps the letters
- **h2:** weight 800, ~28–40px, tight
- **body:** monospace, weight 400–500, 11–13px, line-height 1.5, UPPERCASE, letter-spacing 0.02em, muted gray
- **eyebrow:** monospace uppercase micro-label, 10–11px, muted, sometimes prefixed with a price ("$1799") or status ("NOW AVAILABLE")
- **two_tone_headline:** no — the display is single ink; the orange lives only in the gradient, never the type

## 3. Layout skeleton (section order + structure)
1. Nav — a single rounded **pill toolbar** spanning the top: circular logo chip, segmented text buttons (one ink-filled "News", one orange-filled "Features", ghost ones), a **dashed-outline** rounded search pill ("DISCOVER ALL OUR PRODUCTS"), a dark "Subscribe" pill, and a "#" square button
2. Hero — a large rounded soft-white frame: oversized ink display letters (e.g. "TP") behind a centered, hand-held product photograph; a diagonal orange gradient wash bleeding from a corner; a dashed-circle ▶ play button; a row of monospace uppercase micro-captions ("$1799 · NOW AVAILABLE · ONE OF A KIND · AUDIO · DEVICE") along a baseline; a left mono spec-paragraph and a right mono bulleted spec-list
3. Spec strip — a horizontal rule of monospace key/value tech specs
4. Features — 2–3 rounded white cards, each a product detail crop + a mono caption
5. Buy / CTA — a large ink pill button with price, mono supporting line
6. Footer — mono uppercase link columns, a repeated "#" motif, quiet

## 4. Signature moves (the memorable, must-keep specifics)
- **Oversized ink display letters cut BEHIND a centered product photo** (hand-held), photo overlapping the type
- **Everything captioned in UPPERCASE MONOSPACE** — prices, specs, statuses, nav search
- **One diagonal orange gradient wash** bleeding from a corner across the hero
- **A single rounded pill toolbar** holding the whole nav, with a **dashed-outline search pill** and exactly one orange-filled + one ink-filled segment
- **Dashed-circle play/CTA affordances** (dashed 1px rings)
- **A baseline row of dot/pipe-separated mono micro-captions** under the product
- **Bulleted mono spec-list** (• 24-BIT/96 KHZ …) as real content, catalog-style

## 5. Shape & spacing rules
- **radius:** hero frame ~24px; cards ~18px; pills fully round; the search pill uses a 1px dashed border
- **section_padding:** ~80px vertical
- **card_padding:** ~24px
- **shadow:** soft and low, e.g. 0 30px 60px -34px rgba(20,19,14,.18); the frame floats slightly off the canvas
- **borders:** hairline #D5D2CC; dashed 1px #C7C4BE on search/play affordances

## 6. Imagery
- **style:** clean studio product photography — a single object, often hand-held, neutral light, sharp; no lifestyle scenes
- **treatment:** product centered and overlapping the oversized letters; orange gradient wash behind; no drop-shadow theatrics
- **source:** Unsplash/Pexels API server-side (never hotlink-scrape at request time) — favor isolated product / object shots on neutral grounds

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the single industrial orange (→ one other saturated hue: electric-blue / acid-green / red) applied to the gradient wash + the one filled nav segment + the status LED, moved together
- **must NOT change on remix:** the warm-gray/white ground, the oversized-display-behind-product move, the UPPERCASE-MONOSPACE caption system, the single pill toolbar with dashed search, the dashed-ring affordances, and the mono spec-list
