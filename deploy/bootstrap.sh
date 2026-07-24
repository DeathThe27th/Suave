#!/usr/bin/env bash
# Suave one-shot VPS bring-up: Docker + nginx + HTTPS + systemd + firewall + health cron.
# Idempotent — safe to re-run. Assumes Ubuntu and that DNS already points at this box.
# Run as root (or via sudo) from the repo root:  sudo bash deploy/bootstrap.sh
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
repo_root="$(cd "$here/.." && pwd)"

if [[ $EUID -ne 0 ]]; then
    echo "!! Run as root: sudo bash deploy/bootstrap.sh" >&2
    exit 1
fi
if [[ ! -f "$here/deploy.conf" ]]; then
    echo "!! Missing $here/deploy.conf — copy deploy.conf.example to deploy.conf and fill it in." >&2
    exit 1
fi
# shellcheck source=/dev/null
source "$here/deploy.conf"
: "${DOMAIN:?set DOMAIN in deploy.conf}"
: "${LETSENCRYPT_EMAIL:?set LETSENCRYPT_EMAIL in deploy.conf}"

echo "==> [1/8] Packages (nginx, certbot, docker, gettext-base)"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y nginx certbot python3-certbot-nginx gettext-base curl ca-certificates
if ! command -v docker >/dev/null 2>&1; then
    echo "    installing docker…"
    curl -fsSL https://get.docker.com | sh
fi
systemctl enable --now docker

echo "==> [2/8] Firewall (allow SSH + Nginx Full)"
if command -v ufw >/dev/null 2>&1; then
    ufw allow OpenSSH >/dev/null 2>&1 || ufw allow 22/tcp >/dev/null 2>&1 || true
    ufw allow 'Nginx Full' >/dev/null 2>&1 || { ufw allow 80/tcp; ufw allow 443/tcp; }
    ufw --force enable
    ufw status
else
    echo "    ufw not present — skipping (ensure 22/80/443 are open in your provider firewall)"
fi

echo "==> [3/8] Runtime env at /etc/suave/suave.env"
install -d -m 0750 /etc/suave
if [[ ! -f /etc/suave/suave.env ]]; then
    install -m 0640 "$repo_root/.env.example" /etc/suave/suave.env
    echo "    !! Created /etc/suave/suave.env from .env.example — EDIT IT NOW and set GEMINI_API_KEY."
    echo "    Re-run this script after filling it in, or fill it and continue."
fi

echo "==> [4/8] Build image (suave:latest)"
docker build -t suave:latest "$repo_root"

echo "==> [5/8] systemd unit"
install -m 0644 "$here/systemd/suave.service" /etc/systemd/system/suave.service
systemctl daemon-reload
systemctl enable --now suave.service
sleep 3
systemctl --no-pager --lines=0 status suave.service || true

echo "==> [6/8] nginx site for ${DOMAIN}"
DOMAIN="$DOMAIN" envsubst '$DOMAIN' < "$here/nginx/suave.conf.template" \
    > /etc/nginx/sites-available/suave.conf
ln -sf /etc/nginx/sites-available/suave.conf /etc/nginx/sites-enabled/suave.conf
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "==> [7/8] HTTPS via Let's Encrypt"
certbot --nginx -d "$DOMAIN" \
    --non-interactive --agree-tos -m "$LETSENCRYPT_EMAIL" --redirect
systemctl reload nginx
# certbot installs its own renewal systemd timer; confirm it's active.
systemctl list-timers 'certbot*' --no-pager 2>/dev/null | head -n 3 || true

echo "==> [8/8] Health cron (every 5 min, auto-heal)"
install -m 0755 "$here/healthcheck.sh" /usr/local/bin/suave-healthcheck
# Pass the optional external ping URL through to the check.
install -d -m 0755 /etc/suave
printf 'HEALTHCHECK_PING_URL=%s\n' "${HEALTHCHECK_PING_URL:-}" > /etc/suave/healthcheck.env
( crontab -l 2>/dev/null | grep -v suave-healthcheck || true
  echo "*/5 * * * * /usr/local/bin/suave-healthcheck >> /var/log/suave-health.log 2>&1" ) | crontab -

echo
echo "==> Done. Verify from anywhere:"
echo "    curl -s https://${DOMAIN}/health"
echo "    curl -s https://${DOMAIN}/styles | head"
echo "    (reboot test:  sudo reboot  — then re-check /health)"
