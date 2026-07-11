"""Post-match settlement: grade every published forecast against the final
statistics, store the outcome, and record it onchain."""

from __future__ import annotations

import json
import logging
import re

log = logging.getLogger("olise.settle")


def _combined(result: dict, key: str):
    h = (result["stats"].get("home") or {}).get(key)
    a = (result["stats"].get("away") or {}).get(key)
    if h is None or a is None:
        return None
    return h + a


def grade_forecast(f: dict, result: dict, home: str, away: str) -> str:
    """Returns 'correct' | 'incorrect' | 'void' (stat unavailable)."""
    market = f["market"]
    sel = f["selection"]

    # 90-minute score is the market convention; fall back to overall goals
    ft = result.get("score_90") or {}
    gh = ft.get("home") if ft.get("home") is not None else result["goals_home"]
    ga = ft.get("away") if ft.get("away") is not None else result["goals_away"]
    if gh is None or ga is None:
        return "void"

    def verdict(cond: bool) -> str:
        return "correct" if cond else "incorrect"

    if market == "Match result (1X2)":
        if sel == f"{home} win":
            return verdict(gh > ga)
        if sel == "Draw":
            return verdict(gh == ga)
        if sel == f"{away} win":
            return verdict(ga > gh)
        return "void"

    if market == "Double chance":
        if sel == f"{home} or draw":
            return verdict(gh >= ga)
        if sel == f"{home} or {away}":
            return verdict(gh != ga)
        if sel == f"Draw or {away}":
            return verdict(ga >= gh)
        return "void"

    if market == "Both teams to score":
        yes = gh > 0 and ga > 0
        return verdict(yes if sel == "Yes" else not yes)

    if market == "Total goals":
        m = re.match(r"(Over|Under) ([\d.]+)", sel)
        if not m:
            return "void"
        line = float(m.group(2))
        total = gh + ga
        return verdict(total > line if m.group(1) == "Over" else total < line)

    if market == "Team total goals":
        m = re.match(rf"(.+) over ([\d.]+)", sel)
        if not m:
            return "void"
        team, line = m.group(1), float(m.group(2))
        goals = gh if team == home else (ga if team == away else None)
        if goals is None:
            return "void"
        return verdict(goals > line)

    if market in ("Corners", "Cards", "Shots"):
        key = market.lower()
        total = _combined(result, key)
        if total is None:
            return "void"
        m = re.match(r"(Over|Under) ([\d.]+)", sel)
        if not m:
            return "void"
        line = float(m.group(2))
        return verdict(total > line if m.group(1) == "Over" else total < line)

    if market == "Goal kicks (total range)":
        total = _combined(result, "goal_kicks")
        if total is None:
            return "void"
        m = re.match(r"(\d+)–(\d+)", sel)
        if not m:
            return "void"
        lo, hi = int(m.group(1)), int(m.group(2))
        return verdict(lo <= total <= hi)

    return "void"


async def settle_report(report: dict, store, af, chain, render_mod) -> dict:
    """Full settlement pass for one committed report. Idempotent."""
    report_id = report["report_id"]
    if report.get("settled"):
        existing = store.get_result(report_id)
        return {"report_id": report_id, "already_settled": True,
                "result": existing}

    result = await af.fixture_result_stats(report["fixture_id"])
    if result is None:
        return {"report_id": report_id, "settled": False,
                "reason": "final statistics not yet available"}

    forecasts = store.get_forecasts(report_id)
    home, away = report["home"], report["away"]
    graded, correct, total = [], 0, 0
    for row in forecasts:
        f = {"market": row["market"], "selection": row["selection"]}
        outcome = grade_forecast(f, result, home, away)
        store.update_forecast_outcome(report_id, row["idx"], outcome)
        graded.append({**f, "probability": row["probability"],
                       "grade": row["grade"], "outcome": outcome})
        if outcome == "correct":
            correct += 1
        if outcome in ("correct", "incorrect"):
            total += 1

    results_doc = json.dumps({
        "report_id": report_id,
        "fixture_id": report["fixture_id"],
        "final_score": f"{result['goals_home']}-{result['goals_away']}",
        "statistics": result["stats"],
        "forecasts": graded,
        "correct": correct,
        "graded_total": total,
    }, indent=2)
    try:
        results_uri = await render_mod.upload_json(
            f"{report_id}/results.json", results_doc)
    except Exception as e:
        log.warning("results upload failed: %s", str(e)[:150])
        results_uri = ""

    settle_tx = {}
    if report.get("commit_hash"):
        try:
            settle_tx = await chain.settle(
                report["commit_hash"], results_uri or report_id, correct, total)
        except Exception as e:
            log.warning("onchain settle failed for %s: %s", report_id, str(e)[:150])

    store.save_result({
        "report_id": report_id,
        "fixture_id": report["fixture_id"],
        "results_json": results_doc,
        "correct": correct,
        "total": total,
        "settle_tx": settle_tx.get("tx_hash"),
        "results_uri": results_uri,
    })
    report["settled"] = True
    store.upsert_report(report)

    return {
        "report_id": report_id,
        "settled": True,
        "final_score": f"{result['goals_home']}-{result['goals_away']}",
        "correct": correct,
        "graded_total": total,
        "void": len(graded) - total,
        "results_uri": results_uri,
        "settle_tx": settle_tx,
        "forecasts": graded,
    }


def track_record(store) -> dict:
    """Aggregate accuracy overall, per market and per grade."""
    rows = [r for r in store.all_forecasts()
            if r.get("outcome") in ("correct", "incorrect")]

    def bucket(items):
        n = len(items)
        c = sum(1 for r in items if r["outcome"] == "correct")
        return {"graded": n, "correct": c,
                "accuracy": round(c / n, 4) if n else None}

    per_market, per_grade = {}, {}
    for r in rows:
        per_market.setdefault(r["market"], []).append(r)
        per_grade.setdefault(r["grade"], []).append(r)

    return {
        "overall": bucket(rows),
        "per_market": {k: bucket(v) for k, v in sorted(per_market.items())},
        "per_grade": {k: bucket(v) for k, v in sorted(per_grade.items())},
        "settled_reports": len(store.all_results()),
    }
