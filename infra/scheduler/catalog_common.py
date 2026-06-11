"""
catalog_common.py — Shared helpers for admin portal data pipeline generators.

Imported by generate_landing_status.py and generate_duckdb_catalog.py.
No __main__ block.
"""
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)

REPO = Path("/opt/open-reporting")
LANDING = REPO / "data/landing"
OUT = REPO / "infra/nginx/html/data"
REGISTRY_YAML = REPO / "products/ingestion/registry/source_registry.yaml"
SCHEDULE_YAML = REPO / "products/ingestion/registry/ingestion_schedule.yaml"

# Root-area id → Polish label for DBW manifest grouping
_DBW_ROOT_LABELS: dict[str, str] = {
    "727": "Gospodarka",
    "728": "Społeczeństwo",
    "729": "Środowisko",
}


def human_size(b: int) -> str:
    """Return binary human-readable size with 1 decimal, e.g. '3.1 GB', '18.0 MB', '423 B'."""
    value = float(b)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024.0:
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{value:.1f} TB"


def iso(dt: datetime) -> str:
    """Return ISO-8601 UTC string with Z suffix.

    Handles both aware (any tz) and naive (treated as UTC) datetimes.
    Example: '2026-06-11T09:11:08Z'
    """
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def atomic_write(path: Path, data: "dict | list") -> None:
    """Write JSON (indent=2, ensure_ascii=False) atomically via a tmp file + os.replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def scan_folder(folder: Path) -> "tuple[int, int, str | None]":
    """Scan a folder recursively, returning (file_count, size_bytes, last_modified_iso).

    - file_count: files whose name does NOT start with '_' or '.'
    - size_bytes:  sum of all file sizes (including _ / . prefixed)
    - last_modified_iso: ISO string of max mtime across ALL files, or None if empty/error
    """
    try:
        file_count = 0
        size_bytes = 0
        max_mtime: "float | None" = None

        for path in folder.rglob("*"):
            if not path.is_file():
                continue
            try:
                st = path.stat()
            except OSError:
                continue
            size_bytes += st.st_size
            if max_mtime is None or st.st_mtime > max_mtime:
                max_mtime = st.st_mtime
            name = path.name
            if not name.startswith("_") and not name.startswith("."):
                file_count += 1

        last_modified_iso: "str | None" = None
        if max_mtime is not None:
            last_modified_iso = iso(datetime.fromtimestamp(max_mtime, tz=timezone.utc))

        return file_count, size_bytes, last_modified_iso

    except OSError as exc:
        log.warning("scan_folder: error scanning %s: %s", folder, exc)
        return 0, 0, None


def parse_manifest(folder: Path) -> "tuple[str | None, list[dict]]":
    """Read folder/_manifest.json and return (manifest_kind, progress_rows).

    kind is 'bdl' if top-level key 'subjects' exists, 'dbw' if 'indicators' exists,
    else (None, []).

    BDL progress rows: one per subject, sorted by id.
    DBW progress rows: one per root_area_id group, sorted by id (as string).
    """
    manifest_path = folder / "_manifest.json"
    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        log.info("parse_manifest: no manifest at %s", manifest_path)
        return None, []
    except json.JSONDecodeError as exc:
        log.info("parse_manifest: JSON error in %s: %s", manifest_path, exc)
        return None, []

    if "subjects" in data:
        return "bdl", _parse_bdl_progress(data["subjects"])

    if "indicators" in data:
        return "dbw", _parse_dbw_progress(data["indicators"])

    return None, []


def _parse_bdl_progress(subjects: dict) -> list[dict]:
    """Build one progress row per BDL subject, sorted by id."""
    rows: list[dict] = []
    for subject_id, subj in subjects.items():
        vars_done: list = subj.get("vars_done", [])
        vars_total: int = subj.get("vars_total", 0)
        vars_failed: "dict | list" = subj.get("vars_failed", {})
        rows.append({
            "id": subject_id,
            "label": None,
            "done": len(vars_done),
            "total": vars_total,
            "failed": len(vars_failed),
        })
    rows.sort(key=lambda r: r["id"])
    return rows


def _parse_dbw_progress(indicators: dict) -> list[dict]:
    """Build one progress row per root_area_id in the DBW manifest, sorted by id."""
    # Group indicators by root_area_id
    groups: dict[str, dict] = {}

    for _ind_id, ind in indicators.items():
        root_id = str(ind.get("root_area_id", ""))
        if root_id not in groups:
            groups[root_id] = {"total": 0, "done": 0, "failed": 0}
        groups[root_id]["total"] += 1

        sections_done: list = ind.get("sections_done", [])
        sections_total: list = ind.get("sections_total", [])
        failed: str = ind.get("failed", "")

        if sections_total and len(sections_done) == len(sections_total):
            groups[root_id]["done"] += 1

        if failed:
            groups[root_id]["failed"] += 1

    rows: list[dict] = []
    for root_id, counts in groups.items():
        rows.append({
            "id": root_id,
            "label": _DBW_ROOT_LABELS.get(root_id),
            "done": counts["done"],
            "total": counts["total"],
            "failed": counts["failed"],
        })

    rows.sort(key=lambda r: r["id"])
    return rows


def now_iso() -> str:
    """Return current UTC time as ISO-8601 string with Z suffix."""
    return iso(datetime.now(timezone.utc))
