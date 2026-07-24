# Style Spec — 07 flexfit-bento

**Real extraction** from `references/65550e0cb0b849449ea6e1c9569aa0e5.jpg` ("FlexFit").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** flexfit-bento
- **one-line:** Bold black bento — a 2×2 grid of chunky cards, ultra-heavy condensed uppercase display, acid-yellow accent and one salmon card, filling a single confident screen.
- **best_for:** fitness, sport, streetwear, events, bold consumer brands that want maximal attitude and a single-viewport statement.
- **avoid_for:** enterprise, finance, wellness/calm, or text-heavy long-form pages.

## 1. Palette (named hex + role — never just "yellow")
- **bg:** #0F0C0D   (near-black, the grid gutter/ground)
- **surface:** #FFFFFF   (the white bento cards)
- **ink:** #0F0C0D   (black — display type on white, and the ground)
- **accent:** #F5DD0B   (acid yellow — THE accent: round buttons, marker blocks)
- **accent_soft:** #E7B2AA   (salmon — a single filled card, one accent among white)
- **muted:** #6A6A6A   (secondary text)
- **line:** #ECECEC   (hairlines inside white cards, pill borders)
- **accent_usage_rule:** yellow is the one accent — round arrow buttons, the black+yellow "flag" marker blocks, a highlight behind a portrait. Salmon fills exactly ONE card. Everything else is black, white, and the photo.

## 2. Type
- **display_face:** ultra-bold CONDENSED grotesque (Druk / Anton / a compressed heavy face) — set uppercase, huge
- **body_face:** a normal-width grotesque for labels and body
- **h1:** condensed, weight 800, size clamp(40px→92px), line-height 0.92, uppercase, letter-spacing 0
- **h2:** condensed heavy, uppercase, ~26–36px
- **body/labels:** grotesque, weight 500–600, 12–14px, uppercase for labels with letter-spacing 0.06em
- **eyebrow:** uppercase micro-label preceded by a black+yellow block pair (e.g. "TIME FOR FITNESS — 23")
- **two_tone_headline:** no — single black on white; punch comes from weight and scale

## 3. Layout skeleton (bento — one confident screen)
1. Nav (black bar) — wordmark + mark left; center links (ABOUT / SCHEDULE / STORE / CONTACT); right a ghost pill ("JOIN OUR GYM") + a yellow round arrow button
2. Bento 2×2 grid on the black ground:
   - **top-left (white, tall):** a black+yellow block eyebrow, a huge condensed uppercase headline, a black pill CTA + a small waveform + a "LUXURY FITNESS EXPERIENCE" label
   - **top-right (photo):** a full-bleed athlete photo with a corner icon tile and an overlaid uppercase caption ("TRAIN ON YOUR OWN TIME")
   - **bottom-left (salmon):** a portrait cutout on a yellow block + "24/7 SUPPORT" + address + an uppercase line ("CONTACT US & RISE STRONGER")
   - **bottom-right (white):** a big rating number ("4.98") + stars + a wrapped set of amenity pill tags (BOXING RING / BASKETBALL COURTS / JUICE BAR / …)

## 4. Signature moves (the memorable, must-keep specifics)
- **2×2 bento card grid filling one screen** on a black ground — the defining structure
- **Ultra-bold condensed uppercase display** at enormous scale
- **Black + yellow "flag" block pairs** as eyebrow markers
- **Acid-yellow round arrow buttons**
- **One salmon card** among the white ones (the single soft accent)
- **A big rating number + stars**, and **amenity pill tags** that wrap
- **Portrait cutouts** placed on yellow highlight blocks

## 5. Shape & spacing rules
- **radius:** cards ~20–24px; pills fully round; the whole grid sits in a rounded black frame
- **section_padding:** tight — the bento is the page; gutter/gap ~14–18px between cards
- **card_padding:** ~28–34px
- **shadow:** minimal; separation comes from the black gutter between cards, not shadow
- **borders:** hairline #ECECEC only inside white cards (pill tags)

## 6. Imagery
- **style:** high-attitude studio portraits — athletes, streetwear, confident poses; warm/dramatic lighting
- **treatment:** full-bleed inside a bento card, or a cutout portrait on a yellow block; uppercase caption overlays
- **source:** Unsplash/Pexels API server-side, prefer studio-portrait/fitness queries (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the accent yellow (→ another single electric hue) and the one salmon card (→ another single soft tint) — as a pair
- **must NOT change on remix:** the black bento structure, the ultra-condensed uppercase display, the black+yellow flag markers, round arrow buttons, exactly-one-soft-accent-card, and the single-viewport confidence
