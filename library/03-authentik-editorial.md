# Style Spec — 03 authentik-editorial

**Real extraction** from `references/ea18a83663d0b0f04ec0c2de95fd2d83.jpg` ("Authentik").
Palette sampled from pixels. ⚠️ Pending human by-eye verification (EXTRACT.md).

## 0. Identity
- **id:** authentik-editorial
- **one-line:** Black-on-white editorial minimalism — an oversized two-weight headline ending in a period, duotone photography fading into the page, and nothing but ink, paper, and air.
- **best_for:** brands, studios, coaching, community, and thoughtful products that sell trust and taste through restraint; strong with a strong name and a black-and-white photo.
- **avoid_for:** dense dashboards, playful consumer apps, or anything that needs vivid color or heavy affordances.

## 1. Palette (named hex + role — never just "gray")
- **bg:** #FFFFFF   (paper white, primary background)
- **surface:** #F7F7F7   (alt sections, input fields, the signup card ground)
- **ink:** #111111   (near-black — text, buttons, most everything)
- **accent:** #111111   (there is no chromatic accent; black IS the accent — buttons and rules carry it)
- **accent_soft:** #EDEDED   (subtle fill for a chip/hover)
- **muted:** #A6A6A6   (secondary text, captions, tracked labels)
- **line:** #E6E6E6   (hairline dividers, input borders)
- **accent_usage_rule:** no color enters the page. Emphasis comes only from weight, size, and whitespace. The single darkest element per view is a solid-black button or a tiny black caption tag — never a colored fill.

## 2. Type
- **display_face:** clean grotesque (Helvetica Now / Neue Haas feel) — used at two weights in one line
- **body_face:** a transitional serif (Tiempos / Freight Text feel) — editorial body pairing
- **h1:** display; a light weight ("Welcome to") stacked over a bold weight ("Authentik."), size clamp(40px→84px), line-height 1.0, letter-spacing -0.02em, ALWAYS closed with a period
- **h2:** display, weight 600, size ~34–44px, letter-spacing -0.01em
- **body:** serif, weight 400, size 15–17px, line-height 1.55, ~62ch measure
- **eyebrow / labels:** grotesque, 11px, uppercase, letter-spacing 0.12em, muted
- **two_tone_headline:** yes — but tonal, not chromatic: one word set light, the next set bold (never two colors)

## 3. Layout skeleton (section order + structure)
1. Nav — wordmark + small mark left; text links right with the last ("Get in Touch") bolded; hairline under
2. Hero — left: two-weight headline ending in a period + serif subline + a black pill button and a "LEARN MORE →" underlined link; right: a duotone (B&W) photograph bleeding in and fading to white, with a tiny solid-black location caption tag pinned to it
3. Statement — a centered/flush display h2 ending in a period + short serif intro
4. Trio — 3 columns, each a thin line-icon + bold micro-heading + serif body; an underlined "TAKE THE FIRST STEP →" link beneath
5. Beliefs (gray #F7F7F7 section) — left: display h2; a 2×2 grid of "belief" columns (bold term + serif body); right: a white signup card (First Name / Email inputs + a checkbox consent line + a black "GET STARTED TODAY" button)
6. Footer — mark + "CREATE HONESTLY."; an italic serif pull-quote under a "WE BELIEVE" label; 4 link columns (About / Services / Resources / Connect); copyright + legal row

## 4. Signature moves (the memorable, must-keep specifics)
- **Oversized two-weight headline ending in a period** — the defining move (light word + bold word, then ".")
- **Duotone B&W photography that fades into the page** — no hard frame; the image dissolves into white
- **Tiny solid-black caption tag** pinned to the photo (place / credit)
- **Grotesque display + serif body pairing** — display for impact, serif for reading
- **Underlined text links with a trailing "→"** as secondary CTAs
- **Thin line-art icons** (single-weight strokes)
- **Uppercase, wide-tracked micro-labels**
- Ruthless whitespace; the page breathes more than it speaks

## 5. Shape & spacing rules
- **radius:** small — cards/inputs ~4–6px; buttons ~4px; no pills, no big rounding
- **section_padding:** ~120–140px vertical
- **card_padding:** ~28px (the signup card); most content isn't boxed at all
- **shadow:** none, or a whisper-soft one on the single signup card only
- **borders:** 1px hairline #E6E6E6; inputs and dividers only

## 6. Imagery
- **style:** black-and-white / duotone photography — landscapes, hands, candid moments; editorial and quiet
- **treatment:** bleeds and fades into the page ground (no radius, no drop shadow); a small caption tag beneath or on it
- **source:** Unsplash/Pexels API server-side, prefer monochrome/high-contrast results (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** almost nothing — at most introduce ONE restrained ink-tone accent (a deep ink-blue or forest) for links, and shift the paper warmth slightly
- **must NOT change on remix:** the black-and-white discipline, the two-weight period-headline, duotone-photo-fade, serif-body/grotesque-display pairing, the underline-and-arrow links, and the whitespace
