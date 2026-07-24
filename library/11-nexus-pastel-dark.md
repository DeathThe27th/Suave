# Style Spec — 11 nexus-pastel-dark

**Real extraction** from `references/979e47376e71751419034d39a3089010.jpg` ("nexus").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** nexus-pastel-dark
- **one-line:** Near-black ground carrying soft pastel cards — sage green and powder blue — with one word highlighted in a green pill, connected pill-and-circle buttons, and blob-gradient stat cards.
- **best_for:** agencies, marketing/growth, creative studios, and friendly-but-premium services that want a dark, confident base warmed by playful pastel data.
- **avoid_for:** austere/minimal briefs, dev tools, or high-density dashboards.

## 1. Palette (named hex + role — never just "green")
- **bg:** #151619   (near-black with a faint cool cast, primary background)
- **surface_dark:** #1D1F22   (raised dark cards / review card)
- **ink:** #F4F4F4   (primary text on the dark ground)
- **ink_on_pastel:** #17251C   (dark text used inside the light pastel cards)
- **accent:** #B7D9C4   (sage green — the highlight pill + one filled card)
- **powder:** #BED7E4   (powder blue — a second pastel card fill)
- **teal:** #28596B   (deep teal — the blob-gradient stat card)
- **muted:** #8A8C8C   (secondary text on dark)
- **line:** #2A2D30   (hairlines on the dark ground)
- **accent_usage_rule:** color lives in the CARDS, not the type. The dark ground stays neutral; pastel sage/powder/teal fills carry warmth. Exactly one word of the headline gets a sage-green highlight pill. Primary buttons are white pills; the sage is a fill, not a text color.

## 2. Type
- **display_face:** friendly humanist grotesque (medium weight, soft terminals)
- **body_face:** same family, regular; muted on dark
- **h1:** weight 500–600, size clamp(28px→48px), line-height 1.1, letter-spacing -0.01em; mixed weight across the line
- **h2:** weight 500, ~24–32px
- **body:** weight 400, size 14–15px, line-height 1.55
- **eyebrow:** small, muted; card titles are medium-weight
- **two_tone_headline:** yes, but as a HIGHLIGHT — one word wrapped in a sage-green pill (not a color change), often with a hand-drawn squiggle flourish beneath another word

## 3. Layout skeleton (section order + structure)
1. Nav (on the dark panel) — wordmark + mark left; center links; right a white "Sign In" pill
2. Hero — a large white headline with ONE word inside a sage-green highlight pill and a hand-drawn squiggle under another; on the right a dark review card ("1300+ customer reviews") with an avatar stack, and two white pill tags below ("Marketing", "Search Engine OPT")
3. Card row — three cards of MIXED pastel fill in one row:
   - a powder-blue "Global partners" card (2 small icon+text columns) with a white circular ↗ button
   - a deep-teal blob-gradient card with a big stat ("50K") + caption
   - a sage-green card with a big stat ("1400+") + a small bar chart
4. …continues in the same system (services, team, contact) — dark ground, pastel cards
5. Footer — quiet, on the dark ground

## 4. Signature moves (the memorable, must-keep specifics)
- **Near-black ground carrying soft PASTEL cards** (sage + powder-blue + teal) — the defining contrast
- **One headline word highlighted in a sage-green pill**
- **Hand-drawn squiggle flourish** under a word
- **Connected pill-and-circle buttons** (a pill fused to a round ↗ button)
- **Avatar-stack social proof** ("1300+ …")
- **Blob-gradient stat card** + **bar-chart stat card** as siblings
- Big, generous rounding throughout

## 5. Shape & spacing rules
- **radius:** cards ~20–24px; pills fully round; the outer panel ~28px
- **section_padding:** ~80–96px vertical
- **card_padding:** ~26–30px
- **shadow:** soft, low; on dark, separation is mostly the pastel fill vs. near-black ground
- **borders:** hairline #2A2D30 on dark; pastel cards are borderless

## 6. Imagery
- **style:** mostly non-photographic — abstract teal/blue blob gradients, avatar clusters, small charts; illustration-light
- **treatment:** blob gradients fill a card; avatars in a row; charts drawn in the ink-on-pastel color
- **source:** generate gradients/charts in CSS; Unsplash/Pexels only for avatar-style photos (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the pastel set (sage / powder-blue / teal) can rotate hue together toward another soft pairing; the ground stays near-black
- **must NOT change on remix:** the dark-ground-with-pastel-cards contrast, the highlight-pill word, the squiggle flourish, connected pill-and-circle buttons, and the blob/bar stat cards
