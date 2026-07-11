"""Background jobs (APScheduler, in-process): lineup watcher, auto-settlement,
self-ping. All jobs are idempotent and never propagate exceptions."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from olise import config, pipeline
from olise.settle.grade import settle_report
from olise.report import render

log = logging.getLogger("olise.scheduler")

job_status: dict[str, dict] = {}


def _wrap(name):
    def deco(fn):
        async def runner(*a, **kw):
            job_status[name] = {"last_run": datetime.now(timezone.utc).isoformat(),
                                "ok": None, "detail": "running"}
            try:
                detail = await fn(*a, **kw)
                job_status[name].update(ok=True, detail=detail or "ok")
            except Exception as e:
                log.exception("job %s failed", name)
                job_status[name].update(ok=False, detail=str(e)[:200])
        runner.__name__ = name
        return runner
    return deco


def build_scheduler(state) -> AsyncIOScheduler:
    sched = AsyncIOScheduler(timezone="UTC")

    @_wrap("lineup_watcher")
    async def lineup_watcher():
        now = datetime.now(timezone.utc)
        upgraded = 0
        for rec in state.store.list_reports(status="provisional"):
            if rec.get("settled"):
                continue
            try:
                kickoff = datetime.fromisoformat(rec["kickoff_utc"])
            except (ValueError, TypeError):
                continue
            if not (now <= kickoff <= now + timedelta(hours=2)):
                continue
            # re-run the pipeline; if lineups have landed the input hash
            # changes and a FINAL version is issued under the same report_id
            resp = await pipeline.analyze(
                state.store, state.af, state.chain,
                rec["home"], rec["away"], rec["kickoff_utc"][:10])
            if resp["status"] == "final" and not resp["cached"]:
                upgraded += 1
        return f"checked provisional reports, upgraded {upgraded}"

    @_wrap("auto_settlement")
    async def auto_settlement():
        now = datetime.now(timezone.utc)
        settled = 0
        for rec in state.store.list_reports(settled=False):
            if not rec.get("commit_hash"):
                continue
            try:
                kickoff = datetime.fromisoformat(rec["kickoff_utc"])
            except (ValueError, TypeError):
                continue
            # match (~2h) + required 2h post-final-whistle buffer
            if now < kickoff + timedelta(hours=4):
                continue
            out = await settle_report(rec, state.store, state.af,
                                      state.chain, render)
            if out.get("settled"):
                settled += 1
        return f"settled {settled} report(s)"

    @_wrap("self_ping")
    async def self_ping():
        async with httpx.AsyncClient(timeout=15) as http:
            r = await http.get(f"{config.SELF_URL}/health")
            return f"health {r.status_code}"

    sched.add_job(lineup_watcher, "interval", minutes=10, id="lineup_watcher")
    sched.add_job(auto_settlement, "interval", minutes=30, id="auto_settlement")
    sched.add_job(self_ping, "interval", minutes=10, id="self_ping")
    return sched
