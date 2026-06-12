#!/usr/bin/env bash
# GUS bulk API extraction wrapper — BDL + DBW resumable mirrors.
#
# Invoked by user crontab:
#   30 3 * * *    run_gus_bulk.sh bdl   # daily; ~7k req/day vs 50k/week quota
#   0 4,16 * * *  run_gus_bulk.sh dbw   # 2x daily; 4,500 req vs 5,000/12h quota
#
# Both extractors are resumable (manifest checkpoints) and budget-aware:
# when the weekly quota is spent they exit 0 immediately, so re-running is
# always safe. flock prevents overlapping runs of the same extractor.
set -uo pipefail

REPO=/opt/open-reporting
export PYTHONPATH=$REPO
LOG_DIR=$REPO/data/logs
mkdir -p "$LOG_DIR"

WHICH="${1:-}"
case "$WHICH" in
  bdl)
    LOCK=/tmp/or-bdl-extractor.lock
    LOG="$LOG_DIR/bdl-bulk-$(date -u +%Y-%m-%d).log"
    CMD=(python3 "$REPO/products/ingestion/extractors/bdl_extractor.py"
         --subjects all --max-requests 7000)
    ;;
  dbw)
    LOCK=/tmp/or-dbw-extractor.lock
    LOG="$LOG_DIR/dbw-bulk-$(date -u +%Y-%m-%d).log"
    CMD=(python3 "$REPO/products/ingestion/extractors/dbw_extractor.py"
         --max-requests 4500)
    ;;
  *)
    echo "usage: $0 bdl|dbw" >&2
    exit 2
    ;;
esac

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] run_gus_bulk $WHICH start" >> "$LOG"
flock -n "$LOCK" "${CMD[@]}" >> "$LOG" 2>&1
rc=$?
if [ $rc -eq 1 ] && ! flock -n "$LOCK" true 2>/dev/null; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $WHICH already running — skipped" >> "$LOG"
  exit 0
fi
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] run_gus_bulk $WHICH end (exit=$rc)" >> "$LOG"
exit $rc
