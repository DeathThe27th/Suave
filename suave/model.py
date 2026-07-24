"""Thin wrapper over the Google Gemini API (google-genai SDK).

Suave runs on a Google Gemini free-tier key (not Anthropic). Defaults to
gemini-2.5-flash — fast and free-tier friendly. Calls stream (via
generate_content_stream) so large HTML outputs don't hit HTTP timeouts, and each
call carries its own timeout so one slow model call can't blow the whole request
budget (BUILD.md §3.3).
"""

from __future__ import annotations

from functools import lru_cache

from google import genai
from google.genai import types

from .config import CONFIG


@lru_cache(maxsize=1)
def _client() -> genai.Client:
    CONFIG.require_model()
    return genai.Client(api_key=CONFIG.gemini_api_key)


def _thinking(effort: str) -> types.ThinkingConfig:
    """Map our coarse effort knob onto a Gemini thinking budget.

    low  -> no thinking (fastest; used for the tiny style-pick + the repair pass)
    else -> dynamic thinking (the model decides how much to spend)
    """
    budget = 0 if effort == "low" else -1
    return types.ThinkingConfig(thinking_budget=budget)


def complete(
    *,
    system: str,
    user: str,
    max_tokens: int = 16000,
    effort: str = "medium",
    timeout_s: float | None = None,
) -> str:
    """One streamed request; returns concatenated text. Raises on timeout/API error."""
    timeout_ms = int((timeout_s or CONFIG.model_timeout_s) * 1000)
    config = types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=max_tokens,
        thinking_config=_thinking(effort),
        http_options=types.HttpOptions(timeout=timeout_ms),
    )
    parts: list[str] = []
    for chunk in _client().models.generate_content_stream(
        model=CONFIG.model,
        contents=user,
        config=config,
    ):
        if chunk.text:
            parts.append(chunk.text)
    return "".join(parts).strip()
