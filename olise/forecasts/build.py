"""Forecast generation, confidence grading and consistency hashing.

Exactly ONE forecast is published per market category (match outcome, BTTS,
total goals, one team total per team, corners, cards, shots, goal kicks):
within a category the highest grade wins, ties broken by probability.
Publication threshold 55%; grades A ≥75%, B 65–74%, C 55–64%. Forecasts hit
by a contradiction flag are downgraded to C (never silently averaged).
"""

from __future__ import annotations

import hashlib
import json

from olise import config

_GRADE_RANK = {"A": 3, "B": 2, "C": 1}


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


def _wdl(form: dict) -> str:
    r = [m["result"] for m in form["matches"]]
    return (f"W{r.count('W')} D{r.count('D')} L{r.count('L')}")


def build_forecasts(dataset: dict, engine: dict, factors: list[dict]) -> list[dict]:
    home = dataset["home"]["name"]
    away = dataset["away"]["name"]
    hf = dataset["home"]["form"]
    af = dataset["away"]["form"]
    adj = engine["goals_adj"]
    contradicted = {(c["market"], c["selection"]) for c in engine["contradictions"]}

    def candidate(market, selection, p, driver, min_p=config.PUBLISH_THRESHOLD):
        if p < min_p:
            return None
        g = grade_for(p)
        if g is None:
            return None
        contradiction = (market, selection) in contradicted
        if contradiction:
            g = "C"
        return {
            "market": market, "selection": selection,
            "model_probability": round(p, 4), "grade": g,
            "drivers": [driver], "contradiction": contradiction,
        }

    def pick(cands):
        cands = [c for c in cands if c]
        if not cands:
            return None
        return max(cands, key=lambda c: (_GRADE_RANK[c["grade"]],
                                         c["model_probability"]))

    combined_goals = round((hf["scored_avg"] + hf["conceded_avg"]
                            + af["scored_avg"] + af["conceded_avg"]) / 2, 1)
    both_scored = sum(
        1 for m in hf["matches"] + af["matches"]
        if all(int(x) > 0 for x in m["score"].split("-")))
    n_matches = len(hf["matches"]) + len(af["matches"])

    out = []

    # --- match outcome: best of 1X2 / double chance -----------------------
    outcome_driver = (f"Form (last 5): {home} {_wdl(hf)}, {away} {_wdl(af)}")
    mr, dc = adj["match_result"], adj["double_chance"]
    out.append(pick([
        candidate("Match result (1X2)", f"{home} win", mr["home"], outcome_driver),
        candidate("Match result (1X2)", "Draw", mr["draw"], outcome_driver),
        candidate("Match result (1X2)", f"{away} win", mr["away"], outcome_driver),
        candidate("Double chance", f"{home} or draw", dc["1X"], outcome_driver),
        candidate("Double chance", f"{home} or {away}", dc["12"], outcome_driver),
        candidate("Double chance", f"Draw or {away}", dc["X2"], outcome_driver),
    ]))

    # --- BTTS --------------------------------------------------------------
    btts_driver = (f"Both sides scored in {both_scored} of {n_matches} "
                   f"combined recent matches")
    out.append(pick([
        candidate("Both teams to score", "Yes", adj["btts"]["yes"], btts_driver),
        candidate("Both teams to score", "No", adj["btts"]["no"], btts_driver),
    ]))

    # --- total goals ---------------------------------------------------------
    tg_driver = (f"Average combined goals {combined_goals:.1f} across both "
                 f"teams' last 5")
    out.append(pick([
        candidate("Total goals", f"{side} {line}", probs[side.lower()], tg_driver)
        for line, probs in adj["total_goals"].items()
        for side in ("Over", "Under")
    ]))

    # --- team totals (one per team, only if ≥65%) --------------------------
    tt = adj["team_totals"]
    for team, form, keys in ((home, hf, ("home_over_0.5", "home_over_1.5")),
                             (away, af, ("away_over_0.5", "away_over_1.5"))):
        driver = f"{team} scored {form['scored_avg']} per match over the last 5"
        out.append(pick([
            candidate("Team total goals",
                      f"{team} over {k.rsplit('_', 1)[1]}", tt[k], driver,
                      min_p=config.GRADE_B)
            for k in keys
        ]))

    # --- counts: corners / cards / shots ------------------------------------
    for name, label, lines, unit in (
        ("corners", "Corners", config.CORNER_LINES, "corners"),
        ("cards", "Cards", config.CARD_LINES, "cards"),
        ("shots", "Shots", config.SHOT_LINES, "total shots"),
    ):
        blk = engine["counts"][name]
        if not blk.get("available") or "adj" not in blk:
            continue
        driver = (f"Combined expected {unit} {blk['expected_adj']} "
                  f"from last-5 averages")
        out.append(pick([
            candidate(label, f"{side} {line}",
                      blk["adj"]["lines"][line][side.lower()], driver)
            for line in lines for side in ("Over", "Under")
        ]))

    # --- goal kicks -----------------------------------------------------------
    gk = engine["counts"]["goal_kicks"]
    if gk.get("available"):
        lo, hi = gk["range"]
        driver = f"Combined expected goal kicks {gk['expected']}"
        if gk["estimated"]:
            driver += " (estimated from correlated statistics)"
        out.append(candidate("Goal kicks (total range)",
                             f"{lo}–{hi} total goal kicks",
                             gk["coverage"], driver))

    return [f for f in out if f]


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
        f"{len(forecasts)} market categories cleared the 55% publication "
        f"threshold, {n_a} of them at grade A (≥75%).",
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
