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
import shutil
import sys
import tempfile
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
# Defensive free-space floor. Full-scope BZP notices stream to a local tempfile and
# the landing JSON before dbt picks them up; on the shared 38G root this can drive the
# disk to zero and OSError(errno 28), which also threatens co-tenant services
# (postgres/ghost/nginx). Stop fetching further windows below this floor and exit
# cleanly with what we have — the next run resumes the remaining windows.
MIN_FREE_BYTES = 2 * 1024 ** 3  # 2 GiB


def _free_bytes(path: Path) -> int:
    """Free bytes on the filesystem backing `path` (walk up to an existing parent)."""
    p = path
    while not p.exists():
        p = p.parent
    return shutil.disk_usage(p).free


def _months(frm: str, to: str):
    y, m = map(int, frm.split("-"))
    ey, em = map(int, to.split("-"))
    while (y, m) <= (ey, em):
        last = (date(y + (m // 12), (m % 12) + 1, 1) - date.resolution).day
        yield f"{y:04d}-{m:02d}-01", f"{y:04d}-{m:02d}-{last:02d}"
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def _finalize_output(output_path: Path, tmp_notices_path: Path, ntype: str, ym: str, total_count: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_final_path = output_path.with_suffix(".tmp")

    with open(tmp_final_path, "w", encoding="utf-8") as outfile:
        # Write the initial part of the JSON with metadata
        meta = {
            "source": "uzp_bzp",
            "notice_type": ntype,
            "month": ym,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "count": total_count
        }
        # Write up to "notices": [
        outfile.write(json.dumps({"_meta": meta, "notices": []}, ensure_ascii=False, indent=2)[:-3])

        # Stream notices from the temporary file
        first_notice = True
        if tmp_notices_path.exists():
            with open(tmp_notices_path, "r", encoding="utf-8") as infile:
                for line in infile:
                    if not first_notice:
                        outfile.write(",\n")
                    outfile.write("  " + line.strip()) # Add indentation and write notice
                    first_notice = False
        
        # Close the "notices" array and the main object
        outfile.write("\n  ]\n}")
    
    tmp_final_path.replace(output_path)
    if tmp_notices_path.exists():
        os.remove(tmp_notices_path) # Clean up the temporary notices file


def fetch_window(session, ntype, d_from, d_to, tmp_notices_file) -> int:
    total_rows = 0
    page = 0
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
        for notice in batch:
            tmp_notices_file.write(json.dumps(notice, ensure_ascii=False) + "\n")
        total_rows += len(batch)
        if len(batch) < PAGE_SIZE:
            break
        page += 1
        time.sleep(0.2)
    return total_rows


def main(frm, to, types, dry_run) -> int:
    session = requests.Session()
    total = 0
    # Co-locate the intermediate notices stream with the final output. LANDING is on
    # the large Drive mount (~TB); the previous tempfile.TemporaryDirectory() default
    # placed the per-month stream under /tmp on the 38G root, where a single full-scope
    # ContractNotice month could exhaust the disk and OSError(errno 28). Streaming next
    # to the output keeps the big intermediate off the shared root entirely.
    if not dry_run:
        LANDING.mkdir(parents=True, exist_ok=True)
    tmp_base = str(LANDING)
    for ntype in types:
        for d_from, d_to in _months(frm, to):
            ym = d_from[:7]
            output_path = LANDING / ntype / f"{ym}.json"

            if dry_run:
                logger.info(f"[uzp] would fetch {ntype} {ym}")
                continue

            free = _free_bytes(LANDING)
            if free < MIN_FREE_BYTES:
                logger.warning(
                    f"[uzp] free disk {free / 1024 ** 3:.1f} GiB < "
                    f"{MIN_FREE_BYTES / 1024 ** 3:.1f} GiB floor on landing volume — "
                    f"stopping after {total} notices. Remaining windows resume next run."
                )
                logger.info(f"[uzp] done (partial, low disk) — {total} notices → {LANDING}")
                return 0

            # Stream notices to a temp dir on the LANDING volume (not /tmp on the root).
            with tempfile.TemporaryDirectory(dir=tmp_base) as tmpdir:
                tmp_notices_path = Path(tmpdir) / f"{ntype}_{ym}.notices.tmp"
                with open(tmp_notices_path, "w", encoding="utf-8") as tmp_notices_file:
                    total_rows = fetch_window(session, ntype, d_from, d_to, tmp_notices_file)

                if total_rows > 0:
                    _finalize_output(output_path, tmp_notices_path, ntype, ym, total_rows)
                    logger.info(f"[uzp] {ntype} {ym}: {total_rows} notices → {output_path}")
                    total += total_rows
                else:
                    logger.info(f"[uzp] {ntype} {ym}: no notices found.")

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
