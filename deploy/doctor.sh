#!/usr/bin/env bash
# Read-only VPS state report. Changes nothing — safe to run any time.
# On the box:  curl -fsSL https://raw.githubusercontent.com/DeathThe27th/Suave/main/deploy/doctor.sh | sudo bash
#
# Exists because bootstrap.sh rewrites the nginx site and runs certbot; both behave
# differently on a box that already serves something on the target domain. Run this
# first and you know which of those two apply before anything is overwritten.
set -uo pipefail   # deliberately no -e: every probe must run even when one fails

DOMAIN="${DOMAIN:-suave-demo.duckdns.org}"
hr() { printf '\n=== %s ===\n' "$1"; }

hr "host"
echo "os:     $(. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME")"
echo "uptime:$(uptime -p 2>/dev/null)"
echo "public ip: $(curl -fsS --max-time 5 https://api.ipify.org 2>/dev/null || echo '(lookup failed)')"
echo "$DOMAIN -> $(getent hosts "$DOMAIN" | awk '{print $1}' | paste -sd, - || echo '(no resolve)')"

hr "nginx sites-enabled"
ls -la /etc/nginx/sites-enabled/ 2>/dev/null || echo "(no sites-enabled dir)"
echo "-- server_name / proxy_pass in each --"
grep -rnE 'server_name|proxy_pass|root ' /etc/nginx/sites-enabled/ 2>/dev/null || echo "(none found)"
echo "-- config test --"
nginx -t 2>&1

hr "suave systemd unit"
if systemctl list-unit-files 2>/dev/null | grep -q '^suave\.service'; then
    systemctl status suave --no-pager --lines=0 2>&1 | head -6
    echo "enabled-on-boot: $(systemctl is-enabled suave 2>&1)"
else
    echo "(no suave.service installed -> bootstrap.sh has never completed here)"
fi

hr "other listeners"
ss -lntp 2>/dev/null | grep -E ':(80|443|8000)\b' || echo "(nothing on 80/443/8000)"

hr "docker"
if command -v docker >/dev/null 2>&1; then
    docker --version
    echo "-- containers --"; docker ps -a --format '{{.Names}}\t{{.Image}}\t{{.Status}}' 2>&1
    echo "-- suave image --"; docker images suave --format '{{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}' 2>&1
else
    echo "(docker not installed)"
fi

hr "TLS certificates"
if command -v certbot >/dev/null 2>&1; then
    certbot certificates 2>/dev/null | grep -E 'Certificate Name|Domains|Expiry|VALID|INVALID' || echo "(no certs)"
else
    echo "(certbot not installed)"
fi

hr "runtime env /etc/suave/suave.env"
if [[ -f /etc/suave/suave.env ]]; then
    # Never print secret values — only whether each key is populated.
    echo "exists. keys set:"
    while IFS='=' read -r k v; do
        [[ "$k" =~ ^[A-Z_]+$ ]] || continue
        if [[ -n "${v//[[:space:]]/}" ]]; then echo "  $k = [set]"; else echo "  $k = (empty)"; fi
    done < /etc/suave/suave.env
else
    echo "(missing -> bootstrap will seed it from .env.example and stop)"
fi

hr "repo checkout"
for d in ~/Suave /root/Suave /opt/Suave /srv/Suave; do
    [[ -d "$d/.git" ]] || continue
    echo "$d  branch=$(git -C "$d" rev-parse --abbrev-ref HEAD 2>/dev/null)  head=$(git -C "$d" log --oneline -1 2>/dev/null)"
done
[[ -d ~/Suave/.git || -d /root/Suave/.git || -d /opt/Suave/.git || -d /srv/Suave/.git ]] || echo "(no clone found in the usual places)"

hr "what the domain actually serves right now"
echo "-- https://$DOMAIN/health --"
curl -fsS --max-time 10 "https://$DOMAIN/health" 2>&1 | head -c 400; echo
echo "-- http://127.0.0.1:8000/health (direct to app) --"
curl -fsS --max-time 10 "http://127.0.0.1:8000/health" 2>&1 | head -c 400; echo

hr "health cron"
crontab -l 2>/dev/null | grep suave || echo "(no suave health cron installed)"

printf '\n=== end of report ===\n'
