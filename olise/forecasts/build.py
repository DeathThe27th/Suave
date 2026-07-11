"""Forecast generation, confidence grading and consistency hashing.

Every market whose adjusted model probability ≥ 55% is published as a
forecast graded A (≥75%), B (65–74%) or C (55–64%). Forecasts hit by a
contradiction flag are downgraded to C (never silently averaged).
"""

from __future__ import annotations

import hashlib
import json

from olise import config


def grade_for(p: float) -> str | None:
    if p >= config.GRADE_A:
        return "A"
    if p >= config.GRADE_B:
        return "B"
    if p >= config.PUBLISH_THRESHOLD:
        return "C"
    return None


def input_hash(dataset: dict, factors: list[dict]) -> str:
    """sha256 over the normalized input dataset + context factors."""
    blob = json.dumps({"dataset": dataset, "factors": factors},
                      sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode()).hexdigest()


def canonical_forecasts_json(forecasts: list[dict]) -> str:
    """Stable serialization used inside the onchain commitment hash."""
    slim = [
        {
            "market": f["market"], "selection": f["selection"],
            "model_probability": round(f["model_probability"], 4),
            "grade": f["grade"],
        }
        for f in forecasts
    ]
    return json.dumps(slim, sort_keys=True, separators=(",", ":"))


def build_forecasts(dataset: dict, engine: dict, factors: list[dict]) -> list[dict]:
    home = dataset["home"]["name"]
    away = dataset["away"]["name"]
    hf = dataset["home"]["form"]
    af = dataset["away"]["form"]
    adj = engine["goals_adj"]
    contradicted = {(c["market"], c["selection"]) for c in engine["contradictions"]}
    factor_notes = [f["factor"] for f in factors]

    form_driver = (f"{home} last-5: {hf['scored_avg']} scored / "
                   f"{hf['conceded_avg']} conceded per match; {away} last-5: "
                   f"{af['scored_avg']} scored / {af['conceded_avg']} conceded")
    lam_driver = (f"Model expected goals: {engine['lambdas']['adj_home']} "
                  f"({home}) vs {engine['lambdas']['adj_away']} ({away})")

    out = []

    def add(market, selection, p, extra_drivers=(), include_form=False):
        g = grade_for(p)
        if g is None:
            return
        contradiction = (market, selection) in contradicted
        if contradiction:
            g = "C"
        drivers = list(extra_drivers) if extra_drivers else [lam_driver]
        if include_form:
            drivers.insert(0, form_driver)
        drivers += [f"Context: {n}" for n in factor_notes[:1]]
        out.append({
            "market": market, "selection": selection,
            "model_probability": round(p, 4), "grade": g,
            "drivers": drivers[:5],
            "contradiction": contradiction,
        })

    mr = adj["match_result"]
    add("Match result (1X2)", f"{home} win", mr["home"], include_form=True)
    add("Match result (1X2)", "Draw", mr["draw"], include_form=True)
    add("Match result (1X2)", f"{away} win", mr["away"], include_form=True)

    dc = adj["double_chance"]
    add("Double chance", f"{home} or draw", dc["1X"], include_form=True)
    add("Double chance", f"{home} or {away}", dc["12"], include_form=True)
    add("Double chance", f"Draw or {away}", dc["X2"], include_form=True)

    add("Both teams to score", "Yes", adj["btts"]["yes"])
    add("Both teams to score", "No", adj["btts"]["no"])

    for line, probs in adj["total_goals"].items():
        add("Total goals", f"Over {line}", probs["over"])
        add("Total goals", f"Under {line}", probs["under"])

    tt = adj["team_totals"]
    add("Team total goals", f"{home} over 0.5", tt["home_over_0.5"])
    add("Team total goals", f"{home} over 1.5", tt["home_over_1.5"])
    add("Team total goals", f"{away} over 0.5", tt["away_over_0.5"])
    add("Team total goals", f"{away} over 1.5", tt["away_over_1.5"])

    for name, label, lines, unit in (
        ("corners", "Corners", config.CORNER_LINES, "corners"),
        ("cards", "Cards", config.CARD_LINES, "cards"),
        ("shots", "Shots", config.SHOT_LINES, "total shots"),
    ):
        blk = engine["counts"][name]
        if not blk.get("available") or "adj" not in blk:
            continue
        exp_driver = (f"Combined expected {unit}: {blk['expected_adj']} "
                      f"(raw {blk['expected_raw']})")
        for line in lines:
            probs = blk["adj"]["lines"][line]
            add(label, f"Over {line}", probs["over"], [exp_driver])
            add(label, f"Under {line}", probs["under"], [exp_driver])

    gk = engine["counts"]["goal_kicks"]
    if gk.get("available"):
        lo, hi = gk["range"]
        label = f"{lo}–{hi} total goal kicks"
        drivers = [f"Combined expected goal kicks: {gk['expected']}"]
        if gk["estimated"]:
            drivers.append("Estimated from correlated statistics "
                           "(opponent shots off target + goalkeeper saves)")
        add("Goal kicks (total range)", label, gk["coverage"], drivers)

    return out


def build_summary(dataset: dict, engine: dict, forecasts: list[dict],
                  research: dict) -> str:
    home, away = dataset["home"]["name"], dataset["away"]["name"]
    fx = dataset["fixture"]
    lam = engine["lambdas"]
    mr = engine["goals_adj"]["match_result"]
    lead = max((("%s win" % home, mr["home"]), ("a draw", mr["draw"]),
                ("%s win" % away, mr["away"])), key=lambda x: x[1])
    n_a = sum(1 for f in forecasts if f["grade"] == "A")
    sentences = [
        f"Statistical research report for {home} vs {away} "
        f"({fx.get('competition')}, {fx.get('stage')}).",
        f"The Poisson model projects expected goals of {lam['adj_home']} for "
        f"{home} and {lam['adj_away']} for {away}, built from each side's "
        f"last-five attacking and defensive output.",
        f"The most probable outcome is {lead[0]} at {lead[1]*100:.0f}% model "
        f"probability.",
        f"{len(forecasts)} forecasts met the 55% publication threshold, "
        f"including {n_a} at grade A (≥75%).",
    ]
    if engine["contradictions"]:
        sentences.append(
            f"{len(engine['contradictions'])} market(s) carry a contradiction "
            f"flag where context adjustments oppose the raw quantitative signal.")
    if research.get("factors"):
        sentences.append(
            f"{len(research['factors'])} verified context factors from current "
            f"reporting were applied as bounded adjustments.")
    elif research.get("note"):
        sentences.append("No verified context adjustments were applied; "
                         "projections reflect the quantitative model only.")
    return " ".join(sentences)
