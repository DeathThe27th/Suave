# DEPLOY VIA RENDER — AGENT-EXECUTED

You (Claude Code) are deploying the already-built Olise AI service in this repo to Render's free tier using the **Render REST API** (https://api.render.com/v1), then configuring keep-alive via the **cron-job.org API**. Execute everything yourself with `curl`/Python — do NOT tell the user to open dashboards except where explicitly stated below.

## PHASE 0 — ASK FOR EVERYTHING IN ONE MESSAGE

1. `RENDER_API_KEY` — from Render dashboard → Account Settings → API Keys (user must have already signed up with GitHub and authorized repo access)
2. `CRONJOB_API_KEY` — from console.cron-job.org → Settings → API
3. `SUPABASE_DB_URL` — Supabase dashboard → Connect → connection string (URI, the one with the database password). Needed once, to run schema.sql.
4. Confirm the `.env` used in the build is present locally (it is not in git). If any value is missing, ask for it now.

Then proceed without further questions. Log every step's outcome. Keep all keys out of git.

## PHASE 1 — DATABASE

Run `schema.sql` against `SUPABASE_DB_URL` (use psycopg2/psql; install if needed). Idempotent: use IF NOT EXISTS semantics — if the schema file lacks them, wrap/adjust safely. Verify tables exist afterwards. The deployed service must use Supabase Postgres persistence, NOT the SQLite fallback (Render's disk is ephemeral) — ensure whatever env var the app uses to select Supabase persistence is set.

## PHASE 2 — CREATE THE RENDER SERVICE

Via the Render API:
1. `GET /v1/owners` → take the user's owner id.
2. Create a web service from this GitHub repo (`POST /v1/services`): runtime = docker (the repo's Dockerfile), plan = `free`, region: closest available (default fine), branch = main, autoDeploy = yes.
3. Set ALL env vars from the local `.env` via the env-vars endpoint: API_FOOTBALL_KEY, GEMINI_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_BUCKET, XLAYER_PRIVATE_KEY, ADMIN_TOKEN — plus any additional vars the app's config requires (check the repo's config module). Do NOT set HOST/PORT if the Dockerfile/render.yaml handles them; Render injects PORT.
4. Trigger a deploy if one didn't start automatically. Poll the deploy status until live (builds with WeasyPrint deps can take ~10 min — be patient, poll every 30s).
5. If the build fails: fetch the logs via the API, diagnose, fix the repo (commit + push), redeploy. Repeat until live. Common issues: missing system packages in Dockerfile (pango, cairo, gdk-pixbuf), port binding (must bind 0.0.0.0:$PORT).

## PHASE 3 — CONTRACT ADDRESS PERSISTENCE

The app deploys the OliseCommit contract on first start and saves the address to `.olise_chain.json` — which Render wipes on every redeploy. After the first successful boot:
1. Fetch runtime logs via the API, extract the deployed contract address (the app logs it; if it doesn't, add a log line, push, redeploy).
2. Set it as an env var so future boots REUSE the contract instead of redeploying it. If the app doesn't currently read the contract address from env, make that small code change first (env var takes precedence over the json file), commit, push.
3. Trigger a redeploy and confirm from logs that the existing contract was reused (no new deployment tx).

## PHASE 4 — VERIFY END-TO-END (production URL)

Against `https://<service>.onrender.com`:
1. `GET /health` → all checks green, scheduler running.
2. `POST /analyze` for a real upcoming World Cup fixture → confirm: response OK, PDF URL opens (fetch it, non-zero bytes, %PDF header), commitment tx hash present → verify the tx exists via the X Layer testnet RPC.
3. `GET /verify/{report_id}` → hash matches.
4. Repeat the same `POST /analyze` → cached report returned, no duplicate onchain commit.

## PHASE 5 — KEEP-ALIVE

Via the cron-job.org API (https://api.cron-job.org, Bearer auth): create a job titled "olise-keepalive" hitting `https://<service>.onrender.com/health` every 10 minutes, enabled. Verify with a follow-up GET that the job exists and its last execution succeeded (wait for one tick if needed).

## DONE = report to the user:
- Live service URL
- /health output
- A fresh report: PDF link + X Layer testnet explorer link for its commitment tx
- Contract address (persisted in env)
- Cron job id + status
- Anything you changed in the repo and why
