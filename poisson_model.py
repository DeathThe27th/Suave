"""
Olise AI — Poisson quantitative core.

Two-step methodology:
  Step 1: derive expected goals (lambda) per team from attack/defense
          strength relative to opponents faced, over recent matches.
  Step 2: build the full score probability matrix from independent
          Poisson distributions and derive market probabilities.

Also provides a generic Poisson projector for count markets
(corners, cards, shots, goal kicks) given an expected total.

Pure Python — no external dependencies.
"""

from math import exp, factorial

MAX_GOALS = 10  # matrix dimension; P(>10 goals per team) is negligible


# ---------------------------------------------------------------------------
# Core distribution
# ---------------------------------------------------------------------------

def poisson_pmf(k: int, lam: float) -> float:
    """P(X = k) for X ~ Poisson(lam)."""
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (lam ** k) * exp(-lam) / factorial(k)


def poisson_cdf(k: int, lam: float) -> float:
    """P(X <= k)."""
    return sum(poisson_pmf(i, lam) for i in range(k + 1))


def prob_over(line: float, lam: float) -> float:
    """P(X > line) for a half-line (e.g. 2.5, 9.5)."""
    return 1.0 - poisson_cdf(int(line), lam)


# ---------------------------------------------------------------------------
# Step 1 — expected goals
# ---------------------------------------------------------------------------

def expected_goals(
    team_scored_avg: float,
    team_conceded_avg: float,
    opp_scored_avg: float,
    opp_conceded_avg: float,
    baseline: float = 1.30,
) -> float:
    """
    Expected goals for a team against a given opponent.

    attack strength  = team goals scored avg   / baseline
    opp def weakness = opponent conceded avg   / baseline
    lambda           = attack * def_weakness * baseline

    `baseline` is the average goals per team per match in the sample
    (tournament/competition average). 1.30 is a sensible default for
    international tournament football; pass the real sample average
    when available.
    """
    baseline = max(baseline, 0.1)
    attack = team_scored_avg / baseline
    defense_weakness = opp_conceded_avg / baseline
    lam = attack * defense_weakness * baseline
    return max(lam, 0.05)


# ---------------------------------------------------------------------------
# Step 2 — score matrix and derived markets
# ---------------------------------------------------------------------------

def score_matrix(lam_home: float, lam_away: float) -> list[list[float]]:
    """matrix[h][a] = P(home scores h, away scores a)."""
    return [
        [poisson_pmf(h, lam_home) * poisson_pmf(a, lam_away)
         for a in range(MAX_GOALS + 1)]
        for h in range(MAX_GOALS + 1)
    ]


def match_markets(lam_home: float, lam_away: float,
                  goal_lines: tuple[float, ...] = (1.5, 2.5, 3.5)) -> dict:
    """All goal-derived market probabilities from the score matrix."""
    m = score_matrix(lam_home, lam_away)
    rng = range(MAX_GOALS + 1)

    p_home = sum(m[h][a] for h in rng for a in rng if h > a)
    p_draw = sum(m[h][h] for h in rng)
    p_away = sum(m[h][a] for h in rng for a in rng if h < a)

    btts_yes = sum(m[h][a] for h in rng for a in rng if h > 0 and a > 0)

    totals = {}
    for line in goal_lines:
        over = sum(m[h][a] for h in rng for a in rng if h + a > line)
        totals[line] = {"over": over, "under": 1.0 - over}

    top = sorted(
        ((h, a, m[h][a]) for h in rng for a in rng),
        key=lambda x: x[2], reverse=True,
    )[:5]

    return {
        "lambda_home": lam_home,
        "lambda_away": lam_away,
        "match_result": {"home": p_home, "draw": p_draw, "away": p_away},
        "double_chance": {
            "1X": p_home + p_draw,
            "12": p_home + p_away,
            "X2": p_draw + p_away,
        },
        "btts": {"yes": btts_yes, "no": 1.0 - btts_yes},
        "total_goals": totals,
        "team_totals": {
            "home_over_0.5": prob_over(0.5, lam_home),
            "home_over_1.5": prob_over(1.5, lam_home),
            "away_over_0.5": prob_over(0.5, lam_away),
            "away_over_1.5": prob_over(1.5, lam_away),
        },
        "most_likely_scores": [
            {"score": f"{h}-{a}", "probability": p} for h, a, p in top
        ],
        "matrix": m,  # for the report heatmap
    }


# ---------------------------------------------------------------------------
# Generic count markets (corners, cards, shots, goal kicks)
# ---------------------------------------------------------------------------

def count_market(expected_total: float,
                 lines: tuple[float, ...]) -> dict:
    """
    Poisson projection for a combined count stat.
    expected_total: e.g. home corners avg (adj) + away corners avg (adj).
    """
    out = {"expected": expected_total, "lines": {}}
    for line in lines:
        over = prob_over(line, expected_total)
        out["lines"][line] = {"over": over, "under": 1.0 - over}
    return out


def likely_range(expected_total: float, coverage: float = 0.80) -> tuple[int, int]:
    """
    Smallest symmetric-ish integer range around the mode covering
    >= `coverage` probability. Used for goal-kick range projections.
    """
    mode = int(expected_total)
    lo = hi = mode
    total = poisson_pmf(mode, expected_total)
    while total < coverage and (lo > 0 or hi < 60):
        p_lo = poisson_pmf(lo - 1, expected_total) if lo > 0 else -1.0
        p_hi = poisson_pmf(hi + 1, expected_total)
        if p_hi >= p_lo:
            hi += 1
            total += p_hi
        else:
            lo -= 1
            total += p_lo
    return lo, hi


# ---------------------------------------------------------------------------
# Convenience entry point
# ---------------------------------------------------------------------------

def analyze_fixture(home_stats: dict, away_stats: dict,
                    baseline: float = 1.30) -> dict:
    """
    home_stats/away_stats: {"scored_avg": float, "conceded_avg": float}
    computed from each team's recent matches (last 5 recommended).
    """
    lam_h = expected_goals(
        home_stats["scored_avg"], home_stats["conceded_avg"],
        away_stats["scored_avg"], away_stats["conceded_avg"], baseline,
    )
    lam_a = expected_goals(
        away_stats["scored_avg"], away_stats["conceded_avg"],
        home_stats["scored_avg"], home_stats["conceded_avg"], baseline,
    )
    return match_markets(lam_h, lam_a)


if __name__ == "__main__":
    # smoke test
    demo = analyze_fixture(
        {"scored_avg": 2.2, "conceded_avg": 0.6},
        {"scored_avg": 1.4, "conceded_avg": 1.0},
    )
    print("λ:", round(demo["lambda_home"], 2), round(demo["lambda_away"], 2))
    print("1X2:", {k: round(v, 3) for k, v in demo["match_result"].items()})
    print("O2.5:", round(demo["total_goals"][2.5]["over"], 3))
    print("BTTS:", round(demo["btts"]["yes"], 3))
    print("GK range for E=15.5:", likely_range(15.5))
