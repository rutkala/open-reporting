#!/usr/bin/env python3
"""
GUS DBW non-HVD extractor.

Pulls time-series data for all 1,547 indicators via api-dbw.stat.gov.pl/api/1.1.0.
Writes to data/landing/gus_dbw_api/{root_area_id}/{indicator_id}.json.

Usage:
    python3 dbw_extractor.py                     # all areas (727, 728, 729)
    python3 dbw_extractor.py --areas 727         # specific root area
    python3 dbw_extractor.py --dry-run           # estimate requests, no fetch
    python3 dbw_extractor.py --max-requests 8000
    python3 dbw_extractor.py --force             # re-fetch all indicators
"""

import argparse
import json
import logging
import os
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

BASE = "https://api-dbw.stat.gov.pl/api/1.1.0"
LANDING = Path("/opt/open-reporting/data/landing/gus_dbw_api")
AREA_TREE_PATH = LANDING / "area_tree.json"
MANIFEST_PATH = LANDING / "_manifest.json"
RATELIMIT_PATH = LANDING / "_ratelimit.json"

ROOT_AREAS = {727: "gospodarka", 728: "spoleczenstwo", 729: "srodowisko"}


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
            return json.loads(MANIFEST_PATH.read_text())
        except Exception:
            pass
    return {"version": 1, "indicators": {}}


def save_manifest(manifest: dict) -> None:
    _atomic_write(MANIFEST_PATH, manifest)


def load_area_tree() -> list[dict]:
    if not AREA_TREE_PATH.exists():
        raise FileNotFoundError(
            f"area_tree.json not found at {AREA_TREE_PATH}. "
            "Run bulk ingestion for gus_dbw_api first."
        )
    data = json.loads(AREA_TREE_PATH.read_text())
    # Unwrap envelope if present
    if isinstance(data, dict) and "results" in data:
        return data["results"]
    if isinstance(data, list):
        return data
    return []


def leaf_areas(tree: list[dict], root_id: int) -> list[dict]:
    """Return all areas under root_id where czy-zmienne is true (have indicators)."""
    index: dict[int, dict] = {int(n.get("id", 0)): n for n in tree}
    leaves = []

    def _walk(node_id: int) -> None:
        node = index.get(node_id)
        if not node:
            return
        if node.get("czy-zmienne"):
            leaves.append(node)
        # Find children (nodes whose id-nadrzedny-element == node_id)
        for n in tree:
            if int(n.get("id-nadrzedny-element", -1)) == node_id:
                _walk(int(n.get("id", 0)))

    _walk(root_id)
    return leaves


def discover_indicators(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    area_id: int,
    root_id: int,
    force: bool = False,
) -> list[dict]:
    """Fetch indicator list for a leaf area. Cached per area."""
    cache = LANDING / str(root_id) / f"_indicators_{area_id}.json"
    if cache.exists() and not force:
        data = json.loads(cache.read_text())
        return data.get("results", [])

    data = get_json(
        session, f"{BASE}/area/area-variable",
        {"id-obszaru": area_id, "lang": "pl"},
        limiter,
    )
    results = data if isinstance(data, list) else data.get("results", [])
    envelope = {
        "_meta": {
            "source": "gus_dbw_api", "endpoint": "/area/area-variable",
            "area_id": area_id, "root_area_id": root_id, "fetched_at": _now(),
        },
        "results": results,
    }
    _atomic_write(cache, envelope)
    return results


def fetch_sections(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    indicator_id: int,
) -> list[dict]:
    """Fetch available sections (przekroje) for an indicator.

    Note: endpoint uses id-zmiennej (not id-zmienna — that's the data endpoint).
    """
    data = get_json(
        session, f"{BASE}/variable/variable-section",
        {"id-zmiennej": indicator_id, "lang": "pl"},
        limiter,
    )
    return data if isinstance(data, list) else data.get("results", [])


def fetch_section_data(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    indicator_id: int,
    section_id: int,
) -> list[dict]:
    """Pull all pages for one indicator+section. Omit id-wymiar/id-pozycja = full pull."""
    rows: list[dict] = []
    page = 0
    while True:
        data = get_json(
            session, f"{BASE}/variable/variable-data-section",
            {
                "id-zmienna": indicator_id,   # NOTE: id-zmienna here (not id-zmiennej)
                "id-przekroj": section_id,
                "ile-na-stronie": 100,
                "numer-strony": page,
                "lang": "pl",
            },
            limiter,
        )
        page_rows = data if isinstance(data, list) else data.get("data", data.get("results", []))
        if not page_rows:
            break
        rows.extend(page_rows)
        page += 1
        # Stop when page returned fewer than full page (or on explicit total)
        total = data.get("total") or data.get("totalRecords") if isinstance(data, dict) else None
        if total is not None and page * 100 >= total:
            break
        if isinstance(page_rows, list) and len(page_rows) < 100:
            break
    return rows


def fetch_indicator_data(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    indicator: dict,
    root_id: int,
    manifest: dict,
    force: bool,
) -> int:
    """Pull all sections for one indicator. Returns total rows. Updates manifest in-place."""
    ind_id = int(indicator.get("id", indicator.get("id-zmienna", 0)))
    ind_key = str(ind_id)
    area_id = int(indicator.get("id-obszaru", 0))

    if ind_key not in manifest["indicators"]:
        manifest["indicators"][ind_key] = {
            "area_id": area_id, "root_area_id": root_id,
            "sections_total": [], "sections_done": [],
            "rows": 0, "failed": None, "last_updated": "",
        }
    state = manifest["indicators"][ind_key]

    # Discover sections
    if not state["sections_total"] or force:
        sections = fetch_sections(session, limiter, ind_id)
        state["sections_total"] = [s.get("id", s.get("id-przekroj")) for s in sections]
        if force:
            state["sections_done"] = []

    sections_todo = [
        s for s in state["sections_total"]
        if s not in state["sections_done"]
    ]
    if not sections_todo:
        return state.get("rows", 0)

    # Load existing file if partially done
    dest = LANDING / str(root_id) / f"{ind_id}.json"
    if dest.exists() and not force and state["sections_done"]:
        existing = json.loads(dest.read_text())
        sections_data: dict = existing.get("sections", {})
    else:
        sections_data = {}

    total_rows = sum(len(v.get("rows", [])) for v in sections_data.values())

    for sec_id in sections_todo:
        rows = fetch_section_data(session, limiter, ind_id, sec_id)
        sections_data[str(sec_id)] = {
            "section_meta": {"id-przekroj": sec_id},
            "rows": rows,
        }
        total_rows += len(rows)
        state["sections_done"].append(sec_id)
        state["rows"] = total_rows
        state["last_updated"] = _now()

        # Atomic write after each completed section (resume-safe mid-indicator)
        envelope = {
            "_meta": {
                "source": "gus_dbw_api",
                "indicator_id": ind_id, "area_id": area_id, "root_area_id": root_id,
                "fetched_at": _now(),
                "sections": state["sections_total"],
            },
            "sections": sections_data,
        }
        _atomic_write(dest, envelope)

    return total_rows


def main(
    root_areas: list[int],
    force: bool = False,
    max_requests: int | None = None,
    dry_run: bool = False,
) -> int:
    api_key = os.environ.get("DBW_API_KEY")
    if not api_key:
        logger.error("DBW_API_KEY not set")
        return 2

    LANDING.mkdir(parents=True, exist_ok=True)
    limiter = WeeklyRateLimiter("dbw", 10_000, RATELIMIT_PATH,
                                min_interval_s=0.5, reserve=200)
    session = requests.Session()
    session.headers.update({
        "X-ApiKey": api_key,
        "User-Agent": "OpenReporting-DataPipeline/1.0 (open-reporting.dev)",
        "Accept": "application/json",
    })
    manifest = load_manifest()

    try:
        tree = load_area_tree()
    except FileNotFoundError as e:
        logger.error(str(e))
        return 2

    try:
        for root_id in root_areas:
            root_name = ROOT_AREAS.get(root_id, str(root_id))
            (LANDING / str(root_id)).mkdir(parents=True, exist_ok=True)

            leaves = leaf_areas(tree, root_id)
            logger.info(f"[dbw] {root_name} ({root_id}): {len(leaves)} leaf areas")

            # Discover all indicators across leaf areas
            all_indicators: list[dict] = []
            for area in leaves:
                area_id = int(area.get("id", 0))
                if max_requests and limiter.used_this_run >= max_requests:
                    raise BudgetExhausted(f"per-run cap of {max_requests} reached")
                try:
                    indicators = discover_indicators(
                        session, limiter, area_id, root_id, force
                    )
                    all_indicators.extend(indicators)
                except FetchSkip as e:
                    logger.warning(f"[dbw] Skip area {area_id}: {e}")

            logger.info(f"[dbw] {root_name}: {len(all_indicators)} indicators discovered")

            if dry_run:
                sections_est = 2
                req_est = len(all_indicators) * (1 + sections_est * 2)
                logger.info(f"[dbw] DRY RUN {root_name}: ~{req_est} requests estimated")
                continue

            pulled = failed = skipped = 0
            done_set = {
                k for k, v in manifest["indicators"].items()
                if v.get("sections_done") and v.get("sections_done") == v.get("sections_total")
                and not force
            }

            for indicator in all_indicators:
                ind_id = str(indicator.get("id", indicator.get("id-zmienna", "")))
                if ind_id in done_set:
                    skipped += 1
                    continue
                if max_requests and limiter.used_this_run >= max_requests:
                    raise BudgetExhausted(f"per-run cap of {max_requests} reached")

                try:
                    rows = fetch_indicator_data(
                        session, limiter, indicator, root_id, manifest, force
                    )
                    pulled += 1
                    if pulled % 50 == 0:
                        logger.info(
                            f"[dbw] {root_name}: {pulled} done, "
                            f"{limiter.remaining} req remaining"
                        )
                except FetchSkip as e:
                    ind_key = str(indicator.get("id", "?"))
                    if ind_key in manifest["indicators"]:
                        manifest["indicators"][ind_key]["failed"] = str(e)
                    failed += 1
                    logger.warning(f"[dbw] Skip indicator {ind_id}: {e}")
                finally:
                    save_manifest(manifest)

            logger.info(
                f"[dbw] {root_name}: {pulled} pulled, {skipped} skipped, {failed} failed"
            )

    except BudgetExhausted as e:
        logger.info(f"[dbw] Budget stop: {e} — manifest saved, resume next run")
        save_manifest(manifest)
        return 0
    except FetchAbort as e:
        logger.error(f"[dbw] Abort: {e}")
        save_manifest(manifest)
        return 2

    logger.info(f"[dbw] Done. Requests this run: {limiter.used_this_run}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GUS DBW non-HVD extractor")
    parser.add_argument(
        "--areas", default=",".join(str(a) for a in ROOT_AREAS),
        help="Comma-separated root area IDs (default: 727,728,729)"
    )
    parser.add_argument("--force", action="store_true", help="Re-fetch existing indicators")
    parser.add_argument("--max-requests", type=int, default=9000)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    areas = [int(a.strip()) for a in args.areas.split(",") if a.strip()]
    sys.exit(main(
        root_areas=areas,
        force=args.force,
        max_requests=args.max_requests,
        dry_run=args.dry_run,
    ))
