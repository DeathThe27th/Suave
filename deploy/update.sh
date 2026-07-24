#!/usr/bin/env bash
# Pull latest, rebuild the image, restart the service, re-check health.
# Run as root from the repo root:  sudo bash deploy/update.sh
set -euo pipefail
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

git pull --ff-only
docker build -t suave:latest .
systemctl restart suave.service
sleep 3
if curl -fsS --max-time 10 http://127.0.0.1:8000/health >/dev/null; then
    echo "OK — suave restarted and healthy."
else
    echo "!! health check failed after restart — check: journalctl -u suave -n 50" >&2
    exit 1
fi
