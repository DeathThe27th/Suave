# FINALIZE + REGISTER — ONE SHOT

You (Claude Code) will (A) apply final report fixes, (B) redeploy + generate the flagship report, (C) register Olise AI as an ASP on OKX.AI. Work through phases in order, no questions except where marked ASK.

## PHASE A — REPORT FIXES

### A1. One forecast per market category
Publish exactly ONE forecast per category: match outcome (best of ML/double chance), BTTS, total goals, one team total per team (only if ≥65%), corners, cards, shots, goal kicks range. Selection rule per category: highest grade, then highest probability. Never publish two lines from the same category. Keep the ≥55% threshold; if nothing in a category clears it, omit the category.

### A2. Kill redundancy
- Key drivers must be category-specific and ≤ 1 short line (e.g. corners: "Combined expected corners 8.1 from last-5 averages"). The expected-goals line appears ONCE in the report (section 7), never repeated per row.
- Drop empty/no-data sections entirely (referee with no data, empty H2H) instead of printing "not retrievable" filler. One sentence max for missing injury data.

### A3. Monochrome redesign
Strict black/white/grayscale palette. Clean editorial look: white background, black text, generous whitespace, a strong typographic masthead (OLISE AI · MATCH INTELLIGENCE), thin black rules between sections, tables with hairline gray borders and no fills except the score matrix, which becomes a grayscale heatmap (darker = more probable, white text on dark cells). Grade badges: solid black chip for A, outlined for B, plain text for C. No color anywhere. Verify by regenerating a PDF and checking it renders correctly.

## PHASE B — REDEPLOY + FLAGSHIP REPORT
1. Commit + push all changes; confirm Render redeploys and /health is green.
2. Query API-Football for the next upcoming 2026 World Cup fixtures (semi-finals/final). POST /analyze for the nearest one NOT yet kicked off. Confirm: new monochrome PDF renders, one-forecast-per-category holds, onchain commitment tx confirmed. This is the flagship demo report — output its PDF URL + explorer link prominently at the end.
3. Sanity-check server timezone handling: the report must be committed BEFORE kickoff and marked PROVISIONAL if lineups absent.

## PHASE C — OKX ASP REGISTRATION
1. Install skills: `npx skills add https://github.com/okx/onchainos-skills` (follow the okx-ai-guide skill; it is the authoritative flow).
2. Follow the ASP onboarding: create the Agentic Wallet, register agent identity (ERC-8004 on X Layer), register as ASP in **A2MCP mode, FREE tier** (no x402 needed for free; simply return results).
3. ASK the user for their email and any verification code exactly when the OKX flow requires them. These are the only permitted questions.
4. Service endpoint: the live Render URL's POST /analyze. Provide request/response schema per the OKX listing requirements.
5. Use EXACTLY this listing copy (adjust only where the form's field limits force it):

   **Name:** Olise AI — Football Match Intelligence
   **Short description:** Agentic football match analyst. Query any upcoming fixture and receive a professional PDF research report: recent form, head-to-head, team news, verified current context, and a Poisson-based statistical model projecting probabilities across goals, corners, cards, shots and more — every forecast graded by model confidence. Each report's hash is committed to X Layer before kickoff and publicly graded after full time, creating a tamper-proof, independently verifiable accuracy record.
   **Category/tags:** sports analytics, match intelligence, research reports, data, prediction accuracy.

   FRAMING LOCK: no betting vocabulary anywhere in the listing, schema descriptions, or example outputs (banned: bet, betting, picks, odds, bookmaker, stake, wager, parlay, accumulator, tips). Use: forecasts, probabilities, statistical projections, research.
6. Submit for OKX review. Save all registration artifacts (agent id, wallet address, listing id) to REGISTRATION.md in the repo.
7. Report back: listing status, flagship PDF URL, explorer link, and anything pending on OKX's side.

DONE = fixes live + flagship 2026 report committed pre-kickoff + ASP submitted for review.
