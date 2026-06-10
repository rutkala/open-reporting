#!/usr/bin/env python3
"""
Incremental daily ingestion — fetches only new/updated data via APIs since last run.
Writes delta files to /opt/open-reporting/data/landing/<source>/incremental/

Run nightly via cron. Idempotent — re-running the same day is a no-op.

Usage:
  python3 run_incremental.py              # all sources
  python3 run_incremental.py nbp eurostat # specific sources only
"""

import json
import logging
import os
import sys
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv

load_dotenv(override=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

LANDING_DIR = Path("/opt/open-reporting/data/landing")
HEADERS = {"User-Agent": "OpenReporting-DataPipeline/1.0 (open-reporting.dev)"}
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
YESTERDAY = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")


def _state_file(source_id: str) -> Path:
    return LANDING_DIR / source_id / "incremental" / ".state.json"


def _load_state(source_id: str) -> dict:
    f = _state_file(source_id)
    if f.exists():
        try:
            return json.loads(f.read_text())
        except Exception:
            pass
    return {}


def _save_state(source_id: str, state: dict):
    f = _state_file(source_id)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(state, indent=2))


def _write_delta(source_id: str, filename: str, content: bytes) -> Path:
    dest = LANDING_DIR / source_id / "incremental" / filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)
    return dest


# ---------------------------------------------------------------------------
# Per-source incremental fetchers
# ---------------------------------------------------------------------------

def fetch_nbp(state: dict) -> dict:
    """NBP exchange rates — daily table A (multi-currency)."""
    last = state.get("last_date", YESTERDAY)
    url = f"https://api.nbp.pl/api/exchangerates/tables/A/{last}/{TODAY}/?format=json"
    try:
        resp = requests.get(url, timeout=30, headers=HEADERS)
        if resp.status_code == 404:
            logger.info("[nbp] No new rates since last run")
            return {"last_date": TODAY, "rows": 0}
        resp.raise_for_status()
        data = resp.json()
        rows = sum(len(t.get("rates", [])) for t in data)
        _write_delta("nbp", f"rates_A_{TODAY}.json", resp.content)
        logger.info(f"[nbp] {rows} rates fetched for {last}..{TODAY}")
        return {"last_date": TODAY, "rows": rows}
    except Exception as e:
        logger.error(f"[nbp] {e}")
        return state


def fetch_eurostat_recent(state: dict) -> dict:
    """Eurostat — re-fetch datasets updated since last run (via update catalogue)."""
    last = state.get("last_date", YESTERDAY)
    try:
        resp = requests.get(
            "https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en",
            timeout=60, headers=HEADERS
        )
        resp.raise_for_status()
        updated = []
        for line in resp.text.splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) >= 5:
                code = parts[1].strip('"').strip()
                type_val = parts[2].strip('"').strip()
                updated_date = parts[4].strip('"').strip()[:10] if len(parts) > 4 else ""
                if type_val in ("dataset", "table") and code and updated_date >= last:
                    updated.append(code)

        if not updated:
            logger.info(f"[eurostat] No datasets updated since {last}")
            return {"last_date": TODAY, "updated": 0}

        logger.info(f"[eurostat] {len(updated)} datasets updated since {last} — re-fetching")
        ok = failed = 0
        dest_dir = LANDING_DIR / "eurostat"
        dest_dir.mkdir(parents=True, exist_ok=True)

        def _fetch_one(code):
            url = (f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/"
                   f"{code}/?format=TSV&compressed=true")
            dest = dest_dir / f"{code}.tsv.gz"
            try:
                with requests.get(url, stream=True, timeout=120, headers=HEADERS) as r:
                    if r.status_code != 200:
                        return False
                    with open(dest, "wb") as f:
                        for chunk in r.iter_content(131072):
                            if chunk:
                                f.write(chunk)
                return dest.stat().st_size > 0
            except Exception:
                return False

        with ThreadPoolExecutor(max_workers=8) as ex:
            for result in as_completed({ex.submit(_fetch_one, c): c for c in updated}):
                if result.result():
                    ok += 1
                else:
                    failed += 1

        logger.info(f"[eurostat] {ok} updated, {failed} failed")
        return {"last_date": TODAY, "updated": ok}
    except Exception as e:
        logger.error(f"[eurostat] {e}")
        return state


def fetch_gus_bdl(state: dict) -> dict:
    """GUS BDL — subjects tree (structure rarely changes, fetch weekly)."""
    last = state.get("last_date", "2000-01-01")
    days_since = (datetime.now(timezone.utc) - datetime.fromisoformat(last).replace(tzinfo=timezone.utc)).days
    if days_since < 7:
        logger.info(f"[gus_bdl] Last fetch {days_since}d ago — skipping (weekly)")
        return state
    try:
        resp = requests.get(
            "https://bdl.stat.gov.pl/api/v1/subjects?lang=pl", timeout=30, headers=HEADERS
        )
        resp.raise_for_status()
        _write_delta("gus_bdl", f"subjects_{TODAY}.json", resp.content)
        logger.info(f"[gus_bdl] Subjects tree refreshed")
        return {"last_date": TODAY}
    except Exception as e:
        logger.error(f"[gus_bdl] {e}")
        return state


def fetch_gios(state: dict) -> dict:
    """GIOŚ — current air quality readings for all stations."""
    base = "https://api.gios.gov.pl/pjp-api/v1/rest"
    try:
        stations_resp = requests.get(f"{base}/station/findAll", timeout=20, headers=HEADERS)
        stations_resp.raise_for_status()
        stations = stations_resp.json().get("Lista stacji pomiarów", [])

        readings = {}
        for station in stations:
            sid = station.get("Identyfikator stacji")
            if not sid:
                continue
            try:
                r = requests.get(f"{base}/aqindex/getIndex/{sid}", timeout=10, headers=HEADERS)
                if r.status_code == 200:
                    readings[sid] = r.json()
            except Exception:
                pass

        _write_delta("gios", f"aq_index_{TODAY}.json", json.dumps(readings).encode())
        logger.info(f"[gios] {len(readings)} station readings for {TODAY}")
        return {"last_date": TODAY, "stations": len(readings)}
    except Exception as e:
        logger.error(f"[gios] {e}")
        return state


def fetch_dane_gov_updates(source_id: str, institution_id: str, state: dict) -> dict:
    """dane.gov.pl — check for new/updated resources since last run."""
    last = state.get("last_date", YESTERDAY)
    base = "https://api.dane.gov.pl/1.4"
    new_files = 0
    dest_dir = LANDING_DIR / source_id / "incremental"
    dest_dir.mkdir(parents=True, exist_ok=True)
    try:
        resp = requests.get(
            f"{base}/institutions/{institution_id}/datasets",
            params={"sort": "-updated", "per_page": 20},
            timeout=20, headers=HEADERS
        )
        if resp.status_code != 200:
            return state
        for ds in resp.json().get("data", []):
            updated = ds.get("attributes", {}).get("updated", "")[:10]
            if updated < last:
                break
            ds_id = ds.get("id")
            ds_slug = (ds.get("attributes", {}).get("slug") or str(ds_id))[:60]
            res = requests.get(f"{base}/datasets/{ds_id}/resources", params={"per_page": 50},
                               timeout=15, headers=HEADERS)
            if res.status_code == 200:
                for resource in res.json().get("data", []):
                    dl_url = resource.get("attributes", {}).get("download_url", "")
                    if dl_url:
                        raw_name = dl_url.split("/")[-1].split("?")[0][:60]
                        rid = resource.get("id", "x")
                        name = f"{ds_slug}__{raw_name}" if raw_name else f"{ds_slug}__res_{rid}"
                        try:
                            r = requests.get(dl_url, stream=True, timeout=60, headers=HEADERS)
                            if r.status_code == 200:
                                with open(dest_dir / name[:200], "wb") as f:
                                    for chunk in r.iter_content(131072):
                                        if chunk:
                                            f.write(chunk)
                                new_files += 1
                        except Exception:
                            pass
    except Exception as e:
        logger.error(f"[{source_id}] {e}")

    if new_files:
        logger.info(f"[{source_id}] {new_files} new/updated files since {last}")
    else:
        logger.info(f"[{source_id}] No updates since {last}")
    return {"last_date": TODAY, "new_files": new_files}


# ---------------------------------------------------------------------------
# Source registry
# ---------------------------------------------------------------------------

SOURCES: dict[str, callable] = {
    "nbp":           fetch_nbp,
    "eurostat":      fetch_eurostat_recent,
    "gus_bdl":       fetch_gus_bdl,
    "gios":          fetch_gios,
    "mf_dane":       lambda s: fetch_dane_gov_updates("mf_dane",  "18",  s),
    "nfz":           lambda s: fetch_dane_gov_updates("nfz",      "31",  s),
    "zus":           lambda s: fetch_dane_gov_updates("zus",      "47",  s),
    "gddkia":        lambda s: fetch_dane_gov_updates("gddkia",   "106", s),
    "ure":           lambda s: fetch_dane_gov_updates("ure",      "58",  s),
    "mrirw":         lambda s: fetch_dane_gov_updates("mrirw",    "204", s),
}


def run_source(source_id: str, fetcher: callable) -> str:
    state = _load_state(source_id)
    new_state = fetcher(state)
    _save_state(source_id, new_state)
    return source_id


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = args if args else list(SOURCES.keys())
    selected = {k: SOURCES[k] for k in targets if k in SOURCES}
    unknown = [k for k in targets if k not in SOURCES]
    if unknown:
        logger.warning(f"Unknown sources (ignored): {unknown}")

    logger.info(f"Incremental run {TODAY}: {list(selected.keys())}")

    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(run_source, sid, fn): sid for sid, fn in selected.items()}
        for future in as_completed(futures):
            future.result()

    logger.info("Incremental run complete")


if __name__ == "__main__":
    main()
