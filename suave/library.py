"""Load the style-spec library from flat .md files at startup.

The library IS the product (BUILD.md §1). Specs are read once and cached; a spec
is just its raw markdown plus the parsed identity fields Suave needs to pick one.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .config import CONFIG

_FIELD_RE = re.compile(r"^\s*-\s*\*\*(?P<key>[a-z][a-z_-]*):\*\*\s*(?P<val>.+?)\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class Spec:
    id: str
    one_line: str
    best_for: str
    avoid_for: str
    markdown: str
    path: Path


def _parse(md: str, path: Path) -> Spec | None:
    """Pull the section-0 identity fields; the full markdown is passed to the model."""
    fields: dict[str, str] = {}
    for line in md.splitlines():
        m = _FIELD_RE.match(line)
        if m:
            fields[m.group("key").lower()] = m.group("val").strip()
    spec_id = fields.get("id") or path.stem
    if not spec_id:
        return None
    return Spec(
        id=spec_id,
        one_line=fields.get("one-line", fields.get("one_line", "")),
        best_for=fields.get("best_for", ""),
        avoid_for=fields.get("avoid_for", ""),
        markdown=md,
        path=path,
    )


@lru_cache(maxsize=1)
def load_library() -> dict[str, Spec]:
    """Return {id: Spec} for every NN-*.md in the library dir. Cached for the process."""
    specs: dict[str, Spec] = {}
    for path in sorted(CONFIG.library_dir.glob("*.md")):
        if path.name.upper().startswith(("SPEC-TEMPLATE", "STYLE-SPEC")):
            continue
        spec = _parse(path.read_text(encoding="utf-8"), path)
        if spec:
            specs[spec.id] = spec
    return specs


def get_spec(style_id: str) -> Spec | None:
    return load_library().get(style_id)


def list_specs() -> list[Spec]:
    return list(load_library().values())
