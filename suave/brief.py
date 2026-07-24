"""Step 1 — BRIEF. Normalize the incoming request into a structured brief.

The request is small and trusted-shape; we don't need a model call to parse it.
We just clean it up and fill sensible defaults so downstream steps never see None.
"""

from __future__ import annotations

from dataclasses import dataclass, field

DEFAULT_SECTIONS = ["hero", "about", "advantages", "process", "testimonials", "faq", "cta", "footer"]


@dataclass
class Brief:
    product: str
    what_it_does: str
    audience: str = ""
    tone: str = ""
    sections: list[str] = field(default_factory=lambda: list(DEFAULT_SECTIONS))
    style_id: str | None = None  # explicit style, or None to let Suave pick by best_for

    def summary(self) -> str:
        bits = [f"Product: {self.product}", f"What it does: {self.what_it_does}"]
        if self.audience:
            bits.append(f"Audience: {self.audience}")
        if self.tone:
            bits.append(f"Tone: {self.tone}")
        bits.append(f"Sections: {', '.join(self.sections)}")
        return "\n".join(bits)


def parse_brief(payload: dict) -> Brief:
    product = str(payload.get("product") or payload.get("name") or "").strip()
    what = str(payload.get("what_it_does") or payload.get("description") or "").strip()
    if not product or not what:
        raise ValueError("Brief requires 'product' and 'what_it_does'.")
    sections = payload.get("sections")
    if not isinstance(sections, list) or not sections:
        sections = list(DEFAULT_SECTIONS)
    return Brief(
        product=product,
        what_it_does=what,
        audience=str(payload.get("audience") or "").strip(),
        tone=str(payload.get("tone") or "").strip(),
        sections=[str(s).strip() for s in sections if str(s).strip()],
        style_id=(str(payload["style_id"]).strip() if payload.get("style_id") else None),
    )
