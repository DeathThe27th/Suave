# EXTRACT.md — how to extract a style spec from a reference image

This is the instruction set an operator (you + Claude Code) follows to turn one
Pinterest screenshot in `/references/` into one tight `.md` spec in `/library/`.
The images never ship — they exist only during this offline step (Phase A).

## Inputs
- One reference image in `/references/`
- `SPEC-TEMPLATE.md` (the fixed format every entry must fill)

## The extraction prompt

Point Claude Code at the image and instruct:

> Read this reference image and fill **every** field of `SPEC-TEMPLATE.md`. Rules:
> 1. **Extract, don't copy.** Encode the *system* (exact hexes, type scale, section
>    order, spacing, the signature moves) so it survives being recolored and reused
>    with completely different content. Do not describe this specific page's copy.
> 2. **No blanks, no vibe words.** Every value is concrete: hex, px, weight, order.
>    "Modern and clean" is a failure. "bg #F1F0ED, ink #1A1E2C, one coral accent
>    #EA5C2B used only on eyebrows/stat-suffixes/one filled card" is a pass.
> 3. **Nail the signature moves (section 4).** This is the field that decides quality.
>    Name the specific, memorable, reproducible things (ghost watermark, `//` eyebrow
>    prefix, clipped floating card, black pill + trailing arrow). If you only wrote
>    "modern and clean" here, the spec is worthless — the generated pages drift to
>    the model's average.

## Verification (you, by eye — non-negotiable)

Before saving, check the filled spec against the original:
- Are the hex values actually right (sample them, don't guess)?
- Did it catch the signature moves, or hand-wave them?
- Would two *different* products generated from this spec look like siblings —
  and would neither look like a raw-model default?

If any answer is "no", the spec is too loose. Tighten it before saving. **Perfect one
before you do twenty** (BUILD.md, Rule 1).

## Save

Save to `/library/NN-<id>.md` (zero-padded index, kebab id). Spread the 20 across
deliberately different aesthetics — warm editorial, dark technical, brutalist, soft
consumer, minimal luxury, playful, maximalist, swiss/grid (BUILD.md, Rule 2).
