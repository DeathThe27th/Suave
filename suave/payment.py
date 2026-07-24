"""x402 / payment layer — TASK ZERO, still unresolved (BUILD.md §3.2).

The Olise rejection told us to integrate x402 so unpaid requests return a standard 402
challenge; the ASP docs imply the platform settles via the OKX Payment SDK automatically.
Those two need reconciling and we will NOT build the payment layer on a guess — this is
the exact thing that failed. Until the real spec is confirmed (ask OKX support; check
`npx skills add okx/onchainos-skills`), CONFIG.x402_enabled stays false and every request
is served free.

When enabled, `challenge()` returns the 402 body/headers to emit for an unpaid request,
and `is_paid()` validates an incoming payment proof. Both are stubs pending the real spec.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import CONFIG


@dataclass
class Challenge:
    status: int
    headers: dict[str, str]
    body: dict


def enabled() -> bool:
    return CONFIG.x402_enabled


def is_paid(headers: dict[str, str]) -> bool:
    """Validate a payment proof from the request. STUB — real check pending Task Zero."""
    if not CONFIG.x402_enabled:
        return True
    # TODO(task-zero): verify the X-PAYMENT / PAYMENT-SIGNATURE proof against the OKX
    # Payment SDK / x402 spec before trusting it. Do not guess the scheme.
    return bool(headers.get("x-payment") or headers.get("payment-signature"))


def challenge() -> Challenge:
    """The 402 body to return for an unpaid request. Shape is a placeholder."""
    return Challenge(
        status=402,
        headers={"WWW-Authenticate": "Payment"},
        body={
            "error": "payment_required",
            "price_usdt": CONFIG.price_usdt,
            "note": "x402 scheme pending confirmation with OKX (Task Zero).",
        },
    )
