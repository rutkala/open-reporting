#!/bin/sh
# Run monthly via cron: 0 3 1 * * /root/open-reporting/renew-certs.sh
set -e
cd "$(dirname "$0")"
docker compose run --rm certbot renew
docker compose exec nginx nginx -s reload
