# Style Spec — 08 deploya-mono

**Real extraction** from `references/9162d1861ac6558238b935d7a002ba48.jpg` ("Deploya").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** deploya-mono
- **one-line:** Monochrome B2B SaaS — a light-gray canvas, thin border-defined cards, mixed-weight centered headlines, and chrome-wave black-and-white imagery, with zero accent color.
- **best_for:** B2B SaaS, ops/analytics platforms, infrastructure and template-y product marketing that wants to read clean, neutral, and enterprise-credible.
- **avoid_for:** playful consumer, lifestyle, or brands that need warmth or a color identity.

## 1. Palette (named hex + role — never just "gray")
- **bg:** #F5F5F5   (light gray, primary background)
- **surface:** #FFFFFF   (cards, panels)
- **ink:** #16181C   (near-black — text, buttons)
- **accent:** #16181C   (no chroma — black is the only "accent"; buttons and the dark CTA band carry it)
- **accent_soft:** #ECECED   (subtle gray fill for chips/hover)
- **muted:** #8F908F   (secondary text)
- **line:** #E7E7E9   (the hairline borders that define every card — load-bearing)
- **accent_usage_rule:** strictly monochrome. Structure is drawn with 1px borders, not color or shadow. The only "dark" moments are solid-black buttons, a black marquee band, and a dark CTA band near the footer.

## 2. Type
- **display_face:** neutral grotesque (Inter / Geist feel) used at mixed weights in one centered line
- **body_face:** same family, regular; muted
- **h1/h2:** centered, mixed weight within the line ("All Your SaaS Ops. In One Place."), size clamp(28px→46px), line-height 1.1, letter-spacing -0.01em
- **body:** weight 400, size 14.5–16px, line-height 1.6
- **eyebrow:** 11px uppercase, letter-spacing 0.12em, muted, often centered inside a tiny bordered pill
- **two_tone_headline:** tonal only — mixed font-weight within one line, never two colors

## 3. Layout skeleton (section order + structure)
1. Nav — wordmark + a pill nav cluster + dark buttons
2. Hero — centered mixed-weight headline + subline + a dark "Get Started" + a "Watch Demo"; a dark metallic dashboard screenshot set on a chrome-wave B&W background; a "500+ companies…" line + a grayscale logo row
3. Insight — 2-col: a left feature list / a right 2×2 grid of thin-bordered light UI cards (Data Insights / Smart Automations / Team Collaboration / Live Analytics), each with a "Learn how →"
4. How it works — 3 bordered cards, each with a small 3D metallic icon
5. Visibility — 2-col with a dark B&W portrait card carrying a stat ("27% …")
6. Marquee — a black full-width band scrolling capability keywords (the one dark stripe)
7. Testimonials — 3 thin-bordered quote cards
8. Integrations — "Plug and play with 1,000+…" a bordered grid of grayscale integration icons
9. Pricing — 2 bordered cards ($50 Pro / $150 Enterprise)
10. Blog — "Explore Product Latest…" 3 B&W wave images
11. FAQ — bordered accordion
12. CTA band (dark) — "One Platform. Endless Clarity." on ink ground, then footer

## 4. Signature moves (the memorable, must-keep specifics)
- **Border-defined cards** — every card is a 1px hairline box, no shadow — the defining structural move
- **Chrome / metal-wave B&W photography** as the only imagery (liquid-metal, wave textures)
- **Mixed-weight centered headlines** (weights change within one line)
- **A single black marquee band** scrolling capability keywords
- **Small 3D metallic icons** on the how-it-works cards
- **Strict monochrome** — no accent color anywhere
- Dark CTA band as the lone inverted moment before the footer

## 5. Shape & spacing rules
- **radius:** cards ~12–14px; buttons ~8px; pills fully round
- **section_padding:** ~100px vertical
- **card_padding:** ~24px
- **shadow:** essentially none — depth is the 1px #E7E7E9 border
- **borders:** 1px hairline #E7E7E9 on everything; this is the primary design device

## 6. Imagery
- **style:** black-and-white liquid-metal / chrome-wave abstracts, plus grayscale UI screenshots and grayscale portraits
- **treatment:** inside bordered cards or full-bleed dark hero backdrop; always desaturated
- **source:** Unsplash/Pexels API server-side, prefer B&W abstract/texture queries (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** at most introduce ONE restrained accent for links/primary buttons; the neutrals shift only in temperature
- **must NOT change on remix:** the border-defined-card system, the monochrome discipline, chrome-wave imagery, mixed-weight centered headlines, and the single black marquee band
