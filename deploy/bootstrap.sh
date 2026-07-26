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

echo "==> [1/9] Preflight — is anything already holding the app port?"
# suave.service publishes the container on 127.0.0.1:8000. If a non-Docker process
# already holds that port (e.g. a hand-started uvicorn from an earlier bring-up),
# `docker run` fails with "port is already allocated" and Restart=always turns that
# into a silent crash-loop. Catch it here, while the message is still legible.
port_pid="$(ss -lntpH 'sport = :8000' 2>/dev/null | grep -oE 'pid=[0-9]+' | cut -d= -f2 | head -1)"
if [[ -n "$port_pid" ]]; then
    holder_cmd="$(ps -o comm= -p "$port_pid" 2>/dev/null || echo unknown)"
    holder_unit="$(grep -oE '[a-zA-Z0-9_.@-]+\.service' "/proc/$port_pid/cgroup" 2>/dev/null | head -1)"
    echo "    port 8000 held by pid $port_pid ($holder_cmd), unit: ${holder_unit:-none}"

    if [[ "$holder_cmd" == docker-proxy || "$holder_cmd" == docker ]]; then
        echo "    that's our own container — ExecStartPre will replace it."
    elif [[ "$holder_unit" == "suave.service" ]]; then
        # A pre-Docker suave.service from an earlier bring-up. This script installs
        # suave.service itself, so replacing it is in scope -- but keep a copy, since
        # it is the only record of how the previous deploy ran.
        old_unit="$(systemctl show suave.service -p FragmentPath --value 2>/dev/null)"
        if [[ -n "$old_unit" && -f "$old_unit" ]]; then
            cp -n "$old_unit" "${old_unit}.pre-docker.bak" 2>/dev/null \
                && echo "    backed up previous unit -> ${old_unit}.pre-docker.bak"
        fi
        echo "    stopping + disabling the previous suave.service (replaced in step 6)"
        systemctl disable --now suave.service || true
        sleep 2
        if ss -lntpH 'sport = :8000' 2>/dev/null | grep -q .; then
            echo "!! Port 8000 still held after stopping suave.service. Investigate:" >&2
            ss -lntp 2>/dev/null | grep ':8000' >&2
            exit 1
        fi
        echo "    port 8000 released."
    else
        cat >&2 <<EOF
!! Port 127.0.0.1:8000 is held by pid $port_pid ($holder_cmd), unit ${holder_unit:-none}.

   Suave's container publishes that port and cannot bind it while this runs. This is
   not a unit this script manages, so it will not be touched automatically. Stop it,
   and make sure it does not return on boot -- anything that restarts it wins the
   race after a reboot and leaves Suave crash-looping. Then re-run this script.
EOF
        exit 1
    fi
fi

echo "==> [2/9] Packages (nginx, certbot, docker, gettext-base)"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y nginx certbot python3-certbot-nginx gettext-base curl ca-certificates
if ! command -v docker >/dev/null 2>&1; then
    echo "    installing docker…"
    curl -fsSL https://get.docker.com | sh
fi
systemctl enable --now docker

echo "==> [3/9] Firewall (allow SSH + Nginx Full)"
if command -v ufw >/dev/null 2>&1; then
    ufw allow OpenSSH >/dev/null 2>&1 || ufw allow 22/tcp >/dev/null 2>&1 || true
    ufw allow 'Nginx Full' >/dev/null 2>&1 || { ufw allow 80/tcp; ufw allow 443/tcp; }
    ufw --force enable
    ufw status
else
    echo "    ufw not present — skipping (ensure 22/80/443 are open in your provider firewall)"
fi

echo "==> [4/9] Runtime env at /etc/suave/suave.env"
install -d -m 0750 /etc/suave
if [[ ! -f /etc/suave/suave.env ]]; then
    install -m 0640 "$repo_root/.env.example" /etc/suave/suave.env
    cat >&2 <<EOF
    !! Created /etc/suave/suave.env from .env.example.

    Set GEMINI_API_KEY (and PEXELS_API_KEY for real photography):
        sudo nano /etc/suave/suave.env

    Then re-run this script. Stopping here on purpose — continuing would build and
    start the service with an empty key, which comes up "healthy" but answers
    model_key_set:false and fails every generate call.
EOF
    exit 1
fi

echo "==> [5/9] Build image (suave:latest)"
docker build -t suave:latest "$repo_root"

echo "==> [6/9] systemd unit"
install -m 0644 "$here/systemd/suave.service" /etc/systemd/system/suave.service
systemctl daemon-reload
systemctl enable --now suave.service
sleep 3
systemctl --no-pager --lines=0 status suave.service || true

echo "==> [7/9] nginx site for ${DOMAIN}"
DOMAIN="$DOMAIN" envsubst '$DOMAIN' < "$here/nginx/suave.conf.template" \
    > /etc/nginx/sites-available/suave.conf
ln -sf /etc/nginx/sites-available/suave.conf /etc/nginx/sites-enabled/suave.conf
# Drop any other enabled site claiming this domain. Two server blocks with the same
# server_name is not an error to nginx — it keeps whichever it loads first (alphabetical)
# and merely warns, so an older site named e.g. "suave" would silently outrank our
# "suave.conf" and keep serving the previous app.
for site in /etc/nginx/sites-enabled/*; do
    [[ -e "$site" ]] || continue
    [[ "$(basename "$site")" == "suave.conf" ]] && continue
    if [[ "$(basename "$site")" == "default" ]] || grep -qs "server_name\s*.*${DOMAIN}" "$site"; then
        echo "    disabling conflicting site: $(basename "$site")"
        rm -f "$site"
    fi
done
nginx -t
systemctl reload nginx

echo "==> [8/9] HTTPS via Let's Encrypt"
# --keep-until-expiring matters on a re-run or a box that already has a cert: without
# it, certbot hits the "you have an existing certificate" decision, which it cannot
# resolve under --non-interactive. That non-zero exit would abort this script (set -e)
# before the health cron below ever gets installed, leaving a deploy that looks fine.
# With it, an existing valid cert is reused and the installer still (re)writes the
# 443 block + redirect that rendering the template above just overwrote.
certbot --nginx -d "$DOMAIN" \
    --non-interactive --agree-tos -m "$LETSENCRYPT_EMAIL" --redirect --keep-until-expiring
systemctl reload nginx
# certbot installs its own renewal systemd timer; confirm it's active.
systemctl list-timers 'certbot*' --no-pager 2>/dev/null | head -n 3 || true

echo "==> [9/9] Health cron (every 5 min, auto-heal)"
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
