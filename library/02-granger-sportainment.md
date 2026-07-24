# Style Spec — 02 granger-sportainment

**Real extraction** from `references/76c9833e8e2e5d2057edc2ab7c213755.jpg` (the "Granger"
sportainment/wellness landing page). Palette hexes were sampled from the pixels, not
eyeballed. ⚠️ Pending the human by-eye verification step (EXTRACT.md) before it's trusted.

## 0. Identity
- **id:** granger-sportainment
- **one-line:** Vivid sport-editorial: cool off-white canvas, true-black cards, single hot-orange accent, and an oversized wordmark that bleeds across the hero and footer.
- **best_for:** energetic lifestyle/consumer brands — sport, wellness, fitness, events, community products; strong with bold action photography and a memorable name.
- **avoid_for:** enterprise/technical, luxury-minimal, or somber briefs (too loud and playful).

## 1. Palette (named hex + role — never just "orange")
- **bg:** #F5F6FB   (cool off-white, primary background)
- **surface:** #FFFFFF   (cards, panels)
- **ink:** #0A0A0A   (text, black cards, black pill buttons — true black, not navy)
- **accent:** #DD4F09   (hot orange — ONE accent)
- **accent_soft:** #FBE7DE   (rare orange tint for a chip/badge)
- **muted:** #8B8F98   (secondary text)
- **line:** #E6E8EF   (hairlines, accordion dividers; cards are mostly borderless)
- **accent_usage_rule:** orange touches ONLY: the round arrow buttons, ONE highlighted row inside the black section, eyebrow dots, small badges/chips (New / Boost / Sale), and stat accents. Never a large fill except that single orange row and the round buttons. Black — not orange — carries the primary buttons.

## 2. Type
- **display_face:** tight modern grotesque (PP Neue Montreal / Neue Haas Grotesk feel) — geometric, medium-bold
- **body_face:** same grotesque, regular/medium weights
- **wordmark (oversized):** weight 700–800, enormous — clamp(96px→22vw), letter-spacing -0.03em; bleeds off the container edges
- **h1/h2:** weight 600–700, size clamp(30px→52px), line-height 1.05, letter-spacing -0.02em
- **body:** weight 400–500, size 15–16px, line-height 1.55; muted for supporting copy
- **eyebrow:** weight 600, 12px, uppercase, letter-spacing 0.08em, prefixed with a small "• " dot (orange or ink)
- **two_tone_headline:** no strict two-tone — emphasis instead via inline rounded EMOJI glyphs embedded in the headline (see signature moves)

## 3. Layout skeleton (section order + structure)
1. Nav — left wordmark "granger" + square mark, tiny "CUSTOM WELLNESS" label beneath; center links (Program, Product [New badge], Events, About); right "GET IN TOUCH"; overlaid on the hero photo in white
2. Hero — full-bleed action photo; small eyebrow line + one orange pill note top-left; OVERSIZED white wordmark bleeding across the bottom of the photo
3. Benefit — eyebrow "• THE BENEFIT"; h2 with inline emoji; left column of chips + an expandable "Connections" accordion + "Sport Package +"; right: small "EST — 1997" card, a titled block with a black "Join Now!" pill, and a tinted photo card carrying a floating stat ("86% Boost") + a "Sale" badge
4. Program — eyebrow "• THE PROGRAM"; h2 with inline emoji; left: big "01 /B" slash-fraction numeral + a black card (with "Live" + url pills) + left/right nav arrows and an orange round arrow; right: supporting text + a green-tinted photo card with member avatars/stats
5. Featured — left: photo card with a floating white stat card ("2.780 Cal", mini line chart, legend); right: eyebrow + h2 with inline emoji + glyph-tile chips + "WITH GPT 4.0" + orange round arrow + "EXPLORE MORE" + a small circular "COMING SOON 2025 / Mood Boost" photo chip
6. Current Events (BLACK section) — large white h2 with inline emoji on true black; a stacked list of rows each ending in a ↗; exactly ONE row filled hot-orange with sub-pills and a photo thumbnail
7. Testimonials — h2 with inline emoji; eyebrows "• Testimonial / Customer Says"; left: quote card with "1/20", a star rating (4.5), name + role, orange round arrow; right: a big photo card ("Single Session", "APR — MAY 2025") with a "$99 / Session" price-tag overlay and role chips
8. Final CTA — white rounded panel: left small photo chip + h2; access chips; right: 4 link columns (Program/Product/Event/About → socials), locations, contact email, a big orange starburst mark
9. Footer — OVERSIZED black wordmark "Granger" bleeding across the bottom; a thin links row and a fine "Privacy • EST — 2018 • Terms" row above it

## 4. Signature moves (the memorable, must-keep specifics)
- **Oversized wordmark bleed** — the brand name set enormous, bleeding off-edge across the hero (white on photo) and again in the footer (black). This is THE move.
- **Inline rounded emoji glyphs** embedded mid-headline (e.g. "Explore 🏀 our flexible activity")
- **Dot eyebrows** — "• " prefix, uppercase, small, letter-spaced
- **Black pill primary buttons + orange circular arrow buttons** (↗ / →)
- **Floating stat cards over photos** — big number + tiny label + mini line chart, clipped over a photo corner
- **One black full-width section** with a single orange-highlighted row among dark rows, every row ending in ↗, sub-pills inside the highlighted one
- **Slash-fraction numerals** for sequence ("01 /B")
- **Price-tag overlays** on photo cards ("$99 / Session")
- **Orange starburst / asterisk mark** as the sole ornament

## 5. Shape & spacing rules
- **radius:** cards/panels ~24px; photo cards ~20px; glyph chips ~14px; pills fully round
- **section_padding:** ~110px vertical
- **card_padding:** ~28–32px
- **shadow:** soft, large, low-opacity, downward (e.g. 0 30px 60px -24px rgba(10,10,12,.22)); cards mostly borderless on the off-white bg
- **borders:** hairline #E6E8EF only, used sparingly (accordion dividers, some chips)

## 6. Imagery
- **style:** vivid, high-saturation real sport photography — courts, balls, athletes in context; warm and cool tones both welcome
- **treatment:** rounded cards; some tinted (red/green color overlays); floating stat cards and small circular photo chips clipped over them
- **source:** Unsplash/Pexels API server-side (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the accent orange (→ another single vivid hue), the bg temperature (cool ↔ warm off-white), and photo tint — as a coordinated set
- **must NOT change on remix:** the oversized-wordmark bleed, the inline-emoji headlines, black-pill + orange-round-arrow buttons, the single-orange-row black section, the floating stat cards, the dot eyebrows, and the soft radius/shadow character
