#!/usr/bin/env python3
"""
dane.gov.pl whole-portal harvester (Layer 1).

Extracts EVERYTHING from Poland's national open-data portal — every dataset and
every downloadable resource, across all ~7,000 institutions — not limited to any
subset. This is the broad sweep; per-institution own-API sources (Layer 2) are
defined separately in the source registry.

Flow:
  1. Page /1.4/datasets (full catalogue) → one metadata record per dataset
  2. For each dataset, page its /resources → download every file
  3. Resumable manifest per dataset; polite pacing.

Writes to data/landing/dane_gov_pl/{dataset_id}/{resource_id}.{ext}
plus _catalogue.json (all dataset metadata) and _manifest.json (progress).

Usage:
    python3 danegovpl_harvester.py --catalogue-only     # just pull the dataset list
    python3 danegovpl_harvester.py                       # full harvest (needs landing mount)
    python3 danegovpl_harvester.py --max-datasets 50     # bounded test
"""
import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE = "https://api.dane.gov.pl/1.4"
LANDING = Path("/opt/open-reporting/data/landing/dane_gov_pl")
CATALOGUE = LANDING / "_catalogue.json"
MANIFEST = LANDING / "_manifest.json"
HEADERS = {"Accept": "application/json", "User-Agent": "OpenReporting-DataPipeline/1.0"}
PAGE = 100


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)


def fetch_catalogue(session: requests.Session, max_datasets: int | None) -> list[dict]:
    """Page the full dataset catalogue — id, title, institution, resource count."""
    out, page = [], 1
    while True:
        r = session.get(f"{BASE}/datasets", params={"per_page": PAGE, "page": page},
                        headers=HEADERS, timeout=60)
        r.raise_for_status()
        body = r.json()
        for d in body.get("data", []):
            a = d.get("attributes", {})
            rel = d.get("relationships", {})
            inst = rel.get("institution", {}).get("data", {}) or {}
            out.append({
                "id": d.get("id"),
                "title": a.get("title", ""),
                "notes": (a.get("notes", "") or "")[:300],
                "institution_id": inst.get("id"),
                "category": a.get("category", ""),
                "resources": rel.get("resources", {}).get("meta", {}).get("count", 0),
                "modified": a.get("modified", ""),
            })
        total = body.get("meta", {}).get("count", 0)
        logger.info(f"catalogue page {page}: {len(out)}/{total}")
        if len(out) >= total or (max_datasets and len(out) >= max_datasets):
            break
        page += 1
        time.sleep(0.2)
    if max_datasets:
        out = out[:max_datasets]
    _atomic(CATALOGUE, {"_meta": {"source": "dane_gov_pl", "fetched_at": _now(),
                                  "total_datasets": len(out)}, "datasets": out})
    logger.info(f"catalogue: {len(out)} datasets → {CATALOGUE}")
    return out


def harvest_resources(session, dataset_id: str, manifest: dict) -> int:
    """Download every resource file for one dataset. Returns files pulled."""
    done = set(manifest["datasets"].get(dataset_id, {}).get("resources_done", []))
    pulled, page = 0, 1
    while True:
        r = session.get(f"{BASE}/datasets/{dataset_id}/resources",
                        params={"per_page": PAGE, "page": page}, headers=HEADERS, timeout=60)
        if r.status_code != 200:
            break
        body = r.json()
        data = body.get("data", [])
        if not data:
            break
        for res in data:
            rid = res.get("id")
            if rid in done:
                continue
            a = res.get("attributes", {})
            ext = (a.get("format") or "bin").lower()
            url = f"{BASE.replace('/1.4','')}/resources/{rid}/file"
            dest = LANDING / dataset_id / f"{rid}.{ext}"
            try:
                with session.get(url, headers=HEADERS, timeout=180, stream=True) as fr:
                    fr.raise_for_status()
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    tmp = dest.with_suffix(dest.suffix + ".tmp")
                    with open(tmp, "wb") as fh:
                        for chunk in fr.iter_content(65536):
                            fh.write(chunk)
                    tmp.replace(dest)
                done.add(rid)
                pulled += 1
            except Exception as e:
                logger.warning(f"  dataset {dataset_id} resource {rid}: {e}")
            time.sleep(0.1)
        if len(data) < PAGE:
            break
        page += 1
    manifest["datasets"][dataset_id] = {"resources_done": sorted(done), "last": _now()}
    return pulled


def main(catalogue_only: bool, max_datasets: int | None) -> int:
    LANDING.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    catalogue = fetch_catalogue(session, max_datasets)
    if catalogue_only:
        logger.info("catalogue-only mode — done")
        return 0

    manifest = {"datasets": {}}
    if MANIFEST.exists():
        try:
            manifest = json.loads(MANIFEST.read_text())
        except Exception:
            pass
    manifest.setdefault("datasets", {})

    total_files = 0
    for i, d in enumerate(catalogue, 1):
        if d["resources"] == 0:
            continue
        total_files += harvest_resources(session, d["id"], manifest)
        if i % 25 == 0:
            _atomic(MANIFEST, manifest)
            logger.info(f"{i}/{len(catalogue)} datasets, {total_files} files pulled")
    _atomic(MANIFEST, manifest)
    logger.info(f"Done. {total_files} files across {len(catalogue)} datasets.")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="dane.gov.pl whole-portal harvester")
    p.add_argument("--catalogue-only", action="store_true")
    p.add_argument("--max-datasets", type=int, default=None)
    args = p.parse_args()
    sys.exit(main(args.catalogue_only, args.max_datasets))
