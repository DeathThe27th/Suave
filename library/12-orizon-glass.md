# Style Spec — 12 orizon-glass

**Real extraction** from `references/88e18602161d46b1546656f7b2b346a4.jpg` ("Orizon").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** orizon-glass
- **one-line:** Heavy frosted glassmorphism — translucent blurred panels floating over warm architectural photography, a vertical glass icon rail, a thin oversized headline set behind the glass, and a single deep-indigo accent.
- **best_for:** premium real-estate/travel, high-end product or app marketing, and futuristic-luxury brands that want depth, blur, and a "control panel over a beautiful scene" feel.
- **avoid_for:** text-heavy long-form, budget/utilitarian, or brands with no photography.

## 1. Palette (named hex + role — never just "beige")
- **bg_photo:** warm architectural photography is the literal ground (tan/beige tones ~#C9BFB0)
- **bg:** #E1D8CF   (warm beige — the neutral fallback where no photo shows)
- **glass:** rgba(255,255,255,0.55)   (frosted panel fill — always with backdrop-blur)
- **glass_edge:** rgba(255,255,255,0.7)   (1px light inner edge on glass)
- **ink:** #1A1A1A   (dark text on glass)
- **ink_on_photo:** #FFFFFF   (thin headline over the photo)
- **accent:** #221857   (deep indigo — the one round brand button / active state)
- **muted:** #6E6A72   (secondary text on glass)
- **line:** rgba(20,20,20,0.08)   (faint dividers inside glass)
- **accent_usage_rule:** the "color" is the photograph seen through frosted glass. UI chrome is translucent white; the ONLY solid saturated element is the deep-indigo round button. Never flood a panel with indigo.

## 2. Type
- **display_face:** a thin/light grotesque (airy, wide) — set very large over the photo
- **body_face:** same family, regular; on glass
- **h1:** weight 300–400 (thin), size clamp(40px→96px), line-height 1.0, letter-spacing -0.02em, white, set OVER the photo behind the glass
- **h2/card titles:** weight 500–600, ~18–22px, ink on glass
- **body:** weight 400, size 13.5–15px, line-height 1.55, muted on glass
- **labels:** small, uppercase-ish, muted
- **two_tone_headline:** no

## 3. Layout skeleton (single glass "control panel over a scene")
1. Filter bar (glass) — a top row of translucent pills: an action ("Buy") / Location / Property Type / Max Price / an action ("Rent"), each with a small ↗ or ▾
2. Icon rail (glass) — a vertical stack of translucent circular icon buttons down the left (home / search / grid / chat / avatar / bell / settings / theme)
3. Hero — a huge thin white headline set over the architectural photo, partly behind the glass panels; a short muted intro; a glass "Find The Perfect Place" card carrying a "10K+ Properties" stat with a photo-stack and a ↗
4. Detail card (glass) — a floating property-detail card: title + address + short description + a spec row (m² / yard / bedrooms / baths) + like/save/share pills with counts; a deep-indigo round brand button nearby
5. …the system repeats: glass cards floating over photographic scenes

## 4. Signature moves (the memorable, must-keep specifics)
- **Heavy frosted-glass panels** (translucent + backdrop-blur + light inner edge) floating over photography — the defining move
- **A vertical glass icon rail** of circular buttons down the left
- **A thin oversized headline set OVER the photo**, partly occluded by the glass
- **Glass pill filter row** at the top
- **Property/spec rows** and **like/save/share pills with counts**
- **A single deep-indigo round button** as the only solid saturated element
- Warm architectural photography (amber interiors) as the ground

## 5. Shape & spacing rules
- **radius:** glass cards ~28–32px; pills fully round; icon buttons full circles
- **section_padding:** the composition is a layered single scene more than stacked sections
- **card_padding:** ~22–26px
- **shadow:** soft, wide, low-opacity beneath glass (e.g. 0 30px 60px -30px rgba(20,20,20,.35)); the blur does most of the depth work
- **borders:** a 1px light inner edge (glass_edge) on every glass panel

## 6. Imagery
- **style:** warm, dramatic architectural / interior photography — futuristic villas, amber interior glow, natural landscapes
- **treatment:** full-bleed as the ground; glass panels sit over it; the headline overlaps photo and glass
- **source:** Unsplash/Pexels API server-side, prefer architecture/interior/landscape queries; the glass is CSS (backdrop-filter), never baked into the image (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the single indigo accent (→ another deep jewel tone) and the photographic ground's warmth
- **must NOT change on remix:** the frosted-glass-over-photo model, the glass icon rail, the thin headline set behind glass, the glass filter pills, and the single-solid-accent restraint
