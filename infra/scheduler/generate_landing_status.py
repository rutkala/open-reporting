#!/usr/bin/env python3
"""
generate_landing_status.py — Generate landing_status.json for the admin portal.

Scans all subdirectories of data/landing/, reads manifests where present, and
writes a structured JSON summary to infra/nginx/html/data/landing_status.json.

Usage:
    python3 generate_landing_status.py
"""
import logging
import sys
from pathlib import Path

from catalog_common import (
    LANDING,
    OUT,
    atomic_write,
    human_size,
    now_iso,
    parse_manifest,
    scan_folder,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def generate() -> Path:
    """Scan data/landing/, build JSON summary, write atomically to html/data/landing_status.json."""
    folders: list[dict] = []
    total_files = 0
    total_bytes = 0

    for entry in sorted(LANDING.iterdir()):
        if not entry.is_dir():
            continue

        file_count, size_bytes, last_modified = scan_folder(entry)
        manifest_kind, progress = parse_manifest(entry)

        folder_entry: dict = {
            "name": entry.name,
            "file_count": file_count,
            "size_bytes": size_bytes,
            "size_label": human_size(size_bytes),
            "last_modified": last_modified,
            "manifest_kind": manifest_kind,
            "progress": progress if manifest_kind is not None else None,
        }
        folders.append(folder_entry)

        total_files += file_count
        total_bytes += size_bytes

    output: dict = {
        "generated_at": now_iso(),
        "landing_root": str(LANDING),
        "totals": {
            "folders": len(folders),
            "files": total_files,
            "bytes": total_bytes,
        },
        "folders": folders,
    }

    out_path = OUT / "landing_status.json"
    atomic_write(out_path, output)

    log.info(
        "landing_status: %d folders, %d files, %s",
        len(folders),
        total_files,
        human_size(total_bytes),
    )
    return out_path


if __name__ == "__main__":
    generate()
    sys.exit(0)
