#!/usr/bin/env python3
"""
Polish JSON-REST extractor (config-driven).

Pulls simple and hierarchical Polish public-API sources defined in
products/ingestion/registry/pl_api_sources.yaml. Modes:

  flat  — fetch each endpoint, save one JSON per endpoint (e.g. IMGW synop/hydro).
  sejm  — parliamentary hierarchy: per term pull MPs/clubs/committees/proceedings,
          then votings per proceeding sitting.

Output dir defaults to data/landing/{source_key}/ but can be overridden with the
OR_LANDING_DIR env var (used for testing while the landing mount is unavailable).

Usage:
    python3 pl_api_extractor.py                       # all configured sources
    python3 pl_api_extractor.py --sources imgw_api
    OR_LANDING_DIR=/tmp/land python3 pl_api_extractor.py --sources sejm_api
"""
import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO = Path("/opt/open-reporting")
CONFIG = REPO / "products/ingestion/registry/pl_api_sources.yaml"
LANDING_BASE = Path(os.environ.get("OR_LANDING_DIR", str(REPO / "data/landing")))
HEADERS = {"Accept": "application/json", "User-Agent": "OpenReporting-DataPipeline/1.0"}
TIMEOUT = 60


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write(path: Path, data) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)
    return len(data) if isinstance(data, list) else 1


def _get(session, url, **kw):
    r = session.get(url, headers=HEADERS, timeout=TIMEOUT, **kw)
    r.raise_for_status()
    return r.json()


def fetch_flat(session, key, cfg) -> int:
    base, land = cfg["base"], LANDING_BASE / key
    total = 0
    for ep in cfg["endpoints"]:
        data = _get(session, f"{base}/{ep['path']}")
        n = _write(land / f"{ep['name']}.json", data)
        logger.info(f"[{key}] {ep['name']}: {n} records")
        total += n
        time.sleep(0.3)
    return total


def fetch_sejm(session, key, cfg) -> int:
    base, land = cfg["base"], LANDING_BASE / key
    total = 0
    for term in cfg.get("terms", [10]):
        for coll in cfg.get("collections", []):
            try:
                data = _get(session, f"{base}/term{term}/{coll}")
            except requests.HTTPError as e:
                logger.warning(f"[{key}] term{term}/{coll}: {e}")
                continue
            n = _write(land / f"term{term}" / f"{coll}.json", data)
            logger.info(f"[{key}] term{term}/{coll}: {n} records")
            total += n
            time.sleep(0.3)
        if cfg.get("votings"):
            # proceedings → sittings → votings per sitting day
            try:
                procs = _get(session, f"{base}/term{term}/proceedings")
            except requests.HTTPError:
                procs = []
            sittings = sorted({p.get("number") for p in procs if p.get("number")})
            vtotal = 0
            for s in sittings:
                try:
                    v = _get(session, f"{base}/term{term}/votings/{s}")
                except requests.HTTPError:
                    continue
                if v:
                    _write(land / f"term{term}" / "votings" / f"sitting_{s}.json", v)
                    vtotal += len(v)
                time.sleep(0.2)
            logger.info(f"[{key}] term{term}/votings: {vtotal} across {len(sittings)} sittings")
            total += vtotal
    return total


def main(sources, dry_run) -> int:
    cfg_all = yaml.safe_load(CONFIG.read_text())["sources"]
    todo = sources or list(cfg_all)
    session = requests.Session()
    worst = 0
    for key in todo:
        if key not in cfg_all:
            logger.warning(f"unknown source {key}")
            continue
        cfg = cfg_all[key]
        if dry_run:
            logger.info(f"[{key}] mode={cfg['mode']} — would pull {cfg.get('base')}")
            continue
        try:
            n = {"flat": fetch_flat, "sejm": fetch_sejm}[cfg["mode"]](session, key, cfg)
            logger.info(f"[{key}] done — {n} records → {LANDING_BASE / key}")
        except Exception as e:
            logger.error(f"[{key}] FAILED: {e}")
            worst = 1
    return worst


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Polish JSON-REST extractor")
    p.add_argument("--sources", nargs="*", default=None)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(args.sources, args.dry_run))
