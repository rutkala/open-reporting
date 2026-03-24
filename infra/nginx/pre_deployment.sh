#!/bin/bash
# Run once before first `docker compose up` to bootstrap self-signed certs.
# These let nginx start before real Let's Encrypt certs exist.
set -e
cd "$(dirname "$0")"

DOMAIN="open-reporting.dev"
# Use the same path certbot will use so nginx config always matches
CERT_DIR="./certs/live/$DOMAIN"

echo "[PreDeployment] Creating directories..."
mkdir -p "$CERT_DIR" ./www

# Only generate self-signed if real cert doesn't exist yet
if [ -f "$CERT_DIR/fullchain.pem" ]; then
    echo "[PreDeployment] Cert already exists, skipping self-signed generation."
    exit 0
fi

echo "[PreDeployment] Generating self-signed certificate for $DOMAIN..."
openssl req -x509 -nodes -days 7 -newkey rsa:2048 \
  -keyout "$CERT_DIR/privkey.pem" \
  -out "$CERT_DIR/fullchain.pem" \
  -subj "/CN=$DOMAIN"

echo "[PreDeployment] Done. Self-signed cert valid for 7 days — run request_certificate.sh to get real certs."
