"""The request pipeline (BUILD.md §2):

    1. BRIEF     parse the request
    2. STYLE     load spec (explicit id, or pick by best_for)
    3. COPY      \\  written into the assemble step (the model gets the brief + spec)
    4. IMAGES    fetch photography server-side, matched to the spec's imagery rules
    5. ASSEMBLE  pour copy + images into the skeleton, honoring signature moves
    6. VET       Impeccable detector -> one repair pass -> re-check (hard-capped)
    7. RETURN    single self-contained HTML file

Everything is timeout-aware. If generation exceeds budget we return a valid degraded
result rather than hanging — timeouts are how Olise died (BUILD.md §3.3).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from .assemble import assemble, repair
from .brief import parse_brief
from .config import CONFIG
from .images import fetch_images
from .style import pick_style
from .vet import detect


@dataclass
class Result:
    html: str
    style_id: str
    vetted: bool
    repaired: bool
    elapsed_s: float
    notes: list[str] = field(default_factory=list)


def _image_query(brief_summary: str, spec_best_for: str) -> str:
    # Cheap heuristic query; the spec's imagery rules constrain treatment, not subject.
    return f"{brief_summary.splitlines()[0].replace('Product:', '').strip()} {spec_best_for}".strip()[:80]


def generate(payload: dict) -> Result:
    start = time.monotonic()
    notes: list[str] = []

    # 1. BRIEF
    brief = parse_brief(payload)

    # 2. STYLE
    spec = pick_style(brief)

    # 4. IMAGES (best-effort; never raises)
    query = _image_query(brief.summary(), spec.best_for)
    images = fetch_images(query, count=3)
    if not images:
        notes.append("no image API key or no results — using palette-fit placeholders")

    # 3+5. COPY + ASSEMBLE
    html = assemble(brief, spec, images)

    # 6. VET + one repair pass (hard cap)
    vetted = False
    repaired = False
    remaining = CONFIG.call_budget_s - (time.monotonic() - start)
    if CONFIG.vet_enabled and remaining > CONFIG.vet_timeout_s:
        result = detect(html)
        vetted = result.ran
        if result.ran and not result.clean:
            remaining = CONFIG.call_budget_s - (time.monotonic() - start)
            if remaining > CONFIG.model_timeout_s:
                html = repair(html, result.findings)
                repaired = True
                recheck = detect(html)
                if recheck.ran and not recheck.clean:
                    notes.append("slop findings remained after one repair pass (hard cap reached)")
            else:
                notes.append("skipped repair pass — insufficient time budget remaining")

    return Result(
        html=html,
        style_id=spec.id,
        vetted=vetted,
        repaired=repaired,
        elapsed_s=round(time.monotonic() - start, 2),
        notes=notes,
    )
