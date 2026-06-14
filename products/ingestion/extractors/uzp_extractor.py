#!/usr/bin/env python3
"""
UZP — public procurement (Biuletyn Zamówień Publicznych) extractor.

Pulls all procurement notices from the BZP API on the e-Zamówienia platform.
The API requires a notice type + a publication date window; we iterate notice
types over monthly windows and page through each.

Output: data/landing/uzp_bzp/{notice_type}/{YYYY-MM}.json
(OR_LANDING_DIR env overrides the base, for testing while the mount is down).

Usage:
    python3 uzp_extractor.py                          # default: last 3 months
    python3 uzp_extractor.py --from 2022-01 --to 2026-06
    python3 uzp_extractor.py --types ContractNotice
"""
import argparse
import json
import logging
import os
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO = Path("/opt/open-reporting")
BASE = "https://ezamowienia.gov.pl/mo-board/api/v1/notice"
LANDING = Path(os.environ.get("OR_LANDING_DIR", str(REPO / "data/landing"))) / "uzp_bzp"
HEADERS = {"Accept": "application/json", "User-Agent": "OpenReporting-DataPipeline/1.0"}
PAGE_SIZE = 100
NOTICE_TYPES = ["ContractNotice", "ContractAwardNotice", "ContractModificationNotice"]


def _months(frm: str, to: str):
    y, m = map(int, frm.split("-"))
    ey, em = map(int, to.split("-"))
    while (y, m) <= (ey, em):
        last = (date(y + (m // 12), (m % 12) + 1, 1) - date.resolution).day
        yield f"{y:04d}-{m:02d}-01", f"{y:04d}-{m:02d}-{last:02d}"
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def _write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)


def fetch_window(session, ntype, d_from, d_to) -> list:
    rows, page = [], 0
    while True:
        params = {"PageSize": PAGE_SIZE, "Page": page, "NoticeType": ntype,
                  "PublicationDateFrom": d_from, "PublicationDateTo": d_to}
        r = session.get(BASE, params=params, headers=HEADERS, timeout=60)
        if r.status_code == 400:
            logger.warning(f"  {ntype} {d_from}: 400 {r.text[:120]}")
            break
        r.raise_for_status()
        batch = r.json()
        if not isinstance(batch, list) or not batch:
            break
        rows.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
        page += 1
        time.sleep(0.2)
    return rows


def main(frm, to, types, dry_run) -> int:
    session = requests.Session()
    total = 0
    for ntype in types:
        for d_from, d_to in _months(frm, to):
            ym = d_from[:7]
            if dry_run:
                logger.info(f"[uzp] would fetch {ntype} {ym}")
                continue
            rows = fetch_window(session, ntype, d_from, d_to)
            if rows:
                _write(LANDING / ntype / f"{ym}.json",
                       {"_meta": {"source": "uzp_bzp", "notice_type": ntype, "month": ym,
                                  "fetched_at": datetime.now(timezone.utc).isoformat(),
                                  "count": len(rows)}, "notices": rows})
                logger.info(f"[uzp] {ntype} {ym}: {len(rows)} notices")
                total += len(rows)
    logger.info(f"[uzp] done — {total} notices → {LANDING}")
    return 0


if __name__ == "__main__":
    today = date.today()
    default_from = f"{today.year - (1 if today.month <= 3 else 0):04d}-{(today.month - 3) % 12 + 1:02d}"
    p = argparse.ArgumentParser(description="UZP BZP procurement extractor")
    p.add_argument("--from", dest="frm", default=default_from, help="YYYY-MM")
    p.add_argument("--to", default=f"{today.year:04d}-{today.month:02d}", help="YYYY-MM")
    p.add_argument("--types", nargs="*", default=NOTICE_TYPES)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    sys.exit(main(a.frm, a.to, a.types, a.dry_run))
