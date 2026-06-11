#!/usr/bin/env python3
"""
Full-history bulk downloader — downloads complete dataset dumps for all sources.
Writes raw files to /opt/open-reporting/data/landing/<source>/

Run manually or monthly. Idempotent: skips files that already exist and are non-empty.

Usage:
  python3 run_bulk.py                    # all sources
  python3 run_bulk.py eurostat gus_hvd   # specific sources only
  python3 run_bulk.py --force eurostat   # re-download even if file exists
"""

import logging
import re
import sys
import time
import json
import requests
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

from dotenv import load_dotenv

load_dotenv(override=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

LANDING_DIR = Path("/opt/open-reporting/data/landing")
SOURCE_WORKERS = 4
DANE_GOV_BASE = "https://api.dane.gov.pl/1.4"
HEADERS = {"User-Agent": "OpenReporting-DataPipeline/1.0 (open-reporting.dev)"}
FORCE = "--force" in sys.argv


# ---------------------------------------------------------------------------
# Catalogue builders — each returns list[(filename, url)]
# ---------------------------------------------------------------------------

def get_eurostat_files() -> list[tuple[str, str]]:
    """All datasets from Eurostat TOC, named by dataset code."""
    resp = requests.get(
        "https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en",
        timeout=60, headers=HEADERS
    )
    resp.raise_for_status()
    result = []
    for line in resp.text.splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) >= 3:
            code = parts[1].strip('"').strip()
            type_val = parts[2].strip('"').strip()
            if type_val in ("dataset", "table") and code:
                url = (
                    f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/"
                    f"{code}/?format=TSV&compressed=true"
                )
                result.append((f"{code}.tsv.gz", url))
    logger.info(f"[eurostat] TOC: {len(result)} datasets")
    return result


def get_gus_hvd_files() -> list[tuple[str, str]]:
    """All files from GUS DBW HVD bulk catalogue."""
    resp = requests.get(
        "https://dbw.stat.gov.pl/api_app/getCatalogValues", timeout=30, headers=HEADERS
    )
    resp.raise_for_status()
    data = resp.json()
    base_url = "https://dbw.stat.gov.pl"
    result = []
    seen = set()
    for hvd_cat in data.get("data", []):
        for row in hvd_cat.get("table", {}).get("rows", []):
            for cell in row:
                if isinstance(cell, dict) and "files" in cell:
                    for file_obj in cell["files"]:
                        link = file_obj.get("link", "").replace("\\", "/")
                        if link.endswith(".zip") or link.endswith(".csv"):
                            full_url = urljoin(base_url, link)
                            filename = link.split("/")[-1]
                            if filename not in seen:
                                seen.add(filename)
                                result.append((filename, full_url))
    logger.info(f"[gus_hvd] catalogue: {len(result)} files")
    return result


def _dane_gov_institution(institution_id: str, source_id: str) -> list[tuple[str, str]]:
    """All downloadable resources for a dane.gov.pl institution."""
    result = []
    page = 1
    while True:
        try:
            resp = requests.get(
                f"{DANE_GOV_BASE}/institutions/{institution_id}/datasets",
                params={"page": page, "per_page": 50},
                timeout=20, headers=HEADERS
            )
            if resp.status_code != 200:
                break
            data = resp.json()
        except Exception as e:
            logger.warning(f"[{source_id}] dane.gov.pl page {page}: {e}")
            break

        datasets = data.get("data", [])
        if not datasets:
            break

        for ds in datasets:
            ds_id = ds.get("id")
            ds_slug = (ds.get("attributes", {}).get("slug") or str(ds_id))[:60]
            try:
                res = requests.get(
                    f"{DANE_GOV_BASE}/datasets/{ds_id}/resources",
                    params={"per_page": 100},
                    timeout=15, headers=HEADERS
                )
                if res.status_code == 200:
                    for resource in res.json().get("data", []):
                        dl_url = resource.get("attributes", {}).get("download_url", "")
                        if dl_url:
                            raw_name = dl_url.split("/")[-1].split("?")[0][:60]
                            rid = resource.get("id", "x")
                            name = f"{ds_slug}__{raw_name}" if raw_name else f"{ds_slug}__res_{rid}"
                            result.append((name[:200], dl_url))
            except Exception:
                pass

        meta = data.get("meta", {})
        if page >= meta.get("last_page", 1):
            break
        page += 1
        time.sleep(0.2)

    logger.info(f"[{source_id}] dane.gov.pl: {len(result)} resources")
    return result


def get_gus_teryt_files() -> list[tuple[str, str]]:
    """GUS TERYT administrative unit hierarchy via BDL /api/v1/units — 7 levels, ~4714 units.

    BDL limits pageSize to 100. We probe each level for total pages and generate all page URLs.
    """
    base = "https://bdl.stat.gov.pl/api/v1/units"
    result = []
    for level in range(0, 7):
        try:
            resp = requests.get(base, params={"level": level, "page-size": 100, "lang": "pl"},
                                timeout=20, headers=HEADERS)
            resp.raise_for_status()
            data = resp.json()
            total = data.get("totalRecords", 1)
            page_size = data.get("pageSize", 100)
            total_pages = max(1, -(-total // page_size))  # ceiling division
        except Exception:
            total_pages = 1
        for page in range(0, total_pages):
            suffix = f"_p{page}" if total_pages > 1 else ""
            result.append((
                f"units_level_{level}{suffix}.json",
                f"{base}?level={level}&page-size=100&page={page}&lang=pl"
            ))
    logger.info(f"[gus_teryt] {len(result)} page files across 7 levels")
    return result


def get_gus_sdg_files() -> list[tuple[str, str]]:
    """GUS SDG — national and global indicator data as static JSON from sdg.gov.pl."""
    return [
        ("national_data.json", "https://sdg.gov.pl/api/v1/en/national_data.json"),
        ("global_data.json",   "https://sdg.gov.pl/api/v1/en/global_data.json"),
    ]


def get_gus_biuletyn_files() -> list[tuple[str, str]]:
    """GUS Biuletyn statystyczny długie szeregi — 62+ XLSX files scraped from publication page.

    Files are at new.stat.gov.pl/sites/default/files/{YYYY-MM}/tabl{NN}_{name}.xlsx.
    The page embeds exact URLs in <span class="file-url"> elements — no guessing needed.
    """
    page = "https://new.stat.gov.pl/biuletyn-statystyczny-dlugie-szeregi"
    try:
        resp = requests.get(page, timeout=30, headers=HEADERS)
        resp.raise_for_status()
        urls = re.findall(r'<span class="file-url[^"]*">(https?://[^<]+)</span>', resp.text)
        if urls:
            result = []
            seen: set[str] = set()
            for url in urls:
                url = url.strip()
                name = url.split("/")[-1][:150]
                if name not in seen:
                    seen.add(name)
                    result.append((name, url))
            logger.info(f"[gus_biuletyn] {len(result)} XLSX files")
            return result
        logger.warning("[gus_biuletyn] No file-url spans found on page")
    except Exception as e:
        logger.warning(f"[gus_biuletyn] page scrape failed: {e}")
    return []


def get_nbp_files() -> list[tuple[str, str]]:
    """NBP exchange rate archival XLSX files 2010–present."""
    current_year = datetime.utcnow().year
    result = []
    for year in range(2010, current_year + 1):
        url = f"https://nbp.pl/wp-content/uploads/{current_year}/{year}/archiwum_tab_a_{year}.xlsx"
        result.append((f"exchange_rates_{year}.xlsx", url))
    logger.info(f"[nbp] {len(result)} annual files")
    return result


def get_stooq_files() -> list[tuple[str, str]]:
    """Stooq daily OHLCV CSVs for key Polish indices (stooq.pl requires browser session — skipped)."""
    # Stooq blocks automated downloads without browser cookies.
    # Incremental scraping not feasible. Marked as manual source.
    logger.warning("[stooq] Stooq blocks automated downloads — skipping")
    return []


def get_gios_files() -> list[tuple[str, str]]:
    """GIOŚ air quality: station catalogue + sensor indices (v1 API)."""
    base = "https://api.gios.gov.pl/pjp-api/v1/rest"
    result = [("stations.json", f"{base}/station/findAll")]
    try:
        resp = requests.get(f"{base}/station/findAll", timeout=20, headers=HEADERS)
        stations = resp.json().get("Lista stacji pomiarów", [])
        for station in stations:
            sid = station.get("Identyfikator stacji")
            if sid:
                result.append((
                    f"sensors_station_{sid}.json",
                    f"{base}/station/sensors/{sid}"
                ))
        logger.info(f"[gios] {len(result)} endpoints ({len(stations)} stations)")
    except Exception as e:
        logger.warning(f"[gios] stations fetch failed: {e}")
    return result


def get_gpw_benchmark_files() -> list[tuple[str, str]]:
    """GPW Benchmark: WIBOR/WIBID fixing history — scraped from publications page."""
    # Direct CSV URLs are protected; scrape the publications listing
    result = []
    try:
        resp = requests.get(
            "https://gpwbenchmark.pl/pub/#WIBOR", timeout=15, headers=HEADERS
        )
        matches = re.findall(r'href="([^"]+\.(?:csv|xlsx?))"', resp.text, re.IGNORECASE)
        for m in set(matches):
            full = m if m.startswith("http") else urljoin("https://gpwbenchmark.pl", m)
            result.append((full.split("/")[-1], full))
    except Exception as e:
        logger.warning(f"[gpw_benchmark] scrape failed: {e}")

    if not result:
        # Fallback: known publication archive pattern
        logger.warning("[gpw_benchmark] No CSV links found via scrape — using known archive")
        for tenor in ["ON", "1W", "1M", "3M", "6M", "12M"]:
            url = f"https://gpwbenchmark.pl/pub/WIBOR_History_{tenor}.csv"
            result.append((f"wibor_{tenor.lower()}_history.csv", url))

    logger.info(f"[gpw_benchmark] {len(result)} files")
    return result


def get_saos_files() -> list[tuple[str, str]]:
    """SAOS court judgments — first pages of results catalogue."""
    base = "https://www.saos.org.pl/api"
    result = [("courts.json", f"{base}/courts")]
    for page in range(0, 5):
        result.append((
            f"judgments_p{page}.json",
            f"{base}/judgments?pageSize=100&pageNumber={page}"
        ))
    return result


def get_opi_radon_files() -> list[tuple[str, str]]:
    """OPI RAD-on: research institutions bulk exports."""
    base = "https://radon.nauka.gov.pl/opendata/polon"
    return [
        ("institutions.json",    f"{base}/institutions"),
        ("universities.json",    f"{base}/universities"),
        ("institutes.json",      f"{base}/institutes"),
        ("research_units.json",  f"{base}/researchUnits"),
    ]


def get_krs_files() -> list[tuple[str, str]]:
    """KRS OpenAPI schema."""
    return [("openapi.json", "https://prs.ms.gov.pl/krs/openApi")]


def get_mf_openbudget_files() -> list[tuple[str, str]]:
    """MF OpenBudget datasets catalogue."""
    return [("datasets.json", "https://openbudget.gov.pl/api/v1/datasets")]


# ---------------------------------------------------------------------------
# Source registry
# ---------------------------------------------------------------------------

SOURCES: dict[str, dict] = {
    # GUS
    "gus_dbw_hvd_bulk": {"fetch": get_gus_hvd_files,                              "workers": 8},
    "gus_dbw_api":     {"fetch": lambda: [("area_tree.json", "https://api-dbw.stat.gov.pl/api/1.1.0/area/area-area")], "workers": 1},
    "gus_bdl_api":     {"fetch": lambda: [("subjects.json",  "https://bdl.stat.gov.pl/api/v1/subjects?lang=pl")],      "workers": 1},
    "gus_teryt_bulk":  {"fetch": get_gus_teryt_files,                             "workers": 4},
    "gus_sdg_bulk":    {"fetch": get_gus_sdg_files,                               "workers": 2},
    "gus_biuletyn_bulk": {"fetch": get_gus_biuletyn_files,                        "workers": 4},
    # Institutional
    "eurostat_bulk": {"fetch": get_eurostat_files,                              "workers": 12},
    "mf_api":        {"fetch": get_mf_openbudget_files,                         "workers": 2},
    "mf_bulk":       {"fetch": lambda: _dane_gov_institution("18", "mf_bulk"),  "workers": 4},
    "nbp_bulk":      {"fetch": get_nbp_files,                                   "workers": 4},
    "nfz_bulk":      {"fetch": lambda: _dane_gov_institution("31", "nfz_bulk"), "workers": 4},
    "zus_bulk":      {"fetch": lambda: _dane_gov_institution("47", "zus_bulk"), "workers": 4},
    "men_api":       {"fetch": lambda: _dane_gov_institution("15", "men_api"),  "workers": 4},
    "gddkia_bulk":   {"fetch": lambda: _dane_gov_institution("106", "gddkia_bulk"), "workers": 4},
    "ure_bulk":      {"fetch": lambda: _dane_gov_institution("58", "ure_bulk"), "workers": 4},
    "mrirw_api":     {"fetch": lambda: _dane_gov_institution("204", "mrirw_api"), "workers": 4},
    "gios_bulk":     {"fetch": get_gios_files,                                  "workers": 8},
    "gpw_benchmark_bulk": {"fetch": get_gpw_benchmark_files,                    "workers": 4},
    "knf_bulk":      {"fetch": lambda: [("stats_page.html", "https://www.knf.gov.pl/dane_statystyczne")], "workers": 1},
    # API / other
    "saos_api":      {"fetch": get_saos_files,                                  "workers": 2},
    "krs_api":       {"fetch": get_krs_files,                                   "workers": 1},
    "opi_radon_api": {"fetch": get_opi_radon_files,                             "workers": 2},
    "stooq_api":     {"fetch": get_stooq_files,                                 "workers": 1},
}


# ---------------------------------------------------------------------------
# Download engine
# ---------------------------------------------------------------------------

def download_file(url: str, dest: Path) -> bool:
    """Stream url → dest. Skip if exists and non-empty (unless FORCE). Returns True on success."""
    if not FORCE and dest.exists() and dest.stat().st_size > 0:
        return True
    try:
        with requests.get(url, stream=True, timeout=120, headers=HEADERS) as resp:
            if resp.status_code != 200:
                logger.warning(f"HTTP {resp.status_code}: {url}")
                return False
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=131072):
                    if chunk:
                        f.write(chunk)
        if dest.stat().st_size == 0:
            dest.unlink()
            return False
        return True
    except Exception as e:
        logger.error(f"Download failed {url}: {e}")
        if dest.exists():
            dest.unlink()
        return False


def process_source(source_id: str, config: dict) -> dict:
    target_dir = LANDING_DIR / source_id
    target_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"[{source_id}] Building catalogue...")
    try:
        files = config["fetch"]()
    except Exception as e:
        logger.error(f"[{source_id}] Catalogue failed: {e}")
        return {"source": source_id, "total": 0, "ok": 0, "failed": 0}

    if not files:
        logger.info(f"[{source_id}] No files (source skipped or empty)")
        return {"source": source_id, "total": 0, "ok": 0, "failed": 0}

    logger.info(f"[{source_id}] {len(files)} files, {config['workers']} workers")
    ok = failed = 0

    with ThreadPoolExecutor(max_workers=config["workers"]) as ex:
        futures = {
            ex.submit(download_file, url, target_dir / filename): filename
            for filename, url in files
        }
        for future in as_completed(futures):
            if future.result():
                ok += 1
            else:
                failed += 1

    # Write status file
    status = {
        "source": source_id, "total": len(files), "ok": ok, "failed": failed,
        "last_bulk_run": datetime.utcnow().isoformat() + "Z"
    }
    (target_dir / ".status.json").write_text(json.dumps(status, indent=2))

    logger.info(f"[{source_id}] {ok} ok  {failed} failed  (of {len(files)} total)")
    return status


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = args if args else list(SOURCES.keys())
    selected = {k: SOURCES[k] for k in targets if k in SOURCES}
    unknown = [k for k in targets if k not in SOURCES]
    if unknown:
        logger.warning(f"Unknown sources (ignored): {unknown}")

    mode = "FORCE re-download" if FORCE else "skip existing"
    logger.info(f"Bulk ingestion: {list(selected.keys())} | {mode} | source_workers={SOURCE_WORKERS}")

    results = []
    with ThreadPoolExecutor(max_workers=SOURCE_WORKERS) as ex:
        futures = {ex.submit(process_source, sid, cfg): sid for sid, cfg in selected.items()}
        for future in as_completed(futures):
            results.append(future.result())

    logger.info("=" * 60)
    logger.info("BULK INGESTION SUMMARY")
    logger.info("=" * 60)
    total_ok = total_failed = 0
    for r in sorted(results, key=lambda x: x["source"]):
        logger.info(f"  {r['source']:20}  {r['ok']:5} ok  {r['failed']:4} failed  ({r['total']} total)")
        total_ok += r["ok"]
        total_failed += r["failed"]
    logger.info(f"  {'TOTAL':20}  {total_ok:5} ok  {total_failed:4} failed")


if __name__ == "__main__":
    main()
