# Style Spec — 13 gabrun-blue

**Real extraction** from `references/download.png` ("Gabrun"). Palette sampled from
pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** gabrun-blue
- **one-line:** Friendly bright-blue fintech — a saturated blue gradient hero, blue two-tone headlines, glassy white finance cards floating on a faint blueprint grid, and pill-shaped everything.
- **best_for:** payments, fintech, banking, SaaS onboarding — approachable products that want to feel trustworthy, modern, and energetic without going dark or technical.
- **avoid_for:** luxury-minimal, editorial, or somber/serious brands; anything that should avoid a "startup SaaS" read.

## 1. Palette (named hex + role — never just "blue")
- **bg:** #FFFFFF   (white, primary background)
- **hero:** linear gradient #2F6BE0 → #73B4F2   (the saturated blue hero panel)
- **surface:** #FFFFFF   (glassy white cards)
- **ink:** #12141A   (near-black — headlines, body)
- **accent:** #2F6BE0   (brand blue — buttons, the blue word in two-tone headlines, stats)
- **accent_soft:** #EAF2FE   (pale blue tint — chips, card washes)
- **muted:** #7A828E   (secondary text)
- **line:** #E7ECF3   (hairlines, card borders)
- **grid:** #EDF2FB   (the faint blueprint/dotted grid behind card sections)
- **accent_usage_rule:** blue is generous but disciplined — the hero gradient, primary buttons, ONE gradient feature card, the emphasized phrase in each headline, and stat figures. Body stays ink; secondary surfaces stay white/pale-blue. One saturated blue-gradient card per feature row, never all of them.

## 2. Type
- **display_face:** friendly rounded grotesque (soft, geometric — a warmer Poppins/Jakarta feel)
- **body_face:** same family, regular; muted
- **h1:** weight 700, size clamp(30px→52px), line-height 1.1, letter-spacing -0.01em; white on the hero, ink elsewhere
- **h2:** weight 700, ~28–36px, with ONE phrase set in brand blue (two-tone)
- **body:** weight 400, size 14.5–16px, line-height 1.6
- **eyebrow:** a small pill badge with an icon + micro-label
- **two_tone_headline:** yes — one phrase in brand blue, the rest ink (e.g. "…and **Easy to Use** Payment Software")

## 3. Layout skeleton (section order + structure)
1. Nav — wordmark + mark left; center links (or minimal); right a dark "Menu" pill
2. Hero — a rounded saturated-blue gradient panel: a small pill badge, a large white two-tone headline with an inline app-icon glyph ("…with 🔷 Gabrun"), an email input + a dark "Get Started" pill; floating glassy white finance cards overlapping the panel (a "PayPal Payment $3,050" card, a person card, an income/expenses mini-card)
3. Trust — "Trusted By More Than **+10,000** Users" (the number in blue) + a row of logos rendered as rounded PILLS (PayPal / Notion / Slack / Loom / Monday / Afterpay)
4. Features — a two-tone h2 + a pill TAB switcher (Start-ups / Freelancers / Enterprises) over 3 feature cards, the middle one a BLUE gradient card among white
5. Rewards — a two-tone h2 + an invoice/receipt card with a blue-gradient "Pay Invoice" button
6. Security — a two-tone h2 + floating avatar-and-amount pills scattered around a central balance card
7. Speed — a two-tone h2 + a payment card; faint blueprint grid lines run behind the card sections
8. Footer — link columns, quiet

## 4. Signature moves (the memorable, must-keep specifics)
- **Saturated blue gradient hero panel** (rounded) — the defining ground
- **Blue two-tone headlines** — one phrase in brand blue per heading
- **Glassy white finance cards** floating and overlapping the hero, each with mini stats
- **Logos rendered as rounded PILLS**, not a plain grayscale strip
- **Pill TAB switchers** above feature cards
- **Exactly one blue-gradient feature card** among white siblings
- **A faint blueprint / dotted grid** behind card sections
- **An inline app-icon glyph** dropped into the headline; pill-shaped everything

## 5. Shape & spacing rules
- **radius:** hero panel ~28px; cards ~18–24px; pills fully round; inputs pill/rounded
- **section_padding:** ~96px vertical
- **card_padding:** ~24–28px
- **shadow:** soft, blue-tinted, low (e.g. 0 24px 50px -28px rgba(47,107,224,.28))
- **borders:** hairline #E7ECF3 on white cards; the grid is #EDF2FB

## 6. Imagery
- **style:** UI/product mockups (payment screens, dashboards, cards), soft and clean; little to no stock photography
- **treatment:** glassy white cards with soft blue shadows floating over the gradient; mini charts and figures rendered in blue
- **source:** compose UI cards in HTML/CSS; Unsplash/Pexels only for the occasional avatar (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the brand blue (→ another single saturated hue: indigo / teal / violet) applied to the hero gradient, buttons, two-tone phrase, and the one gradient card together
- **must NOT change on remix:** the gradient-hero + two-tone-headline pattern, floating glassy finance cards, logo-as-pills, pill tab switchers, one-gradient-card-per-row, and the faint blueprint grid
