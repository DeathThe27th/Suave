"""API-Football (api-sports.io) client + dataset normalizers.

Every raw response is cached in the store (api_cache) keyed by
endpoint+params, both to conserve the daily quota and to keep report
content a pure function of its input dataset.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from datetime import datetime, timezone

import httpx

from olise import config

log = logging.getLogger("olise.data")

FINISHED = {"FT", "AET", "PEN"}


class ApiFootballError(Exception):
    pass


class FixtureNotFound(ApiFootballError):
    pass


def _cache_key(endpoint: str, params: dict) -> str:
    blob = endpoint + "?" + json.dumps(params, sort_keys=True)
    return "af:" + hashlib.sha256(blob.encode()).hexdigest()


class ApiFootball:
    def __init__(self, store):
        self.store = store
        self.http = httpx.AsyncClient(
            base_url=config.AF_BASE,
            headers={"x-apisports-key": config.API_FOOTBALL_KEY},
            timeout=25,
        )
        self.requests_remaining: str | None = None
        self.last_ok: str | None = None

    async def close(self):
        await self.http.aclose()

    async def get(self, endpoint: str, params: dict | None = None,
                  ttl: float = config.TTL_FIXTURE) -> list:
        params = params or {}
        key = _cache_key(endpoint, params)
        cached = self.store.cache_get(key, ttl)
        if cached is not None:
            return cached.get("response", [])

        for attempt in range(5):
            r = await self.http.get(endpoint, params=params)
            if r.status_code == 429:
                # free plan: ~10 requests/minute — wait out the window
                wait = 15 * (attempt + 1)
                log.info("rate limited on %s, retrying in %ss", endpoint, wait)
                await asyncio.sleep(wait)
                continue
            break
        r.raise_for_status()
        data = r.json()
        errors = data.get("errors")
        if errors and (not isinstance(errors, list) or len(errors) > 0):
            msg = json.dumps(errors)
            # plan-restriction errors are soft: caller decides how to degrade
            raise ApiFootballError(msg)
        self.requests_remaining = r.headers.get("x-ratelimit-requests-remaining")
        self.last_ok = datetime.now(timezone.utc).isoformat()
        self.store.cache_set(key, endpoint, params, data)
        return data.get("response", [])

    async def get_soft(self, endpoint: str, params: dict | None = None,
                       ttl: float = config.TTL_FIXTURE) -> list:
        """Like get() but returns [] on plan/permission errors."""
        try:
            return await self.get(endpoint, params, ttl)
        except ApiFootballError as e:
            log.warning("soft failure on %s %s: %s", endpoint, params, str(e)[:160])
            return []

    # ------------------------------------------------------------------
    # Fixture resolution
    # ------------------------------------------------------------------

    async def team_id(self, name: str) -> tuple[int, str]:
        teams = await self.get("/teams", {"search": name}, ttl=config.TTL_STATIC)
        if not teams:
            raise FixtureNotFound(f"No team found matching '{name}'")
        # prefer national teams / exact-ish match
        exact = [t for t in teams if t["team"]["name"].lower() == name.lower()]
        national = [t for t in (exact or teams) if t["team"].get("national")]
        pick = (national or exact or teams)[0]["team"]
        return pick["id"], pick["name"]

    async def resolve_fixture(self, home: str, away: str,
                              date: str | None = None) -> dict:
        """Resolve team names (+optional YYYY-MM-DD date) to a fixture object.

        Preference order: date match → next scheduled meeting → most recent
        meeting (supports settlement dry-runs and restricted API plans).
        """
        hid, hname = await self.team_id(home)
        aid, aname = await self.team_id(away)
        meetings = await self.get(
            "/fixtures/headtohead", {"h2h": f"{hid}-{aid}"}, ttl=config.TTL_FIXTURE)
        if not meetings:
            raise FixtureNotFound(
                f"No fixture found between '{hname}' and '{aname}'")

        if date:
            for f in meetings:
                if f["fixture"]["date"][:10] == date:
                    return f
            raise FixtureNotFound(
                f"No {hname} vs {aname} fixture on {date}")

        now = datetime.now(timezone.utc)
        def kickoff(f):
            return datetime.fromisoformat(f["fixture"]["date"])
        upcoming = sorted(
            (f for f in meetings if kickoff(f) > now
             and f["fixture"]["status"]["short"] not in FINISHED),
            key=kickoff)
        if upcoming:
            return upcoming[0]
        finished = sorted(
            (f for f in meetings if f["fixture"]["status"]["short"] in FINISHED),
            key=kickoff, reverse=True)
        if finished:
            return finished[0]
        raise FixtureNotFound(f"No usable fixture between '{hname}' and '{aname}'")

    # ------------------------------------------------------------------
    # Per-team form
    # ------------------------------------------------------------------

    @staticmethod
    def _stat_value(stats: list, type_name: str):
        for s in stats:
            if s.get("type", "").lower() == type_name.lower():
                v = s.get("value")
                if isinstance(v, str) and v.endswith("%"):
                    v = v.rstrip("%")
                try:
                    return float(v) if v is not None else None
                except (TypeError, ValueError):
                    return None
        return None

    async def team_form(self, team_id: int, before_iso: str,
                        n: int = config.FORM_MATCHES) -> dict:
        """Last-n finished matches before `before_iso`, with per-fixture stats."""
        cutoff = datetime.fromisoformat(before_iso)

        def usable(fixtures):
            return [
                f for f in fixtures
                if f["fixture"]["status"]["short"] in FINISHED
                and datetime.fromisoformat(f["fixture"]["date"]) < cutoff
            ]

        played = usable(await self.get_soft(
            "/fixtures", {"team": team_id, "last": n + 5},
            ttl=config.TTL_FIXTURE))
        if len(played) < 2:
            # plan-restricted or stale window: fall back to season queries
            # around the fixture date
            year = cutoff.year
            merged = []
            for season in (year, year - 1):
                merged += await self.get_soft(
                    "/fixtures", {"team": team_id, "season": season},
                    ttl=config.TTL_FIXTURE)
                if len(usable(merged)) >= n:
                    break
            played = usable(merged)
        played.sort(key=lambda f: f["fixture"]["date"], reverse=True)
        played = played[:n]

        matches, agg = [], {
            "scored": [], "conceded": [], "corners_for": [], "corners_against": [],
            "cards_for": [], "cards_against": [], "shots_for": [], "shots_against": [],
            "goal_kicks_for": [], "off_target_against": [], "saves_for": [],
            "possession_for": [],
        }
        for f in played:
            fid = f["fixture"]["id"]
            is_home = f["teams"]["home"]["id"] == team_id
            gf = f["goals"]["home" if is_home else "away"] or 0
            ga = f["goals"]["away" if is_home else "home"] or 0
            opp = f["teams"]["away" if is_home else "home"]["name"]

            stats_resp = await self.get_soft(
                "/fixtures/statistics", {"fixture": fid}, ttl=config.TTL_STATIC)
            mine, theirs = [], []
            for block in stats_resp:
                if block["team"]["id"] == team_id:
                    mine = block.get("statistics", [])
                else:
                    theirs = block.get("statistics", [])

            row = {
                "fixture_id": fid,
                "date": f["fixture"]["date"][:10],
                "opponent": opp,
                "home_away": "H" if is_home else "A",
                "score": f"{gf}-{ga}",
                "result": "W" if gf > ga else ("D" if gf == ga else "L"),
                "corners": self._stat_value(mine, "Corner Kicks"),
                "cards": None,
                "shots": self._stat_value(mine, "Total Shots"),
                "possession": self._stat_value(mine, "Ball Possession"),
                "goal_kicks": self._stat_value(mine, "Goal Kicks"),
            }
            yc = self._stat_value(mine, "Yellow Cards") or 0
            rc = self._stat_value(mine, "Red Cards") or 0
            row["cards"] = (yc + rc) if mine else None

            agg["scored"].append(gf)
            agg["conceded"].append(ga)
            for key, val in (
                ("corners_for", row["corners"]),
                ("corners_against", self._stat_value(theirs, "Corner Kicks")),
                ("cards_for", row["cards"]),
                ("cards_against",
                 ((self._stat_value(theirs, "Yellow Cards") or 0)
                  + (self._stat_value(theirs, "Red Cards") or 0)) if theirs else None),
                ("shots_for", row["shots"]),
                ("shots_against", self._stat_value(theirs, "Total Shots")),
                ("goal_kicks_for", row["goal_kicks"]),
                ("off_target_against", self._stat_value(theirs, "Shots off Goal")),
                ("saves_for", self._stat_value(mine, "Goalkeeper Saves")),
                ("possession_for", row["possession"]),
            ):
                if val is not None:
                    agg[key].append(val)
            matches.append(row)

        def avg(xs):
            return round(sum(xs) / len(xs), 3) if xs else None

        return {
            "matches": matches,
            "sample_size": len(matches),
            "scored_avg": avg(agg["scored"]) or 0.0,
            "conceded_avg": avg(agg["conceded"]) or 0.0,
            "corners_avg": avg(agg["corners_for"]),
            "corners_conceded_avg": avg(agg["corners_against"]),
            "cards_avg": avg(agg["cards_for"]),
            "cards_drawn_avg": avg(agg["cards_against"]),
            "shots_avg": avg(agg["shots_for"]),
            "shots_conceded_avg": avg(agg["shots_against"]),
            "goal_kicks_avg": avg(agg["goal_kicks_for"]),
            "off_target_against_avg": avg(agg["off_target_against"]),
            "saves_avg": avg(agg["saves_for"]),
            "possession_avg": avg(agg["possession_for"]),
        }

    # ------------------------------------------------------------------
    # Full dataset for a fixture
    # ------------------------------------------------------------------

    async def fixture_dataset(self, fixture: dict) -> dict:
        fx = fixture["fixture"]
        fid = fx["id"]
        home = fixture["teams"]["home"]
        away = fixture["teams"]["away"]
        kickoff = fx["date"]

        home_form = await self.team_form(home["id"], kickoff)
        away_form = await self.team_form(away["id"], kickoff)

        h2h_raw = await self.get_soft(
            "/fixtures/headtohead",
            {"h2h": f"{home['id']}-{away['id']}"}, ttl=config.TTL_FIXTURE)
        h2h = [
            {
                "date": f["fixture"]["date"][:10],
                "home": f["teams"]["home"]["name"],
                "away": f["teams"]["away"]["name"],
                "score": f"{f['goals']['home']}-{f['goals']['away']}",
                "competition": f["league"]["name"],
            }
            for f in sorted(h2h_raw, key=lambda f: f["fixture"]["date"], reverse=True)
            if f["fixture"]["status"]["short"] in FINISHED
            and f["fixture"]["date"] < kickoff
        ][:5]

        injuries_raw = await self.get_soft(
            "/injuries", {"fixture": fid}, ttl=config.TTL_VOLATILE)
        injuries = [
            {
                "team": i["team"]["name"],
                "player": i["player"]["name"],
                "type": i["player"].get("type"),
                "reason": i["player"].get("reason"),
            }
            for i in injuries_raw
        ]

        lineups_raw = await self.get_soft(
            "/fixtures/lineups", {"fixture": fid}, ttl=config.TTL_VOLATILE)
        lineups = {"available": len(lineups_raw) >= 2, "teams": []}
        for lu in lineups_raw:
            lineups["teams"].append({
                "team": lu["team"]["name"],
                "formation": lu.get("formation"),
                "coach": (lu.get("coach") or {}).get("name"),
                "starters": [
                    p["player"]["name"] for p in (lu.get("startXI") or [])
                ],
            })

        gk_available = (home_form["goal_kicks_avg"] is not None
                        and away_form["goal_kicks_avg"] is not None)

        return {
            "fixture": {
                "id": fid,
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
            "injuries": injuries,
            "lineups": lineups,
            "goal_kicks_available": gk_available,
        }

    # ------------------------------------------------------------------

    async def fixture_result_stats(self, fixture_id: int) -> dict | None:
        """Final score + full-time statistics for settlement."""
        rows = await self.get("/fixtures", {"id": fixture_id}, ttl=config.TTL_VOLATILE)
        if not rows:
            return None
        f = rows[0]
        if f["fixture"]["status"]["short"] not in FINISHED:
            return None
        stats_resp = await self.get_soft(
            "/fixtures/statistics", {"fixture": fixture_id}, ttl=config.TTL_STATIC)
        per_team = {}
        for block in stats_resp:
            side = "home" if block["team"]["id"] == f["teams"]["home"]["id"] else "away"
            st = block.get("statistics", [])
            per_team[side] = {
                "corners": self._stat_value(st, "Corner Kicks"),
                "cards": ((self._stat_value(st, "Yellow Cards") or 0)
                          + (self._stat_value(st, "Red Cards") or 0)) if st else None,
                "shots": self._stat_value(st, "Total Shots"),
                "goal_kicks": self._stat_value(st, "Goal Kicks"),
            }
        return {
            "fixture_id": fixture_id,
            "status": f["fixture"]["status"]["short"],
            "goals_home": f["goals"]["home"],
            "goals_away": f["goals"]["away"],
            "score_90": f.get("score", {}).get("fulltime", {}),
            "stats": per_team,
        }

    async def status(self) -> dict:
        r = await self.http.get("/status")
        r.raise_for_status()
        return r.json().get("response", {})
