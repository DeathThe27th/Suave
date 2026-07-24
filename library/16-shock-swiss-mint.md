# Style Spec — 16 shock-swiss-mint

**Real extraction** from `references/d4d7ccb1bb2b8601294bc4fa3d88ed5e.jpg` ("SHOCK" digital clothing).
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** shock-swiss-mint
- **one-line:** Swiss-grid fashion-tech — an off-white canvas framed by a deep-navy top band, a big uppercase grotesque headline, an asymmetric photo-tile bento with one mint award tile, a circular chrome blob overlapping the tiles on a connector line, and a numbered `01 … /2022` index list.
- **best_for:** fashion/streetwear, metaverse & web3 apparel, design studios, award-winning agencies, product drops — brands that want confident, grid-disciplined, editorial-cool.
- **avoid_for:** warm/friendly consumer, finance/trust-heavy, or dense-data SaaS; the cold grid and sparse copy suit statement pages, not utilities.

## 1. Palette (named hex + role — never just "green")
- **bg:** #ECEBE8   (off-white, the main canvas)
- **surface:** #FFFFFF   (white tiles/cards)
- **ink:** #16223C   (deep navy — headlines, the top frame band, the primary pill)
- **accent:** #7CE0C2   (mint — exactly one tile / award panel)
- **accent_soft:** #DEF6EE   (pale mint tint, for a chip or hover)
- **muted:** #6B7385   (secondary text, index numbers' captions)
- **line:** #DAD9D5   (hairlines, the numbered-list rules)
- **accent_usage_rule:** mint fills exactly ONE tile (the "A'Design Award Winner" panel) and may tint one small chip. It must NOT touch the headline, the primary pill, or more than one tile; navy is the ink/structure color, mint is the single spark.

## 2. Type
- **display_face:** a bold neo-grotesque (Helvetica/Neue Montreal feel), UPPERCASE, tight — set large and blocky
- **body_face:** the same grotesque, regular
- **h1:** weight 700, size clamp(40px→84px), line-height 0.98, letter-spacing -0.01em, UPPERCASE, navy
- **h2:** weight 700, ~24–32px, UPPERCASE or sentence, navy
- **body:** weight 400, 14–15px, line-height 1.5, muted
- **eyebrow:** weight 600, 12px, navy or muted; small labels like "BUILD YOUR METAVERSE LOOK" set on the dark tile
- **two_tone_headline:** no — headline is single navy; the mint never enters the type

## 3. Layout skeleton (section order + structure)
1. Nav — a **deep-navy top frame band** carrying: logo left (mark + "SHOCK"), centered links (Shop / Lookbook / Our Story), right a "Cart (0)" + a circular dark theme toggle; the band reads as a bracket around the top of the page
2. Hero — an asymmetric two-zone Swiss layout: LEFT a bento cluster of rounded photo tiles (a portrait tile with a "+" circle, a **mint award tile**, a small navy caption tile, an abstract topographic tile) with a **circular chrome-blob** in a white ring overlapping them, dropped on a thin **connector line** to a "Cooperate As Designer / Media" label; RIGHT a big uppercase headline, a navy "WEAR NOW" pill + a circular ↗ button + a small halftone-sphere chip, and below a **numbered index list** (01, 02) each row: big number · thumbnail · one-line label · right-aligned `/2022` year
3. Marquee / logos — a thin strip of collaborator marks or a scrolling label
4. Grid gallery — a strict 2- or 3-column tile grid of looks, rounded corners, consistent gutters
5. Statement — one large uppercase line with generous space
6. Footer — navy band mirroring the nav, link columns, mark repeated

## 4. Signature moves (the memorable, must-keep specifics)
- **Deep-navy top (and bottom) frame band** bracketing an off-white page
- **Asymmetric photo-tile bento** — rounded tiles of different sizes packed on a grid, one of them a **caption tile** (dark, white micro-label)
- **Exactly one mint tile** (the award/badge panel) as the only color
- **A circular chrome/liquid-metal blob in a white ring**, overlapping the tiles, hung on a thin **connector line** to a small role label
- **Numbered index list** — oversized `01 / 02`, a round thumbnail, a terse label, and a right-aligned `/year`
- **Connected pill + circular icon-button** pairing for the CTA
- **UPPERCASE grotesque headline** anchored right of the bento

## 5. Shape & spacing rules
- **radius:** tiles/cards ~16–20px; pills fully round; the blob ring is a perfect circle
- **section_padding:** ~88px vertical
- **card_padding:** ~20px
- **shadow:** minimal — tiles sit flat on the grid; the chrome-blob ring gets a soft 0 20px 40px -24px rgba(22,34,60,.25)
- **borders:** hairline #DAD9D5 on the numbered-list rules; tiles are borderless (defined by fill)

## 6. Imagery
- **style:** editorial fashion portraits (studio, styled looks), plus abstract 3D chrome/liquid-metal blobs and topographic line textures as accents
- **treatment:** photos cropped into rounded rectangular tiles on a strict grid; the chrome blob isolated in a circular ring; consistent gutters, no tilt
- **source:** Unsplash/Pexels API server-side (never hotlink-scrape at request time) — favor styled fashion portraits and metallic-3D abstract renders

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the single mint accent (→ one other clean pop: lime / coral / periwinkle) on its one tile, and the navy ink (→ another near-black hue: aubergine / forest) applied to bands + headline + pill together
- **must NOT change on remix:** the navy top/bottom frame bands, the asymmetric photo-tile bento with a caption tile, the single-color-tile rule, the chrome-blob-on-connector-line move, the numbered `01 … /year` index list, and the strict-grid gutters
