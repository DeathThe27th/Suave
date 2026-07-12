"""End-to-end analysis pipeline: data → research → engine → forecasts →
PDF → storage → onchain commitment. Pure function of the input dataset:
identical input data returns the cached report without re-committing."""

from __future__ import annotations

import asyncio
import hashlib
import logging
from datetime import datetime, timezone

from olise import config
from olise.data.apifootball import FINISHED
from olise.engine.core import run_engine
from olise.forecasts.build import (build_forecasts, build_summary,
                                   canonical_forecasts_json, input_hash)
from olise.chain.xlayer import commitment_hash
from olise.report import render
from olise.research.context import research_fixture

log = logging.getLogger("olise.pipeline")

_analyze_lock = asyncio.Lock()


class MatchAlreadyStarted(Exception):
    pass


def _response_from_report(rec: dict, forecasts: list[dict], cached: bool) -> dict:
    rj = rec.get("report_json") or {}
    return {
        "report_id": rec["report_id"],
        "status": rec["status"],
        "cached": cached,
        "fixture": {
            "home": rec["home"], "away": rec["away"],
            "kickoff_utc": rec["kickoff_utc"],
            "competition": rec["competition"], "stage": rec["stage"],
            "fixture_id": rec["fixture_id"],
        },
        "pdf_url": rec["pdf_url"],
        "summary": rj.get("summary"),
        "forecasts": forecasts,
        "contradictions": (rj.get("engine") or {}).get("contradictions", []),
        "commitment": {
            "hash": rec.get("commit_hash"),
            "tx_hash": rec.get("tx_hash"),
            "explorer_url": rec.get("explorer_url"),
        },
        "research_note": (rj.get("research") or {}).get("note"),
        "retrospective": rj.get("retrospective", False),
    }


async def analyze(store, af, chain, home: str, away: str,
                  date: str | None = None, allow_started: bool = False,
                  force: bool = False) -> dict:
    async with _analyze_lock:
        return await _analyze(store, af, chain, home, away, date,
                              allow_started, force)


async def _analyze(store, af, chain, home, away, date, allow_started,
                   force=False) -> dict:
    fixture = await af.resolve_fixture(home, away, date)
    fx = fixture["fixture"]
    kickoff = datetime.fromisoformat(fx["date"])
    now = datetime.now(timezone.utc)
    started = kickoff <= now or fx["status"]["short"] in FINISHED
    if started and not allow_started:
        raise MatchAlreadyStarted(
            f"Fixture {fixture['teams']['home']['name']} vs "
            f"{fixture['teams']['away']['name']} ({fx['date']}) has already "
            "started or finished. Prediction reports are only issued before "
            "kickoff.")

    dataset = await af.fixture_dataset(fixture)

    if started:
        research = {"factors": [],
                    "note": "fixture already played — research pass skipped "
                            "(retrospective analysis for grading demonstration)",
                    "grounded": False}
    else:
        research = await research_fixture(dataset)
    factors = research["factors"]

    ih = input_hash(dataset, factors)

    # consistency cache: same fixture + same normalized input → same report
    # (admin `force` bypasses it and issues a new version instead)
    existing = store.find_reports_by_fixture(dataset["fixture"]["id"])
    for rec in existing if not force else []:
        if rec.get("input_hash") == ih:
            if rec.get("commit_hash") and not rec.get("tx_hash"):
                # earlier commit tx failed — heal it, never re-render
                try:
                    commitment = await chain.commit(
                        rec["commit_hash"], rec["report_id"])
                    rec["tx_hash"] = commitment.get("tx_hash")
                    rec["explorer_url"] = commitment.get("explorer_url")
                    store.upsert_report(rec)
                except Exception as e:
                    log.warning("commit retry failed for %s: %s",
                                rec["report_id"], str(e)[:150])
            return _response_from_report(
                rec, store.get_forecasts(rec["report_id"]), cached=True)

    engine = run_engine(dataset, factors)
    forecasts = build_forecasts(dataset, engine, factors)
    summary = build_summary(dataset, engine, forecasts, research)
    status = "final" if dataset["lineups"]["available"] else "provisional"

    if existing:
        rec = sorted(existing, key=lambda r: r.get("created_at") or "")[0]
        report_id = rec["report_id"]
        versions = rec.get("versions") or []
        created_at = rec.get("created_at")
    else:
        report_id = f"OLISE-{dataset['fixture']['id']}-{ih[:8]}"
        versions, created_at = [], None
    version_no = len(versions) + 1

    ctx = render.assemble_context(report_id, status, dataset, engine,
                                  research, forecasts, summary)
    pdf = await render.render_pdf_async(ctx)
    pdf_url = await render.upload_pdf(report_id, pdf, version_no)
    pdf_sha = hashlib.sha256(pdf).hexdigest()

    canonical = canonical_forecasts_json(forecasts)
    c_hash = commitment_hash(pdf, canonical)
    commitment = {}
    try:
        commitment = await chain.commit(c_hash, report_id)
    except Exception as e:
        log.error("onchain commit failed for %s: %s", report_id, str(e)[:200])
        commitment = {"hash": c_hash, "tx_hash": None, "explorer_url": None,
                      "error": str(e)[:200]}

    versions.append({
        "version": version_no, "status": status, "input_hash": ih,
        "pdf_url": pdf_url, "pdf_sha256": pdf_sha, "commit_hash": c_hash,
        "tx_hash": commitment.get("tx_hash"),
        "created_at": now.isoformat(),
    })

    rec = {
        "report_id": report_id,
        "fixture_id": dataset["fixture"]["id"],
        "cache_key": f"{dataset['fixture']['id']}:{ih}",
        "home": dataset["home"]["name"],
        "away": dataset["away"]["name"],
        "kickoff_utc": dataset["fixture"]["date_utc"],
        "competition": dataset["fixture"]["competition"],
        "stage": dataset["fixture"]["stage"],
        "status": status,
        "input_hash": ih,
        "pdf_url": pdf_url,
        "pdf_sha256": pdf_sha,
        "commit_hash": c_hash,
        "tx_hash": commitment.get("tx_hash"),
        "explorer_url": commitment.get("explorer_url"),
        "settled": False,
        "created_at": created_at,
        "report_json": {
            "summary": summary,
            "dataset": dataset,
            "research": research,
            "engine": engine,
            "canonical_forecasts_json": canonical,
            "retrospective": started,
        },
        "versions": versions,
    }
    store.upsert_report(rec)
    store.save_forecasts(report_id, forecasts)

    return _response_from_report(rec, forecasts, cached=False)
