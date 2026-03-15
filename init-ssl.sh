#!/bin/sh
# Run once to obtain the first SSL cert, then use docker compose up -d for everything.
set -e
cd "$(dirname "$0")"

echo "==> Starting nginx with HTTP-only bootstrap config..."
mv nginx/conf.d/metabase.conf nginx/conf.d/metabase.conf.disabled
docker compose up -d nginx

echo "==> Obtaining SSL certificate for ${DOMAIN}..."
docker compose run --rm certbot

echo "==> Switching to full SSL config..."
mv nginx/conf.d/metabase.conf.disabled nginx/conf.d/metabase.conf
rm nginx/conf.d/bootstrap.conf
docker compose exec nginx nginx -s reload

echo "==> Starting remaining services..."
docker compose up -d

echo "Done. Visit https://${DOMAIN}"
