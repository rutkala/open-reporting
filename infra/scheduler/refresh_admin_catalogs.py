#!/usr/bin/env python3
"""
refresh_admin_catalogs.py — Regenerate all admin portal JSON data files.

Runs in sequence:
  1. generate_landing_status.py   → infra/nginx/html/data/landing_status.json
  2. generate_duckdb_catalog.py   → infra/nginx/html/data/duckdb_catalog.json
  3. generate_source_registry.py  → infra/nginx/html/data/source_registry.json
  4. generate_ingestion_plan.py   → infra/nginx/html/data/ingestion_plan.json
                                    infra/nginx/html/data/ingestion_capacity.json

Usage:
    python3 infra/scheduler/refresh_admin_catalogs.py
    python3 infra/scheduler/refresh_admin_catalogs.py --skip landing
"""
import argparse
import importlib.util
import logging
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

SCHED_DIR = Path(__file__).parent
REPO = SCHED_DIR.parents[1]

STEPS = [
    ("landing",   SCHED_DIR / "generate_landing_status.py"),
    ("duckdb",    SCHED_DIR / "generate_duckdb_catalog.py"),
    ("registry",  SCHED_DIR / "generate_source_registry.py"),
    ("plan",      SCHED_DIR / "generate_ingestion_plan.py"),
]


def run_script(name: str, path: Path) -> bool:
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return True
    except SystemExit as e:
        if e.code and e.code != 0:
            log.error(f"{name}: exited with code {e.code}")
            return False
        return True
    except Exception as e:
        log.error(f"{name}: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip", nargs="*", default=[], metavar="STEP",
                        help="Steps to skip: landing, duckdb, registry, plan")
    args = parser.parse_args()
    skip = set(args.skip or [])

    sys.path.insert(0, str(SCHED_DIR))

    failed = []
    for name, path in STEPS:
        if name in skip:
            log.info(f"skip: {name}")
            continue
        t0 = time.monotonic()
        ok = run_script(name, path)
        elapsed = time.monotonic() - t0
        if ok:
            log.info(f"ok: {name} ({elapsed:.1f}s)")
        else:
            failed.append(name)

    if failed:
        log.error(f"Failed steps: {', '.join(failed)}")
        return 1
    log.info("All catalog refresh steps complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
