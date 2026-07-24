# Style Spec — 09 concord-serif

**Real extraction** from `references/e829f757679983d3cd4f65535a0d3daa.jpg` (conversational-
AI-for-finance landing; brand name not shown — id chosen). Palette sampled from pixels.
⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** concord-serif
- **one-line:** Serif editorial meets technical blueprint — a large two-tone serif headline over a dotted grid, with architectural line-art illustrations partly tinted in a single periwinkle blue.
- **best_for:** trust-forward fintech, B2B, legal/compliance, consulting, and "serious but human" products that want editorial gravitas with a technical edge.
- **avoid_for:** playful consumer, bold/loud brands, or image-heavy lifestyle pages.

## 1. Palette (named hex + role — never just "blue")
- **bg:** #FFFFFF   (white, primary background, with a faint dotted grid)
- **surface:** #FFFFFF   (cards sit flush; structure is drawn with rules)
- **ink:** #171717   (near-black — serif headlines, body)
- **accent:** #7C82E6   (periwinkle blue — the blueprint tint + small emphasis; the line-art draws in a lighter #959AE9)
- **accent_soft:** #E9EAFC   (pale periwinkle wash behind blueprint art)
- **muted:** #8A8A8A   (the light "first word" of the headline, secondary text)
- **line:** #E6E6E6   (thin rules and card outlines)
- **grid_dot:** #EDEDF3   (the faint background dot grid)
- **accent_usage_rule:** periwinkle appears ONLY in the blueprint line-art (a partly-tinted region) and the odd emphasized word or bracket. Type is otherwise ink and muted-gray; buttons are solid black. Never a periwinkle fill on a large surface.

## 2. Type
- **display_face:** a large transitional/old-style SERIF (Tiempos / Canela / Freight Display feel) — this is the personality
- **body_face:** a neutral grotesque for body, labels, and UI
- **h1:** serif, weight 500–600, size clamp(40px→80px), line-height 1.02, letter-spacing -0.01em; the FIRST word set in muted gray, the rest in ink (tonal two-tone), often ending in a period
- **h2:** serif, weight 500, size ~34–46px
- **body:** grotesque, weight 400, size 15–16px, line-height 1.6
- **eyebrow:** grotesque, 11px, uppercase, letter-spacing 0.12em, wrapped in literal brackets "[ WHAT DO WE DO? ]"
- **two_tone_headline:** yes — tonal: muted-gray first word + ink remainder

## 3. Layout skeleton (section order + structure)
1. Hero — centered: a large two-tone serif headline (gray word + ink) ending in a period, a grotesque subline, and a solid-black pill ("Book A Demo"); the ground is a faint dotted grid, and a blueprint architectural line-drawing (e.g. a Colosseum) rises from the bottom edge, a portion of it tinted periwinkle
2. What-we-do — a bracketed eyebrow "[ WHAT DO WE DO? ]" + a serif h2 in a 2-col split (heading left / paragraph right) divided by thin rules; the blueprint line-art continues down the left edge
3. Capabilities — slash-numbered items "01 / Conversational", "02 / Connected", "03 / Compliant" as bordered/rule-separated cells
4. …continues in the same editorial system (proof, pricing, FAQ) with serif headings, thin rules, and generous whitespace
5. Footer — quiet, rule-topped, grotesque link columns

## 4. Signature moves (the memorable, must-keep specifics)
- **Large two-tone SERIF display** — muted first word + ink remainder, ending in a period — the defining move
- **Blueprint / technical line-art illustrations** (architecture) partly tinted in the single periwinkle accent
- **A faint dotted background grid** running behind the editorial content
- **Bracketed "[ label ]" eyebrows**
- **Slash-numbered items** "01 / X"
- **Thin rules** as the primary divider; solid-black pill CTAs
- Serif for gravitas, grotesque for the working text

## 5. Shape & spacing rules
- **radius:** small — cards/cells ~8px; buttons pill or ~6px
- **section_padding:** ~120px vertical; wide editorial margins
- **card_padding:** ~24px (cells are rule-defined more than boxed)
- **shadow:** none — depth is thin rules and the dotted grid
- **borders:** 1px #E6E6E6 rules; the grid dots are #EDEDF3

## 6. Imagery
- **style:** technical blueprint / engraving line-art (architecture, machinery), part-tinted in the accent; no photography in the hero
- **treatment:** line drawings bleed from an edge; a periwinkle-tinted region marks the "active" portion; pale periwinkle wash behind
- **source:** line-art is a phase-2 asset; Unsplash/Pexels only for restrained supporting imagery (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the single accent (periwinkle → a muted teal / ink-blue / oxblood) used for the blueprint tint and emphasis
- **must NOT change on remix:** the serif display + two-tone headline, the blueprint line-art with a tinted region, the dotted grid, bracketed eyebrows, slash-numbering, and the thin-rule editorial structure
