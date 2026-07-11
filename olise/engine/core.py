"""Quantitative engine.

Wraps the provided poisson_model.py (used as-is), adds:
  - secondary count markets (corners, cards, shots, goal kicks)
  - bounded multiplicative context adjustments from research factors
  - contradiction detection between raw and adjusted probabilities
"""

from __future__ import annotations

import logging

import poisson_model as pm
from olise import config

log = logging.getLogger("olise.engine")

# direction → (target key, sign). Targets: lam_home, lam_away, corners,
# cards, shots. "goals" targets both lambdas.
DIRECTION_MAP = {
    "suppresses_goals": [("lam_home", -1), ("lam_away", -1)],
    "boosts_goals": [("lam_home", +1), ("lam_away", +1)],
    "boosts_home_attack": [("lam_home", +1)],
    "suppresses_home_attack": [("lam_home", -1)],
    "boosts_away_attack": [("lam_away", +1)],
    "suppresses_away_attack": [("lam_away", -1)],
    "boosts_cards": [("cards", +1)],
    "suppresses_cards": [("cards", -1)],
    "boosts_corners": [("corners", +1)],
    "suppresses_corners": [("corners", -1)],
    "boosts_shots": [("shots", +1)],
    "suppresses_shots": [("shots", -1)],
}


def _blend(team_avg, opp_concede_avg):
    """Expected count for one team: own production blended with what the
    opponent typically concedes. Falls back to whichever side has data."""
    vals = [v for v in (team_avg, opp_concede_avg) if v is not None]
    return sum(vals) / len(vals) if vals else None


def _multipliers(factors: list[dict]) -> tuple[dict, list[dict]]:
    """Net bounded multiplier per target + traceable adjustment log."""
    mult = {"lam_home": 1.0, "lam_away": 1.0,
            "corners": 1.0, "cards": 1.0, "shots": 1.0}
    trace = []
    for f in factors:
        pct = config.MAGNITUDE_PCT[f["magnitude"]]
        for target, sign in DIRECTION_MAP.get(f["direction"], []):
            mult[target] *= (1 + sign * pct)
            trace.append({
                "target": target,
                "factor": f["factor"],
                "delta": round(sign * pct, 4),
                "source_note": f.get("source_note", ""),
            })
    lo, hi = 1 - config.MAX_ADJUSTMENT, 1 + config.MAX_ADJUSTMENT
    for k in mult:
        capped = min(max(mult[k], lo), hi)
        if capped != mult[k]:
            trace.append({"target": k, "factor": "cap ±20% applied",
                          "delta": round(capped - mult[k], 4), "source_note": ""})
            mult[k] = capped
    return mult, trace


def _count_block(expected_raw, mult, lines):
    if expected_raw is None:
        return {"available": False}
    expected_adj = expected_raw * mult
    return {
        "available": True,
        "expected_raw": round(expected_raw, 2),
        "expected_adj": round(expected_adj, 2),
        "raw": pm.count_market(expected_raw, lines),
        "adj": pm.count_market(expected_adj, lines),
    }


def run_engine(dataset: dict, factors: list[dict]) -> dict:
    hf = dataset["home"]["form"]
    af = dataset["away"]["form"]

    # baseline: real average goals per team per match in the sample
    baseline = (hf["scored_avg"] + hf["conceded_avg"]
                + af["scored_avg"] + af["conceded_avg"]) / 4
    baseline = max(baseline, 0.5)

    lam_h = pm.expected_goals(hf["scored_avg"], hf["conceded_avg"],
                              af["scored_avg"], af["conceded_avg"], baseline)
    lam_a = pm.expected_goals(af["scored_avg"], af["conceded_avg"],
                              hf["scored_avg"], hf["conceded_avg"], baseline)

    mult, trace = _multipliers(factors)
    lam_h_adj = lam_h * mult["lam_home"]
    lam_a_adj = lam_a * mult["lam_away"]

    goals_raw = pm.match_markets(lam_h, lam_a, config.GOAL_LINES)
    goals_adj = pm.match_markets(lam_h_adj, lam_a_adj, config.GOAL_LINES)

    # --- count markets ------------------------------------------------
    def combined(key_for, key_against):
        h = _blend(hf.get(key_for), af.get(key_against))
        a = _blend(af.get(key_for), hf.get(key_against))
        if h is None or a is None:
            return None
        return h + a

    corners_exp = combined("corners_avg", "corners_conceded_avg")
    cards_exp = combined("cards_avg", "cards_drawn_avg")
    shots_exp = combined("shots_avg", "shots_conceded_avg")

    counts = {
        "corners": _count_block(corners_exp, mult["corners"], config.CORNER_LINES),
        "cards": _count_block(cards_exp, mult["cards"], config.CARD_LINES),
        "shots": _count_block(shots_exp, mult["shots"], config.SHOT_LINES),
    }

    # --- goal kicks ----------------------------------------------------
    gk = {"available": False, "estimated": False}
    if dataset.get("goal_kicks_available"):
        exp_total = hf["goal_kicks_avg"] + af["goal_kicks_avg"]
        gk = {"available": True, "estimated": False}
    else:
        # Estimate from correlated statistics: goal kicks are driven mainly
        # by opponent shots off target plus a share of goalkeeper saves.
        parts = []
        for form in (hf, af):
            ot = form.get("off_target_against_avg")
            sv = form.get("saves_avg")
            if ot is None and sv is None:
                parts = []
                break
            parts.append(max((ot or 0.0) + 0.5 * (sv or 0.0), 4.0))
        exp_total = sum(parts) if parts else None
        if exp_total is not None:
            gk = {"available": True, "estimated": True}
    if gk["available"]:
        lo, hi = pm.likely_range(exp_total)
        coverage = sum(pm.poisson_pmf(k, exp_total) for k in range(lo, hi + 1))
        gk.update({
            "expected": round(exp_total, 2),
            "range": [lo, hi],
            "coverage": round(coverage, 4),
        })
    counts["goal_kicks"] = gk

    # --- contradiction detection ---------------------------------------
    contradictions = []

    def check(market, selection, p_raw, p_adj):
        if p_raw >= config.PUBLISH_THRESHOLD and p_adj < 0.5:
            contradictions.append({
                "market": market, "selection": selection,
                "raw_probability": round(p_raw, 4),
                "adjusted_probability": round(p_adj, 4),
                "reason": "context adjustments moved this market across 50% "
                          "against the raw Poisson signal",
            })

    for line in config.GOAL_LINES:
        check("Total goals", f"Over {line}",
              goals_raw["total_goals"][line]["over"],
              goals_adj["total_goals"][line]["over"])
        check("Total goals", f"Under {line}",
              goals_raw["total_goals"][line]["under"],
              goals_adj["total_goals"][line]["under"])
    check("Both teams to score", "Yes", goals_raw["btts"]["yes"], goals_adj["btts"]["yes"])
    check("Both teams to score", "No", goals_raw["btts"]["no"], goals_adj["btts"]["no"])
    for name, lines in (("corners", config.CORNER_LINES),
                        ("cards", config.CARD_LINES),
                        ("shots", config.SHOT_LINES)):
        blk = counts[name]
        if not blk.get("available") or "raw" not in blk:
            continue
        for line in lines:
            check(name.capitalize(), f"Over {line}",
                  blk["raw"]["lines"][line]["over"], blk["adj"]["lines"][line]["over"])
            check(name.capitalize(), f"Under {line}",
                  blk["raw"]["lines"][line]["under"], blk["adj"]["lines"][line]["under"])

    return {
        "baseline": round(baseline, 3),
        "lambdas": {
            "raw_home": round(lam_h, 3), "raw_away": round(lam_a, 3),
            "adj_home": round(lam_h_adj, 3), "adj_away": round(lam_a_adj, 3),
        },
        "multipliers": {k: round(v, 4) for k, v in mult.items()},
        "goals_raw": goals_raw,
        "goals_adj": goals_adj,
        "counts": counts,
        "adjustments": trace,
        "contradictions": contradictions,
    }
