"""Research layer: one Gemini pass with Google Search grounding per fixture.

Returns a list of verifiable context factors:
    {factor, direction, magnitude, source_note}

Degrades gracefully: if grounding quota is unavailable (429/403) or output
is unparseable, returns no factors with a note — the engine then runs on
raw quantitative data only. We never substitute an ungrounded pass for
current-events research, to avoid unverifiable claims in reports.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re

from olise import config

log = logging.getLogger("olise.research")

VALID_DIRECTIONS = {
    "suppresses_goals", "boosts_goals",
    "boosts_home_attack", "suppresses_home_attack",
    "boosts_away_attack", "suppresses_away_attack",
    "boosts_cards", "suppresses_cards",
    "boosts_corners", "suppresses_corners",
    "boosts_shots", "suppresses_shots",
}

PROMPT = """You are a football match research assistant. Use Google Search to find ONLY verifiable, current, factual context for this upcoming match:

{home} vs {away} — {competition}, {stage}, kickoff {kickoff} UTC.

Look for:
1. Managerial changes or tactical/formation shifts in either team's recent matches
2. CONFIRMED injury or suspension news (named players, confirmed by club/press)
3. Stage context: if this is a knockout/semi-final/final, any documented pattern of either team playing more conservatively or aggressively at this stage
4. Press conference signals: rotation hints, key player fitness doubts

Output STRICT JSON only — no markdown, no commentary — in exactly this shape:
{{"factors": [{{"factor": "<one-sentence factual finding>", "direction": "<one of: suppresses_goals, boosts_goals, boosts_home_attack, suppresses_home_attack, boosts_away_attack, suppresses_away_attack, boosts_cards, suppresses_cards, boosts_corners, suppresses_corners, boosts_shots, suppresses_shots>", "magnitude": "<low|med|high>", "source_note": "<where this was reported, e.g. 'reported by Marca, 2026-07-08'>"}}]}}

Rules:
- Include ONLY facts you found via search with a real source. If you cannot verify something, leave it out.
- No speculation, no odds, no predictions of your own. Maximum 6 factors.
- If you find nothing verifiable, output {{"factors": []}}."""


def _extract_json(text: str) -> dict | None:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if m:
        text = m.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


async def research_fixture(dataset: dict) -> dict:
    """Returns {"factors": [...], "note": str, "grounded": bool}."""
    fx = dataset["fixture"]
    prompt = PROMPT.format(
        home=dataset["home"]["name"], away=dataset["away"]["name"],
        competition=fx.get("competition") or "international football",
        stage=fx.get("stage") or "unknown stage",
        kickoff=fx.get("date_utc"),
    )

    def _run():
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        last_err = None
        for model in config.GEMINI_MODELS:
            try:
                resp = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=0.1,
                    ),
                )
                gm = resp.candidates[0].grounding_metadata if resp.candidates else None
                grounded = bool(gm and getattr(gm, "grounding_chunks", None))
                return resp.text or "", grounded, None
            except Exception as e:  # quota, model retired, transient
                last_err = e
                continue
        return None, False, last_err

    try:
        text, grounded, err = await asyncio.to_thread(_run)
    except Exception as e:
        text, grounded, err = None, False, e

    if text is None:
        # raw provider errors are logged, never rendered into the report
        log.warning("research pass unavailable: %s", str(err)[:200])
        return {"factors": [],
                "note": "No verified context research was available for this "
                        "fixture; projections reflect the quantitative model "
                        "only.",
                "grounded": False}

    parsed = _extract_json(text) or {}
    factors = []
    for f in (parsed.get("factors") or [])[:6]:
        if not isinstance(f, dict):
            continue
        direction = str(f.get("direction", "")).strip()
        magnitude = str(f.get("magnitude", "")).strip().lower()
        if direction not in VALID_DIRECTIONS or magnitude not in config.MAGNITUDE_PCT:
            continue
        if not f.get("factor") or not f.get("source_note"):
            continue  # unverifiable → discard
        factors.append({
            "factor": str(f["factor"])[:300],
            "direction": direction,
            "magnitude": magnitude,
            "source_note": str(f["source_note"])[:200],
        })

    if not grounded:
        # Without search grounding we cannot verify currency of claims.
        note = ("Search grounding was unavailable, so context factors are "
                "omitted; projections reflect the quantitative model only.")
        log.warning(note)
        return {"factors": [], "note": note, "grounded": False}

    return {"factors": factors, "note": "grounded research pass completed",
            "grounded": True}
