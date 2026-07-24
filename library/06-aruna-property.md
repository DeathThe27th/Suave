# Style Spec — 06 aruna-property

**Real extraction** from `references/e92350bd27cf6de2987f885e8c5e9e74.jpg` ("Aruna").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** aruna-property
- **one-line:** Warm real-estate editorial — a light neutral canvas that lets architectural photography lead, spec-rich property cards, and an oversized wordmark bleeding over a building at the footer.
- **best_for:** real estate, architecture, hospitality, interiors, travel-stay, and marketplace products with a strong photo library and listing/spec data.
- **avoid_for:** dev tools, dense analytics, or brands with no photography.

## 1. Palette (named hex + role — never just "beige")
- **bg:** #FFFFFF   (clean white, primary background)
- **surface:** #FBF7F1   (warm off-white — alt sections, form ground)
- **ink:** #1A1614   (warm near-black — text, headlines, buttons)
- **accent:** #1A1614   (black is the primary UI color; the warmth comes from photography, not a chroma accent)
- **accent_soft:** #F0EAE1   (warm tint for a chip/hover)
- **muted:** #8C8680   (secondary text, spec labels)
- **line:** #EAE6E0   (hairlines, card borders, form fields)
- **accent_usage_rule:** no loud color — the palette is warm-neutral and the architecture photos carry all the richness. Buttons and circular "Details" tags are solid ink-black; the dark contact section inverts to ink ground with white type.

## 2. Type
- **display_face:** a clean grotesque with slightly humanist warmth (Aeonik / Neue Haas feel)
- **body_face:** same family, regular; muted for supporting text
- **h1:** weight 600, size clamp(30px→52px), line-height 1.06, letter-spacing -0.02em
- **wordmark (oversized):** weight 700, enormous — clamp(80px→18vw), bleeding over a photo at the footer
- **h2:** weight 600, size ~28–36px
- **body:** weight 400, size 14.5–16px, line-height 1.55
- **eyebrow:** 12px uppercase, letter-spacing 0.08em, muted or with a "•" dot
- **two_tone_headline:** no

## 3. Layout skeleton (section order + structure)
1. Nav — left links, centered wordmark, right "Book a Call"; thin and quiet
2. Hero — a large h1 left + a short right-aligned paragraph and a "©…" note; a wide architecture photo carrying a horizontal SEARCH BAR (Looking for / Type / Price / Location / a black Search button)
3. About (video) — a full-width video still with a circular play button and a caption overlay ("What is Aruna?")
4. Listings carousel — "Explore Our Property Listings"; 3 photo cards with a location pin tag and a black circular "Details" tag clipped on the photo; left/right arrows
5. Property grid — "Discover Aruna Property"; a grid of 6 property cards, each: photo + name + location + an icon spec row (beds / baths / m²)
6. Contact (dark section) — inverts to ink ground: "Still haven't found…" + a form (First / Last / I want to / Notes / a white Submit button) beside a warm photo
7. FAQ — 2-col: heading left / hairline accordion right
8. Footer wordmark — an oversized wordmark ("ARUNA") bleeding across a building photo; then footer links + socials + copyright

## 4. Signature moves (the memorable, must-keep specifics)
- **Oversized wordmark bleeding over a building photo** at the footer — the defining move
- **Search-bar hero** embedded on the hero photo (Looking-for / Type / Price / Location / Search)
- **Property cards with an icon spec row** (beds / baths / m²) under name + location
- **Black circular "Details" tags** clipped onto photo corners
- **Embedded video hero** with a circular play button and a caption overlay
- **A dark inverted contact section** among the light layout
- Warm-neutral restraint letting photography lead

## 5. Shape & spacing rules
- **radius:** cards/photos ~14–18px; buttons ~10px; circular tags full-round
- **section_padding:** ~96px vertical
- **card_padding:** ~18–22px (cards are photo-led, light chrome)
- **shadow:** soft, low, wide (e.g. 0 24px 50px -28px rgba(26,22,20,.22))
- **borders:** hairline #EAE6E0 on form fields and some cards

## 6. Imagery
- **style:** warm architectural / interior photography — modern homes, natural light, wood + glass + greenery; people-in-space occasionally
- **treatment:** rounded cards, minimal overlays; small pin/spec/Details tags clipped on; the footer photo runs full-bleed under the wordmark
- **source:** Unsplash/Pexels API server-side, prefer architecture/interior queries (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the warmth of the neutrals (warm ↔ cool off-white) and, if needed, ONE restrained accent for links; the ink stays near-black
- **must NOT change on remix:** the photography-led restraint, the footer wordmark bleed, the search-bar hero, the spec-row property cards, the Details tags, and the dark inverted contact section
