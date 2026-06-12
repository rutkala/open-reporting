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
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

SCHED_DIR = Path(__file__).parent
REPO = SCHED_DIR.parents[1]

# (name, script, timeout_s) — landing scans ~50k files over the rclone FUSE
# mount and can take >30 min when the cache is cold
STEPS = [
    ("landing",   SCHED_DIR / "generate_landing_status.py", 3300),
    ("duckdb",    SCHED_DIR / "generate_duckdb_catalog.py", 600),
    ("registry",  SCHED_DIR / "generate_source_registry.py", 600),
    ("plan",      SCHED_DIR / "generate_ingestion_plan.py", 600),
]


def run_script(name: str, path: Path, timeout_s: int) -> bool:
    # Subprocess (not importlib): the generators do their work under
    # `if __name__ == "__main__":`, which never fires for an imported module.
    env = dict(os.environ, PYTHONPATH=str(REPO))
    try:
        proc = subprocess.run(
            [sys.executable, str(path)],
            env=env, capture_output=True, text=True, timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        log.error(f"{name}: timed out after {timeout_s}s")
        return False
    for line in (proc.stdout + proc.stderr).splitlines():
        log.info(f"  {name}: {line}")
    if proc.returncode != 0:
        log.error(f"{name}: exited with code {proc.returncode}")
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip", nargs="*", default=[], metavar="STEP",
                        help="Steps to skip: landing, duckdb, registry, plan")
    args = parser.parse_args()
    skip = set(args.skip or [])

    sys.path.insert(0, str(SCHED_DIR))

    failed = []
    for name, path, timeout_s in STEPS:
        if name in skip:
            log.info(f"skip: {name}")
            continue
        t0 = time.monotonic()
        ok = run_script(name, path, timeout_s)
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
