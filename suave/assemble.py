"""Steps 3 + 5 — COPY + ASSEMBLE. Pour the brief into the spec's skeleton as HTML.

The model receives the *full spec markdown* (the encoded system: palette, type scale,
section order, signature moves, spacing) plus the brief and the fetched image URLs, and
returns ONE self-contained HTML file. Single-file HTML is the v1 output (BUILD.md §2):
self-contained, no build step, no dependency that can 404 during OKX's review.

If the vet step flags slop, repair() runs exactly one fix pass (hard-capped).
"""

from __future__ import annotations

import re

from .brief import Brief
from .library import Spec
from .model import complete

_ASSEMBLE_SYSTEM = """You are Suave's page assembler. You are given ONE design-system \
spec and a product brief. Produce ONE complete, self-contained HTML landing page that \
faithfully executes the spec.

Hard rules:
- Output ONLY the HTML document. No markdown fences, no commentary before or after.
- Self-contained single file: inline all CSS in a <style> tag. No external CSS/JS, no \
build step, no CDN that could 404. Web fonts via a single Google Fonts <link> are allowed.
- Honor the spec EXACTLY: use its named hex values, its type scale, its numbered section \
order, and — most importantly — every one of its signature moves. The signature moves are \
what stop this from looking like a raw-model default. Do not drop them.
- Write real landing copy grounded in the brief. No filler adjectives, no lorem ipsum, no \
"revolutionize your workflow" slop. Concrete, specific, product-true sentences.
- Use the provided image URLs in <img> tags where the spec calls for photography. If none \
are provided, use tasteful CSS/gradient placeholders that fit the palette — never broken \
image links.
- Responsive; must not scroll horizontally on mobile."""

_REPAIR_SYSTEM = """You are Suave's slop repair pass. You are given an HTML landing page \
and a list of anti-pattern findings from a deterministic detector. Fix ONLY the flagged \
issues while preserving the design system, layout, copy, and signature moves. Output ONLY \
the corrected, complete HTML document — no fences, no commentary."""


def _strip_fences(text: str) -> str:
    """Models sometimes wrap output in ```html fences despite instructions."""
    m = re.search(r"```(?:html)?\s*(.*?)```", text, re.DOTALL)
    body = m.group(1) if m else text
    return body.strip()


def assemble(brief: Brief, spec: Spec, image_urls: list[str], *, timeout_s: float | None = None) -> str:
    imgs = "\n".join(f"- {u}" for u in image_urls) if image_urls else "(none — use palette-fit placeholders)"
    user = (
        f"# Design system spec\n\n{spec.markdown}\n\n"
        f"# Product brief\n\n{brief.summary()}\n\n"
        f"# Image URLs (server-fetched, safe to embed)\n{imgs}\n\n"
        "Assemble the landing page now."
    )
    html = complete(system=_ASSEMBLE_SYSTEM, user=user, max_tokens=32000, effort="medium", timeout_s=timeout_s)
    return _strip_fences(html)


def repair(html: str, findings: str, *, timeout_s: float | None = None) -> str:
    user = f"# Findings\n{findings}\n\n# HTML to fix\n{html}"
    fixed = complete(system=_REPAIR_SYSTEM, user=user, max_tokens=32000, effort="low", timeout_s=timeout_s)
    return _strip_fences(fixed)
