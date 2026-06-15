#!/usr/bin/env bash
# Dedicated runner for the dane.gov.pl whole-portal harvester (Layer 1).
#
# This is a massive, resumable bulk sweep (every dataset + resource across ~7,000
# institutions) — same class as GUS BDL/DBW. It must NOT run inside the synchronous
# orchestrator (run_ingestion.py skips it), or it blocks the other ~200 sources.
# Each invocation runs a bounded time budget and resumes from its manifest next time.
#
# Usage: run_danegovpl_harvest.sh [budget_seconds]   (default 10800 = 3h)
set -uo pipefail
cd /opt/open-reporting || exit 1
BUDGET="${1:-10800}"
echo "=== danegovpl harvest start $(date -u) (budget ${BUDGET}s) ==="
timeout "${BUDGET}" /usr/bin/env PYTHONPATH=/opt/open-reporting /usr/bin/python3 \
  products/ingestion/extractors/danegovpl_harvester.py
rc=$?
if [ "$rc" -eq 124 ]; then
  echo "=== budget reached — stopped; resumes from manifest next run $(date -u) ==="
else
  echo "=== danegovpl harvest finished rc=$rc $(date -u) ==="
fi
exit 0
