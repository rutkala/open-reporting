#!/usr/bin/env python3
"""
generate_source_registry.py — Generate source_registry.json for the admin portal.

Reads products/ingestion/registry/source_registry.yaml, computes extraction status
for each source by inspecting landing folders and manifests, and writes a structured
JSON summary to infra/nginx/html/data/source_registry.json.

Usage:
    python3 infra/scheduler/generate_source_registry.py
"""
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

# catalog_common.py lives in infra/scheduler/ alongside this script.
# In a worktree scenario the resolved real path may differ, so resolve both.
_this_dir = Path(__file__).resolve().parents[0]
_repo_scheduler = Path("/opt/open-reporting/infra/scheduler")
for _p in (_this_dir, _repo_scheduler):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
# allow catalog_common import when running from repo root
sys.path.insert(0, str(Path(__file__).parents[1]))

import yaml

from catalog_common import (
    LANDING,
    OUT,
    atomic_write,
    now_iso,
    scan_folder,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# REGISTRY_YAML path is relative to the script's repo root (parents[2] from infra/scheduler/)
REGISTRY_YAML = Path(__file__).parents[2] / "products/ingestion/registry/source_registry.yaml"

# Sort order: blocked first, then partial, not_started, scheduled, complete
_STATUS_ORDER = {"blocked": 0, "partial": 1, "not_started": 2, "scheduled": 3, "complete": 4}


def _rate_limit_label(source: dict) -> str:
    """Build human-readable rate limit string from registry entry."""
    rl = source.get("rate_limit")
    if rl is None:
        return "unlimited"

    label = f"{rl['requests']:,} req/{rl['period']}"
    if source.get("auth") == "key_required":
        label += " (registered key)"
    burst_note = rl.get("burst_note")
    if burst_note:
        label += f"; {burst_note}"
    return label


def _parse_iso_date(s: str) -> "datetime | None":
    """Parse an ISO-8601 string to UTC-aware datetime. Return None on failure."""
    if not s:
        return None
    # fromisoformat handles Python 3.11+ extended formats; cover older versions manually
    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
    ):
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def _max_mtime_date(folders: list[Path]) -> "str | None":
    """Return YYYY-MM-DD of the newest data file mtime across the given folders, or None.

    Only counts files not starting with '_' or '.'. Uses a shallow stat loop to avoid
    the performance cost of rglob on large nested structures.
    """
    max_mtime: "float | None" = None
    for folder in folders:
        if not folder.exists():
            continue
        try:
            for path in folder.rglob("*"):
                if not path.is_file():
                    continue
                if path.name.startswith("_") or path.name.startswith("."):
                    continue
                try:
                    mtime = path.stat().st_mtime
                    if max_mtime is None or mtime > max_mtime:
                        max_mtime = mtime
                except OSError:
                    continue
        except OSError:
            continue
    if max_mtime is None:
        return None
    return datetime.fromtimestamp(max_mtime, tz=timezone.utc).strftime("%Y-%m-%d")


def _read_manifest(folder: Path) -> "dict | None":
    """Read and parse folder/_manifest.json. Return None on missing/invalid."""
    manifest_path = folder / "_manifest.json"
    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        log.warning("manifest JSON error in %s: %s", manifest_path, exc)
        return None


def _compute_bdl_status(
    landing_folder: Path, default_status: str
) -> "tuple[str, str, str | None, int]":
    """Compute (extraction_status, status_detail, last_ingested, file_count) for BDL source.

    file_count is derived from the manifest (sum of vars_done) to avoid slow recursive scan
    on the 20k+ file BDL landing tree.
    """
    if not landing_folder.exists():
        log.warning("bdl landing folder missing: %s", landing_folder)
        return default_status, "no files yet", None, 0

    try:
        list(landing_folder.iterdir())
    except OSError:
        return "blocked", "landing folder unreadable (mount error)", None, 0

    raw = _read_manifest(landing_folder)
    if raw is None or "subjects" not in raw:
        log.warning("bdl manifest missing or invalid in %s; falling back to file scan",
                    landing_folder)
        try:
            fc, _, _ = scan_folder(landing_folder)
        except OSError:
            return "blocked", "landing folder unreadable (mount error)", None, 0
        status = "complete" if fc > 0 else default_status
        detail = f"{fc} files in landing" if fc > 0 else "no files yet"
        last_ing = _max_mtime_date([landing_folder])
        return status, detail, last_ing, fc

    subjects = raw["subjects"]

    done_subj = sum(
        1 for subj in subjects.values()
        if len(subj.get("vars_done", [])) == subj.get("vars_total", 0)
        and subj.get("vars_total", 0) > 0
    )
    total_subj = len(subjects)
    total_vars_done = sum(len(subj.get("vars_done", [])) for subj in subjects.values())
    any_done = any(len(subj.get("vars_done", [])) > 0 for subj in subjects.values())

    if done_subj == total_subj and total_subj > 0:
        status = "complete"
    elif any_done:
        status = "partial"
    else:
        status = default_status

    detail = f"{done_subj}/{total_subj} subjects complete ({total_vars_done:,} variables)"

    # last_ingested: max last_updated across subjects; fall back to manifest mtime
    max_dt: "datetime | None" = None
    for subj in subjects.values():
        lu = subj.get("last_updated", "")
        dt = _parse_iso_date(lu)
        if dt is not None and (max_dt is None or dt > max_dt):
            max_dt = dt

    if max_dt is not None:
        last_ing: "str | None" = max_dt.strftime("%Y-%m-%d")
    else:
        # Fall back to manifest file mtime (fast single-file stat)
        manifest_path = landing_folder / "_manifest.json"
        try:
            mtime = manifest_path.stat().st_mtime
            last_ing = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d")
        except OSError:
            last_ing = None

    # file_count: use total vars_done from manifest — avoids 26-second rglob on 20k files
    return status, detail, last_ing, total_vars_done


def _compute_dbw_status(
    landing_folder: Path, default_status: str
) -> "tuple[str, str, str | None, int]":
    """Compute (extraction_status, status_detail, last_ingested, file_count) for DBW source."""
    if not landing_folder.exists():
        log.warning("dbw landing folder missing: %s", landing_folder)
        return default_status, "no files yet", None, 0

    try:
        list(landing_folder.iterdir())
    except OSError:
        return "blocked", "landing folder unreadable (mount error)", None, 0

    raw = _read_manifest(landing_folder)
    if raw is None or "indicators" not in raw:
        log.warning("dbw manifest missing or invalid in %s; falling back to file scan",
                    landing_folder)
        try:
            fc, _, _ = scan_folder(landing_folder)
        except OSError:
            return "blocked", "landing folder unreadable (mount error)", None, 0
        status = "complete" if fc > 0 else default_status
        detail = f"{fc} files in landing" if fc > 0 else "no files yet"
        last_ing = _max_mtime_date([landing_folder])
        return status, detail, last_ing, fc

    indicators = raw["indicators"]

    done_ind = sum(
        1 for ind in indicators.values()
        if (
            ind.get("sections_total")
            and len(ind.get("sections_done", [])) == len(ind["sections_total"])
        )
    )
    failed_ind = sum(1 for ind in indicators.values() if ind.get("failed", ""))
    total_ind = len(indicators)
    any_done = any(len(ind.get("sections_done", [])) > 0 for ind in indicators.values())

    if done_ind > 0 and done_ind == total_ind:
        status = "complete"
    elif any_done:
        status = "partial"
    elif not any_done and failed_ind > 0:
        status = "blocked"
    else:
        status = default_status

    detail = f"{done_ind}/{total_ind} indicators complete; {failed_ind} failing"

    # last_ingested: max last_updated from manifest
    max_dt: "datetime | None" = None
    for ind in indicators.values():
        lu = ind.get("last_updated", "")
        dt = _parse_iso_date(lu)
        if dt is not None and (max_dt is None or dt > max_dt):
            max_dt = dt

    if max_dt is not None:
        last_ing: "str | None" = max_dt.strftime("%Y-%m-%d")
    else:
        manifest_path = landing_folder / "_manifest.json"
        try:
            mtime = manifest_path.stat().st_mtime
            last_ing = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d")
        except OSError:
            last_ing = None

    # file_count: use number of indicator rows (each corresponds to downloaded data)
    rows_total = sum(ind.get("rows", 0) for ind in indicators.values())
    file_count = rows_total if rows_total > 0 else done_ind

    return status, detail, last_ing, file_count


def _compute_file_status(
    landing_folders: list[Path], default_status: str
) -> "tuple[str, str, str | None, int]":
    """Compute (extraction_status, status_detail, last_ingested, file_count) for file sources."""
    # Check for mount/access errors first
    for folder in landing_folders:
        if folder.exists():
            try:
                list(folder.iterdir())
            except OSError:
                return "blocked", "landing folder unreadable (mount error)", None, 0
        else:
            log.warning("landing folder missing: %s", folder)

    total_files = 0
    # scan_folder returns (file_count, size_bytes, last_modified_iso)
    # last_modified_iso is a UTC ISO string like "2026-06-11T09:11:08Z" or None
    last_iso: "str | None" = None

    for folder in landing_folders:
        if not folder.exists():
            continue
        try:
            fc, _, folder_last_iso = scan_folder(folder)
            total_files += fc
            if folder_last_iso is not None:
                if last_iso is None or folder_last_iso > last_iso:
                    last_iso = folder_last_iso
        except OSError:
            return "blocked", "landing folder unreadable (mount error)", None, 0

    if total_files > 0:
        status = "complete"
        detail = f"{total_files} files in landing"
    else:
        status = default_status
        detail = "no files yet"

    # Convert ISO datetime string to YYYY-MM-DD date
    last_ing: "str | None" = None
    if last_iso is not None:
        try:
            last_ing = last_iso[:10]  # "2026-06-11T09:11:08Z" → "2026-06-11"
        except Exception:
            last_ing = None

    return status, detail, last_ing, total_files


def generate() -> Path:
    """Read source_registry.yaml, compute per-source status, write source_registry.json."""
    with open(REGISTRY_YAML, "r", encoding="utf-8") as fh:
        registry = yaml.safe_load(fh)

    raw_sources: list[dict] = registry.get("sources", [])
    output_sources: list[dict] = []

    for src in raw_sources:
        source_key: str = src["source_key"]
        manifest_kind: "str | None" = src.get("manifest_kind")
        default_status: str = src.get("default_status", "not_started")
        landing_folder_names: list[str] = src.get("landing_folders", [])
        landing_folders: list[Path] = [LANDING / name for name in landing_folder_names]

        rate_label = _rate_limit_label(src)

        try:
            if manifest_kind == "bdl":
                folder = landing_folders[0] if landing_folders else LANDING / source_key
                extraction_status, status_detail, last_ingested, file_count = (
                    _compute_bdl_status(folder, default_status)
                )
            elif manifest_kind == "dbw":
                folder = landing_folders[0] if landing_folders else LANDING / source_key
                extraction_status, status_detail, last_ingested, file_count = (
                    _compute_dbw_status(folder, default_status)
                )
            else:
                extraction_status, status_detail, last_ingested, file_count = (
                    _compute_file_status(landing_folders, default_status)
                )
        except OSError as exc:
            log.warning("OSError processing source %s: %s", source_key, exc)
            extraction_status = "blocked"
            status_detail = "landing folder unreadable (mount error)"
            last_ingested = None
            file_count = 0
        except Exception as exc:
            log.warning("Error processing source %s: %s", source_key, exc)
            extraction_status = default_status
            status_detail = "manifest unreadable"
            last_ingested = None
            file_count = 0

        output_sources.append({
            "source_key": source_key,
            "name": src["name"],
            "institution": src["institution"],
            "type": src["type"],
            "auth": src["auth"],
            "rate_limit_label": rate_label,
            "landing_folders": landing_folder_names,
            "extraction_status": extraction_status,
            "status_detail": status_detail,
            "last_ingested": last_ingested,
            "extractor_kind": src["extractor_kind"],
            "extractor_path": src["extractor_path"],
            "docs_url": src["docs_url"],
            "file_count": file_count,
        })

    # Sort: blocked < partial < not_started < scheduled < complete; within group: alpha by key
    output_sources.sort(
        key=lambda s: (_STATUS_ORDER.get(s["extraction_status"], 99), s["source_key"])
    )

    # Build status_counts — always include all 5 keys even if 0
    status_counts: dict[str, int] = {
        "complete": 0,
        "partial": 0,
        "scheduled": 0,
        "not_started": 0,
        "blocked": 0,
    }
    for s in output_sources:
        st = s["extraction_status"]
        if st in status_counts:
            status_counts[st] += 1

    source_count = len(output_sources)

    output: dict = {
        "generated_at": now_iso(),
        "source_count": source_count,
        "status_counts": status_counts,
        "sources": output_sources,
    }

    out_path = OUT / "source_registry.json"
    atomic_write(out_path, output)

    log.info(
        "source_registry: %d sources, status_counts=%s",
        source_count,
        status_counts,
    )
    return out_path


if __name__ == "__main__":
    generate()
    sys.exit(0)
