"""Thin wrapper over the Google Gemini API (google-genai SDK).

Suave runs on a Google Gemini free-tier key (not Anthropic). Defaults to
gemini-2.5-flash — fast and free-tier friendly. Calls stream (via
generate_content_stream) so large HTML outputs don't hit HTTP timeouts, and each
call carries its own timeout so one slow model call can't blow the whole request
budget (BUILD.md §3.3).
"""

from __future__ import annotations

import re
from functools import lru_cache

from google import genai
from google.genai import errors as genai_errors
from google.genai import types

from .config import CONFIG


class RateLimited(RuntimeError):
    """Gemini returned 429 / RESOURCE_EXHAUSTED (free-tier quota).

    Carries the provider's own "retry in Ns" hint so callers can tell the user how
    long to wait instead of surfacing a raw stack trace.
    """

    def __init__(self, retry_after_s: float | None):
        self.retry_after_s = retry_after_s
        super().__init__(rate_limit_message(retry_after_s))


def format_wait(seconds: float | None) -> str:
    """Human wait string: '~45 seconds', '~2 min 10s', or a gentle fallback."""
    if not seconds or seconds <= 0:
        return "a little while"
    s = int(round(seconds))
    if s < 60:
        return f"~{s} second{'s' if s != 1 else ''}"
    m, r = divmod(s, 60)
    return f"~{m} min {r}s" if r else f"~{m} min"


def rate_limit_message(seconds: float | None) -> str:
    return (
        f"Gemini free-tier rate limit reached. Please wait {format_wait(seconds)} "
        "and try again."
    )


_RETRY_PATTERNS = (
    re.compile(r"retry in ([\d.]+)\s*s", re.I),
    re.compile(r"retryDelay['\"]?\s*[:=]\s*['\"]?([\d.]+)s", re.I),
)


def _retry_after(err: Exception) -> float | None:
    """Pull the retry-after seconds out of a Gemini 429 (message or RetryInfo)."""
    text = str(err)
    for pat in _RETRY_PATTERNS:
        m = pat.search(text)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                pass
    return None


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
    try:
        for chunk in _client().models.generate_content_stream(
            model=CONFIG.model,
            contents=user,
            config=config,
        ):
            if chunk.text:
                parts.append(chunk.text)
    except genai_errors.APIError as e:
        if getattr(e, "code", None) == 429 or "RESOURCE_EXHAUSTED" in str(e):
            raise RateLimited(_retry_after(e)) from e
        raise
    return "".join(parts).strip()
