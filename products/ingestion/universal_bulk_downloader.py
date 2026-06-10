#!/usr/bin/env python3
"""
Parallel bulk downloader for all identified Polish & EU data sources.
Files land in /opt/open-reporting/data/landing/<source>/<filename>

Usage:
  python3 universal_bulk_downloader.py               # all sources
  python3 universal_bulk_downloader.py eurostat gus_hvd  # specific sources only
"""

import logging
import re
import sys
import time
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

from dotenv import load_dotenv

load_dotenv(override=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

LANDING_DIR = Path("/opt/open-reporting/data/landing")
SOURCE_WORKERS = 4    # sources processed in parallel
DANE_GOV_BASE = "https://api.dane.gov.pl/1.4"
HEADERS = {"User-Agent": "OpenReporting-DataPipeline/1.0 (open-reporting.dev)"}


# ---------------------------------------------------------------------------
# Catalogue parsers — each returns list[(filename, url)]
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
    """All files from GUS DBW HVD bulk catalogue, named by original filename."""
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
            ds_slug = ds.get("attributes", {}).get("slug", str(ds_id))
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
                            raw_name = dl_url.split("/")[-1].split("?")[0]
                            rid = resource.get("id", "x")
                            filename = f"{ds_slug}__{raw_name}" if raw_name else f"{ds_slug}__res_{rid}"
                            result.append((filename, dl_url))
            except Exception:
                pass

        meta = data.get("meta", {})
        if page >= meta.get("last_page", 1):
            break
        page += 1
        time.sleep(0.2)

    logger.info(f"[{source_id}] dane.gov.pl: {len(result)} resources")
    return result


def get_nbp_files() -> list[tuple[str, str]]:
    """NBP statistical XLSX/CSV bulk files from key statistics pages."""
    pages = [
        "https://nbp.pl/statystyka-i-sprawozdawczosc/statystyka-monetarna-i-finansowa/miary-pieniadza-i-indeksy-divisia/",
        "https://nbp.pl/statystyka-i-sprawozdawczosc/kursy/archiwalne-kursy-walut/",
        "https://nbp.pl/statystyka-i-sprawozdawczosc/statystyka-monetarna-i-finansowa/",
    ]
    result = []
    seen = set()
    for page_url in pages:
        try:
            resp = requests.get(page_url, timeout=15, headers=HEADERS)
            matches = re.findall(r'href="([^"]+\.(?:xlsx?|csv))"', resp.text, re.IGNORECASE)
            for m in matches:
                full = m if m.startswith("http") else urljoin("https://nbp.pl", m)
                fname = full.split("/")[-1]
                if full not in seen:
                    seen.add(full)
                    result.append((fname, full))
        except Exception as e:
            logger.warning(f"[nbp] {page_url}: {e}")
    logger.info(f"[nbp] found {len(result)} files")
    return result


def get_stooq_files() -> list[tuple[str, str]]:
    """Daily OHLCV CSV for key Polish market indices from Stooq."""
    tickers = [
        "wig20", "wig", "mwig40", "swig80",
        "wig_banki", "wig_energia", "wig_spozywczy", "wig_budow", "wig_telkom",
    ]
    return [(f"{t}_daily.csv", f"https://stooq.pl/q/d/l/?s={t}&i=d") for t in tickers]


def get_gios_files() -> list[tuple[str, str]]:
    """GIOŚ: station index + per-station sensor list."""
    result = [("stations.json", "https://api.gios.gov.pl/pjp-api/rest/station/findAll")]
    try:
        resp = requests.get(
            "https://api.gios.gov.pl/pjp-api/rest/station/findAll", timeout=20, headers=HEADERS
        )
        for station in resp.json():
            sid = station.get("id")
            if sid:
                result.append((
                    f"sensors_station_{sid}.json",
                    f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{sid}"
                ))
    except Exception as e:
        logger.warning(f"[gios] stations: {e}")
    logger.info(f"[gios] {len(result)} endpoints")
    return result


def get_gpw_benchmark_files() -> list[tuple[str, str]]:
    """GPW Benchmark: WIBOR/WIBID fixing files."""
    # Historical fixings published as downloadable CSVs
    return [
        ("wibor_on.csv",  "https://gpwbenchmark.pl/pobierz/WIBOR_ON.csv"),
        ("wibor_1w.csv",  "https://gpwbenchmark.pl/pobierz/WIBOR_1W.csv"),
        ("wibor_1m.csv",  "https://gpwbenchmark.pl/pobierz/WIBOR_1M.csv"),
        ("wibor_3m.csv",  "https://gpwbenchmark.pl/pobierz/WIBOR_3M.csv"),
        ("wibor_6m.csv",  "https://gpwbenchmark.pl/pobierz/WIBOR_6M.csv"),
        ("wibor_12m.csv", "https://gpwbenchmark.pl/pobierz/WIBOR_12M.csv"),
        ("wibid_on.csv",  "https://gpwbenchmark.pl/pobierz/WIBID_ON.csv"),
        ("wibid_1m.csv",  "https://gpwbenchmark.pl/pobierz/WIBID_1M.csv"),
        ("wibid_3m.csv",  "https://gpwbenchmark.pl/pobierz/WIBID_3M.csv"),
        ("wibid_6m.csv",  "https://gpwbenchmark.pl/pobierz/WIBID_6M.csv"),
    ]


def get_saos_files() -> list[tuple[str, str]]:
    """SAOS: first page of court judgments (REST paged — catalogue only)."""
    return [
        ("judgments_p0.json", "https://saos.org.pl/api/judgments?pageSize=100&pageNumber=0"),
        ("judgments_p1.json", "https://saos.org.pl/api/judgments?pageSize=100&pageNumber=1"),
        ("courts.json",       "https://saos.org.pl/api/courts"),
    ]


def get_krs_files() -> list[tuple[str, str]]:
    """KRS OpenAPI spec (schema only — full data requires entity-level queries)."""
    return [("openapi.json", "https://prs.ms.gov.pl/krs/openApi")]


def get_opi_radon_files() -> list[tuple[str, str]]:
    """OPI RAD-on: institutions and universities catalogue."""
    return [
        ("institutions.json", "https://radon.nauka.gov.pl/opendata/polon/institutions"),
        ("universities.json", "https://radon.nauka.gov.pl/opendata/polon/universities"),
        ("institutes.json",   "https://radon.nauka.gov.pl/opendata/polon/institutes"),
    ]


def get_mf_openbudget_files() -> list[tuple[str, str]]:
    """MF OpenBudget: dataset catalogue."""
    return [("datasets.json", "https://openbudget.gov.pl/api/v1/datasets")]


# ---------------------------------------------------------------------------
# Source registry
# ---------------------------------------------------------------------------

SOURCES: dict[str, dict] = {
    "eurostat":      {"fetch": get_eurostat_files,                          "workers": 12},
    "gus_hvd":       {"fetch": get_gus_hvd_files,                           "workers": 8},
    "gus_api":       {"fetch": lambda: [("area_tree.json", "https://api-dbw.stat.gov.pl/api/1.1.0/area/area-area")], "workers": 1},
    "gus_bdl":       {"fetch": lambda: [("subjects.json",  "https://bdl.stat.gov.pl/api/v1/subjects?lang=pl")],      "workers": 1},
    "mf_openbudget": {"fetch": get_mf_openbudget_files,                     "workers": 2},
    "mf_dane":       {"fetch": lambda: _dane_gov_institution("18", "mf_dane"),    "workers": 4},
    "nbp":           {"fetch": get_nbp_files,                               "workers": 4},
    "stooq":         {"fetch": get_stooq_files,                             "workers": 4},
    "nfz":           {"fetch": lambda: _dane_gov_institution("31", "nfz"),        "workers": 4},
    "zus":           {"fetch": lambda: _dane_gov_institution("47", "zus"),        "workers": 4},
    "cie_men":       {"fetch": lambda: _dane_gov_institution("15", "cie_men"),    "workers": 4},
    "gddkia":        {"fetch": lambda: _dane_gov_institution("106", "gddkia"),    "workers": 4},
    "ure":           {"fetch": lambda: _dane_gov_institution("58", "ure"),        "workers": 4},
    "mrirw":         {"fetch": lambda: _dane_gov_institution("204", "mrirw"),     "workers": 4},
    "gios":          {"fetch": get_gios_files,                              "workers": 8},
    "gpw_benchmark": {"fetch": get_gpw_benchmark_files,                     "workers": 4},
    "saos":          {"fetch": get_saos_files,                              "workers": 2},
    "krs":           {"fetch": get_krs_files,                               "workers": 1},
    "opi_radon":     {"fetch": get_opi_radon_files,                         "workers": 2},
    "knf":           {"fetch": lambda: [("stats_page.html", "https://www.knf.gov.pl/dane_statystyczne")], "workers": 1},
}


# ---------------------------------------------------------------------------
# Download engine
# ---------------------------------------------------------------------------

def download_file(url: str, dest: Path) -> bool:
    """Stream download url → dest. Skip if already exists and non-empty. Returns success."""
    if dest.exists() and dest.stat().st_size > 0:
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
        logger.warning(f"[{source_id}] No files found")
        return {"source": source_id, "total": 0, "ok": 0, "failed": 0}

    logger.info(f"[{source_id}] Downloading {len(files)} files ({config['workers']} workers)...")
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

    logger.info(f"[{source_id}] {ok} ok  {failed} failed  (of {len(files)} total)")
    return {"source": source_id, "total": len(files), "ok": ok, "failed": failed}


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(SOURCES.keys())
    selected = {k: SOURCES[k] for k in targets if k in SOURCES}
    unknown = [k for k in targets if k not in SOURCES]
    if unknown:
        logger.warning(f"Unknown sources (ignored): {unknown}")

    logger.info(f"Starting ingestion: {list(selected.keys())} | source_workers={SOURCE_WORKERS}")

    results = []
    with ThreadPoolExecutor(max_workers=SOURCE_WORKERS) as ex:
        futures = {ex.submit(process_source, sid, cfg): sid for sid, cfg in selected.items()}
        for future in as_completed(futures):
            results.append(future.result())

    logger.info("=" * 60)
    logger.info("INGESTION SUMMARY")
    logger.info("=" * 60)
    total_ok = total_failed = 0
    for r in sorted(results, key=lambda x: x["source"]):
        logger.info(f"  {r['source']:20}  {r['ok']:5} ok  {r['failed']:4} failed  ({r['total']} total)")
        total_ok += r["ok"]
        total_failed += r["failed"]
    logger.info(f"  {'TOTAL':20}  {total_ok:5} ok  {total_failed:4} failed")


if __name__ == "__main__":
    main()
