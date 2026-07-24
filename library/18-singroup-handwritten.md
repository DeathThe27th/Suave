# Style Spec — 18 singroup-handwritten

**Real extraction** from `references/f4b05e1f0b18ffd8198e838fc4b38ea8.jpg` ("Singroup").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** singroup-handwritten
- **one-line:** Playful full-bleed nature hero — a bright daisy-meadow-under-blue-sky photograph fills the screen, a big white **handwritten marker-script** headline sits centered over it, and a floating dark-glass pill nav plus one white pill CTA are the only chrome.
- **best_for:** research/insight tools, wellness, travel, sustainability, consumer apps, campaigns — friendly, optimistic brands that want warmth and a human, hand-made touch.
- **avoid_for:** enterprise/technical, finance-serious, luxury-minimal, or dense dashboards; the script headline and photo hero read as consumer/playful, not authoritative.

## 1. Palette (named hex + role — never just "blue")
- **bg:** #1E63A8   (sky-blue — the photographic ground's dominant tone; base fallback behind the hero image)
- **surface:** rgba(14,22,30,0.55)   (smoked dark-glass — the nav pill and any floating chips)
- **ink:** #FFFFFF   (white — the handwritten headline and all hero text sit on the photo)
- **accent:** #FFFFFF   (the single solid CTA pill is white with dark text — white *is* the accent here)
- **accent_soft:** rgba(255,255,255,0.16)   (frosted white — the active nav tab, hover states)
- **muted:** rgba(255,255,255,0.78)   (secondary hero text — softened white)
- **line:** rgba(255,255,255,0.22)   (hairline separators on glass)
- **accent_usage_rule:** no *chromatic* accent is added — the photograph supplies all the color (sky blue, daisy white/yellow, grass green). UI stays white/frosted-white on the image. The one solid element is a **white** pill CTA with dark text; the one highlighted nav tab is a frosted-white pill. Never drop a colored button onto the photo.

## 2. Type
- **display_face:** a **handwritten marker/brush script** (a Caveat / "felt-tip" feel) — casual, slightly irregular baseline, the whole personality of the page
- **body_face:** a clean neutral sans (Inter/Helvetica feel), small
- **h1:** the script face, weight ~500–600, size clamp(40px→88px), line-height 1.05, letter-spacing 0, white, centered over the photo, gentle two-line break
- **h2 (on inner sections):** the sans, weight 600, ~24–30px
- **body:** sans, weight 400, 14–16px, line-height 1.6, softened white on the hero (or ink on light inner sections)
- **eyebrow:** none in the hero; inner sections may use a small uppercase sans label
- **two_tone_headline:** no — the headline is a single white script; contrast comes from the script face + the photo behind it

## 3. Layout skeleton (section order + structure)
1. Nav — a floating **dark-glass pill** centered at top holding the links (What we do / AI Intelligence / Tools / Blog) with one active tab as a frosted-white pill; the wordmark sits far left outside the pill; a "Login" text link + a "Get started" frosted pill far right
2. Hero — one **full-bleed bright photograph** (meadow + sky); the white **handwritten headline** centered in the upper-middle; a short softened-white sans subhead beneath; a single **white pill "About the platform ●"** CTA centered under it; huge breathing room, no cards over the photo
3. Transition — the page drops from the edge-to-edge photo into a light or dark inner canvas (the meadow's tone can carry through as a tint)
4. Value sections — clean sans copy blocks and simple cards on the inner canvas; the script face returns only for section-title accents
5. Feature / product — a calm 2–3 column layout, minimal chrome
6. CTA band — the script headline reprised over a second nature photo or a solid tinted band
7. Footer — quiet sans link columns

## 4. Signature moves (the memorable, must-keep specifics)
- **White handwritten marker-script headline** centered over the photo — the entire identity
- **One full-bleed, bright, optimistic nature photograph** as the hero (no gradient overlays fighting it)
- **Floating dark-glass pill nav** with the wordmark set outside it and one frosted-white active tab
- **A single white pill CTA** (dark text, small trailing dot/arrow) — the only solid button
- **Zero added accent color** — the photo is the palette; UI is white/frosted only
- **Generous emptiness** over the image; no cards, stats, or logos crowding the hero

## 5. Shape & spacing rules
- **radius:** all pills fully round; inner cards ~16–20px
- **section_padding:** hero fills the viewport; inner sections ~96px vertical
- **card_padding:** ~24px on inner cards
- **shadow:** the glass nav gets a soft 0 10px 30px -12px rgba(0,0,0,.35) and a 1px inner white hairline; no heavy shadows on the photo
- **borders:** 1px rgba(255,255,255,0.22) on glass elements; none on the photo

## 6. Imagery
- **style:** bright, sunny, high-key nature and lifestyle photography — flower meadows, open sky, daylight; optimistic and real (not rendered)
- **treatment:** full-bleed hero, edge to edge; NO dark overlay (text legibility comes from choosing a sky/light zone for the headline); shallow depth of field; the photo's own colors are the palette
- **source:** Unsplash/Pexels API server-side (never hotlink-scrape at request time) — favor bright meadow/sky/daylight nature shots with a clear light zone for text

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the hero photograph's subject/season (a different bright nature scene → a different dominant color) — the palette follows the chosen photo; the glass tint may warm or cool to match
- **must NOT change on remix:** the handwritten-script headline, the full-bleed bright-nature hero with no dark overlay, the floating dark-glass pill nav with an outside wordmark, the single white pill CTA, the no-added-accent rule, and the generous empty hero
