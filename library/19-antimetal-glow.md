# Style Spec — 19 antimetal-glow

**Real extraction** from `references/f456c13bbf8de7f4919114c6f5bffd0b.jpg` ("Antimetal").
Palette sampled from pixels. ⚠️ Pending human by-eye verification.

## 0. Identity
- **id:** antimetal-glow
- **one-line:** Deep-space technical SaaS — a single hero section graduates from near-black navy at the top through an electric-blue dotted-particle "globe" glow and fades seamlessly to white at the bottom, with a lone acid-lime pill CTA and a "New · Introducing…" ribbon.
- **best_for:** infra/devtools, AI platforms, observability, security, cloud/agent products — technical B2B that wants a premium, "deep-tech", confident-dark feel that still hands off to clean light content.
- **avoid_for:** warm/human consumer, editorial, wellness, or playful brands; the space-gradient and lime spark read as engineering, not lifestyle.

## 1. Palette (named hex + role — never just "blue")
- **bg:** #060F20   (deep navy-black — top of the hero)
- **bg_glow:** #1E6BFF   (electric blue — the mid gradient / particle glow)
- **surface:** #FFFFFF   (the light lower half + all body cards)
- **ink:** #0B1220   (near-black — text on the light sections)
- **ink_on_dark:** #EAF0FA   (near-white — headline + text on the dark hero)
- **accent:** #C6F24E   (acid lime — the single pill CTA and one status dot)
- **accent_soft:** #E9F9C0   (pale lime, for a hover/tint)
- **muted:** #93A2BC   (secondary text — cool slate)
- **line:** #E4E8EF   (hairlines on the light sections)
- **accent_usage_rule:** acid lime touches ONLY the primary pill CTA (repeated once or twice max) and maybe one live-status dot. Everything else is the blue gradient + white/near-white text on dark and ink on light. Never use lime for headings, links, or large fills.

## 2. Type
- **display_face:** a refined grotesque or a subtle transitional serif-lite (a clean, slightly editorial sans — Söhne / a light serif feel) — calm, not shouty
- **body_face:** a neutral grotesque (Inter feel)
- **h1:** weight 500–600, size clamp(34px→56px), line-height 1.1, letter-spacing -0.01em; near-white on the dark hero, centered
- **h2:** weight 500, ~26–34px; ink on light, often with **one phrase in muted slate** for emphasis
- **body:** weight 400, 15–16px, line-height 1.6; muted slate on dark, ink on light
- **eyebrow:** a small rounded **"New · Introducing … ›" ribbon pill** with a hairline border, centered above the headline
- **two_tone_headline:** light — one supporting phrase may drop to muted slate (e.g. "…reliable, efficient, and secure"), but no color

## 3. Layout skeleton (section order + structure)
1. Nav — transparent over the dark hero: wordmark + mark left, centered links (Platform / Resources / Pricing / Careers), right "Log in" + a bordered "Book a demo" pill; all in near-white
2. Hero — one tall section with a **vertical gradient from #060F20 → #1E6BFF → #FFFFFF**; a centered "New · Introducing…" ribbon pill; a centered near-white headline + subhead; a single **acid-lime pill CTA**; behind the text a **dotted-particle globe/sphere glow** (dot-matrix world) lit from the electric-blue mid-band; the section fades to white at the very bottom with no hard seam
3. Handoff — the white lower edge of the hero flows directly into the first light content section ("Ship more, break less") — headline + muted sub, no divider
4. Product proof — a large realistic product screenshot / dashboard sitting on the white ground, soft shadow, rounded corners
5. Features — clean 2–3 column light cards, hairline borders, small icons
6. Social proof / logos — a quiet grayscale logo row
7. CTA band — a dark navy band reprising the gradient + lime pill
8. Footer — dark navy, link columns, near-white text

## 4. Signature moves (the memorable, must-keep specifics)
- **One continuous vertical gradient hero: deep-navy → electric-blue → white**, fading seamlessly into the light body with no hard seam
- **A dotted-particle "globe" glow** behind the headline, lit by the blue mid-band
- **A single acid-lime pill CTA** as the only saturated color on the whole page
- **A "New · Introducing … ›" ribbon pill** above the headline
- **Dark-to-light handoff** — the hero's white base IS the next section's ground
- **Cool near-white headline on dark, ink on light**, calm/editorial weight (not heavy)
- **A realistic product screenshot** floating on the first white section as proof

## 5. Shape & spacing rules
- **radius:** pills fully round; cards & product frame ~16–20px; the ribbon pill fully round with a 1px hairline
- **section_padding:** hero ~140px tall; light sections ~96px vertical
- **card_padding:** ~24px
- **shadow:** product screenshot gets a soft 0 40px 90px -40px rgba(6,15,32,.28); lime pill may carry a faint glow 0 8px 30px -8px rgba(198,242,78,.5)
- **borders:** hairline #E4E8EF on light cards; 1px rgba(255,255,255,.25) on dark-hero pills

## 6. Imagery
- **style:** abstract particle/dot-matrix renders (a glowing world/sphere) for the hero; clean, realistic product UI screenshots for proof sections
- **treatment:** hero art is a glowing dot-field integrated INTO the gradient (not a framed image); product shots are rounded, softly shadowed, sitting on white
- **source:** compose the dotted-globe glow in CSS/canvas; Unsplash/Pexels API server-side only if a supporting photo is needed (never hotlink-scrape at request time)

## 7. Recolor slots (what may change on remix, what may NOT)
- **may recolor:** the mid gradient hue (→ violet / teal / cyan glow) and the acid-lime CTA (→ one other high-chroma pop: cyan / amber) — moved together; the deep-navy top and white base stay
- **must NOT change on remix:** the navy→blue→white vertical-gradient hero, the dotted-particle globe glow, the single-saturated-pill rule, the "New · Introducing" ribbon, the seamless dark-to-light handoff, and the calm near-white-on-dark headline weight
