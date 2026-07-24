# Style Spec — 04 bloomfi-lavender

**Real extraction** from `references/60ada601819c10a93a75ee300966deaa.jpg` ("BloomFi /
USD Bloom"). Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** bloomfi-lavender
- **one-line:** Soft lavender fintech — pastel ground, deep-plum cards, and dreamy 3D-rendered objects (coins, a classical temple) nested in fields of purple flowers.
- **best_for:** crypto/DeFi, savings/yield, calm fintech and "money that grows" products that want to feel gentle and premium rather than aggressive.
- **avoid_for:** hard technical/dev tools, urgent/utilitarian dashboards, or high-contrast bold brands.

## 1. Palette (named hex + role — never just "purple")
- **bg:** #F5F5F7   (near-white with a lavender bias, primary background)
- **surface:** #FFFFFF   (light cards, panels)
- **ink:** #1D1731   (deep plum-black — text, headlines)
- **accent:** #8B7EAB   (soft violet — links, small accents, gradients)
- **accent_soft:** #D9DAF1   (lavender — the pastel hero field / tinted card)
- **plum:** #2B2742   (deep plum — the dark filled cards + pill buttons)
- **muted:** #8A86A0   (secondary text)
- **line:** #E7E6EF   (hairlines, card borders)
- **accent_usage_rule:** the mood is soft, so color is spread gently: lavender grounds and one or two tinted cards, deep-plum for the filled cards and pill buttons, violet for links and gentle gradients. Avoid harsh saturated fills — everything is desaturated and dreamy.

## 2. Type
- **display_face:** humanist grotesque (medium contrast, friendly) — e.g. a softened Neue Montreal
- **body_face:** same family, regular
- **h1:** weight 600, size clamp(30px→52px), line-height 1.08, letter-spacing -0.01em
- **h2:** weight 600, size ~28–36px
- **body:** weight 400, size 15–16px, line-height 1.6; muted for supporting copy
- **eyebrow:** small sparkle/star glyph "✦" prefix, 12px, letter-spaced, violet or muted
- **two_tone_headline:** no — single ink; emphasis via the 3D imagery and card color, not type color

## 3. Layout skeleton (section order + structure)
1. Nav — wordmark + star mark left; center links; right a deep-plum pill ("Launch BETA")
2. Hero — centered: a small "✦" glyph, a calm h1, a short subline, a deep-plum pill CTA; then a full-width rounded hero image: 3D-rendered coins rising from a field of lavender flowers
3. Explainer — 2-col: left h2 + a plum pill / right a short paragraph
4. Feature trio — 3 rounded cards of MIXED fill: one lavender photo-card (3D object) + two deep-plum cards with a title + short body (siblings, different grounds)
5. Backers — a muted "Backed by…" line + a row of grayscale partner logos
6. Use cases — 2-col: left h2 + intro / right a white card ("Business") containing a 3D-rendered classical temple in a lavender scene
7. Footer — calm link columns on the pastel ground

## 4. Signature moves (the memorable, must-keep specifics)
- **Dreamy 3D-rendered objects** (coins, a classical temple) nested in fields of purple flowers — the defining imagery
- **Mixed-fill card siblings** — a lavender photo-card beside deep-plum solid cards in the same row
- **Deep-plum pill buttons** on a pale lavender ground
- **"✦" sparkle/star glyph** as the brand mark and eyebrow prefix
- **Desaturated, airy pastel palette** — nothing shouts
- Large, soft rounded corners everywhere

## 5. Shape & spacing rules
- **radius:** cards/hero ~18–22px; pills fully round; feature cards ~18px
- **section_padding:** ~96px vertical
- **card_padding:** ~28px
- **shadow:** very soft, low-opacity, wide (e.g. 0 30px 60px -30px rgba(29,23,49,.25))
- **borders:** hairline #E7E6EF where needed; mostly borderless

## 6. Imagery
- **style:** 3D CGI renders of glossy soft objects (coins, columns, orbs) staged in lavender/violet floral or misty scenes; high softness, gentle rim light
- **treatment:** rounded cards, sometimes full-bleed inside a card; gentle violet gradient wash
- **source:** Unsplash/Pexels API server-side for photographic fallbacks; render-style hero art is a phase-2 asset (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the violet family (lavender/plum/violet) can shift hue together toward blue-lilac or rose-mauve — as ONE coordinated pastel set
- **must NOT change on remix:** the soft-desaturated discipline, the 3D-object-in-flowers imagery, the mixed-fill card siblings, plum pills on a pale ground, and the airy rounded spacing
