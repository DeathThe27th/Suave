"""Step 6 — VET. Run the Impeccable detector over the generated HTML.

`npx impeccable detect` — 46 deterministic rules, no LLM call, exit codes only
(BUILD.md §2). Wire as a post-assembly check. On flags, the pipeline feeds the
anti-patterns back for ONE repair pass, then re-detects (hard cap — a runaway loop
is a timeout, and timeouts are how Olise died).

MUST VERIFY on the VPS: that this runs headless inside the request path and how long
it takes. Keep the bypass flag (CONFIG.vet_enabled) so a detector failure degrades to
"return unvetted page", never "return nothing".
"""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .config import CONFIG


@dataclass
class VetResult:
    ran: bool
    clean: bool
    findings: str = ""  # raw detector output, fed back to the repair pass


def detect(html: str) -> VetResult:
    """Return a VetResult. Never raises — a broken detector must not break the request."""
    if not CONFIG.vet_enabled:
        return VetResult(ran=False, clean=True)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "page.html"
            f.write_text(html, encoding="utf-8")
            proc = subprocess.run(
                ["npx", "--yes", "impeccable", "detect", str(f)],
                capture_output=True,
                text=True,
                timeout=CONFIG.vet_timeout_s,
            )
        clean = proc.returncode == 0
        return VetResult(ran=True, clean=clean, findings="" if clean else (proc.stdout + proc.stderr).strip())
    except Exception:
        # Detector unavailable / timed out: degrade gracefully, do not block the page.
        return VetResult(ran=False, clean=True)
