# DECISIONS.md — judgment calls made during the build

All decisions made autonomously after the Phase 0 interview, as instructed.

## Infrastructure

1. **Storage bucket name**: the interview reply didn't specify one, so the
   spec default `olise-reports` (public read) was used and created via the
   Storage API.
2. **X Layer testnet chain ID is 1952, not 195.** Both spec'd RPCs
   (`testrpc.xlayer.tech`, `xlayertestrpc.okx.com`) respond and both return
   `0x7a0` (1952) — the testnet migrated since the spec was written. The
   client uses whatever chain ID the live RPC reports. Explorer links use
   `https://www.oklink.com/xlayer-test/tx/{hash}`.
3. **Supabase Postgres tables cannot be created with the service role key**
   (PostgREST exposes no DDL). The store probes the four tables at startup:
   if present it uses Supabase Postgres; if not it transparently falls back
   to a local SQLite database with the identical shape and logs a pointer to
   `schema.sql` (run once in the Supabase SQL editor to switch backends).
   PDF/results artifacts always live in Supabase Storage regardless.
4. **API-Football key is on the Free plan (100 requests/day).** Every raw
   response is cached (`api_cache`) with TTLs: 30 days for finished-fixture
   statistics, 6 h for fixture lookups, 15 min for lineups/injuries. Plan-
   restricted endpoints (e.g. `/injuries`) degrade gracefully to empty
   sections rather than failing the report.

## Research layer

5. **Gemini model**: `gemini-2.5-flash` is retired for new API users; the
   service tries `gemini-3.5-flash` → `gemini-flash-latest` →
   `gemini-2.5-flash` in order.
6. **Search grounding quota is 0 on the provided key** (429 on every
   grounded call; plain generation works). Rather than run an *ungrounded*
   model pass and risk unverifiable claims in a report that gets hashed
   onchain, the research layer returns **no context factors** with an
   explicit note when grounding is unavailable, and reports run on the
   quantitative model alone. Grounding is retried on every analysis, so a
   key upgrade starts working with no code change.
7. Research is skipped entirely for retrospective analyses (fixture already
   played) — current-context search for a finished match is meaningless and
   wastes quota.

## Engine

8. **Baseline goals** passed to the Poisson core = mean of the four
   last-5 averages (home scored/conceded + away scored/conceded), floored
   at 0.5 — the sample's real average goals per team per match.
9. **Magnitude → adjustment mapping**: low = ±3%, med = ±7%, high = ±12%
   per factor, multiplicative on the target (team λ or count-market
   expectation), with the **net** multiplier capped at ±20% per target.
   Every applied factor is stored as `(target, factor, delta, source_note)`.
10. **Count-market expectations**: per team = mean(own production avg,
    opponent's concession avg), summed to a combined total, projected with
    `count_market()`. Lines: corners 8.5/9.5/10.5, cards 3.5/4.5/5.5,
    shots 20.5/23.5/26.5, goals 1.5/2.5/3.5.
11. **Goal kicks**: API-Football's `/fixtures/statistics` does not include a
    goal-kick stat type on this plan, so the projection is estimated from
    correlated statistics per the spec: per team,
    `opponent shots off target + 0.5 × goalkeeper saves`, floored at 4;
    labeled "estimated from correlated statistics" in report and drivers.
    The published range is `likely_range()` at ~80% coverage, so it grades A
    only when coverage ≥ 75%.
12. **Contradiction rule**: raw probability ≥ 55% (publishable) while the
    adjusted probability drops below 50% → flagged with both numbers; the
    forecast is **downgraded to C** (kept, never averaged, not excluded, so
    the flag stays visible and gradeable).

## Reports & commitments

13. **The commitment hash cannot be printed inside the PDF** — the hash
    covers the PDF bytes (chicken-and-egg). The cover explains that the
    keccak-256 of the PDF + canonical forecasts JSON is recorded onchain and
    points to `GET /verify/{report_id}`, which returns hash, tx and
    recompute instructions.
14. **`report_id` is stable per fixture** (`OLISE-{fixtureId}-{hash8}` from
    the first analysis). Data changes (lineups landing, new team news)
    produce a new *version* under the same report_id — each version's PDF,
    input hash and onchain commitment are kept in `versions`.
15. **Retrospective analyses** (fixture already started/finished) are
    rejected with 409 for public callers per spec, but allowed with the
    admin token — needed for the settlement grading demonstration and for
    the Free API plan, which exposes no future fixtures (seasons 2021–2023
    only). Such reports carry `"retrospective": true`; their commitment is
    timestamped after kickoff by construction, and the E2E demo says so
    explicitly.
16. Grading uses the **90-minute score** (`score.fulltime`) per market
    convention, falling back to overall goals if unavailable. Forecasts
    whose stat is missing from the provider are graded `void` and excluded
    from the accuracy denominator.
17. **Auto-settlement trigger**: kickoff + 4 h (≈ match duration + the
    spec's 2 h post-finish buffer), then retried every 30 min until final
    statistics are available.
18. Track record aggregates only `correct`/`incorrect` outcomes; `void` and
    `pending` are excluded from accuracy.

## Data provider switch (2026-07-12)

20. **football-data.org is the preferred provider when `FOOTBALL_DATA_TOKEN`
    is set** (`olise/data/footballdata.py`, same client interface). Reasons:
    the API-Football account was suspended, and its free plan cannot see
    2026 World Cup fixtures at all, while football-data.org's free tier
    serves the current World Cup schedule with no date-window lock.
    Trade-offs accepted: the free tier exposes **no match statistics
    (corners/cards/shots/possession), no lineups and no injuries**, so
    count-market forecasts are unavailable (the engine's `available` flags
    already handle this), reports stay PROVISIONAL, and count markets that
    were forecast under the old provider grade `void` at settlement.
    Goals markets, last-5 form, H2H and referee data are unaffected.
    Statuses are mapped to API-Football short codes (`FT`/`AET`/`PEN`/`NS`)
    so the pipeline's FINISHED semantics are unchanged; the 90-minute score
    uses `regularTime` when a match went to extra time. A form sample of
    zero matches for either team aborts the analysis rather than letting a
    degenerate dataset be hashed and committed onchain.

## E2E test constraint

19. The Free API-Football plan cannot return 2026 World Cup fixtures
    (upcoming seasons are outside the plan window). The end-to-end test
    therefore exercises the full pipeline — data, engine, PDF, storage,
    onchain commit, cache identity, verification, settlement — on a real
    finished World Cup 2022 knockout fixture in admin (retrospective) mode.
    With a paid key, the identical code path serves upcoming fixtures with
    commit-before-kickoff semantics.
