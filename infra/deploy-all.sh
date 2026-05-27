#!/usr/bin/env bash
# deploy-all.sh — Run all pending VPS tasks in one shot.
#
# Run as the 'radek' user on the production VPS:
#   cd /opt/open-reporting && git pull && bash infra/deploy-all.sh
#
# What this does (in order):
#   1. Pull latest code from git
#   2. Publish OR-147 COFOG article to Ghost
#   3. Publish OR-148 EU fiscal article to Ghost
#   4. Run dbt seed + dbt run for OR-83 ENV dashboard + OR-87 fix
#   5. Deploy OR-83 ENV dashboard (dbr validate → dbr run → systemd → nginx)
#
# Prerequisites: .env must exist with GHOST_KEY_ID, GHOST_KEY_SECRET, DUCKDB_PATH

set -euo pipefail
REPO=/opt/open-reporting
PY="PYTHONPATH=$REPO python3"

cd "$REPO"

echo "=== [0] Git pull ==="
git pull --ff-only origin main

echo ""
echo "=== [1] Publish OR-147 COFOG article ==="
$PY products/blog/publish_to_ghost.py \
    products/blog/drafts/or-147-cofog.md \
    --publish
echo "OR-147 published ✓"

echo ""
echo "=== [2] Publish OR-148 EU fiscal comparison article ==="
$PY products/blog/publish_to_ghost.py \
    products/blog/drafts/or-148-eu-fiscal-comparison.md \
    --publish
echo "OR-148 published ✓"

echo ""
echo "=== [3] OR-87 fix — re-seed + rebuild MAC/BUS models ==="
cd "$REPO/products/warehouse"
DUCKDB_PATH="$REPO/data/warehouse.duckdb" dbt seed --select eurostat_series --profiles-dir . --quiet
DUCKDB_PATH="$REPO/data/warehouse.duckdb" dbt run \
    --select stg_eurostat mac_indicators fact_macro_overview bus_indicators \
    --profiles-dir .
echo "OR-87 mac/bus rebuild ✓"

echo ""
echo "=== [4] OR-83 ENV dashboard — seed + dbt run ==="
DUCKDB_PATH="$REPO/data/warehouse.duckdb" dbt run \
    --select env_indicators fact_env_overview \
    --profiles-dir .
echo "OR-83 dbt models ✓"

echo ""
echo "=== [5] OR-83 ENV dashboard — validate ==="
cd "$REPO"
dbr validate products/dashboards/environment
echo "OR-83 validate ✓"

echo ""
echo "=== [6] OR-83 ENV dashboard — deploy (dbr run) ==="
dbr run products/dashboards/environment
echo "OR-83 dbr run ✓"

echo ""
echo "=== [7] OR-83 systemd service ==="
sudo cp infra/systemd/or-environment.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable or-environment
sudo systemctl start or-environment
echo "or-environment service started ✓"

echo ""
echo "=== [8] OR-83 nginx route ==="
sudo cp infra/nginx/conf.d/dbr-routes/environment.conf /etc/nginx/conf.d/dbr-routes/
sudo nginx -t
sudo nginx -s reload
echo "nginx reloaded ✓"

echo ""
echo "=== DONE ==="
echo "Verify:"
echo "  https://portal.open-reporting.dev/environment/   (should show 4 KPIs with data)"
echo "  https://www.open-reporting.dev/cofog-wydatki-polska-2023-gdzie-trafi-kazda-zlotowka/"
echo "  https://www.open-reporting.dev/polska-na-tle-ue-deficyt-dlug-2024/"
