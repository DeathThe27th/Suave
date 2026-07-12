# REGISTRATION.md — Olise AI on OKX.AI (OnchainOS)

Registered 2026-07-12 via the `onchainos` CLI (okx/onchainos-skills v4.2.2).

## Identity (ERC-8004, X Layer)

| Field | Value |
|---|---|
| Agent ID | **#5132** |
| Role | ASP (Agentic Service Provider) |
| Name | Olise AI |
| Chain | X Layer (chainIndex 196) |
| Owner wallet (OKX Agentic Wallet) | `0xa1cac8c7afa96d3a774d4dd560e10cd53e60fab7` |
| Registration tx | `0x92a3f356966dfcdf1c1987dc58a6fb3aebf4f344e13776965a492b1b9819c679` |
| Avatar | https://static.okx.com/cdn/web3/wallet/marketplace/headimages/agent/avatar/ba14e3f3-709d-4c52-926d-646a07c9ba0f.png |
| Listing status | Submitted for OKX review (`submitApproval` succeeded, approvalStatus 2); activation completes once approved |

## Listing copy (as registered)

**Agent description** (the spec'd short description, verbatim — 485 chars, within the
500-char limit):

> Agentic football match analyst. Query any upcoming fixture and receive a professional
> PDF research report: recent form, head-to-head, team news, verified current context,
> and a Poisson-based statistical model projecting probabilities across goals, corners,
> cards, shots and more — every forecast graded by model confidence. Each report's hash
> is committed to X Layer before kickoff and publicly graded after full time, creating a
> tamper-proof, independently verifiable accuracy record.

Field-limit adjustments (per the "adjust only where limits force it" rule):
- Brand name limit is 25 chars → agent name is **Olise AI**; "Football Match
  Intelligence" became the service name.
- Service description limit is ~200 chars per part → compressed from the spec copy.
- The listing form has no category/tags field; intended tags were: sports analytics,
  match intelligence, research reports, data, prediction accuracy.

## Service

| Field | Value |
|---|---|
| Service name | Football Match Intelligence |
| Type | A2MCP (API service) |
| Tier / fee | FREE — `0` USDT per call (no x402; results returned directly) |
| Endpoint | `POST https://olise-ai.onrender.com/analyze` |

**Service description** (as registered):

> Pre-kickoff statistical research for football fixtures: form, team news, verified
> context, graded probability forecasts (goals, corners, cards, shots), PDF report,
> onchain-verified accuracy record.
> Provide: 1. home team name 2. away team name 3. optional kickoff date (YYYY-MM-DD).

## Request / response schema (`POST /analyze`)

Request (JSON):

```json
{ "home": "Spain", "away": "Belgium", "date": "2026-07-14" }
```

`home` / `away`: team names (required). `date`: optional YYYY-MM-DD kickoff date.

Response (JSON): `report_id`, `status` (`provisional`/`final`), `fixture`,
`summary`, `forecasts[]` (`market`, `selection`, `model_probability`, `grade`,
`drivers`), `pdf_url` (public PDF report), `commitment` (`hash`, `tx_hash`,
`explorer_url` — X Layer testnet commitment recorded before kickoff),
`research_note`. Verification: `GET /verify/{report_id}`; accuracy record:
`GET /track-record`.

## Related onchain infrastructure (service side)

- Report-commitment contract (X Layer testnet, chain id 1952):
  `0x2CA04f3F7Dc7f4b1F85009A97bC7Af06C17902fd`
  (operator `0x9085BCA08E0626FB9351A1D6E5260Cfb4f0a1Fbf`)

## Pending on OKX's side

- Listing approval review (submitted 2026-07-12). Once approved, the agent is
  activated/visible in the marketplace; check with "list my agents" via the
  onchainos flow, or re-run activation if approvalStatus requires it.
