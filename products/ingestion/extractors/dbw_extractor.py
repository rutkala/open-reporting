#!/usr/bin/env python3
"""
GUS DBW (Dziedzinowe Bazy Wiedzy) extractor — API 1.2.0.

Pulls time-series data for ~1,518 variables via api-dbw.stat.gov.pl/api/1.2.0.
Spec: https://api-dbw.stat.gov.pl/apidocs/ (auth header X-ClientId; registered
key = 50,000 req/7d, 5,000 req/12h, 500 req/15min).

Flow:
  1. /variable/variable-section-periods (paged) — catalog of every valid
     (id-zmienna, id-przekroj, id-okres) combination. Cached in _catalog.json.
  2. /variable/variable-meta per variable — przekroje with szereg-czasowy
     ("2006 - 2024") giving exact year coverage. Cached per variable.
  3. /variable/variable-data-section per (zmienna, przekroj, rok, okres) —
     all four params required by the API. One file per (variable, przekroj, rok).

Writes to data/landing/gus_dbw_api/variables/{id}/{przekroj}_{rok}.json.

Usage:
    python3 dbw_extractor.py                       # all variables
    python3 dbw_extractor.py --variables 814,815   # specific variables
    python3 dbw_extractor.py --dry-run             # estimate requests, no fetch
    python3 dbw_extractor.py --max-requests 4500   # per-run cap (12h quota is 5,000)
    python3 dbw_extractor.py --force               # re-fetch everything
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(override=True)
sys.path.insert(0, str(Path(__file__).parents[3]))

from products.ingestion.extractors.gus_ratelimit import (
    BudgetExhausted, FetchAbort, FetchSkip, WeeklyRateLimiter, get_json,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE = "https://api-dbw.stat.gov.pl/api/1.2.0"
LANDING = Path("/opt/open-reporting/data/landing/gus_dbw_api")
CATALOG_PATH = LANDING / "_catalog.json"
MANIFEST_PATH = LANDING / "_manifest.json"
RATELIMIT_PATH = LANDING / "_ratelimit.json"

WEEKLY_CAP = 50_000      # registered key, confirmed via X-Rate-Limit-Remaining
MIN_INTERVAL_S = 1.9     # ≤474 req/15min — under the 500/15min burst cap
PAGE_SIZE = 5000
MIN_YEAR = 1995          # clamp szereg-czasowy lower bound


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        try:
            m = json.loads(MANIFEST_PATH.read_text())
            if m.get("version") == 2:
                return m
            logger.info("[dbw] v1 manifest found (old extractor) — starting fresh v2")
        except Exception:
            pass
    return {"version": 2, "variables": {}}


def save_manifest(manifest: dict) -> None:
    _atomic_write(MANIFEST_PATH, manifest)


def fetch_catalog(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    force: bool = False,
) -> list[dict]:
    """Full (zmienna, przekroj, okres) catalog from variable-section-periods."""
    if CATALOG_PATH.exists() and not force:
        return json.loads(CATALOG_PATH.read_text())["rows"]

    rows: list[dict] = []
    page = 0
    while True:
        data = get_json(
            session, f"{BASE}/variable/variable-section-periods",
            {"ile-na-stronie": PAGE_SIZE, "numer-strony": page, "lang": "pl"},
            limiter,
        )
        rows.extend(data.get("data", []))
        page += 1
        if page >= int(data.get("page-count", 1)):
            break

    _atomic_write(CATALOG_PATH, {
        "_meta": {"source": "gus_dbw_api", "endpoint": "/variable/variable-section-periods",
                  "fetched_at": _now(), "total_rows": len(rows)},
        "rows": rows,
    })
    logger.info(f"[dbw] catalog: {len(rows)} (variable, przekroj, okres) combinations")
    return rows


def parse_year_range(szereg: str) -> tuple[int, int] | None:
    """'2006 - 2024' → (2006, 2024). Single year '2020' → (2020, 2020)."""
    if not szereg:
        return None
    years = re.findall(r"\d{4}", szereg)
    if not years:
        return None
    lo, hi = int(years[0]), int(years[-1])
    return (max(lo, MIN_YEAR), hi)


def fetch_meta(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    var_id: int,
    force: bool = False,
) -> dict:
    """Fetch variable-meta. Returns {przekroj_id: (year_lo, year_hi)}. Cached on disk."""
    cache = LANDING / "variables" / str(var_id) / "_meta.json"
    if cache.exists() and not force:
        meta = json.loads(cache.read_text())
    else:
        # First call for a variable can be slow server-side — generous timeout
        data = get_json(
            session, f"{BASE}/variable/variable-meta",
            {"id-zmiennej": var_id, "lang": "pl"},
            limiter, timeout_s=120,
        )
        meta = data[0] if isinstance(data, list) and data else data
        if not isinstance(meta, dict):
            raise FetchSkip(f"variable-meta for {var_id}: unexpected shape")
        meta["_meta"] = {"source": "gus_dbw_api", "endpoint": "/variable/variable-meta",
                         "fetched_at": _now()}
        _atomic_write(cache, meta)

    ranges: dict[str, tuple[int, int]] = {}
    for prz in meta.get("przekroje", []):
        rng = parse_year_range(prz.get("szereg-czasowy", ""))
        if rng:
            # Same przekroj can appear per-frequency with different ranges — merge
            key = str(prz.get("id-przekroj"))
            old = ranges.get(key)
            ranges[key] = (min(old[0], rng[0]), max(old[1], rng[1])) if old else rng
    return ranges


def fetch_year_data(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    var_id: int,
    przekroj_id: int,
    rok: int,
    okresy: list[int],
) -> int:
    """Pull all okres slices for one (variable, przekroj, year). Returns row count."""
    slices: dict[str, list] = {}
    total = 0
    for okres in okresy:
        rows: list[dict] = []
        page = 0
        while True:
            try:
                data = get_json(
                    session, f"{BASE}/variable/variable-data-section",
                    {"id-zmienna": var_id, "id-przekroj": przekroj_id,
                     "id-rok": rok, "id-okres": okres,
                     "ile-na-stronie": PAGE_SIZE, "numer-strony": page, "lang": "pl"},
                    limiter,
                )
            except FetchSkip:
                # 404 = no data for this (year, okres) slice — normal (e.g. future months)
                break
            rows.extend(data.get("data", []))
            page += 1
            if page >= int(data.get("page-count", 1)):
                break
        if rows:
            slices[str(okres)] = rows
            total += len(rows)

    if slices:
        dest = LANDING / "variables" / str(var_id) / f"{przekroj_id}_{rok}.json"
        _atomic_write(dest, {
            "_meta": {"source": "gus_dbw_api", "endpoint": "/variable/variable-data-section",
                      "variable_id": var_id, "przekroj_id": przekroj_id, "rok": rok,
                      "okresy": okresy, "fetched_at": _now(), "total_records": total},
            "slices": slices,
        })
    return total


def _var_state(manifest: dict, var_id: int) -> dict:
    key = str(var_id)
    if key not in manifest["variables"]:
        manifest["variables"][key] = {
            "name": "", "meta_done": False, "przekroje": {}, "last_updated": "",
        }
    return manifest["variables"][key]


def main(
    variables: list[int] | None = None,
    force: bool = False,
    max_requests: int | None = 4500,
    dry_run: bool = False,
) -> int:
    api_key = os.environ.get("DBW_API_KEY")
    if not api_key:
        logger.error("DBW_API_KEY not set")
        return 2

    LANDING.mkdir(parents=True, exist_ok=True)
    limiter = WeeklyRateLimiter("dbw", WEEKLY_CAP, RATELIMIT_PATH,
                                min_interval_s=MIN_INTERVAL_S, reserve=500)
    session = requests.Session()
    session.headers.update({
        "X-ClientId": api_key,
        "User-Agent": "OpenReporting-DataPipeline/1.0 (open-reporting.dev)",
        "Accept": "application/json",
    })
    manifest = load_manifest()

    try:
        catalog = fetch_catalog(session, limiter, force)

        # Group: var_id -> przekroj_id -> [okres, ...]
        combos: dict[int, dict[int, list[int]]] = {}
        names: dict[int, str] = {}
        for row in catalog:
            vid = int(row["id-zmienna"])
            pid = int(row["id-przekroj"])
            combos.setdefault(vid, {}).setdefault(pid, []).append(int(row["id-okres"]))
            names[vid] = row.get("nazwa-zmienna", "")

        todo_vars = sorted(combos) if not variables else [v for v in variables if v in combos]
        if variables:
            missing = [v for v in variables if v not in combos]
            if missing:
                logger.warning(f"[dbw] not in catalog, skipping: {missing}")
        logger.info(f"[dbw] {len(todo_vars)} variables to process")

        if dry_run:
            est = 0
            for vid in todo_vars:
                state = manifest["variables"].get(str(vid), {})
                if not state.get("meta_done"):
                    est += 1  # meta call; year counts unknown until meta — rough lower bound
                for pid, okresy in combos[vid].items():
                    pstate = state.get("przekroje", {}).get(str(pid), {})
                    done_years = set(pstate.get("years_done", []))
                    rng = pstate.get("year_range")
                    n_years = (rng[1] - rng[0] + 1 - len(done_years)) if rng else 10
                    est += max(0, n_years) * len(okresy)
            logger.info(f"[dbw] DRY RUN: ~{est} requests estimated "
                        f"(remaining this week: {limiter.remaining})")
            return 0

        pulled = skipped = 0
        for vid in todo_vars:
            if max_requests and limiter.used_this_run >= max_requests:
                raise BudgetExhausted(f"per-run cap of {max_requests} reached")

            state = _var_state(manifest, vid)
            state["name"] = names.get(vid, state["name"])

            # Year coverage per przekroj from variable-meta
            try:
                ranges = fetch_meta(session, limiter, vid, force)
                state["meta_done"] = True
            except FetchSkip as e:
                logger.warning(f"[dbw] Skip var {vid} (meta failed): {e}")
                state["meta_failed"] = str(e)
                save_manifest(manifest)
                continue

            current_year = datetime.now(timezone.utc).year
            for pid, okresy in sorted(combos[vid].items()):
                pkey = str(pid)
                if pkey not in state["przekroje"]:
                    state["przekroje"][pkey] = {"years_done": [], "year_range": None}
                pstate = state["przekroje"][pkey]

                rng = ranges.get(pkey)
                if rng is None:
                    # In section-periods catalog but not in meta przekroje — try
                    # a recent window rather than skipping silently
                    rng = (current_year - 5, current_year)
                pstate["year_range"] = list(rng)

                done_years = set(pstate["years_done"]) if not force else set()
                for rok in range(rng[0], min(rng[1], current_year) + 1):
                    if rok in done_years:
                        skipped += 1
                        continue
                    if max_requests and limiter.used_this_run >= max_requests:
                        raise BudgetExhausted(f"per-run cap of {max_requests} reached")
                    rows = fetch_year_data(session, limiter, vid, pid, rok, okresy)
                    pstate["years_done"].append(rok)
                    pulled += 1
                    if pulled % 25 == 0:
                        logger.info(f"[dbw] {pulled} (var,przekroj,rok) slices done, "
                                    f"{limiter.remaining} req remaining (var {vid})")
                state["last_updated"] = _now()
                save_manifest(manifest)

        logger.info(f"[dbw] Done. {pulled} slices pulled, {skipped} skipped. "
                    f"Requests this run: {limiter.used_this_run}")

    except BudgetExhausted as e:
        logger.info(f"[dbw] Budget stop: {e} — manifest saved, resume next run")
        save_manifest(manifest)
        return 0
    except FetchAbort as e:
        logger.error(f"[dbw] Abort: {e}")
        save_manifest(manifest)
        return 2

    save_manifest(manifest)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GUS DBW extractor (API 1.2.0)")
    parser.add_argument("--variables", default="",
                        help="Comma-separated variable IDs (default: all in catalog)")
    parser.add_argument("--force", action="store_true", help="Re-fetch everything")
    parser.add_argument("--max-requests", type=int, default=4500,
                        help="Per-run cap; API allows 5,000 per 12h")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    var_list = [int(v.strip()) for v in args.variables.split(",") if v.strip()] or None
    sys.exit(main(
        variables=var_list,
        force=args.force,
        max_requests=args.max_requests,
        dry_run=args.dry_run,
    ))
