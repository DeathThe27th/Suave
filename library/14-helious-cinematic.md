# Style Spec — 14 helious-cinematic

**Real extraction** from `references/0569e0ae4f0c254626ea1e061e84132a.jpg` ("Helious").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** helious-cinematic
- **one-line:** Cinematic warm-black editorial — an oversized cream serif wordmark bleeds across the bottom of a moody, golden-hour isometric photograph, with a tiny right-aligned body column and a single ghost-outline "Get started" pill.
- **best_for:** creative collectives, studios, residencies, courses, retreats, culture/film brands, premium newsletters — anything that wants a moody, editorial, "prestige-film" feel.
- **avoid_for:** dashboards, fintech, high-density SaaS, anything cheerful or high-information; the huge wordmark and single-photo hero can't carry data-heavy products.

## 1. Palette (named hex + role — never just "black")
- **bg:** #0E0B08   (warm near-black, the whole canvas)
- **surface:** #17110B   (barely-lifted panels/nav backdrop, if any)
- **ink:** #EDE6D6   (warm cream — the giant wordmark, headlines, nav)
- **accent:** #C9A24E   (muted antique gold — used ONLY on the wordmark's trailing asterisk and hairline detail)
- **accent_soft:** #6B5836   (dim gold, for a hairline or focus ring)
- **muted:** #8B8172   (secondary/body text — warm taupe-gray)
- **line:** #2A2018   (hairline dividers on the dark ground)
- **accent_usage_rule:** the gold accent is almost absent — it may touch ONLY the small superscript asterisk beside the wordmark and, optionally, one hairline. It must NEVER color the CTA (that stays cream), body text, or fill any shape. The real "color" is the warm photograph itself; the UI stays cream-on-warm-black.

## 2. Type
- **display_face:** high-contrast transitional/Didone serif (a Canela / Times-display feel) — set ENORMOUS as a wordmark, tight optical tracking
- **body_face:** a neutral grotesque (Inter/Söhne feel), small
- **h1 (the wordmark):** weight 500, size clamp(84px→220px), line-height 0.9, letter-spacing -0.015em, cream, baseline sitting low so the photo overlaps its top
- **h2:** weight 500 serif, ~32–44px, letter-spacing -0.01em
- **body:** weight 400 sans, 13–15px, line-height 1.5, muted taupe, set in a narrow right-aligned column (~260px)
- **eyebrow:** none as a label; instead a small superscript gold **asterisk** hung off the wordmark's last letter
- **two_tone_headline:** no — the wordmark is single-color cream; contrast comes from scale, not color

## 3. Layout skeleton (section order + structure)
1. Nav — a slim centered horizontal link row (About us / Community / Residencies / Courses / Questions) floating at the very top over the photo; no logo lockup (the wordmark below IS the brand)
2. Hero — one full-bleed cinematic photograph occupying the upper ~65%; the giant serif wordmark sits across the lower third so the photo's bottom edge overlaps the tops of the letters; a narrow right-aligned muted paragraph; a ghost-outline pill "Get started" with a trailing circular arrow button at bottom-right
3. Manifesto — a large centered/left serif statement on the warm-black ground, generous negative space
4. Offerings — 2–3 large text-led rows or a sparse grid (residencies / courses), each a serif line + one small photo
5. Gallery — a few full-width cinematic photos, edge to edge, minimal captions
6. Quote / ethos — oversized serif pull-quote, cream on black
7. Footer — the wordmark repeated small, a thin link row, quiet

## 4. Signature moves (the memorable, must-keep specifics)
- **Oversized cream serif wordmark bleeding UNDER the hero photo** — the photo's lower edge crops into the tops of the letters (the defining move)
- **Warm-black, not neutral-black** ground (#0E0B08) so cream and gold read as candlelit
- **Tiny gold superscript asterisk** hung off the wordmark — the only chromatic spark
- **Narrow right-aligned body column** dropped into open space beside the wordmark
- **Ghost-outline pill + trailing circular-arrow button** as the single CTA (never a filled button)
- **Cinematic, film-grain, golden-hour isometric photography** as the only imagery
- **Centered slim nav with no logo** (wordmark is the identity)

## 5. Shape & spacing rules
- **radius:** pills fully round; the circular arrow button is a perfect circle; photos have a small 8–12px radius or none (full-bleed)
- **section_padding:** ~120px vertical, luxuriously loose
- **card_padding:** minimal — this style avoids cards; text sits on open ground
- **shadow:** essentially none on the dark ground; the photo may carry a soft inner vignette
- **borders:** hairline #2A2018 only where a divider is unavoidable; the CTA pill is a 1px cream outline

## 6. Imagery
- **style:** cinematic, warm, grainy, golden-hour or blue-hour; isometric/aerial landscapes, lone figures, moody nature — a "film still" quality
- **treatment:** full-bleed or large-crop; slight film grain and warm color grade; the hero photo is positioned to overlap the wordmark's top edge; no hard frames
- **source:** Unsplash/Pexels API server-side (never hotlink-scrape at request time) — favor moody, high-grain, warm-graded landscape/portrait shots

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the cream ink hue (→ bone / warm white) and the gold accent (→ dim bronze / oxblood), and the photo's color grade — shifted together to stay candlelit
- **must NOT change on remix:** the warm-near-black ground, the oversized-serif-wordmark-under-photo move, the near-total absence of accent color, the narrow right-aligned body column, the ghost-pill + circular-arrow CTA, and the cinematic single-photo hero
