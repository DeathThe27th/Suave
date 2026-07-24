"""x402 seller layer — Task Zero (BUILD.md §3.2), now partly resolved.

CONFIRMED (from the local okx-agent-payments-protocol skill, which is the *buyer* side):
a seller emits an x402 402 whose challenge a buyer decodes from the `PAYMENT-REQUIRED`
header (v2, base64 JSON) or the body `x402Version` field (v1). Each `accepts[]` entry
carries `scheme` / `network` / `asset` / `amount` (v2) or `maxAmountRequired` (v1) /
`payTo`. Header names are byte-exact per the protocol: `PAYMENT-REQUIRED`, `X-PAYMENT`,
`PAYMENT-SIGNATURE`. So `challenge()` below emits a real, spec-shaped x402 challenge.

STILL OPEN (the reason x402 stays OFF by default): the *seller-side* verify/settle path.
The buyer's OKX wallet signs and the buyer-side facilitator settles — but whether Suave
must POST the payment proof to an x402 facilitator (`/verify`, `/settle`) itself, or the
OKX A2MCP gateway fronts billing entirely (as the ASP docs imply), is not in the local
skills. Confirm with OKX support before enabling. `verify()` below is written against the
standard x402 facilitator contract and is inert until `X402_FACILITATOR_URL` is set.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass

import httpx

from .config import CONFIG


@dataclass
class Challenge:
    status: int
    headers: dict[str, str]
    body: dict


def enabled() -> bool:
    return CONFIG.x402_enabled


def _atomic_price() -> str:
    """Price in the asset's base units, as the string x402 expects."""
    return str(int(round(CONFIG.price_usdt * (10**CONFIG.x402_asset_decimals))))


def _requirements() -> dict:
    """One x402 PaymentRequirements entry (the `accepts[]` element)."""
    amount = _atomic_price()
    return {
        "scheme": "exact",
        "network": CONFIG.x402_network,
        "asset": CONFIG.x402_asset,
        "payTo": CONFIG.x402_pay_to,
        "amount": amount,  # v2 field
        "maxAmountRequired": amount,  # v1 field — emit both for buyer compatibility
        "resource": CONFIG.x402_resource,
        "description": "Suave — one self-contained HTML landing page",
        "mimeType": "text/html",
        "maxTimeoutSeconds": int(CONFIG.call_budget_s) + 30,
    }


def challenge() -> Challenge:
    """The 402 to return for an unpaid request. Spec-shaped x402 (v1 body + v2 header)."""
    body = {
        "x402Version": CONFIG.x402_version,
        "accepts": [_requirements()],
        "error": "payment required",
    }
    header = base64.b64encode(json.dumps(body).encode()).decode()
    return Challenge(
        status=402,
        headers={"PAYMENT-REQUIRED": header},  # v2 delivery; body carries v1
        body=body,
    )


def _payment_proof(headers: dict[str, str]) -> str | None:
    return headers.get("x-payment") or headers.get("payment-signature")


def is_paid(headers: dict[str, str]) -> bool:
    """True if the request carries a payment proof this seller can verify.

    With a facilitator configured, verify the proof against it (standard x402). Without
    one, we cannot verify a seller-side payment — so we refuse (return False) rather than
    trust an unverified header. This is the open half of Task Zero; x402 stays off until
    the facilitator (or gateway) contract is confirmed with OKX.
    """
    if not CONFIG.x402_enabled:
        return True
    proof = _payment_proof(headers)
    if not proof:
        return False
    if not CONFIG.x402_facilitator_url:
        return False  # cannot verify without the (unconfirmed) facilitator/gateway
    return verify(proof)


def verify(proof: str) -> bool:
    """POST the proof + requirements to the x402 facilitator's /verify. Never raises."""
    try:
        r = httpx.post(
            f"{CONFIG.x402_facilitator_url.rstrip('/')}/verify",
            json={"x402Version": CONFIG.x402_version, "paymentPayload": proof, "paymentRequirements": _requirements()},
            timeout=CONFIG.image_timeout_s,
        )
        r.raise_for_status()
        return bool(r.json().get("isValid"))
    except Exception:
        return False


def settle(proof: str) -> dict | None:
    """POST to the facilitator's /settle after serving. Returns the settlement, or None.

    x402 flow: verify -> serve -> settle -> return a PAYMENT-RESPONSE header. Inert until
    the facilitator contract is confirmed.
    """
    if not (CONFIG.x402_enabled and CONFIG.x402_facilitator_url):
        return None
    try:
        r = httpx.post(
            f"{CONFIG.x402_facilitator_url.rstrip('/')}/settle",
            json={"x402Version": CONFIG.x402_version, "paymentPayload": proof, "paymentRequirements": _requirements()},
            timeout=CONFIG.image_timeout_s,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return None
