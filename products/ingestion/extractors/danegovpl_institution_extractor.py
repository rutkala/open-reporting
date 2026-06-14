#!/usr/bin/env python3
"""
dane.gov.pl by-institution extractor (config-driven).

For sources whose data is an institution's catalogue on dane.gov.pl, pulls every
dataset + resource for that institution by its (verified) portal institution id.
One engine for the whole set of dane.gov.pl-published institutions.

This replaces the old per-institution pulls that used WRONG ids (NFZ was 31,
should be 32; ZUS 47→20; URE 58→107; MEN 15→165; GDDKiA 106→55; MF 18→13).

Config: products/ingestion/registry/danegovpl_institutions.yaml
Output: data/landing/{source_key}/{dataset_id}/{resource_id}.{ext}
(OR_LANDING_DIR overrides base.)

Usage:
    python3 danegovpl_institution_extractor.py                  # all configured
    python3 danegovpl_institution_extractor.py --sources nfz_bulk
    python3 danegovpl_institution_extractor.py --list
"""
import argparse
import logging
import os
import sys
import time
from pathlib import Path

import requests
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO = Path("/opt/open-reporting")
CONFIG = REPO / "products/ingestion/registry/danegovpl_institutions.yaml"
LANDING = Path(os.environ.get("OR_LANDING_DIR", str(REPO / "data/landing")))
API = "https://api.dane.gov.pl/1.4"
HEADERS = {"Accept": "application/json", "User-Agent": "OpenReporting-DataPipeline/1.0"}


def institution_datasets(session, inst_id) -> list[str]:
    out, page = [], 1
    while True:
        r = session.get(f"{API}/institutions/{inst_id}/datasets",
                        params={"per_page": 100, "page": page}, headers=HEADERS, timeout=60)
        r.raise_for_status()
        body = r.json()
        out.extend(d.get("id") for d in body.get("data", []))
        if len(out) >= body.get("meta", {}).get("count", 0):
            break
        page += 1
    return out


def dataset_resources(session, ds_id) -> list[dict]:
    out, page = [], 1
    while True:
        r = session.get(f"{API}/datasets/{ds_id}/resources",
                        params={"per_page": 100, "page": page}, headers=HEADERS, timeout=60)
        r.raise_for_status()
        body = r.json()
        for res in body.get("data", []):
            a = res.get("attributes", {})
            out.append({"id": res.get("id"), "format": (a.get("format") or "bin").lower()})
        if len(out) >= body.get("meta", {}).get("count", 0):
            break
        page += 1
    return out


def download(session, rid, dest: Path) -> bool:
    try:
        with session.get(f"https://api.dane.gov.pl/resources/{rid}/file",
                         headers=HEADERS, timeout=180, stream=True) as r:
            r.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            tmp = dest.with_suffix(dest.suffix + ".tmp")
            with open(tmp, "wb") as fh:
                for chunk in r.iter_content(65536):
                    fh.write(chunk)
            tmp.replace(dest)
        return True
    except Exception as e:
        logger.warning(f"  resource {rid}: {e}")
        return False


def main(sources, list_only) -> int:
    cfg = yaml.safe_load(CONFIG.read_text())["sources"]
    todo = sources or list(cfg)
    session = requests.Session()
    worst = 0
    for key in todo:
        if key not in cfg:
            logger.warning(f"unknown source {key}")
            continue
        inst_id = cfg[key]["institution_id"]
        try:
            datasets = institution_datasets(session, inst_id)
        except Exception as e:
            logger.error(f"[{key}] institution {inst_id}: {e}")
            worst = 1
            continue
        logger.info(f"[{key}] institution {inst_id}: {len(datasets)} datasets")
        if list_only:
            continue
        land, total = LANDING / key, 0
        for ds in datasets:
            for res in dataset_resources(session, ds):
                dest = land / str(ds) / f"{res['id']}.{res['format']}"
                if download(session, res["id"], dest):
                    total += 1
                time.sleep(0.1)
        logger.info(f"[{key}] done — {total} files → {land}")
    return worst


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="dane.gov.pl by-institution extractor")
    p.add_argument("--sources", nargs="*", default=None)
    p.add_argument("--list", action="store_true", dest="list_only")
    a = p.parse_args()
    sys.exit(main(a.sources, a.list_only))
