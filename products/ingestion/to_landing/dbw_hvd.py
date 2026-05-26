#!/usr/bin/env python3
"""
Landing: GUS DBW HVD Catalogue → data/landing/dbw_hvd/
Downloads all CSV ZIPs from the HVD catalogue and extracts them to the landing zone.
Catalogue API: https://dbw.stat.gov.pl/api_app/getCatalogValues
No API key required. No rate limiting.
Usage:
  PYTHONPATH=/opt/open-reporting python3 products/ingestion/to_landing/dbw_hvd.py
  PYTHONPATH=/opt/open-reporting python3 products/ingestion/to_landing/dbw_hvd.py --force
Notes:
  - Default run skips files already present in the landing zone.
  - --force re-downloads all files.
  - Extracts both data CSV and Dictionaries CSV from each ZIP.
  - Output: data/landing/dbw_hvd/<file_id>_data.csv and <file_id>_dict.csv
"""
import argparse
import io
import logging
import os
import zipfile

import requests
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

CATALOGUE_URL = "https://dbw.stat.gov.pl/api_app/getCatalogValues"
HVD_BASE_URL  = "https://dbw.stat.gov.pl"
LANDING_DIR   = os.path.join(
    os.environ.get("REPO_ROOT", "/opt/open-reporting"),
    "data/landing/dbw_hvd"
)


def get_hvd_catalogue() -> list[dict]:
    resp = requests.get(CATALOGUE_URL, params={"czy_pl": "false"}, timeout=30)
    resp.raise_for_status()
    entries = []
    for dataset in resp.json().get("data", []):
        category = dataset["title"]
        for row in dataset["table"]["rows"]:
            indicator = next((c for c in row if "indicator_id" in c), {})
            section   = next((c for c in row if "section_id"   in c), {})
            files     = next((c for c in row if "files"        in c), {})
            for f in files.get("files", []):
                if f["type"] == "ZIP_CSV":
                    file_id = f["filename"].replace("_csv_en.zip", "")
                    entries.append({
                        "category":    category,
                        "variable_id": indicator.get("indicator_id"),
                        "section_id":  section.get("section_id"),
                        "link":        f["link"].replace("\\", "/").lstrip("/"),
                        "file_id":     file_id,
                        "description": indicator.get("value", ""),
                    })
    log.info("HVD catalogue: %d CSV ZIP entries", len(entries))
    return entries


def run(force: bool = False) -> None:
    os.makedirs(LANDING_DIR, exist_ok=True)
    catalogue  = get_hvd_catalogue()
    downloaded = 0
    skipped    = 0

    for i, entry in enumerate(catalogue, 1):
        file_id   = entry["file_id"]
        data_path = os.path.join(LANDING_DIR, f"{file_id}_data.csv")
        dict_path = os.path.join(LANDING_DIR, f"{file_id}_dict.csv")

        if not force and os.path.exists(data_path):
            log.debug("Skip %s — already in landing", file_id)
            skipped += 1
            continue

        log.info("[%d/%d] %s | %s", i, len(catalogue), entry["category"], entry["description"][:60])

        try:
            resp = requests.get(f"{HVD_BASE_URL}/{entry['link']}", timeout=120)
            resp.raise_for_status()
        except Exception as exc:
            log.warning("  Download failed: %s", exc)
            continue

        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            names     = z.namelist()
            data_name = next((n for n in names if n.endswith(".csv") and "Dict" not in n), None)
            dict_name = next((n for n in names if "Dict" in n and n.endswith(".csv")), None)
            if data_name:
                with open(data_path, "wb") as f:
                    f.write(z.read(data_name))
            if dict_name:
                with open(dict_path, "wb") as f:
                    f.write(z.read(dict_name))

        size_kb = os.path.getsize(data_path) // 1024
        log.info("  → %s (%d KB)", file_id, size_kb)
        downloaded += 1

    log.info("Done: %d downloaded, %d skipped. Landing: %s", downloaded, skipped, LANDING_DIR)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download GUS DBW HVD ZIPs to landing zone")
    parser.add_argument("--force", action="store_true", help="Re-download all files")
    args = parser.parse_args()
    run(force=args.force)


if __name__ == "__main__":
    main()
