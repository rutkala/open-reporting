#!/usr/bin/env python3
"""
Ingestion orchestrator.

Runs every source due for a given cadence by invoking its extractor engine.
Replaces ~130 cron lines with 3 (nightly/weekly/monthly). Reads the schedule
(products/ingestion/registry/ingestion_schedule.yaml), groups due sources by
engine, and invokes each engine once with its due source keys.

Usage:
    python3 run_ingestion.py --cadence weekly        # run all weekly sources
    python3 run_ingestion.py --cadence nightly --dry-run
    python3 run_ingestion.py --cadence monthly --only web_scraper_extractor.py
"""
import argparse
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

REPO = Path("/opt/open-reporting")
SCHEDULE = REPO / "products/ingestion/registry/ingestion_schedule.yaml"
EXTRACTORS = REPO / "products/ingestion/extractors"

# How to invoke each engine:
#   sources — engine accepts `--sources k1 k2 …` (run once with all due keys)
#   single  — engine has its own scope; run once regardless of source set
#   skip    — handled by a dedicated cron (bdl/dbw via run_gus_bulk.sh)
ENGINE_MODE = {
    "web_scraper_extractor.py": "sources",
    "danegovpl_institution_extractor.py": "sources",
    "danegovpl_dataset_extractor.py": "sources",
    "intl_extractor.py": "sources",
    "pl_api_extractor.py": "sources",
    "wfs_extractor.py": "sources",
    "uzp_extractor.py": "single",
    "krs_extractor.py": "single",
    "danegovpl_harvester.py": "skip",  # whole-portal sweep — dedicated cron (run_danegovpl_harvest.sh)
    "run_incremental.py": "skip",   # owned by run_daily.sh (22:00 nightly + dbt)
    "run_bulk.py": "single",
    "universal_bulk_downloader.py": "single",
    "kpp_institution_registry.py": "single",
    "bdl_extractor.py": "skip",
    "dbw_extractor.py": "skip",
}
ENGINE_PATH = {
    "run_incremental.py": REPO / "products/ingestion/incremental/run_incremental.py",
    "run_bulk.py": REPO / "products/ingestion/bulk/run_bulk.py",
    "universal_bulk_downloader.py": REPO / "products/ingestion/universal_bulk_downloader.py",
    "kpp_institution_registry.py": REPO / "infra/scheduler/kpp_institution_registry.py",
}


# Per-engine wall-clock budget (seconds). Bounded so one slow/hung engine cannot
# stall the whole cadence (a single source must never block the other ~200).
DEFAULT_ENGINE_TIMEOUT = 2700          # 45 min
ENGINE_TIMEOUT = {
    "web_scraper_extractor.py": 5400,            # ~148 sources in one batch
    "danegovpl_institution_extractor.py": 3600,  # ~29 institutions
    "universal_bulk_downloader.py": 3600,
}


def engine_path(eng: str) -> Path:
    return ENGINE_PATH.get(eng, EXTRACTORS / eng)


def run(cmd, dry, timeout=DEFAULT_ENGINE_TIMEOUT) -> int:
    log.info(("DRY " if dry else "RUN ") + " ".join(str(c) for c in cmd))
    if dry:
        return 0
    env = dict(os.environ, PYTHONPATH=str(REPO))
    t0 = time.monotonic()
    try:
        proc = subprocess.run([sys.executable, *map(str, cmd)], env=env,
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        log.warning(f"    TIMEOUT after {timeout}s — killed, continuing to next engine")
        return 124
    except Exception as e:                         # never let one engine crash the cadence
        log.error(f"    ERROR launching engine: {e}")
        return 1
    for line in (proc.stdout + proc.stderr).strip().splitlines()[-3:]:
        log.info(f"    {line}")
    log.info(f"    exit={proc.returncode} ({time.monotonic()-t0:.0f}s)")
    return proc.returncode


def main(cadence, dry, only) -> int:
    sched = yaml.safe_load(SCHEDULE.read_text())["entries"]
    due = [e for e in sched if e["cadence"] == cadence]
    by_engine = {}
    for e in due:
        by_engine.setdefault(e["engine"], []).append(e["source_key"])

    log.info(f"=== ingestion: cadence={cadence}, {len(due)} sources, "
             f"{len(by_engine)} engines ===")
    worst = 0
    for eng, keys in sorted(by_engine.items()):
        if only and eng != only:
            continue
        mode = ENGINE_MODE.get(eng, "sources")
        path = engine_path(eng)
        if mode == "skip":
            log.info(f"[{eng}] {len(keys)} sources — handled by dedicated cron, skipping")
            continue
        if not path.exists():
            log.warning(f"[{eng}] not found at {path}, skipping")
            continue
        timeout = ENGINE_TIMEOUT.get(eng, DEFAULT_ENGINE_TIMEOUT)
        if mode == "single":
            log.info(f"[{eng}] single-run ({len(keys)} sources in scope)")
            rc = run([path], dry, timeout)
        else:  # sources
            log.info(f"[{eng}] {len(keys)} sources: {','.join(keys)}")
            rc = run([path, "--sources", *keys], dry, timeout)
        worst = worst or rc
    log.info(f"=== done (cadence={cadence}, worst exit={worst}) ===")
    return worst


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Ingestion orchestrator")
    p.add_argument("--cadence", required=True,
                   choices=["nightly", "weekly", "monthly", "continuous"])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--only", help="restrict to one engine basename")
    a = p.parse_args()
    sys.exit(main(a.cadence, a.dry_run, a.only))
