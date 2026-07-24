# Style Spec — 20 musmentor-outline-bento

**Real extraction** from `references/323ab834d82bb6e589b1fc0aeb4fc479.jpg` ("Musmentor").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** musmentor-outline-bento
- **one-line:** Cream neo-brutalist bento — thin black-outline rounded cards on a warm-cream frame, orange-red diamond bullets and butter-yellow highlight pills, fused two-tone pill buttons, and playful catalog motifs (a barcode ticket, a struck-through price, a review-diamonds row).
- **best_for:** courses/education, community, events, indie SaaS, marketplaces, playful startups — brands that want friendly-but-structured, tactile, "sticker-sheet" energy.
- **avoid_for:** luxury-minimal, corporate-serious, finance-trust, or moody/cinematic brands; the outlines and pops read as approachable and craft-y, not premium-somber.

## 1. Palette (named hex + role — never just "yellow")
- **bg:** #E7E1D5   (warm cream — the outer frame/margin)
- **surface:** #FFFFFF   (white outline cards) and #EDE7DB (tinted cream cards)
- **ink:** #17140F   (near-black — the 1.5px card outlines, text, the dark pill)
- **accent:** #E8481F   (orange-red — diamond bullets, review markers, one avatar ring)
- **accent_soft:** #F2ED84   (butter yellow — the "Sign up" pill, discount chips, the icon-button fill)
- **muted:** #7C7A73   (secondary text)
- **line:** #17140F   (the black card outline itself — the defining structural line)
- **accent_usage_rule:** two coordinated pops share the load: **orange-red** for diamond bullets / rating markers / one accent circle, and **butter-yellow** for highlight pills, discount chips, and the small circular icon-buttons. Neither floods a card; body stays ink; the structural color is the **black outline**, not a fill. Use at most one yellow pill and one orange-red marker cluster per card.

## 2. Type
- **display_face:** a clean geometric-leaning grotesque (a Poppins/Aeonik feel), medium weight — friendly but not heavy
- **body_face:** the same family, regular
- **h1:** weight 500–600, size clamp(30px→52px), line-height 1.08, letter-spacing -0.01em, ink; may end with a small **inline glyph pair** (two overlapping circle marks) dropped after the last word
- **h2 (card titles):** weight 600, ~18–24px, ink
- **body:** weight 400, 13–15px, line-height 1.5, muted
- **eyebrow:** small ink label or a **butter-yellow pill** ("-15%", "music"); occasionally a mono price
- **two_tone_headline:** light — one word may sit inside a butter-yellow pill or gain an inline circle-glyph; no color on the type itself

## 3. Layout skeleton (section order + structure)
1. Nav — a single **black-outline rounded pill bar**: logo left, a **dashed/solid rule** separating groups, centered links, right a "Log in" text link + a **butter-yellow "Sign up" pill**
2. Hero — an asymmetric **bento of outline cards** around a large right-side headline: LEFT column stacks a stat card ("174+ Music programs" + a yellow ↗ circle-button), a grayscale **stacked-paper image** card, and a promo card with a **struck-through price ("12$  ~~35$~~")**, a **date range row (24 July – 28 July)**, a big time, and a **barcode**; MIDDLE column a review card (a **row of orange-red diamonds** + "4.5 review"), a team card (avatar cluster), and a **circular portrait photo tinted orange** ("Music covers"); RIGHT the headline + body + a **fused two-tone pill button** ("Get started →" dark fused with "Watch video ●" light) + two outline stat cards each led by an **orange-red diamond** and a right-aligned "music" chip
3. Logos / trust — a thin outline strip or diamond-separated marks
4. Features — a 2×2 or 3-up grid of outline cards, each: icon (in a yellow circle) + title + one line
5. Pricing / CTA — outline cards with yellow highlight pills and the fused-pill button reprised
6. Footer — outline-framed, link columns, quiet

## 4. Signature moves (the memorable, must-keep specifics)
- **Thin (1.5px) solid-black rounded outlines on every card** — the structure is drawn, not shadowed
- **Orange-red diamonds (◆)** as bullets, rating markers, and section ticks
- **Butter-yellow highlight pills** (nav "Sign up", "-15%", "music", icon-circles) as the second pop
- **Fused two-tone pill button** — a dark "Get started →" segment welded to a light "Watch video ●" segment in one capsule
- **Catalog/ticket motifs** — a **barcode**, a **struck-through price**, a **date-range row**, a **big time**, review **diamonds** — treated as real content
- **Circular portrait photo with an orange color-tint** inside an outline card
- **Small circular icon-buttons filled butter-yellow** with a ↗ arrow

## 5. Shape & spacing rules
- **radius:** cards ~14–18px; pills fully round; the nav bar is one long rounded pill; icon-buttons are perfect circles
- **section_padding:** ~72px vertical
- **card_padding:** ~18–22px
- **shadow:** essentially none — depth comes from the black outline, not shadow (flat neo-brutalist); at most a 2px hard offset on a hover
- **borders:** **1.5px solid #17140F** on every card and the nav pill — the signature; dashed variant only for the nav group-separators

## 6. Imagery
- **style:** a mix of grayscale abstract crops (stacked paper), tinted circular portraits, and small avatar clusters — playful, catalog-like
- **treatment:** photos cropped into outline cards or circles; portraits get a flat **orange color-tint**; images are supporting, not full-bleed heroes
- **source:** Unsplash/Pexels API server-side (never hotlink-scrape at request time) — favor portraits (for the tinted circle) and simple objects; render barcodes/tickets in CSS/SVG

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the two-pop pair — orange-red (→ another warm pop: coral / red / magenta) and butter-yellow (→ mint / sky / peach) — shifted together while keeping two distinct pops
- **must NOT change on remix:** the 1.5px black-outline-on-cream card system, the diamond bullets, the fused two-tone pill button, the catalog motifs (barcode / struck-price / date-range / diamonds), the tinted circular portrait, and the flat no-shadow depth
