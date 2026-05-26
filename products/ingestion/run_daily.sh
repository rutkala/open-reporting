#!/usr/bin/env bash
# Daily ingestion wrapper — NBP exchange rates + Eurostat observations.
#
# Invoked by user crontab at 22:00 UTC (00:00 Warsaw next day, CEST), in
# the quiet hours so the brief dbr restart is invisible. NBP publishes
# rates around 12:15 CET; by 22:00 UTC the publish has had ~9h to settle.
#
# DuckDB is file-locked: the live dbr-served dashboards hold an exclusive
# lock on warehouse.duckdb, blocking writers. We work around this by
# stopping or-public_finance.service before ingestion and starting it
# again after. Total downtime ~30 seconds.
#
# Idempotent: both upstream scripts use upsert semantics on their natural
# keys (NBP: currency_code+rate_date; Eurostat: dataset+geo+period+dim_key).
# Re-running the same day is safe and a no-op for already-loaded rows.
#
# Logs to /opt/open-reporting/data/logs/ingest-daily-YYYY-MM-DD.log with
# rotation by date (one file per day; old files persist for inspection).
# Exit code: max of the two sub-scripts (non-zero if anything failed).
# The dashboard is always restarted, even on ingestion failure.
#
# Linear: OR-85
set -uo pipefail

REPO=/opt/open-reporting
export PYTHONPATH=$REPO
LOG_DIR=$REPO/data/logs
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/ingest-daily-$(date -u +%Y-%m-%d).log"

ts() { date -u +'%Y-%m-%dT%H:%M:%SZ'; }
log() { echo "[$(ts)] $*" | tee -a "$LOG"; }

log "=== daily ingestion start ==="
log "host: $(hostname)  user: $(whoami)  python: $(python3 --version 2>&1)"

# Trap to always restart dashboard even on early exit
ensure_dashboard_running() {
  log "ensuring or-public_finance.service is running…"
  sudo -n /usr/bin/systemctl start or-public_finance.service >>"$LOG" 2>&1 || log "WARN: dashboard start failed"
}
trap ensure_dashboard_running EXIT

log "stopping or-public_finance.service to release DuckDB lock…"
sudo -n /usr/bin/systemctl stop or-public_finance.service >>"$LOG" 2>&1

run() {
  local name=$1 script=$2
  log "--- $name ---"
  if python3 "$script" >>"$LOG" 2>&1; then
    log "$name: OK"
    return 0
  else
    local rc=$?
    log "$name: FAILED (exit $rc)"
    return $rc
  fi
}

worst=0

if ! run "NBP exchange rates" "$REPO/products/ingestion/to_raw/nbp_exchange_rates.py"; then
  worst=1
fi

if ! run "Eurostat observations" "$REPO/products/ingestion/to_raw/eurostat_observations.py"; then
  worst=1
fi

log "=== daily ingestion end (exit=$worst) ==="
# trap will restart the dashboard
exit $worst
