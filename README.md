# Olise AI — Football Match Intelligence, Verifiable Onchain

**Olise AI is an agent-queryable match research analyst.** Ask it about any
upcoming fixture and it returns a professional statistical research report:
recent form, head-to-head, team news, verified current context, a full
Poisson scoreline model, and graded probability forecasts across a dozen
statistical markets — delivered as JSON plus a rendered PDF, with the
report's hash committed to the X Layer blockchain **before kickoff**.

Every forecast is publicly graded after full time, building a tamper-proof,
independently verifiable accuracy record. No cherry-picking, no rewriting
history: the hash was onchain before the match started.

## What you get per query

- **Executive summary** an agent can quote directly (4–6 sentences)
- **Quantitative model**: expected goals, full score-probability matrix,
  most likely scorelines
- **Statistical forecasts** across match result, double chance, both teams
  to score, total goals (multiple lines), team totals, corners, cards,
  shots, and total goal kicks — each with a model probability and a
  confidence grade (**A ≥ 75%, B 65–74%, C 55–64%**; below 55% is never
  published)
- **Current-context research** (search-grounded): managerial changes,
  confirmed team news, knockout-stage patterns — applied as bounded,
  traceable adjustments (net cap ±20% per market)
- **Contradiction flags**: when verified context opposes the raw model, the
  conflict is shown with both numbers — never silently averaged
- **PDF research report** at a public URL
- **Onchain commitment**: keccak-256(PDF bytes + canonical forecasts JSON)
  recorded on X Layer testnet before kickoff, settled onchain after full time

## API

Base URL: your deployment (see `DEPLOY_WINDOWS.md` / `Dockerfile`).

### `POST /analyze`

```json
{ "home": "Spain", "away": "Belgium", "date": "2026-07-14" }
```

Returns:

```json
{
  "report_id": "OLISE-1435553-a1b2c3d4",
  "status": "provisional",
  "pdf_url": "https://…/olise-reports/OLISE-…/v1.pdf",
  "summary": "Statistical research report for Spain vs Belgium…",
  "forecasts": [
    {
      "market": "Total goals",
      "selection": "Under 2.5",
      "model_probability": 0.61,
      "grade": "C",
      "drivers": ["Model expected goals: 1.31 (Spain) vs 0.89 (Belgium)"]
    }
  ],
  "commitment": {
    "hash": "0x…",
    "tx_hash": "0x…",
    "explorer_url": "https://www.oklink.com/xlayer-test/tx/0x…"
  }
}
```

Reports are a pure function of their input data: repeating a query returns
the identical cached report with no duplicate onchain commitment. Reports
issued before lineups are published are marked `provisional` and
automatically reissued as `final` (same `report_id`, new version) when
lineups land — both versions stay committed onchain.

### Other endpoints

| Endpoint | Purpose |
|---|---|
| `GET /report/{report_id}` | Full stored report data, forecasts, versions, settlement |
| `GET /verify/{report_id}` | Commitment hash, tx, and recompute instructions — verify the report was never altered |
| `GET /track-record` | Public accuracy record: overall, per market, per confidence grade |
| `POST /settle/{report_id}` | Post-match grading pass (admin token required; also runs automatically) |
| `GET /health` | Connectivity checks + background job status |

### Verifying a report independently

`GET /verify/{report_id}` returns everything needed:

1. Download the PDF (`pdf_url`); its SHA-256 must match `pdf_sha256`.
2. Append the `canonical_forecasts_json` bytes to the PDF bytes.
3. `keccak256` the result — it must equal `commitment_hash`, recorded in
   `tx_hash` on X Layer testnet before kickoff.

## Self-operating

An in-process scheduler runs the service autonomously:

- **Lineup watcher** (10 min): upgrades provisional reports to final when
  official lineups are published
- **Auto-settlement** (30 min): grades every forecast of finished fixtures
  against final match statistics and records the outcome onchain
- **Self-ping** (10 min): keep-warm health check

## Architecture

FastAPI · API-Football data layer with quota-aware caching · Gemini
search-grounded research pass · Poisson quantitative core with bounded
context adjustments · Jinja2 + WeasyPrint PDF rendering · Supabase (Postgres
+ Storage) · web3.py on X Layer testnet (`OliseCommit` contract) ·
APScheduler background jobs. Single deployable service; runs identically on
Windows and Linux.

## Setup

1. `pip install -r requirements.txt` (Windows: see `DEPLOY_WINDOWS.md` for
   the GTK3 runtime WeasyPrint needs)
2. Create `.env` — see `DEPLOY_WINDOWS.md` §4 for the variable list
3. Optional: run `schema.sql` in the Supabase SQL editor (otherwise a local
   SQLite fallback is used automatically)
4. `python -m olise.main` — the first start deploys the commitment contract
   and persists its address in `.olise_chain.json`

---

*Statistical research for informational purposes. Not financial advice.*
