#!/usr/bin/env bash
# Daily ingestion wrapper — NBP exchange rates + Eurostat observations.
#
# Invoked by user crontab at 22:00 UTC (00:00 Warsaw next day, CEST). NBP
# publishes rates around 12:15 CET; by 22:00 UTC the publish has had ~9h to settle.
#
# As of OR-168 the dashboards are pre-rendered STATIC HTML served by nginx — no
# process holds a live lock on warehouse.duckdb during ingestion, so the old
# "stop every or-*.service, ingest, restart" dance is gone (it also never refreshed
# dashboard content: the dashboards render from curated marts, updated only by a
# deliberate `dbt run` + `dbr build`, not by raw ingestion).
#
# Idempotent: both upstream scripts use upsert semantics on their natural
# keys (NBP: currency_code+rate_date; Eurostat: dataset+geo+period+dim_key).
# Re-running the same day is safe and a no-op for already-loaded rows.
#
# Logs to /opt/open-reporting/data/logs/ingest-daily-YYYY-MM-DD.log with
# rotation by date (one file per day; old files persist for inspection).
# Exit code: max of the two sub-scripts (non-zero if anything failed).
#
# Linear: OR-85, OR-168
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

# Incremental ingestion — API deltas only (bulk runs are manual via bulk/run_bulk.py)
if ! run "Incremental ingestion" "$REPO/products/ingestion/incremental/run_incremental.py"; then
  worst=1
fi

log "--- dbt run ---"
if ! (cd "$REPO/products/warehouse" && DUCKDB_PATH=$REPO/data/warehouse.duckdb dbt run --profiles-dir .) >>"$LOG" 2>&1; then
  rc=$?
  log "dbt run: FAILED (exit $rc)"
  worst=1
else
  log "dbt run: OK"
fi

# NOTE: mf_extractor.py / nfz_extractor.py / zus_extractor.py were MOCKS that
# wrote 3 hardcoded fake rows each into raw_mf_budget / raw_nfz_services /
# raw_zus_benefits. Removed from the nightly run (2026-06-13) — real MF/NFZ/ZUS
# data lands via the bulk dane.gov.pl mirror (mf_bulk/nfz_bulk/zus_bulk); a real
# incremental loader for those tables is tracked in docs/ingestion-roadmap.md.

if ! run "Admin catalog refresh" "$REPO/infra/scheduler/refresh_admin_catalogs.py"; then
  worst=1
fi

log "=== daily ingestion end (exit=$worst) ==="

# On non-zero exit, drop a Telegram outbox file so the bot pings the PO.
# Silent failures yesterday (2026-05-27) motivated this — OR-76.
if [ "$worst" -ne 0 ]; then
  OUTBOX="$REPO/data/telegram-outbox"
  mkdir -p "$OUTBOX"
  ALERT="$OUTBOX/$(date -u +%Y%m%dT%H%M%SZ)-ingest-FAIL.md"
  {
    echo "## [ALERT] Daily ingestion FAILED — $(ts)"
    echo
    echo "Exit code: \`$worst\`"
    echo "Log: \`$LOG\`"
    echo
    echo "Last 30 lines of log:"
    echo
    echo '```'
    tail -30 "$LOG"
    echo '```'
    echo
    echo "Investigate: \`tail -200 $LOG\` on VPS."
  } > "$ALERT" 2>/dev/null || true
fi

exit $worst
