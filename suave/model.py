"""Thin wrapper over the Anthropic Messages API.

Defaults follow the claude-api guidance: claude-opus-4-8, adaptive thinking, and
streaming (via .get_final_message()) so large HTML outputs don't hit HTTP timeouts.
Every call carries its own timeout + fallback so one slow model call can't blow the
whole request budget (BUILD.md §3.3).
"""

from __future__ import annotations

from functools import lru_cache

import anthropic

from .config import CONFIG


@lru_cache(maxsize=1)
def _client() -> anthropic.Anthropic:
    CONFIG.require_model()
    return anthropic.Anthropic(api_key=CONFIG.anthropic_api_key)


def complete(
    *,
    system: str,
    user: str,
    max_tokens: int = 16000,
    effort: str = "medium",
    timeout_s: float | None = None,
) -> str:
    """One streamed request; returns concatenated text. Raises on timeout/API error."""
    client = _client().with_options(timeout=timeout_s or CONFIG.model_timeout_s)
    parts: list[str] = []
    with client.messages.stream(
        model=CONFIG.model,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        final = stream.get_final_message()
    for block in final.content:
        if block.type == "text":
            parts.append(block.text)
    return "".join(parts).strip()
