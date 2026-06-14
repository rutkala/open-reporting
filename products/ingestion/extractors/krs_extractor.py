#!/usr/bin/env python3
"""
KRS register-extract extractor (Krajowy Rejestr Sądowy open API).

Pulls the current register extract (OdpisAktualny) for a curated, bounded set of
entities from the sanctioned Ministry of Justice API (api-krs.ms.gov.pl — not the
Incapsula-protected document browser). The KRS API is per-entity lookup by KRS
number, not bulk-mirrorable, so we maintain an explicit target list
(registry/krs_targets.yaml) of high-value entities (state-owned + major listed
companies) and pull one register record per entity. Expand the target list freely.

NOTE: this is company *register* data (name, address, capital, board, PKD, status)
— NOT financial statements. The financial-statement documents (RDF) sit behind
anti-bot protection and have no free programmatic access (see decisions log).

Output: data/landing/krs_api/{krs}.json (OR_LANDING_DIR overrides).

Usage:
    python3 krs_extractor.py                       # all targets
    python3 krs_extractor.py --sources krs_api     # orchestrator passes this (ignored scope)
    python3 krs_extractor.py --targets /path/to/targets.yaml
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
TARGETS = REPO / "products/ingestion/registry/krs_targets.yaml"
LANDING = Path(os.environ.get("OR_LANDING_DIR", str(REPO / "data/landing"))) / "krs_api"
API = "https://api-krs.ms.gov.pl/api/krs/OdpisAktualny"
HEADERS = {"User-Agent": "OpenReporting-DataPipeline/1.0 (open-reporting.dev)",
           "Accept": "application/json"}
TIMEOUT = 40


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)


def _name_of(odpis: dict) -> str:
    try:
        return odpis["odpis"]["dane"]["dzial1"]["danePodmiotu"]["nazwa"]
    except (KeyError, TypeError):
        return "(name not found)"


def fetch_one(session, krs: str, rejestr: str) -> dict | None:
    r = session.get(f"{API}/{krs}", params={"rejestr": rejestr, "format": "json"},
                    headers=HEADERS, timeout=TIMEOUT)
    if r.status_code == 404:
        logger.warning(f"[krs] {krs}: 404 (rejestr={rejestr}) — not found, skipping")
        return None
    r.raise_for_status()
    if not r.text.strip():
        logger.warning(f"[krs] {krs}: empty response, skipping")
        return None
    return r.json()


def main(targets_path: Path, dry_run: bool) -> int:
    cfg = yaml.safe_load(targets_path.read_text())
    targets = cfg.get("targets", [])
    if not targets:
        logger.error(f"no targets in {targets_path}")
        return 2
    session = requests.Session()
    ok = fail = 0
    for t in targets:
        krs = str(t["krs"]).zfill(10)
        rejestr = t.get("rejestr", "P")
        if dry_run:
            logger.info(f"[krs] would fetch {krs} ({t.get('name','')}) rejestr={rejestr}")
            ok += 1
            continue
        try:
            payload = fetch_one(session, krs, rejestr)
            if payload is None:
                fail += 1
                continue
            doc = {"_meta": {"source": "krs_api", "krs": krs, "rejestr": rejestr,
                             "name": _name_of(payload), "fetched_at": _now()},
                   "data": payload}
            _atomic_write(LANDING / f"{krs}.json", doc)
            logger.info(f"[krs] {krs}: {_name_of(payload)} → {LANDING / f'{krs}.json'}")
            ok += 1
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"[krs] {krs}: FAILED — {e}")
            fail += 1
    logger.info(f"[krs] done — {ok} ok, {fail} failed of {len(targets)} targets")
    return 1 if fail and not ok else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="KRS register-extract extractor")
    p.add_argument("--sources", nargs="*", default=None, help="ignored (orchestrator compat)")
    p.add_argument("--targets", default=str(TARGETS))
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    sys.exit(main(Path(a.targets), a.dry_run))
