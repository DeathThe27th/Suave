"""Step 2 — STYLE. Load the spec the brief will be poured into.

If the brief names a style_id, use it. Otherwise pick by best_for: a fast, cheap
model call that only chooses among existing library ids (never invents a style).
"""

from __future__ import annotations

from .brief import Brief
from .library import Spec, get_spec, list_specs
from .model import complete

_PICK_SYSTEM = (
    "You match a product brief to the single best design style from a fixed list. "
    "Reply with ONLY the chosen id, exactly as written, nothing else."
)


def pick_style(brief: Brief) -> Spec:
    specs = list_specs()
    if not specs:
        raise RuntimeError("Library is empty — no specs in /library to pour into.")

    if brief.style_id:
        spec = get_spec(brief.style_id)
        if spec is None:
            raise ValueError(f"Unknown style_id: {brief.style_id!r}")
        return spec

    if len(specs) == 1:
        return specs[0]

    catalog = "\n".join(f"- {s.id}: best_for {s.best_for} | avoid_for {s.avoid_for}" for s in specs)
    user = f"{brief.summary()}\n\nStyles:\n{catalog}\n\nWhich id best fits this brief?"
    choice = complete(system=_PICK_SYSTEM, user=user, max_tokens=64, effort="low").strip()
    return get_spec(choice) or specs[0]
