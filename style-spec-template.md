# Style Spec — Library Entry Format

Every style in the library is one file in this exact shape. Claude Code fills every
field by reading a reference image. No field is optional. "Vibe words" are banned as
the only description of anything — every choice is concrete (hex, px, weight, order).

The point: a spec is tight enough that two different products generated from it look
like siblings, and neither looks like a raw-model default.

---

## 0. Identity
- **id:** swiftlogix-warm-logistics
- **one-line:** Warm light-gray editorial SaaS, single coral accent, floating photo hero with ghost watermark.
- **best_for:** products that want to feel energetic, trustworthy, modern; strong with a hero object/photo.
- **avoid_for:** luxury-minimal or dark-technical briefs (accent is too warm/friendly).

## 1. Palette (named hex + role — never just "orange")
- **bg:** #F1F0ED   (warm light gray, primary background)
- **surface:** #FFFFFF   (cards, panels)
- **ink:** #1A1E2C   (primary text / headlines)
- **accent:** #EA5C2B   (coral — ONE accent, used sparingly)
- **accent_soft:** #FBE7DE   (accent tint for glyph tiles)
- **muted:** #9AA0A8   (secondary text)
- **line:** #E4E2DE   (dividers, hairlines)
- **accent_usage_rule:** accent touches ONLY: one headline word, // eyebrows, stat suffixes, glyph tiles, one filled testimonial card. Never on body text or large fills.

## 2. Type
- **display_face:** Plus Jakarta Sans (geometric, friendly-bold)
- **body_face:** Plus Jakarta Sans (same family, lighter weights)
- **h1:** weight 800, size clamp(34px→62px), line-height 1.04, letter-spacing -0.03em
- **h2:** weight 700–800, size ~34–40px, letter-spacing -0.02em
- **body:** weight 400–500, size 14.5–16px, line-height 1.6
- **eyebrow:** weight 600, 13px, prefixed with "// ", in accent
- **two_tone_headline:** yes — first phrase in accent, remainder in ink

## 3. Layout skeleton (section order + structure)
1. Nav — left wordmark w/ square mark, center links, right outline pill CTA
2. Hero — ghost watermark behind; large photo panel (rotated ~-1deg, radius 20px); round badge top-left; small photo+text card clipped to bottom-right corner; two-tone headline BELOW the photo
3. About — 2-col: faded ghost SVG illustration left / eyebrow + dark→muted two-tone h2 + hairline + 3-stat row right
4. Advantages — header row (h2 left / supporting text + black pill right) then 2×2 white cards, each with accent-soft glyph tile bottom-right
5. Process — one white rounded panel, 3 steps as icon tiles + arrows
6. Testimonials — 3 cards, ONE filled accent card among white
7. FAQ — 2-col: heading left / plus-style accordion right
8. Final CTA — white rounded panel, centered, radial accent glow, mark + h2 + 2 pills
9. Footer — hairline top, copyright left / compliance-ish line right

## 4. Signature moves (the memorable, must-keep specifics)
- Oversized ghost brand-name watermark bleeding behind hero (~17vw, accent at ~7% opacity)
- Hero photo panel slightly rotated with a small photo card overlapping its corner
- "// " eyebrow prefix on every section label
- Two-tone bold headline (accent phrase + ink phrase)
- Black pill buttons with a trailing arrow → ; secondary is outline pill
- Glyph tiles: rounded accent-soft square with a thin-stroke accent icon
- Stats: big number, accent-colored suffix (+ / %)

## 5. Shape & spacing rules
- **radius:** cards/panels 20px; glyph tiles 18px; pills fully round (30px)
- **section_padding:** ~96px vertical
- **card_padding:** ~34px
- **shadow:** soft, large, low-opacity, downward (e.g. 0 40px 80px -30px rgba(ink,.4)); never hard/tight
- **borders:** hairline #E4E2DE only; no heavy outlines

## 6. Imagery
- **style:** real photography, warm-lit, object-forward (documents, product, people-in-context)
- **treatment:** rounded panel, subtle accent gradient overlay; cutouts are phase-2
- **source:** Unsplash/Pexels API server-side (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** accent, accent_soft, bg temperature, ink — as a coordinated set
- **must NOT change on remix:** the layout skeleton, the signature moves, the spacing/shape rules
- (This is what keeps a remix from drifting back to generic.)
