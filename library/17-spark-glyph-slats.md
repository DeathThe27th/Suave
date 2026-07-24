# Style Spec — 17 spark-glyph-slats

**Real extraction** from `references/8f20d736786e405284ad2112edebf3a6.jpg` ("Spark" marketing).
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** spark-glyph-slats
- **one-line:** Pale-periwinkle marketing dashboard — a big UPPERCASE grotesque headline with little pill/glyph icons dropped *inside* the words, a row of numbered vertical "slat" panels (01–06) with rotated labels beside a blue-duotone image, and a stat row of icon tiles, all inside one rounded white app frame.
- **best_for:** marketing/growth agencies, analytics, SaaS with "capabilities" to show off, data-forward B2B — brands that want busy-but-organized, confident, iconographic.
- **avoid_for:** luxury-minimal, editorial, calm/wellness, or anything that needs quiet; this style is dense and playful with icons.

## 1. Palette (named hex + role — never just "blue")
- **bg:** #E9ECF6   (pale periwinkle, the outer canvas)
- **surface:** #FFFFFF   (the rounded app frame + cards)
- **ink:** #10131C   (near-black — headline, body)
- **accent:** #4A5FD6   (periwinkle-blue — filled slats, pills, the map glyph, social chips)
- **accent_soft:** #C9D2F3   (pale blue — lighter slats, tag chips, tints)
- **muted:** #838BA0   (secondary text, stat labels)
- **line:** #E4E8F3   (hairlines, stat-tile borders)
- **accent_usage_rule:** blue carries the vertical slats (alternating full #4A5FD6 and soft #C9D2F3), the primary pills, one or two inline headline glyphs, and social chips. Body stays ink; stat tiles stay near-white with hairline borders. Never flood a section fully blue except the numbered slats and the duotone image.

## 2. Type
- **display_face:** a bold neo-grotesque (Helvetica/Arial-black feel), UPPERCASE, tight — set large
- **body_face:** the same grotesque, regular
- **h1:** weight 700, size clamp(34px→64px), line-height 1.02, letter-spacing -0.005em, UPPERCASE, ink, with **inline glyphs** substituted between words
- **h2:** weight 600, ~22–28px, sentence case
- **body:** weight 400, 14–15px, line-height 1.55, muted
- **eyebrow:** weight 600, 12px, ink; small pill tabs (e.g. "• Home" active pill in nav)
- **two_tone_headline:** partial — the words stay ink, but small **blue pill/glyph tokens** (a map pill, a spark/asterisk, a flower/cog mark) sit inline in the sentence as the "color"

## 3. Layout skeleton (section order + structure)
1. Nav — inside the white frame: logo left (mark + wordmark), a centered **pill nav group** with one filled active tab ("• Home"), a right blue "Get started →" pill
2. Hero headline — a large UPPERCASE multi-line statement with **inline glyph tokens** dropped between words (a blue map-pill, an asterisk-spark, a small mark); a small right-side "label: sentence" microcopy block
3. Capability rail — a wide panel: LEFT a **blue-duotone image** with floating tag chips (SEO / Digital Marketing / Content Strategy…) and a corner index "01"; RIGHT a row of **numbered vertical slat panels 02–06**, each a tall rounded column filled full-blue or soft-blue, with a **vertically rotated label** (Marketing / Innovate / Elevate / Transform) and a circled number at its foot; one slat expands into a mini feature card ("Spark Your Creativity", "Explore Now ↓")
4. Stat row — a small label block ("Fueling growth with data Insights" + a blue "Create project →" pill) beside a row of **near-white stat tiles**, each: a small square icon + a caption + a big figure (2.3M / 35% / 2,341 / +83.3%)
5. Social — round blue social chips (Behance / IG / X)
6. Body sections — feature grids reusing the icon-tile + pill vocabulary
7. Footer — link columns, quiet, inside the frame

## 4. Signature moves (the memorable, must-keep specifics)
- **Inline glyph/pill tokens dropped INSIDE the headline** (a map pill, a spark, a mark between words) — the defining move
- **Numbered vertical slat panels (01–06)** with **rotated vertical labels** and circled foot-numbers, one slat expanding into a feature card
- **A blue-duotone hero image** carrying floating tag chips
- **Everything wrapped in one rounded white app frame** floating on a pale-periwinkle ground
- **Pill-group nav** with a single filled active tab
- **Near-white stat tiles** with tiny square icons + big figures
- **Round social chips** in accent blue

## 5. Shape & spacing rules
- **radius:** app frame ~28px; slats/cards ~16–20px; pills fully round; stat tiles ~12px
- **section_padding:** ~64px vertical (denser than most specs)
- **card_padding:** ~18–22px
- **shadow:** the app frame gets one soft 0 40px 90px -40px rgba(74,95,214,.20); tiles are flat with hairline borders
- **borders:** hairline #E4E8F3 on stat tiles and chips; slats borderless (defined by fill)

## 6. Imagery
- **style:** abstract 3D renders (soft spheres, cloth/paper forms) recolored to blue duotone; plus a small figure cut-out inside a feature slat
- **treatment:** hero image forced to a single-blue **duotone**; overlaid with translucent tag chips and a corner index number; slats are flat color, not photographic
- **source:** Unsplash/Pexels API server-side (never hotlink-scrape at request time) — favor abstract 3D/soft-body renders that duotone cleanly

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the periwinkle-blue system (→ one other hue: indigo / teal / violet) applied together to slats, pills, inline glyphs, duotone image, and social chips
- **must NOT change on remix:** the inline-glyphs-in-headline move, the numbered vertical slats with rotated labels, the duotone hero image with tag chips, the single rounded app frame, the pill-group nav, and the near-white stat-tile row
