#!/usr/bin/env python3
"""
generate_ingestion_plan.py — Generate ingestion_plan.json and ingestion_capacity.json.

Reads products/ingestion/registry/ingestion_schedule.yaml plus live manifests from
data/landing/gus_bdl_api/ and data/landing/gus_dbw_api/ and writes two JSON files:

  data/ingestion_plan.json      — flat schedule stripped of subject_meta
  data/ingestion_capacity.json  — API capacity + bulk source inventory

Usage:
    python3 infra/scheduler/generate_ingestion_plan.py
"""
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml  # pyyaml

# Insert own directory first (works when installed in infra/scheduler/).
# Also insert the canonical scheduler path so worktree invocations can resolve
# catalog_common from the live checkout.
_SELF_DIR = Path(__file__).parent
_CANON_DIR = Path("/opt/open-reporting/infra/scheduler")
for _p in (_SELF_DIR, _CANON_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
from catalog_common import REPO, LANDING, OUT, iso, atomic_write, now_iso  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

SCHEDULE_YAML = REPO / "products/ingestion/registry/ingestion_schedule.yaml"
PLAN_OUT = OUT / "ingestion_plan.json"
CAPACITY_OUT = OUT / "ingestion_capacity.json"

# Static metadata for capacity output
_BDL_NAME = "Bank Danych Lokalnych (BDL API)"
_DBW_NAME = "Bank Danych Regionalnych — DBW (API)"
_BDL_BUDGET = 50_000
_DBW_BUDGET = 10_000

_STATUS_ORDER = {"blocked": 0, "failed_partial": 1, "in_progress": 2, "pending": 3, "complete": 4}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_json_safe(path: Path) -> "dict | None":
    """Load JSON file; return None on any error."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        log.info("File not found: %s", path)
        return None
    except json.JSONDecodeError as exc:
        log.warning("JSON decode error in %s: %s", path, exc)
        return None


def _scan_last_refresh(folder: Path) -> "str | None":
    """Return YYYY-MM-DD of the newest non-underscore file in folder, or None."""
    max_mtime: "float | None" = None
    try:
        for p in folder.iterdir():
            if not p.is_file():
                continue
            if p.name.startswith("_") or p.name.startswith("."):
                continue
            try:
                mtime = p.stat().st_mtime
                if max_mtime is None or mtime > max_mtime:
                    max_mtime = mtime
            except OSError:
                continue
    except OSError as exc:
        log.warning("Cannot scan folder %s: %s", folder, exc)
        return None
    if max_mtime is None:
        return None
    return datetime.fromtimestamp(max_mtime, tz=timezone.utc).strftime("%Y-%m-%d")


def _count_non_underscore(folder: Path) -> int:
    """Count files that don't start with _ or . in folder (non-recursive)."""
    try:
        return sum(
            1 for p in folder.iterdir()
            if p.is_file() and not p.name.startswith("_") and not p.name.startswith(".")
        )
    except OSError:
        return 0


def _subject_status(done: int, total: "int | None", failed: int) -> str:
    if failed > 0 and done > 0:
        return "failed_partial"
    if failed > 0 and done == 0:
        return "blocked"
    if total and done == total:
        return "complete"
    if done > 0:
        return "in_progress"
    return "pending"


def _sort_key_for_subject(row: dict) -> tuple:
    order = _STATUS_ORDER.get(row.get("status", "pending"), 99)
    sid = row.get("id", "")
    # Natural sort: strip leading alpha prefix and sort numeric part
    numeric_part = "".join(filter(str.isdigit, sid)) or "0"
    return (order, sid[:1], int(numeric_part))


# ---------------------------------------------------------------------------
# BDL capacity builder
# ---------------------------------------------------------------------------

def _build_bdl_capacity(schedule_entry: dict) -> dict:
    bdl_folder = LANDING / "gus_bdl_api"
    manifest = _load_json_safe(bdl_folder / "_manifest.json")
    ratelimit = _load_json_safe(bdl_folder / "_ratelimit.json")
    subject_meta: dict = schedule_entry.get("subject_meta") or {}

    # Rate-limit fields
    iso_week = budget_per_week = used_this_week = header_remaining = header_reset = None
    budget_per_week = _BDL_BUDGET
    if ratelimit:
        iso_week = ratelimit.get("week")
        used_this_week = ratelimit.get("used")
        header_remaining = ratelimit.get("header_remaining")
        raw_reset = ratelimit.get("header_reset", "")
        # Normalise to Z-suffix ISO (strip sub-seconds)
        if raw_reset:
            try:
                dt = datetime.fromisoformat(raw_reset.replace("Z", "+00:00"))
                header_reset = iso(dt)
            except ValueError:
                header_reset = raw_reset

    manifest_subjects: dict = {}
    if manifest:
        manifest_subjects = manifest.get("subjects", {})

    # Build subject rows: union of manifest keys and subject_meta keys
    all_ids = set(manifest_subjects.keys()) | set(subject_meta.keys())

    subjects_out: list[dict] = []
    units_done_total = 0
    units_total_known = 0

    for sid in all_ids:
        msubj = manifest_subjects.get(sid, {})
        meta = subject_meta.get(sid, {})

        vars_done: list = msubj.get("vars_done", [])
        vars_total: int = msubj.get("vars_total", 0)
        vars_failed: "dict | list" = msubj.get("vars_failed", {})
        raw_updated = msubj.get("last_updated", "")
        last_updated: "str | None" = None
        if raw_updated:
            try:
                dt = datetime.fromisoformat(raw_updated.replace("Z", "+00:00"))
                last_updated = iso(dt)
            except ValueError:
                last_updated = raw_updated

        done = len(vars_done)
        total: "int | None" = vars_total if vars_total > 0 else None
        failed = len(vars_failed) if isinstance(vars_failed, (dict, list)) else 0
        status = _subject_status(done, total, failed)

        est_requests = meta.get("est_requests") if meta else None
        label = meta.get("label") if meta else None

        units_done_total += done
        if vars_total > 0:
            units_total_known += vars_total

        subjects_out.append({
            "id": sid,
            "label": label,
            "done": done,
            "total": total,
            "failed": failed,
            "status": status,
            "est_requests": est_requests,
            "last_updated": last_updated,
        })

    # Sort: blocked first, then in_progress, then pending, then complete; within group: natural id sort
    subjects_out.sort(key=_sort_key_for_subject)

    # est_requests_remaining = sum est_requests for non-complete subjects with non-null est_requests
    non_complete = [s for s in subjects_out if s["status"] != "complete"]
    has_estimates = [s for s in non_complete if s["est_requests"] is not None]
    est_requests_remaining: "int | None" = None
    if has_estimates:
        est_requests_remaining = sum(s["est_requests"] for s in has_estimates)

    if non_complete:
        if len(has_estimates) == len(non_complete):
            confidence = "high"
        elif has_estimates:
            confidence = "low"
        else:
            confidence = "unknown"
    else:
        confidence = "high"

    est_weeks_to_complete: "float | None" = None
    if est_requests_remaining is not None:
        est_weeks_to_complete = round(est_requests_remaining / budget_per_week, 1)

    return {
        "source_key": "gus_bdl_api",
        "name": _BDL_NAME,
        "budget_per_week": budget_per_week,
        "iso_week": iso_week,
        "used_this_week": used_this_week,
        "header_remaining": header_remaining,
        "header_reset": header_reset,
        "units_label": "variables",
        "units_done": units_done_total,
        "units_total_known": units_total_known,
        "progress_pct": None,
        "est_requests_remaining": est_requests_remaining,
        "est_weeks_to_complete": est_weeks_to_complete,
        "estimate_confidence": confidence,
        "subjects": subjects_out,
    }


# ---------------------------------------------------------------------------
# DBW capacity builder
# ---------------------------------------------------------------------------

def _build_dbw_capacity(schedule_entry: dict) -> dict:
    dbw_folder = LANDING / "gus_dbw_api"
    manifest = _load_json_safe(dbw_folder / "_manifest.json")
    ratelimit = _load_json_safe(dbw_folder / "_ratelimit.json")
    subject_meta: dict = schedule_entry.get("subject_meta") or {}

    budget_per_week = _DBW_BUDGET
    iso_week = used_this_week = header_remaining = header_reset = None
    if ratelimit:
        iso_week = ratelimit.get("week")
        used_this_week = ratelimit.get("used")
        header_remaining = ratelimit.get("header_remaining")
        raw_reset = ratelimit.get("header_reset", "")
        if raw_reset:
            try:
                dt = datetime.fromisoformat(raw_reset.replace("Z", "+00:00"))
                header_reset = iso(dt)
            except ValueError:
                header_reset = raw_reset

    # Group indicators by root_area_id (str key)
    groups: dict[str, dict] = {}  # area_id -> {total, done, failed}
    if manifest:
        indicators: dict = manifest.get("indicators", {})
        for _ind_id, ind in indicators.items():
            root_id = str(ind.get("root_area_id", ""))
            if root_id not in groups:
                groups[root_id] = {"total": 0, "done": 0, "failed": 0}
            groups[root_id]["total"] += 1

            sections_done: list = ind.get("sections_done", [])
            sections_total: list = ind.get("sections_total", [])
            failed_str: str = ind.get("failed", "")

            if sections_total and len(sections_done) == len(sections_total):
                groups[root_id]["done"] += 1
            if failed_str:
                groups[root_id]["failed"] += 1

    # Build subject rows: union of manifest groups and subject_meta keys
    all_ids = set(groups.keys()) | set(str(k) for k in subject_meta.keys())
    subjects_out: list[dict] = []
    units_done_total = 0
    units_total_known = 0

    for sid in all_ids:
        g = groups.get(sid, {})
        meta = subject_meta.get(sid) or subject_meta.get(int(sid) if sid.isdigit() else sid, {})

        done = g.get("done", 0)
        total_count = g.get("total") or None  # None if no indicators seen
        failed = g.get("failed", 0)
        status = _subject_status(done, total_count, failed)
        label = meta.get("label") if meta else None

        units_done_total += done
        if total_count:
            units_total_known += total_count

        subjects_out.append({
            "id": sid,
            "label": label,
            "done": done,
            "total": total_count,
            "failed": failed,
            "status": status,
            "est_requests": None,
        })

    subjects_out.sort(key=_sort_key_for_subject)

    return {
        "source_key": "gus_dbw_api",
        "name": _DBW_NAME,
        "budget_per_week": budget_per_week,
        "iso_week": iso_week,
        "used_this_week": used_this_week,
        "header_remaining": header_remaining,
        "header_reset": header_reset,
        "units_label": "indicators",
        "units_done": units_done_total,
        "units_total_known": units_total_known if units_total_known else None,
        "progress_pct": None,
        "est_requests_remaining": None,
        "est_weeks_to_complete": None,
        "estimate_confidence": "unknown",
        "subjects": subjects_out,
    }


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate() -> "tuple[Path, Path]":
    """Read schedule YAML + manifests, write ingestion_plan.json and ingestion_capacity.json."""
    with open(SCHEDULE_YAML, "r", encoding="utf-8") as fh:
        schedule = yaml.safe_load(fh)

    entries: list[dict] = schedule.get("entries", [])
    generated_at = now_iso()

    # --- ingestion_plan.json ---
    plan_entries: list[dict] = []
    for entry in entries:
        plan_entry = {k: v for k, v in entry.items() if k != "subject_meta"}
        plan_entries.append(plan_entry)

    # Sort by priority asc, then source_key
    plan_entries.sort(key=lambda e: (e.get("priority", 99), e.get("source_key", "")))

    plan_doc = {
        "generated_at": generated_at,
        "entries": plan_entries,
    }
    atomic_write(PLAN_OUT, plan_doc)
    log.info("ingestion_plan.json: %d entries written to %s", len(plan_entries), PLAN_OUT)

    # --- ingestion_capacity.json ---

    # Build lookup of schedule entries by source_key for subject_meta access
    entry_by_key: dict[str, dict] = {e["source_key"]: e for e in entries}

    # API sources: BDL + DBW
    api_sources: list[dict] = [
        _build_bdl_capacity(entry_by_key.get("gus_bdl_api", {})),
        _build_dbw_capacity(entry_by_key.get("gus_dbw_api", {})),
    ]

    # Bulk sources: all entries whose mechanism does NOT mention _ratelimit (i.e. no budget_per_week)
    # Rule: entries NOT in api_sources list
    api_keys = {"gus_bdl_api", "gus_dbw_api"}
    bulk_sources: list[dict] = []
    for entry in entries:
        sk = entry.get("source_key", "")
        if sk in api_keys:
            continue
        folder = LANDING / sk
        file_count = _count_non_underscore(folder)
        last_refresh = _scan_last_refresh(folder)

        # Derive a display name from source_key (best effort)
        name = sk.replace("_", " ").title()

        bulk_sources.append({
            "source_key": sk,
            "name": name,
            "file_count": file_count,
            "last_refresh": last_refresh,
        })

    # Sort bulk by source_key for stable output
    bulk_sources.sort(key=lambda s: s["source_key"])

    capacity_doc = {
        "generated_at": generated_at,
        "api_sources": api_sources,
        "bulk_sources": bulk_sources,
    }
    atomic_write(CAPACITY_OUT, capacity_doc)
    log.info(
        "ingestion_capacity.json: %d api sources, %d bulk sources written to %s",
        len(api_sources),
        len(bulk_sources),
        CAPACITY_OUT,
    )

    # Log summary for verification
    bdl = api_sources[0]
    log.info(
        "BDL: estimate_confidence=%s, est_weeks_to_complete=%s, "
        "units_done=%s, units_total_known=%s",
        bdl["estimate_confidence"],
        bdl["est_weeks_to_complete"],
        bdl["units_done"],
        bdl["units_total_known"],
    )
    dbw = api_sources[1]
    log.info(
        "DBW: units_done=%s, units_total_known=%s",
        dbw["units_done"],
        dbw["units_total_known"],
    )

    return PLAN_OUT, CAPACITY_OUT


if __name__ == "__main__":
    generate()
    sys.exit(0)
