#!/bin/bash
# Run after `docker compose up -d nginx` to get real Let's Encrypt certs.
# Add new subdomains to -d flags as the stack grows.
set -e
cd "$(dirname "$0")/.."

docker compose run --rm --entrypoint certbot certbot certonly \
  --webroot -w /var/www/certbot \
  -d open-reporting.dev \
  -d portal.open-reporting.dev \
  -d www.open-reporting.dev \
  --cert-name open-reporting.dev \
  --expand \
  --non-interactive \
  --agree-tos \
  -m r.utkala@gmail.com

echo "Reloading nginx..."
docker compose exec nginx nginx -s reload
echo "Done. Certs live at nginx/certs/live/open-reporting.dev/"
