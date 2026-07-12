"""football-data.org (v4) client + dataset normalizers.

Drop-in alternative to the API-Football client: produces the identical
fixture envelope and dataset shapes, so pipeline/engine/report/settlement
are provider-agnostic. Selected at startup when FOOTBALL_DATA_TOKEN is set.

Free-tier caveats (all handled by graceful degradation downstream):
match statistics (corners/cards/shots/possession), lineups and injuries
are not exposed, so count-market forecasts are unavailable and reports
stay PROVISIONAL; goals markets, form, H2H and referee data are full.
Every raw response is cached in the store (api_cache), both to conserve
the 10 req/min budget and to keep reports a pure function of their input.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone

import httpx

from olise import config
from olise.data.apifootball import (ApiFootballError, FixtureNotFound,
                                    FINISHED, _cache_key)

log = logging.getLogger("olise.data.fd")

# football-data.org status (+ score.duration) → API-Football short code,
# which is what the pipeline's FINISHED set understands.
_DURATION_SHORT = {"REGULAR": "FT", "EXTRA_TIME": "AET",
                   "PENALTY_SHOOTOUT": "PEN"}
_STATUS_SHORT = {"SCHEDULED": "NS", "TIMED": "NS", "IN_PLAY": "LIVE",
                 "PAUSED": "HT", "SUSPENDED": "SUSP", "POSTPONED": "PST",
                 "CANCELLED": "CANC", "AWARDED": "FT"}


def _short_status(m: dict) -> str:
    if m["status"] == "FINISHED":
        return _DURATION_SHORT.get(m["score"].get("duration"), "FT")
    return _STATUS_SHORT.get(m["status"], m["status"])


def _iso(utc_date: str) -> str:
    return utc_date.replace("Z", "+00:00")


def _score_90(m: dict) -> tuple[int | None, int | None]:
    """90-minute score: regularTime when the match went long, else fullTime."""
    sc = m["score"]
    src = sc.get("regularTime") if sc.get("duration") not in (None, "REGULAR") \
        else sc.get("fullTime")
    src = src or sc.get("fullTime") or {}
    return src.get("home"), src.get("away")


def _stage_label(stage: str | None) -> str | None:
    return stage.replace("_", " ").title() if stage else None


def _referee(m: dict) -> str | None:
    for r in m.get("referees") or []:
        if r.get("type") == "REFEREE":
            return r.get("name")
    return None


def _names(team: dict) -> set[str]:
    return {v.casefold() for v in (team.get("name"), team.get("shortName"),
                                   team.get("tla")) if v}


class FootballData:
    def __init__(self, store):
        self.store = store
        self.http = httpx.AsyncClient(
            base_url=config.FD_BASE,
            headers={"X-Auth-Token": config.FOOTBALL_DATA_TOKEN},
            timeout=25,
        )
        self.requests_remaining: str | None = None
        self.last_ok: str | None = None

    async def close(self):
        await self.http.aclose()

    async def get(self, endpoint: str, params: dict | None = None,
                  ttl: float = config.TTL_FIXTURE) -> dict:
        params = params or {}
        key = _cache_key("fd:" + endpoint, params)
        cached = self.store.cache_get(key, ttl)
        if cached is not None:
            return cached

        for attempt in range(5):
            r = await self.http.get(endpoint, params=params)
            if r.status_code == 429:
                # free plan: 10 requests/minute — wait out the window
                wait = 20 * (attempt + 1)
                log.info("rate limited on %s, retrying in %ss", endpoint, wait)
                await asyncio.sleep(wait)
                continue
            break
        if r.status_code >= 400:
            raise ApiFootballError(
                f"football-data.org {r.status_code} on {endpoint}: "
                f"{r.text[:200]}")
        data = r.json()
        self.requests_remaining = r.headers.get("X-Requests-Available-Minute")
        self.last_ok = datetime.now(timezone.utc).isoformat()
        self.store.cache_set(key, endpoint, params, data)
        return data

    async def get_soft(self, endpoint: str, params: dict | None = None,
                       ttl: float = config.TTL_FIXTURE) -> dict:
        try:
            return await self.get(endpoint, params, ttl)
        except (ApiFootballError, httpx.HTTPError) as e:
            log.warning("soft failure on %s %s: %s", endpoint, params,
                        str(e)[:160])
            return {}

    # ------------------------------------------------------------------
    # Fixture resolution
    # ------------------------------------------------------------------

    def _envelope(self, m: dict) -> dict:
        """football-data match → the API-Football-shaped fixture envelope
        the pipeline consumes."""
        return {
            "fixture": {
                "id": m["id"],
                "date": _iso(m["utcDate"]),
                "status": {"short": _short_status(m)},
                "referee": _referee(m),
                "venue": {"name": m.get("venue"), "city": None},
            },
            "teams": {
                "home": {"id": m["homeTeam"]["id"], "name": m["homeTeam"]["name"]},
                "away": {"id": m["awayTeam"]["id"], "name": m["awayTeam"]["name"]},
            },
            "league": {
                "name": (m.get("competition") or {}).get("name"),
                "season": (m.get("season") or {}).get("startDate", "")[:4] or None,
                "round": _stage_label(m.get("stage")),
            },
        }

    async def _competition_matches(self) -> list[dict]:
        data = await self.get(f"/competitions/{config.WORLD_CUP_CODE}/matches")
        return data.get("matches", [])

    async def resolve_fixture(self, home: str, away: str,
                              date: str | None = None) -> dict:
        """Resolve team names (+optional YYYY-MM-DD date) to a fixture.

        Preference order: date match → next scheduled meeting → most recent
        meeting (either home/away orientation), within the configured
        competition.
        """
        h, a = home.casefold(), away.casefold()

        def involves(m):
            pair = (_names(m["homeTeam"]), _names(m["awayTeam"]))
            return ((h in pair[0] and a in pair[1])
                    or (h in pair[1] and a in pair[0]))

        meetings = [m for m in await self._competition_matches()
                    if m["homeTeam"].get("id") and involves(m)]
        if not meetings:
            raise FixtureNotFound(
                f"No fixture found between '{home}' and '{away}' in the "
                f"{config.WORLD_CUP_CODE} schedule")

        if date:
            for m in meetings:
                if m["utcDate"][:10] == date:
                    return self._envelope(m)
            raise FixtureNotFound(f"No {home} vs {away} fixture on {date}")

        now = datetime.now(timezone.utc)

        def kickoff(m):
            return datetime.fromisoformat(_iso(m["utcDate"]))

        upcoming = sorted((m for m in meetings if kickoff(m) > now
                           and m["status"] != "FINISHED"), key=kickoff)
        if upcoming:
            return self._envelope(upcoming[0])
        finished = sorted((m for m in meetings if m["status"] == "FINISHED"),
                          key=kickoff, reverse=True)
        if finished:
            return self._envelope(finished[0])
        raise FixtureNotFound(
            f"No usable fixture between '{home}' and '{away}'")

    # ------------------------------------------------------------------
    # Per-team form
    # ------------------------------------------------------------------

    async def team_form(self, team_id: int, before_iso: str,
                        n: int = config.FORM_MATCHES) -> dict:
        cutoff = datetime.fromisoformat(_iso(before_iso))
        # dateFrom/dateTo must be passed together; a ~14-month window
        # comfortably covers the last n matches of any national side
        window_start = (cutoff - timedelta(days=430)).date().isoformat()
        data = await self.get_soft(
            f"/teams/{team_id}/matches",
            {"status": "FINISHED", "limit": n + 5,
             "dateFrom": window_start, "dateTo": before_iso[:10]},
            ttl=config.TTL_FIXTURE)
        played = [
            m for m in data.get("matches", [])
            if m["status"] == "FINISHED"
            and datetime.fromisoformat(_iso(m["utcDate"])) < cutoff
        ]
        played.sort(key=lambda m: m["utcDate"], reverse=True)
        played = played[:n]

        matches, scored, conceded = [], [], []
        for m in played:
            is_home = m["homeTeam"]["id"] == team_id
            gh, ga = _score_90(m)
            gf = (gh if is_home else ga) or 0
            gc = (ga if is_home else gh) or 0
            opp = m["awayTeam" if is_home else "homeTeam"]["name"]
            matches.append({
                "fixture_id": m["id"],
                "date": m["utcDate"][:10],
                "opponent": opp,
                "home_away": "H" if is_home else "A",
                "score": f"{gf}-{gc}",
                "result": "W" if gf > gc else ("D" if gf == gc else "L"),
                # free tier exposes no per-match statistics
                "corners": None, "cards": None, "shots": None,
                "possession": None, "goal_kicks": None,
            })
            scored.append(gf)
            conceded.append(gc)

        def avg(xs):
            return round(sum(xs) / len(xs), 3) if xs else None

        return {
            "matches": matches,
            "sample_size": len(matches),
            "scored_avg": avg(scored) or 0.0,
            "conceded_avg": avg(conceded) or 0.0,
            "corners_avg": None, "corners_conceded_avg": None,
            "cards_avg": None, "cards_drawn_avg": None,
            "shots_avg": None, "shots_conceded_avg": None,
            "goal_kicks_avg": None, "off_target_against_avg": None,
            "saves_avg": None, "possession_avg": None,
        }

    # ------------------------------------------------------------------
    # Full dataset for a fixture
    # ------------------------------------------------------------------

    async def fixture_dataset(self, fixture: dict) -> dict:
        fx = fixture["fixture"]
        home = fixture["teams"]["home"]
        away = fixture["teams"]["away"]
        kickoff = fx["date"]

        home_form = await self.team_form(home["id"], kickoff)
        away_form = await self.team_form(away["id"], kickoff)
        if not home_form["matches"] or not away_form["matches"]:
            # never let a degenerate 0-goal form sample reach the engine
            # (its output would be hashed and committed onchain)
            raise ApiFootballError(
                "insufficient recent-form data for "
                f"{home['name']} vs {away['name']}")

        h2h_data = await self.get_soft(f"/matches/{fx['id']}/head2head",
                                       {"limit": 10}, ttl=config.TTL_FIXTURE)
        h2h = [
            {
                "date": m["utcDate"][:10],
                "home": m["homeTeam"]["name"],
                "away": m["awayTeam"]["name"],
                "score": "{}-{}".format(*_score_90(m)),
                "competition": (m.get("competition") or {}).get("name"),
            }
            for m in sorted(h2h_data.get("matches", []),
                            key=lambda m: m["utcDate"], reverse=True)
            if m["status"] == "FINISHED" and _iso(m["utcDate"]) < kickoff
        ][:5]

        return {
            "fixture": {
                "id": fx["id"],
                "date_utc": kickoff,
                "status": fx["status"]["short"],
                "referee": fx.get("referee"),
                "venue": (fx.get("venue") or {}).get("name"),
                "city": (fx.get("venue") or {}).get("city"),
                "competition": fixture["league"]["name"],
                "season": fixture["league"].get("season"),
                "stage": fixture["league"].get("round"),
            },
            "home": {"id": home["id"], "name": home["name"], "form": home_form},
            "away": {"id": away["id"], "name": away["name"], "form": away_form},
            "h2h": h2h,
            # not exposed on the football-data.org free tier
            "injuries": [],
            "lineups": {"available": False, "teams": []},
            "goal_kicks_available": False,
        }

    # ------------------------------------------------------------------

    async def fixture_result_stats(self, fixture_id: int) -> dict | None:
        """Final score for settlement. Count-market statistics are not
        exposed on this provider, so those forecasts grade `void`."""
        m = await self.get(f"/matches/{fixture_id}", ttl=config.TTL_VOLATILE)
        if m.get("status") != "FINISHED":
            return None
        gh90, ga90 = _score_90(m)
        ft = m["score"].get("fullTime") or {}
        return {
            "fixture_id": fixture_id,
            "status": _short_status(m),
            "goals_home": ft.get("home"),
            "goals_away": ft.get("away"),
            "score_90": {"home": gh90, "away": ga90},
            "stats": {},
        }

    async def health_check(self) -> dict:
        try:
            await self.get(f"/competitions/{config.WORLD_CUP_CODE}",
                           ttl=config.TTL_HEALTH)
            return {"ok": True, "provider": "football-data.org",
                    "plan": "free tier",
                    "requests_remaining_minute": self.requests_remaining}
        except Exception as e:
            return {"ok": False, "provider": "football-data.org",
                    "error": str(e)[:150]}
