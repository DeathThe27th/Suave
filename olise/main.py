"""Olise AI — agent-queryable football match intelligence service."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from types import SimpleNamespace

import httpx
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from olise import config, pipeline, scheduler as sched_mod
from olise.chain.xlayer import ChainClient
from olise.data.apifootball import ApiFootball, ApiFootballError, FixtureNotFound
from olise.report import render
from olise.settle.grade import settle_report, track_record
from olise.store.db import Store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("olise.main")

state = SimpleNamespace(store=None, af=None, chain=None, scheduler=None,
                        started_at=None)


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.store = Store()
    if config.FOOTBALL_DATA_TOKEN:
        from olise.data.footballdata import FootballData
        state.af = FootballData(state.store)
    else:
        state.af = ApiFootball(state.store)
    state.chain = ChainClient()
    await state.chain.setup()
    state.scheduler = sched_mod.build_scheduler(state)
    state.scheduler.start()
    state.started_at = datetime.now(timezone.utc).isoformat()
    log.info("Olise AI ready (store=%s, chain=%s)",
             state.store.backend.name, state.chain.mode)
    yield
    state.scheduler.shutdown(wait=False)
    await state.af.close()


app = FastAPI(
    title="Olise AI — Match Intelligence",
    description="Agent-queryable football match research analyst. Statistical "
                "forecasts with verified onchain accuracy records. "
                "Statistical research for informational purposes; not "
                "financial advice.",
    version="1.0.0",
    lifespan=lifespan,
)


class AnalyzeRequest(BaseModel):
    home: str = Field(..., min_length=2, examples=["Spain"])
    away: str = Field(..., min_length=2, examples=["Belgium"])
    date: str | None = Field(None, description="Optional YYYY-MM-DD kickoff date")


def _err(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status,
                        content={"error": code, "message": message})


@app.post("/analyze")
async def analyze(req: AnalyzeRequest,
                  x_admin_token: str | None = Header(default=None)):
    """Generate (or return the cached) research report for a fixture."""
    allow_started = bool(config.ADMIN_TOKEN
                         and x_admin_token == config.ADMIN_TOKEN)
    try:
        return await pipeline.analyze(
            state.store, state.af, state.chain,
            req.home.strip(), req.away.strip(), req.date,
            allow_started=allow_started)
    except FixtureNotFound as e:
        return _err(404, "fixture_not_found", str(e))
    except pipeline.MatchAlreadyStarted as e:
        return _err(409, "match_already_started", str(e))
    except ApiFootballError as e:
        return _err(502, "data_provider_error",
                    f"Upstream football data API error: {str(e)[:200]}")
    except httpx.HTTPError as e:
        return _err(502, "upstream_unreachable", str(e)[:200])


@app.get("/report/{report_id}")
async def get_report(report_id: str):
    rec = state.store.get_report(report_id)
    if not rec:
        return _err(404, "report_not_found", f"No report '{report_id}'")
    forecasts = state.store.get_forecasts(report_id)
    result = state.store.get_result(report_id)
    rj = rec.get("report_json") or {}
    return {
        "report_id": rec["report_id"],
        "status": rec["status"],
        "settled": rec.get("settled", False),
        "fixture": {
            "home": rec["home"], "away": rec["away"],
            "kickoff_utc": rec["kickoff_utc"],
            "competition": rec["competition"], "stage": rec["stage"],
            "fixture_id": rec["fixture_id"],
        },
        "summary": rj.get("summary"),
        "pdf_url": rec["pdf_url"],
        "forecasts": forecasts,
        "research": rj.get("research"),
        "engine": {k: v for k, v in (rj.get("engine") or {}).items()
                   if k not in ("goals_raw", "goals_adj")},
        "commitment": {
            "hash": rec.get("commit_hash"),
            "tx_hash": rec.get("tx_hash"),
            "explorer_url": rec.get("explorer_url"),
        },
        "versions": rec.get("versions"),
        "settlement": result,
    }


@app.get("/verify/{report_id}")
async def verify(report_id: str):
    rec = state.store.get_report(report_id)
    if not rec:
        return _err(404, "report_not_found", f"No report '{report_id}'")
    rj = rec.get("report_json") or {}
    return {
        "report_id": report_id,
        "commitment_hash": rec.get("commit_hash"),
        "tx_hash": rec.get("tx_hash"),
        "explorer_url": rec.get("explorer_url"),
        "contract_address": state.chain.address,
        "chain_id": state.chain.chain_id,
        "pdf_url": rec.get("pdf_url"),
        "pdf_sha256": rec.get("pdf_sha256"),
        "canonical_forecasts_json": rj.get("canonical_forecasts_json"),
        "recompute": [
            "1. Download the PDF from pdf_url (bytes must sha256-match pdf_sha256).",
            "2. Take canonical_forecasts_json exactly as returned here (UTF-8).",
            "3. Compute keccak256(pdf_bytes + canonical_forecasts_json_bytes).",
            "4. The result must equal commitment_hash, which was recorded in "
            "tx_hash on X Layer testnet before kickoff (see explorer_url).",
        ],
    }


@app.post("/settle/{report_id}")
async def settle(report_id: str,
                 x_admin_token: str | None = Header(default=None)):
    if not config.ADMIN_TOKEN or x_admin_token != config.ADMIN_TOKEN:
        raise HTTPException(401, "invalid admin token")
    rec = state.store.get_report(report_id)
    if not rec:
        return _err(404, "report_not_found", f"No report '{report_id}'")
    try:
        return await settle_report(rec, state.store, state.af,
                                   state.chain, render)
    except ApiFootballError as e:
        return _err(502, "data_provider_error", str(e)[:200])


@app.get("/track-record")
async def get_track_record():
    """Public accuracy record across all settled reports."""
    return track_record(state.store)


@app.get("/health")
async def health():
    checks = {}
    # data provider (cached to conserve quota)
    cached = state.store.cache_get("health:data", config.TTL_HEALTH)
    if cached is None:
        cached = await state.af.health_check()
        state.store.cache_set("health:data", "health", {}, cached)
    checks["data_provider"] = cached

    try:
        async with httpx.AsyncClient(timeout=10) as http:
            r = await http.get(
                f"{config.SUPABASE_URL}/storage/v1/bucket/{config.SUPABASE_BUCKET}",
                headers={"Authorization": f"Bearer {config.SUPABASE_SERVICE_ROLE_KEY}",
                         "apikey": config.SUPABASE_SERVICE_ROLE_KEY})
        checks["supabase_storage"] = {"ok": r.status_code == 200}
    except Exception as e:
        checks["supabase_storage"] = {"ok": False, "error": str(e)[:150]}

    checks["store"] = {"ok": True, "backend": state.store.backend.name}
    checks["chain"] = state.chain.health()
    checks["scheduler"] = {
        "running": bool(state.scheduler and state.scheduler.running),
        "jobs": sched_mod.job_status,
    }
    ok = (checks["data_provider"].get("ok")
          and checks["supabase_storage"].get("ok")
          and checks["chain"].get("ok"))
    return {"status": "ok" if ok else "degraded",
            "started_at": state.started_at, "checks": checks}


def run():
    import uvicorn
    uvicorn.run("olise.main:app", host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    run()
