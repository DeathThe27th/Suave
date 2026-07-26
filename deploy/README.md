# Deploy — Suave on a VPS (Docker + nginx + HTTPS)

This kit takes Suave from a fresh Ubuntu VPS to a **publicly reachable, HTTPS,
domain-bound** endpoint — the exact bar OKX's A2MCP review requires (BUILD.md §3.1).
It maps 1:1 to that checklist: domain → nginx reverse proxy → Let's Encrypt cert →
firewall → systemd (survives reboot) → uptime ping.

**Target for this deployment:** `https://suave-demo.duckdns.org`
**Run style:** the app runs as the committed Docker image; systemd owns `docker run`;
nginx terminates TLS and proxies to `127.0.0.1:8000`.

```
deploy/
  deploy.conf.example   copy -> deploy.conf (DOMAIN, email, optional heartbeat)
  doctor.sh             read-only state report — run first, changes nothing
  bootstrap.sh          one-shot bring-up (idempotent, run as root)
  update.sh             pull + rebuild + restart + health-check
  healthcheck.sh        cron probe every 5 min, auto-heals, optional external ping
  systemd/suave.service systemd unit: docker run, restart=always, on-boot
  nginx/suave.conf.template  HTTP block; certbot upgrades it to 443 + redirect
```

---

## What you need before starting
- An Ubuntu VPS (22.04/24.04) with root/sudo and ports **22, 80, 443** reachable.
- The DuckDNS subdomain `suave-demo` pointed at the VPS's public IP (step 1).
- A Gemini API key and (optional but wired) a Pexels key for imagery.

---

## Step 1 — Point DuckDNS at the VPS
DuckDNS is dynamic DNS; set the subdomain's IP to your VPS.

1. On https://www.duckdns.org, set **suave-demo** → your VPS public IP.
2. If your VPS IP is static (usual), that's it. If it's dynamic, add the DuckDNS
   updater cron on the box (token from the DuckDNS dashboard):
   ```bash
   # */5 * * * *  curl -fsS "https://www.duckdns.org/update?domains=suave-demo&token=YOUR_TOKEN&ip="
   ```
3. Verify it resolves to your VPS from your laptop **before** running bootstrap:
   ```bash
   dig +short suave-demo.duckdns.org      # must print your VPS IP
   ```
   Certbot's HTTP-01 challenge will fail if this doesn't resolve yet.
   (Note: `duckdns.org` is on the Public Suffix List, so each subdomain gets its own
   Let's Encrypt rate-limit bucket — no shared-limit surprises.)

## Step 1.5 — Check what's already on the box
If the VPS has ever served anything on this domain, find out what before overwriting it:
```bash
curl -fsSL https://raw.githubusercontent.com/DeathThe27th/Suave/main/deploy/doctor.sh | sudo bash
```
Read-only. It reports the nginx sites, what holds port 8000 and what restarts it,
Docker/cert/env state, and what the domain currently answers. The two things that
block a clean bootstrap are **a non-Docker process on 127.0.0.1:8000** (the container
can't bind it) and **an older enabled nginx site with the same `server_name`**
(nginx keeps whichever loads first). bootstrap.sh now detects both, but knowing up
front beats reading an abort message.

## Step 2 — Get the code on the box
```bash
sudo apt-get update && sudo apt-get install -y git
git clone https://github.com/DeathThe27th/Suave.git
cd Suave
```

## Step 3 — Runtime secrets (never in the repo)
The app reads its env from `/etc/suave/suave.env`. bootstrap.sh seeds it from
`.env.example` on first run, then stops so you can fill it. You can also create it now:
```bash
sudo install -d -m 0750 /etc/suave
sudo cp .env.example /etc/suave/suave.env
sudo nano /etc/suave/suave.env      # set GEMINI_API_KEY and PEXELS_API_KEY
```
Minimum required: `GEMINI_API_KEY`. `SUAVE_MODEL` defaults to `gemini-3.1-flash-lite`
(the model this free tier has quota on). `PEXELS_API_KEY` enables real photography.

## Step 4 — Fill deploy.conf
```bash
cp deploy/deploy.conf.example deploy/deploy.conf
nano deploy/deploy.conf
#   DOMAIN=suave-demo.duckdns.org
#   LETSENCRYPT_EMAIL=you@example.com
#   HEALTHCHECK_PING_URL=        # optional (healthchecks.io / UptimeRobot)
```

## Step 5 — Run bootstrap
```bash
sudo bash deploy/bootstrap.sh
```
It installs Docker + nginx + certbot, opens the firewall, builds `suave:latest`,
installs & starts the systemd service, renders the nginx site, obtains the cert with
`--redirect`, and installs the health cron. Idempotent — re-run any time.
> **First run stops early, on purpose.** If `/etc/suave/suave.env` didn't exist, it's
> created from the template and the script exits so you can fill in `GEMINI_API_KEY`.
> Continuing with an empty key would build and start a service that reports healthy
> but answers `model_key_set:false` and fails every generate call. Fill it in, then
> run the same command again — it's idempotent and picks up where it left off.

## Step 6 — Verify (from anywhere, not just the box)
```bash
curl -s https://suave-demo.duckdns.org/health
#   {"status":"ok","model":"gemini-3.1-flash-lite","model_key_set":true,
#    "library_count":20,"vet_enabled":true,"x402_enabled":false}

curl -s https://suave-demo.duckdns.org/styles | head

curl -sX POST https://suave-demo.duckdns.org/generate \
  -H 'content-type: application/json' \
  -d '{"product":"Ferry","what_it_does":"same-day courier for law firms","tone":"trustworthy"}' \
  -o page.html && echo "bytes: $(wc -c < page.html)"
```

## Step 7 — Reboot test (BUILD.md §3.5)
```bash
sudo reboot
# reconnect, then:
curl -s https://suave-demo.duckdns.org/health   # must come back on its own
```

---

## Operations
- **Logs:** `journalctl -u suave -f`
- **Restart:** `sudo systemctl restart suave`
- **Update to latest code:** `sudo bash deploy/update.sh`
- **Cert renewal:** automatic via certbot's systemd timer — `systemctl list-timers 'certbot*'`
- **Health:** `/usr/local/bin/suave-healthcheck` runs every 5 min (cron), restarts the
  service after two failed probes, logs to `/var/log/suave-health.log`, and pings your
  external monitor if `HEALTHCHECK_PING_URL` is set.

## Troubleshooting
| Symptom | Check |
|---|---|
| certbot fails | `dig +short suave-demo.duckdns.org` matches VPS IP? port 80 open? |
| `/health` 502 | container up? `journalctl -u suave -n 50`; env key set in `/etc/suave/suave.env`? |
| `model_key_set:false` | `GEMINI_API_KEY` missing/empty in `/etc/suave/suave.env`, then `systemctl restart suave` |
| 429 from `/generate` | free-tier per-minute quota — the API returns a clean `rate_limited` JSON + `Retry-After`; wait that long, or set a different `SUAVE_MODEL` |
| nginx won't reload | `sudo nginx -t` prints the exact line |

## MCP endpoint
The FastMCP tool is mounted at **`/mcp`** (streamable HTTP) — verified by a real client
handshake (`generate_landing_page` lists with its params). After deploy, point the MCP
Inspector at `https://suave-demo.duckdns.org/mcp` (BUILD.md §3.5). nginx already proxies
it (buffering off, SSE-ready); no extra proxy config. A plain `GET /mcp/` returns 406
(needs MCP `Accept` headers) — that's expected, not an error.

## Not covered here
- **x402 payment:** stays OFF until Task Zero (the seller-side settle path) is confirmed
  with OKX (BUILD.md §3.2).
