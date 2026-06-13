#!/usr/bin/env python3
"""
International (category-d) extractor.

Config-driven puller for the international comparator sources. Reads
products/ingestion/registry/intl_indicators.yaml and fetches a curated set of
indicators per source (Poland + EU/CEE comparators), writing one JSON envelope
per indicator/series into data/landing/{source_key}/.

Supported source kinds:
  worldbank      — World Bank v2 REST (JSON), one call per indicator, all comparators
  imf_datamapper — IMF DataMapper API (WEO), one call per indicator, all countries
  ecb_sdmx       — ECB Data Portal SDMX (CSV), one call per series key

These are public, generous-quota APIs — one run pulls full history; re-running
refreshes. No API key required.

Usage:
    python3 intl_extractor.py                  # all configured sources
    python3 intl_extractor.py --sources worldbank_wdi ecb_sdw
    python3 intl_extractor.py --dry-run
"""
import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO = Path("/opt/open-reporting")
CONFIG = REPO / "products/ingestion/registry/intl_indicators.yaml"
LANDING = REPO / "data/landing"
HEADERS = {"User-Agent": "OpenReporting-DataPipeline/1.0 (open-reporting.dev)",
           "Accept": "application/json"}
TIMEOUT = 60


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    if isinstance(data, (dict, list)):
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        tmp.write_text(data)
    tmp.replace(path)


def _envelope(source_key: str, endpoint: str, ident: str, label: str, payload) -> dict:
    return {
        "_meta": {"source": source_key, "endpoint": endpoint, "id": ident,
                  "label": label, "fetched_at": _now()},
        "data": payload,
    }


def fetch_worldbank(session, source_key, cfg, comparators, dry_run) -> int:
    base = cfg["base"]
    countries = ";".join(comparators)
    n = 0
    for code, label in cfg["indicators"].items():
        dest = LANDING / source_key / f"{code}.json"
        if dry_run:
            logger.info(f"[{source_key}] would fetch {code} ({label})")
            n += 1
            continue
        url = f"{base}/country/{countries}/indicator/{code}"
        rows, page = [], 1
        while True:
            r = session.get(url, params={"format": "json", "per_page": 1000, "page": page},
                            headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            body = r.json()
            if not isinstance(body, list) or len(body) < 2 or body[1] is None:
                break
            rows.extend(body[1])
            meta = body[0]
            if page >= int(meta.get("pages", 1)):
                break
            page += 1
        _atomic_write(dest, _envelope(source_key, f"/country/.../indicator/{code}", code, label, rows))
        logger.info(f"[{source_key}] {code}: {len(rows)} obs ({label})")
        n += 1
        time.sleep(0.2)
    return n


def fetch_imf_datamapper(session, source_key, cfg, comparators, dry_run) -> int:
    base = cfg["base"]
    countries = "/".join(comparators)
    n = 0
    for code, label in cfg["indicators"].items():
        dest = LANDING / source_key / f"{code}.json"
        if dry_run:
            logger.info(f"[{source_key}] would fetch {code} ({label})")
            n += 1
            continue
        url = f"{base}/{code}/{countries}"
        r = session.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        body = r.json()
        values = body.get("values", {}).get(code, {})
        _atomic_write(dest, _envelope(source_key, f"/{code}/{{countries}}", code, label, values))
        ncty = len(values)
        logger.info(f"[{source_key}] {code}: {ncty} countries ({label})")
        n += 1
        time.sleep(0.3)
    return n


def fetch_ecb_sdmx(session, source_key, cfg, dry_run) -> int:
    base = cfg["base"]
    n = 0
    for key, label in cfg["series"].items():
        flow = key.split(".", 1)[0]
        skey = key.split(".", 1)[1]
        dest = LANDING / source_key / f"{key.replace('.', '_')}.csv"
        if dry_run:
            logger.info(f"[{source_key}] would fetch {key} ({label})")
            n += 1
            continue
        url = f"{base}/{flow}/{skey}"
        r = session.get(url, params={"format": "csvdata"},
                        headers={**HEADERS, "Accept": "text/csv"}, timeout=TIMEOUT)
        if r.status_code == 404:
            logger.warning(f"[{source_key}] {key}: 404 — series key not found, skipping")
            continue
        r.raise_for_status()
        _atomic_write(dest, r.text)
        nlines = max(0, r.text.count("\n") - 1)
        logger.info(f"[{source_key}] {key}: {nlines} obs ({label})")
        n += 1
        time.sleep(0.3)
    return n


def main(sources: list[str] | None, dry_run: bool) -> int:
    cfg_all = yaml.safe_load(CONFIG.read_text())
    comparators = cfg_all["comparators"]
    src_cfg = cfg_all["sources"]
    todo = sources or list(src_cfg)

    session = requests.Session()
    worst = 0
    for sk in todo:
        if sk not in src_cfg:
            logger.warning(f"unknown source {sk}, skipping")
            continue
        cfg = src_cfg[sk]
        kind = cfg["kind"]
        try:
            if kind == "worldbank":
                cnt = fetch_worldbank(session, sk, cfg, comparators, dry_run)
            elif kind == "imf_datamapper":
                cnt = fetch_imf_datamapper(session, sk, cfg, comparators, dry_run)
            elif kind == "ecb_sdmx":
                cnt = fetch_ecb_sdmx(session, sk, cfg, dry_run)
            else:
                logger.error(f"[{sk}] unknown kind {kind}")
                worst = 1
                continue
            logger.info(f"[{sk}] done — {cnt} indicators/series{'(dry-run)' if dry_run else ''}")
        except Exception as e:
            logger.error(f"[{sk}] FAILED: {e}")
            worst = 1
    return worst


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="International comparator extractor")
    p.add_argument("--sources", nargs="*", default=None,
                   help="Subset of source keys (default: all configured)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(args.sources, args.dry_run))
