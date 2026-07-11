# OLISE AI — One-Shot Build Spec

You (Claude Code) are building **Olise AI**, a sports match intelligence Agent Service Provider (ASP) for the OKX AI Genesis Hackathon. Read this entire file before writing any code. Build the complete system in this single session.

---

## PHASE 0 — INTERVIEW FIRST, THEN BUILD UNINTERRUPTED

Before writing ANY code, ask the user for ALL of the following in ONE message. Do not start building until you have everything. After this interview, do NOT stop to ask questions again — make reasonable decisions yourself and document them in `DECISIONS.md`.

Ask for:

1. `API_FOOTBALL_KEY` — API-Football (api-sports.io) key
2. `GEMINI_API_KEY` — Google AI Studio key
3. `SUPABASE_URL` — Supabase project URL
4. `SUPABASE_SERVICE_ROLE_KEY` — Supabase service role key (not anon key)
5. `XLAYER_PRIVATE_KEY` — private key of a FRESH burner wallet funded with X Layer testnet OKB (never a wallet holding real funds)
6. Confirm the Supabase storage bucket name to use (default: `olise-reports`, public).

**Note:** `poisson_model.py` is provided alongside this spec in the repo root. It IS the quantitative core — use it as-is via `analyze_fixture()`, `count_market()`, and `likely_range()`. Do not rewrite it; extend around it if needed.

Write all secrets to `.env`, add `.env` to `.gitignore` immediately, and load via `python-dotenv`. Never print secrets to the terminal or commit them.

Verify before building:
- Ping API-Football (`/status`) to confirm the key works and check remaining quota.
- Connect to X Layer TESTNET via RPC and confirm `eth_chainId` returns the testnet chain ID (expected: 195 / 0xC3). Try `https://testrpc.xlayer.tech` first; if unreachable, try `https://xlayertestrpc.okx.com`. If neither works, look up the current official X Layer testnet RPC in OKX docs. Confirm the wallet has a nonzero OKB balance. If balance is zero, tell the user to hit the faucet and WAIT for their confirmation — this is the only permitted mid-build stop.
- Confirm the Supabase bucket exists; create it via the API if it doesn't (public read).

---

## WHAT OLISE AI IS

An agent-queryable football match research analyst. Any agent or user asks about an upcoming fixture (e.g. "Spain vs Belgium"). Olise:

1. Pulls all relevant data (form, H2H, injuries, lineups, referee, per-match stats)
2. Runs a web research pass for current context (coach changes, formation shifts, knockout-stage mentality, press conference news)
3. Runs the Poisson engine for the quantitative base
4. Applies context adjustments on top of the raw numbers
5. Generates statistical forecasts across many markets, each graded by confidence
6. Renders a professional PDF research report, uploads it, returns the public link
7. Commits the report hash onchain (X Layer testnet) BEFORE kickoff — a tamper-proof prediction record
8. After the match, a settlement pass grades every forecast, building a publicly auditable accuracy track record

**Positioning: this is a sports analytics / match intelligence product.** It produces statistical forecasts and research. It is NOT a betting product.

---

## CRITICAL FRAMING RULES (violating these gets the ASP rejected)

Apply to ALL user-facing surfaces: API responses, PDF reports, README, service descriptions, code comments that might surface in docs.

NEVER use: bet, bets, betting, bet builder, picks (as a betting term), bookie, bookmaker, odds, stake, staking (gambling sense), bankroll, punt, wager, accumulator, parlay, tips/tipster, or any bookmaker brand name.

ALWAYS use instead: forecast(s), prediction(s), statistical projection, probability, market (statistical sense), match intelligence, research report, model confidence, verified accuracy record.

Example: NOT "Pick: Over 9.5 corners ✅" → YES "Forecast: Over 9.5 corners — 71% model probability — Confidence: A"

---

## ARCHITECTURE

```
Client/Agent → FastAPI
                ├── data/        API-Football client + normalizers
                ├── research/    Gemini (with Google Search grounding) context pass
                ├── engine/      Poisson core (user's poisson_model.py) + context adjuster
                ├── forecasts/   market projections + confidence grading
                ├── report/      HTML template → PDF (WeasyPrint) → Supabase storage
                ├── chain/       X Layer testnet commitment + verification
                ├── settle/      post-match grading + track record
                └── store/       Supabase Postgres: reports, forecasts, cache, results
```

Python 3.11+, FastAPI, httpx, web3.py, weasyprint, jinja2, supabase-py, python-dotenv. Keep it a single deployable service.

---

## DATA LAYER (API-Football)

For a requested fixture (team names + optional date → resolve to fixture ID; World Cup 2026 is league id 1, season 2026):

- Last 5 matches per team: results, goals for/against, and per-fixture statistics (corners, cards, shots, possession — whatever `/fixtures/statistics` returns)
- H2H (last 5 meetings)
- Injuries/suspensions (`/injuries`)
- Lineups if published (`/fixtures/lineups`) — if absent, mark report PROVISIONAL
- Referee: name from fixture data; card counts from their recent fixtures if retrievable, otherwise omit the referee stats section gracefully
- **Goal kicks:** check whether `/fixtures/statistics` includes a goal kicks stat type. If yes, average each team's goal kicks over their last 3–5 matches and project a combined range (e.g. "14–18 total goal kicks"). If the stat is NOT available, estimate from correlated stats (opponent shots off target + goalkeeper saves are the main drivers of goal kicks) and clearly label the projection "estimated from correlated statistics." Never invent numbers.

Cache every raw API response (Supabase table `api_cache`, keyed by endpoint+params, with fetched_at) to conserve quota and enforce consistency.

---

## RESEARCH LAYER (Gemini + Search grounding)

One structured research pass per fixture using Gemini (use the current flash model, e.g. `gemini-2.5-flash` or newer, with the Google Search grounding tool). Prompt it to find ONLY verifiable current context:

- Managerial changes, tactical/formation shifts in recent matches
- Confirmed injury/suspension news beyond the API data
- Stage context: is this a knockout/semi/final? Any documented pattern of either team playing more conservatively or aggressively in knockouts?
- Relevant press conference signals (rotation hints, key player fitness)

Require STRICT JSON output: a list of context factors, each with `factor`, `direction` (e.g. suppresses_goals / boosts_cards / boosts_home_attack), `magnitude` (low/med/high), `source_note`. Discard anything speculative. This JSON feeds the adjuster and the report's "Current Context" section.

---

## ENGINE

1. **Poisson core:** use the provided `poisson_model.py`. `analyze_fixture(home_stats, away_stats, baseline)` takes each team's scored/conceded averages from their last 5 matches (pass the sample's real average goals-per-team as `baseline`) and returns 1X2, double chance, BTTS, total goals O/U, team totals, most likely scores, and the full score matrix for the report heatmap.
2. **Secondary markets:** corners, cards, shots — compute each team's adjusted expected value from last-5 averages (team avg blended with opponent's concession avg), sum to a combined expectation, then use `count_market(expected_total, lines)` for O/U probabilities. Goal kicks: same expectation approach per the data-layer rule, projected as a range via `likely_range(expected_total)`.
3. **Context adjuster:** apply the research layer's factors as bounded multiplicative adjustments to expected values (cap total adjustment at ±20% per market; document the mapping from magnitude → % in DECISIONS.md). Every adjustment must be traceable: store `(market, factor, delta)` so the report can show WHY numbers moved.
4. **Contradiction detection:** if context factors push a market's probability across a threshold the raw Poisson had it on the other side of (e.g. raw says Over 2.5 at 61%, adjusted says 48%), do NOT silently average — flag it as a CONTRADICTION in the report with both numbers and the reasoning, and either exclude the forecast or downgrade it to C.

---

## FORECASTS & GRADING

Generate every forecast whose model probability ≥ 55%:

- Match result (1X2), double chance
- BTTS
- Total goals O/U (multiple lines), team totals
- Corners O/U, cards O/U, shots O/U (where data supports)
- Goal kicks total range

Grades: **A ≥ 75%**, **B 65–74%**, **C 55–64%**. Below 55% → not published. Each forecast: `{market, selection, model_probability, grade, drivers[]}` where drivers reference the data/context behind it.

**Consistency rule:** report content is a pure function of the input dataset. Cache key = `fixture_id + sha256(normalized_input_data)`. Same query → same cached report. Regenerate ONLY when input data changes (lineups drop, new injury). PROVISIONAL reports (no lineups) upgrade to FINAL when lineups land.

---

## REPORT (PDF)

Jinja2 HTML template → WeasyPrint → PDF → upload to Supabase storage bucket (public URL). Design it clean and professional: cover block (fixture, competition, stage, kickoff UTC, PROVISIONAL/FINAL badge, report ID, onchain commitment hash), then sections:

1. Executive summary (3–5 sentences)
2. Recent form (both teams, last 5, key stats table)
3. Head-to-head
4. Team news: injuries/suspensions/lineups
5. Referee profile (if data available)
6. Current context (research findings, cited as "reported by press" style notes)
7. Quantitative model: the Poisson score matrix rendered as a heatmap-style table, expected goals, and a plain-language interpretation of how forecasts derive from it
8. Forecasts table: market / selection / probability / grade / key drivers
9. Contradiction flags (if any)
10. Methodology + disclaimer footer: "Statistical research for informational purposes. Not financial advice."

---

## ONCHAIN COMMITMENT (X Layer testnet)

Minimal Solidity contract:

```solidity
contract OliseCommit {
    event ReportCommitted(bytes32 indexed reportHash, string reportId, uint256 timestamp);
    event ReportSettled(bytes32 indexed reportHash, string resultsUri, uint256 correct, uint256 total);
    function commit(bytes32 reportHash, string calldata reportId) external;
    function settle(bytes32 reportHash, string calldata resultsUri, uint256 correct, uint256 total) external;
}
```

Compile with py-solc-x, deploy once at startup if no address in `.env`/config (persist the deployed address). Commitment hash = keccak256(PDF bytes + canonical forecasts JSON). Commit BEFORE kickoff, store tx hash + explorer link (OKLink X Layer testnet) with the report. `GET /verify/{report_id}` returns hash, tx, and recompute instructions so anyone can verify the report wasn't altered.

If deployment fails after 3 attempts, fall back to embedding the hash in a self-transaction's calldata and note it in DECISIONS.md — do not block the build on this.

---

## BACKGROUND SCHEDULER (the agent must run itself)

Use APScheduler (AsyncIOScheduler) inside the FastAPI app — no external cron required:

1. **Lineup watcher** — every 10 min, for any PROVISIONAL report with kickoff within 2 hours: re-pull lineups; if published, regenerate the report as FINAL, upload new PDF, commit the new hash onchain (the report keeps its report_id but records both versions).
2. **Auto-settlement** — every 30 min, for any committed report whose fixture finished ≥ 2 hours ago and isn't settled: pull final statistics, grade all forecasts, store results, call `settle()` onchain. Retry with backoff if stats aren't available yet.
3. **Self-ping** — every 10 min, GET its own /health (harmless on a VPS; keeps the service warm if deployed on a sleeping free tier).

Jobs must be idempotent (safe to run twice) and must never crash the API — wrap in try/except with logging. `GET /health` should report scheduler status and last-run times of each job.

---

## SETTLEMENT & TRACK RECORD

- `POST /settle/{report_id}`: after full-time, pull final fixture statistics, grade every forecast correct/incorrect (skip gracefully where the stat is unavailable), store results, call `settle()` onchain.
- `GET /track-record`: aggregate accuracy overall and per market type, per grade. This is the public credibility endpoint.

---

## API SURFACE

- `POST /analyze` — `{home, away, date?}` → `{report_id, status: provisional|final, pdf_url, summary, forecasts[], commitment: {hash, tx_hash, explorer_url}}`
- `GET /report/{report_id}` — full stored report data
- `GET /verify/{report_id}` — onchain verification info
- `POST /settle/{report_id}` — settlement (protect with a simple `ADMIN_TOKEN` env secret)
- `GET /track-record` — accuracy stats
- `GET /health` — checks API-Football, Supabase, RPC connectivity

Return clear, agent-friendly JSON errors (fixture not found, match already started, upstream API down). The `summary` field should be 4–6 sentences an agent can quote directly.

---

## DEPLOYMENT & DOCS

Primary deploy target: **an always-on 8GB Windows VPS, running natively (no Docker)**. Ship:

- `requirements.txt` + a `DEPLOY_WINDOWS.md` with exact steps: install Python 3.11+, install the GTK3 runtime for WeasyPrint (link the standard gtk3-runtime installer for Windows), `pip install -r requirements.txt`, create `.env`, run via `uvicorn`, then register as an auto-restarting Windows service (NSSM preferred; Task Scheduler `onstart` as alternative). Include a smoke-test command.
- Also ship a `Dockerfile` (WeasyPrint system deps: pango, cairo, gdk-pixbuf) + `docker-compose.yml` (`restart: unless-stopped`) and `render.yaml` as fallback deploy options for Linux/Render.
- The app must bind host/port from env (`HOST`, `PORT`) and run identically on Windows and Linux — use `pathlib` everywhere, no POSIX-only calls.
- `README.md` written as the ASP listing description — lead with the match intelligence framing, features, verifiable onchain accuracy record, API usage examples. Zero prohibited vocabulary.
- `DECISIONS.md` — every judgment call you made during the build

---

## END-TO-END TEST (required before you declare done)

1. `GET /health` all green
2. `POST /analyze` on a REAL upcoming 2026 World Cup knockout fixture (query API-Football for the next scheduled fixtures) — verify: PDF renders correctly and opens, public URL works, forecasts populated across multiple markets, commitment tx confirmed on testnet explorer
3. Re-run the same `POST /analyze` — verify the cached report returns (identical report_id) and no duplicate onchain commit
4. `GET /verify/{report_id}` — hash matches a local recompute
5. Run a settlement dry-run against any RECENT finished fixture to prove the grading logic works

Show the user the PDF URL, the explorer link, and the track-record output as final proof.

## DONE =
Working deployed-ready service + passing end-to-end test + README + DECISIONS.md. Do not gold-plate beyond this spec; ship.
