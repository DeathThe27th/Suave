#!/usr/bin/env bash
# Uptime ping + auto-heal. Installed to /usr/local/bin/suave-healthcheck, run by cron
# every 5 min. Two failed probes -> restart the service. Optional external heartbeat.
set -u

URL="http://127.0.0.1:8000/health"
[[ -f /etc/suave/healthcheck.env ]] && . /etc/suave/healthcheck.env  # HEALTHCHECK_PING_URL

probe() { curl -fsS --max-time 10 "$URL" >/dev/null 2>&1; }

if probe; then
    [[ -n "${HEALTHCHECK_PING_URL:-}" ]] && curl -fsS --max-time 10 "$HEALTHCHECK_PING_URL" >/dev/null 2>&1 || true
    exit 0
fi

sleep 3
if probe; then
    [[ -n "${HEALTHCHECK_PING_URL:-}" ]] && curl -fsS --max-time 10 "$HEALTHCHECK_PING_URL" >/dev/null 2>&1 || true
    exit 0
fi

echo "$(date -Is) health check FAILED — restarting suave.service"
systemctl restart suave.service
