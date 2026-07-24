"""Runtime configuration, read once from the environment.

Copy .env.example -> .env and fill it in. Nothing here is secret in source;
secrets live only in the environment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _env_float(name: str, default: float) -> float:
    raw = _env(name)
    try:
        return float(raw) if raw else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Config:
    # Model — default to the latest capable Claude (see BUILD.md §4).
    anthropic_api_key: str = field(default_factory=lambda: _env("ANTHROPIC_API_KEY"))
    model: str = field(default_factory=lambda: _env("SUAVE_MODEL", "claude-opus-4-8"))

    # Images — server-side API, never hotlink-scrape (BUILD.md §2).
    unsplash_access_key: str = field(default_factory=lambda: _env("UNSPLASH_ACCESS_KEY"))
    pexels_api_key: str = field(default_factory=lambda: _env("PEXELS_API_KEY"))

    # Library location.
    library_dir: Path = field(default_factory=lambda: REPO_ROOT / "library")

    # Timeout budget, seconds. Everything must return within this — timeouts are
    # how Olise died (BUILD.md §3.3). Well under whatever OKX's tester tolerates.
    call_budget_s: float = field(default_factory=lambda: _env_float("SUAVE_CALL_BUDGET_S", 45.0))
    model_timeout_s: float = field(default_factory=lambda: _env_float("SUAVE_MODEL_TIMEOUT_S", 25.0))
    image_timeout_s: float = field(default_factory=lambda: _env_float("SUAVE_IMAGE_TIMEOUT_S", 8.0))

    # Vet step (Impeccable detector). Keep a bypass so a detector failure degrades
    # to "return unvetted page" instead of "return nothing" (BUILD.md §2 vet step).
    vet_enabled: bool = field(default_factory=lambda: _env("SUAVE_VET_ENABLED", "true").lower() != "false")
    vet_timeout_s: float = field(default_factory=lambda: _env_float("SUAVE_VET_TIMEOUT_S", 10.0))

    # Payment — TASK ZERO is unresolved (BUILD.md §3.2). Off until the real
    # OKX Payment SDK / x402 spec is confirmed. Price is per call, in USDT.
    x402_enabled: bool = field(default_factory=lambda: _env("SUAVE_X402_ENABLED", "false").lower() == "true")
    price_usdt: float = field(default_factory=lambda: _env_float("SUAVE_PRICE_USDT", 0.03))

    def require_model(self) -> None:
        if not self.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set — the model layer cannot run.")


CONFIG = Config()
