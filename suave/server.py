"""Suave service — FastAPI app, wrapped as MCP with FastMCP (both named in OKX docs).

Endpoints
  GET  /health         connectivity + library status (keep-warm / uptime ping)
  GET  /styles         list available library styles
  POST /generate       brief -> single self-contained HTML landing page

The same `generate` capability is exposed as an MCP tool so an AI client can call it
end-to-end (BUILD.md §3.5 pre-submit checklist). Run this module to serve both.

x402: gated behind CONFIG.x402_enabled, which stays false until Task Zero is resolved
(BUILD.md §3.2). When enabled, an unpaid /generate returns a 402 challenge.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse

from . import model, payment
from .config import CONFIG
from .library import list_specs
from .pipeline import generate

app = FastAPI(title="Suave", version="0.1.0")


@app.get("/health")
def health() -> dict:
    specs = list_specs()
    return {
        "status": "ok",
        "model": CONFIG.model,
        "model_key_set": bool(CONFIG.gemini_api_key),
        "library_count": len(specs),
        "vet_enabled": CONFIG.vet_enabled,
        "x402_enabled": CONFIG.x402_enabled,
    }


@app.get("/styles")
def styles() -> dict:
    return {
        "styles": [
            {"id": s.id, "one_line": s.one_line, "best_for": s.best_for, "avoid_for": s.avoid_for}
            for s in list_specs()
        ]
    }


@app.post("/generate")
async def generate_endpoint(request: Request) -> Response:
    headers_lower = {k.lower(): v for k, v in request.headers.items()}
    if payment.enabled() and not payment.is_paid(headers_lower):
        ch = payment.challenge()
        return JSONResponse(ch.body, status_code=ch.status, headers=ch.headers)

    try:
        payload = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid_json"}, status_code=400)

    try:
        result = generate(payload)
    except ValueError as e:  # bad brief
        return JSONResponse({"error": str(e)}, status_code=400)
    except model.RateLimited as e:  # provider quota — tell the caller how long to wait
        headers = {}
        if e.retry_after_s:
            headers["Retry-After"] = str(int(e.retry_after_s) + 1)
        return JSONResponse(
            {
                "error": "rate_limited",
                "message": str(e),
                "retry_after_s": round(e.retry_after_s) if e.retry_after_s else None,
            },
            status_code=429,
            headers=headers,
        )
    except Exception as e:  # degrade, don't hang or 500 silently
        return JSONResponse({"error": "generation_failed", "detail": str(e)}, status_code=502)

    # x402 flow: verify (above) -> serve -> settle -> return PAYMENT-RESPONSE.
    resp_headers: dict[str, str] = {}
    if payment.enabled():
        proof = headers_lower.get("x-payment") or headers_lower.get("payment-signature")
        settlement = payment.settle(proof) if proof else None
        if settlement is not None:
            import base64
            import json as _json

            resp_headers["PAYMENT-RESPONSE"] = base64.b64encode(_json.dumps(settlement).encode()).decode()

    fmt = str(payload.get("format", "html")).lower()
    if fmt == "json":
        return JSONResponse(
            {
                "style_id": result.style_id,
                "vetted": result.vetted,
                "repaired": result.repaired,
                "elapsed_s": result.elapsed_s,
                "notes": result.notes,
                "html": result.html,
            },
            headers=resp_headers,
        )
    return HTMLResponse(result.html, headers=resp_headers)


# --- MCP wrapper (FastMCP) -------------------------------------------------------
# Exposes `generate` as an MCP tool so an AI client / OKX A2MCP can call it.
def build_mcp():
    from fastmcp import FastMCP

    mcp = FastMCP("Suave")

    @mcp.tool()
    def generate_landing_page(
        product: str,
        what_it_does: str,
        audience: str = "",
        tone: str = "",
        style_id: str | None = None,
    ) -> str:
        """Generate a single self-contained HTML landing page with sourced design taste.

        Provide the product name and what it does; optionally an audience, tone, and a
        style_id from /styles (otherwise Suave picks a style by fit). Returns the full HTML.
        """
        result = generate(
            {
                "product": product,
                "what_it_does": what_it_does,
                "audience": audience,
                "tone": tone,
                "style_id": style_id,
            }
        )
        return result.html

    return mcp


if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
