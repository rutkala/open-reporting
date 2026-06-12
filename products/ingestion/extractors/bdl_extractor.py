#!/usr/bin/env python3
"""
GUS BDL (Bank Danych Lokalnych) extractor.

Pulls variable-level data from bdl.stat.gov.pl/api/v1 for priority subject domains.
Writes to data/landing/gus_bdl_api/{subject_id}/{variable_id}.json.

Usage:
    python3 bdl_extractor.py                         # all priority subjects
    python3 bdl_extractor.py --subjects K27,K40      # specific subjects
    python3 bdl_extractor.py --dry-run               # count requests, no fetch
    python3 bdl_extractor.py --max-requests 5000     # per-run budget cap
    python3 bdl_extractor.py --force                 # re-fetch all variables
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

BASE = "https://bdl.stat.gov.pl/api/v1"
LANDING = Path("/opt/open-reporting/data/landing/gus_bdl_api")
MANIFEST_PATH = LANDING / "_manifest.json"
RATELIMIT_PATH = LANDING / "_ratelimit.json"

# Priority subject IDs — order determines pull sequence.
# K27=finanse publiczne, K40=rynek pracy, K3=ludność, K15=ceny, K11=mieszkalnictwo
PRIORITY_SUBJECTS = ["K27", "K40", "K3", "K15", "K11"]
YEARS = list(range(2000, 2026))
DEFAULT_UNIT_LEVEL = 2  # województwo


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
    return {"version": 1, "unit_level": DEFAULT_UNIT_LEVEL,
            "years": [YEARS[0], YEARS[-1]], "subjects": {}}


def save_manifest(manifest: dict) -> None:
    _atomic_write(MANIFEST_PATH, manifest)


def _subject_state(manifest: dict, subject_id: str) -> dict:
    if subject_id not in manifest["subjects"]:
        manifest["subjects"][subject_id] = {
            "leaf_subjects": [], "vars_total": 0,
            "vars_done": [], "vars_failed": {}, "last_updated": "",
        }
    return manifest["subjects"][subject_id]


def fetch_subject_info(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    subject_id: str,
) -> dict:
    """Fetch subject metadata (name, hasVariables, children)."""
    cache = LANDING / subject_id / "subtree.json"
    if cache.exists():
        return json.loads(cache.read_text())
    data = get_json(session, f"{BASE}/subjects/{subject_id}", {"lang": "pl"}, limiter)
    _atomic_write(cache, data)
    return data


def resolve_leaf_subjects(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    subject_id: str,
) -> list[str]:
    """Walk subject tree to find P-level leaves where hasVariables=true."""
    info = fetch_subject_info(session, limiter, subject_id)
    if info.get("hasVariables"):
        return [info["id"]]
    leaves = []
    for child in info.get("children", []):
        cid = child if isinstance(child, str) else child.get("id")
        if not cid:
            continue
        try:
            leaves.extend(resolve_leaf_subjects(session, limiter, str(cid)))
        except FetchSkip as e:
            logger.warning(f"[bdl] Skipping child {cid}: {e}")
    return leaves


def fetch_variables(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    subject_id: str,
    leaf_subjects: list[str],
    force: bool = False,
) -> list[dict]:
    """Fetch all variables across all leaf subjects for a K-subject."""
    cache = LANDING / subject_id / "variables.json"
    if cache.exists() and not force:
        data = json.loads(cache.read_text())
        return data.get("results", [])

    all_vars: list[dict] = []
    for leaf_id in leaf_subjects:
        page = 0
        while True:
            data = get_json(
                session, f"{BASE}/variables",
                {"subject-id": leaf_id, "lang": "pl", "page-size": 100, "page": page},
                limiter,
            )
            all_vars.extend(data.get("results", []))
            page += 1
            if page * 100 >= data.get("totalRecords", 0):
                break

    envelope = {
        "_meta": {
            "source": "gus_bdl_api", "endpoint": "/variables",
            "subject_id": subject_id, "leaf_subjects": leaf_subjects,
            "fetched_at": _now(), "total_records": len(all_vars),
        },
        "results": all_vars,
    }
    _atomic_write(cache, envelope)
    logger.info(f"[bdl] {subject_id}: {len(all_vars)} variables across {len(leaf_subjects)} leaves")
    return all_vars


def fetch_variable_data(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
    subject_id: str,
    var: dict,
    unit_level: int,
    years: list[int],
) -> int:
    """Pull all pages for one variable. Returns row count. Raises FetchSkip on failure."""
    var_id = var["id"]
    rows: list[dict] = []
    page = 0
    while True:
        # years must be repeated params — requests handles list correctly
        data = get_json(
            session, f"{BASE}/data/by-variable/{var_id}",
            {"unit-level": unit_level, "year": years,
             "lang": "pl", "page-size": 100, "page": page},
            limiter,
        )
        rows.extend(data.get("results", []))
        page += 1
        if page * 100 >= data.get("totalRecords", 0):
            break

    envelope = {
        "_meta": {
            "source": "gus_bdl_api", "endpoint": f"/data/by-variable/{var_id}",
            "variable_id": var_id, "subject_id": subject_id,
            "unit_level": unit_level, "years": [years[0], years[-1]],
            "fetched_at": _now(), "pages": page, "total_records": len(rows),
        },
        "results": rows,
    }
    dest = LANDING / subject_id / f"{var_id}.json"
    _atomic_write(dest, envelope)
    return len(rows)


def fetch_all_root_subjects(
    session: requests.Session,
    limiter: WeeklyRateLimiter,
) -> list[str]:
    """Fetch the full list of root (K-level) subject IDs from /subjects."""
    ids: list[str] = []
    page = 0
    while True:
        data = get_json(session, f"{BASE}/subjects",
                        {"lang": "pl", "page-size": 100, "page": page}, limiter)
        ids.extend(s["id"] for s in data.get("results", []))
        page += 1
        if page * 100 >= data.get("totalRecords", 0):
            break
    return ids


def main(
    subjects: list[str],
    unit_level: int = DEFAULT_UNIT_LEVEL,
    years: list[int] = YEARS,
    force: bool = False,
    max_requests: int | None = None,
    dry_run: bool = False,
) -> int:
    api_key = os.environ.get("BDL_API_KEY")
    if not api_key:
        logger.error("BDL_API_KEY not set")
        return 2

    LANDING.mkdir(parents=True, exist_ok=True)
    limiter = WeeklyRateLimiter("bdl", 50_000, RATELIMIT_PATH,
                                min_interval_s=0.15, reserve=500)
    session = requests.Session()
    session.headers.update({
        "X-ClientId": api_key,
        "User-Agent": "OpenReporting-DataPipeline/1.0 (open-reporting.dev)",
        "Accept": "application/json",
    })
    manifest = load_manifest()
    manifest["unit_level"] = unit_level
    manifest["years"] = [years[0], years[-1]]

    try:
        if subjects == ["all"]:
            subjects = fetch_all_root_subjects(session, limiter)
            logger.info(f"[bdl] 'all' resolved to {len(subjects)} root subjects: "
                        f"{','.join(subjects)}")

        for subject_id in subjects:
            state = _subject_state(manifest, subject_id)

            # Resolve leaf subjects
            if not state["leaf_subjects"] or force:
                logger.info(f"[bdl] Resolving subject tree for {subject_id}...")
                try:
                    leaves = resolve_leaf_subjects(session, limiter, subject_id)
                except FetchSkip as e:
                    logger.warning(f"[bdl] Skip subject {subject_id} (subject tree failed): {e}")
                    continue
                state["leaf_subjects"] = leaves
                save_manifest(manifest)
            else:
                leaves = state["leaf_subjects"]

            # Fetch variable list
            try:
                variables = fetch_variables(session, limiter, subject_id, leaves, force)
            except FetchSkip as e:
                logger.warning(f"[bdl] Skip subject {subject_id} (variable list failed): {e}")
                continue
            state["vars_total"] = len(variables)
            save_manifest(manifest)

            if dry_run:
                pages_est = 2
                req_est = len(variables) * pages_est
                logger.info(f"[bdl] DRY RUN {subject_id}: {len(variables)} vars "
                            f"~{req_est} requests estimated")
                continue

            done_set = set(str(v) for v in state["vars_done"])
            pulled = failed = skipped = 0

            for var in variables:
                var_id = str(var["id"])
                if var_id in done_set and not force:
                    skipped += 1
                    continue
                if max_requests and limiter.used_this_run >= max_requests:
                    raise BudgetExhausted(f"per-run cap of {max_requests} reached")

                try:
                    rows = fetch_variable_data(
                        session, limiter, subject_id, var, unit_level, years
                    )
                    state["vars_done"].append(var_id)
                    state["vars_failed"].pop(var_id, None)
                    pulled += 1
                    if pulled % 25 == 0:
                        logger.info(f"[bdl] {subject_id}: {pulled} done, "
                                    f"{limiter.remaining} req remaining")
                except FetchSkip as e:
                    state["vars_failed"][var_id] = str(e)
                    failed += 1
                    logger.warning(f"[bdl] Skip var {var_id}: {e}")
                finally:
                    state["last_updated"] = _now()
                    save_manifest(manifest)

            logger.info(f"[bdl] {subject_id}: {pulled} pulled, "
                        f"{skipped} skipped, {failed} failed")

    except BudgetExhausted as e:
        logger.info(f"[bdl] Budget stop: {e} — manifest saved, resume next run")
        save_manifest(manifest)
        return 0
    except FetchAbort as e:
        logger.error(f"[bdl] Abort: {e}")
        save_manifest(manifest)
        return 2

    logger.info(f"[bdl] Done. Requests this run: {limiter.used_this_run}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GUS BDL extractor")
    parser.add_argument("--subjects", default=",".join(PRIORITY_SUBJECTS),
                        help="Comma-separated subject IDs, or 'all' to fetch the "
                             "full root list from /subjects (default: priority list)")
    parser.add_argument("--unit-level", type=int, default=DEFAULT_UNIT_LEVEL,
                        help="BDL unit level (2=województwo, 4=powiat, 5=gmina)")
    parser.add_argument("--years", default=f"{YEARS[0]}-{YEARS[-1]}",
                        help="Year range e.g. 2010-2025")
    parser.add_argument("--force", action="store_true", help="Re-fetch existing files")
    parser.add_argument("--max-requests", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    subjects = [s.strip() for s in args.subjects.split(",") if s.strip()]
    if "-" in args.years:
        y_start, y_end = args.years.split("-", 1)
        years = list(range(int(y_start), int(y_end) + 1))
    else:
        years = [int(args.years)]

    sys.exit(main(
        subjects=subjects,
        unit_level=args.unit_level,
        years=years,
        force=args.force,
        max_requests=args.max_requests,
        dry_run=args.dry_run,
    ))
