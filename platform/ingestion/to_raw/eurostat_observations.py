#!/usr/bin/env python3
"""
Ingestion: Eurostat SDMX REST API → raw.eurostat_observations
Tool: Python / requests
API: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}?format=JSON&lang=en
Update method: upsert on (dataset_code, geo, period, dimension_key)
Schema: raw.eurostat_observations
Catalogue: reads all rows WHERE source_id='eurostat' AND verified=true
Usage:
  PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/eurostat_observations.py
  PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/eurostat_observations.py --dataset demo_gind
  PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/eurostat_observations.py --backfill
Notes:
  - series_id format: "dataset_code?geo=PL&dim=val&..."
  - Default run fetches only the last 5 periods per dataset (fast daily refresh).
  - --backfill fetches full history (no lastTimePeriod limit).
  - One API call per unique dataset_code; all PL series extracted in one response.
"""
import argparse
import logging
import os
import time
from urllib.parse import urlparse, parse_qs, urlencode

import duckdb
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

EUROSTAT_BASE   = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
GEO             = "PL"
DEFAULT_PERIODS = 5
RETRY_WAIT      = 5

# Special geo sentinel: fetch without geo restriction, keep rows starting with this prefix.
# Used for regional/NUTS2 datasets where geo=PL would only return the national aggregate.
_NUTS2_PREFIX = "PL_NUTS2"

# Special geo sentinel: fetch without geo restriction and keep ALL returned rows.
# Used for multi-country datasets (e.g. GFS) where we want the full EU coverage.
_ALL_GEOS = "ALL_GEOS"


# ── Catalogue ─────────────────────────────────────────────────────────────────

def _pg():
    return psycopg2.connect(
        host="localhost", port=5432, dbname="reporting", user="reporting",
        password=os.environ["POSTGRES_PASSWORD"],
    )


def verified_series(dataset_filter: str | None = None) -> dict[str, list[dict]]:
    """
    Return {dataset_code: [parsed_filters, ...]} for all verified Eurostat entries.
    series_id format: "dataset_code?geo=PL&dim=val&..."
    Deduplicates identical filter sets so we don't fetch the same data twice.
    """
    from urllib.parse import parse_qs
    conn = _pg()
    cur  = conn.cursor()
    sql  = """
        SELECT series_id
        FROM catalogue.domain_detail_sources
        WHERE source_id = 'eurostat' AND verified = true AND series_id IS NOT NULL
    """
    params = []
    if dataset_filter:
        sql += " AND series_id LIKE %s"
        params.append(f"{dataset_filter}?%")
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    # {dataset_code: [(filters_dict, geo_value), ...]}
    by_dataset: dict[str, list[tuple[dict, str]]] = {}
    seen: set[str] = set()
    for (sid,) in rows:
        if sid in seen:
            continue
        seen.add(sid)
        dataset, _, qs = sid.partition("?")
        qs_parsed = parse_qs(qs)
        geo = qs_parsed.get("geo", [GEO])[0]
        filters = {k: v[0] for k, v in qs_parsed.items() if k != "geo"}
        by_dataset.setdefault(dataset, []).append((filters, geo))
    return by_dataset


# ── Eurostat API ──────────────────────────────────────────────────────────────

def _dimension_key(dimensions: dict[str, str]) -> str:
    """Canonical sorted dim=val string, excluding geo/freq/time."""
    skip = {"geo", "freq", "time"}
    return "&".join(f"{k}={v}" for k, v in sorted(dimensions.items()) if k not in skip)


def fetch_dataset(
    dataset_code: str,
    filters: dict,
    geo: str = GEO,
    backfill: bool = False,
) -> list[dict]:
    """
    Fetch observations for a dataset with specific dimension filters.
    Returns list of {dataset_code, geo, period, dimension_key, value, obs_status}.

    geo: geo value to pass to the API, or PL_NUTS2 to fetch all geographies and
         post-filter to rows starting with 'PL' (for NUTS2 regional datasets).
    """
    regional = geo == _NUTS2_PREFIX
    all_geos = geo == _ALL_GEOS
    params: dict = {"format": "JSON", "lang": "en"}
    if not regional and not all_geos:
        params["geo"] = geo
    params.update(filters)
    if not backfill:
        params["lastTimePeriod"] = DEFAULT_PERIODS

    url = f"{EUROSTAT_BASE}/{dataset_code}"

    for attempt in range(3):
        resp = requests.get(url, params=params, timeout=60)
        if resp.status_code == 429:
            log.warning("Rate limited on %s — waiting %ds", dataset_code, RETRY_WAIT)
            time.sleep(RETRY_WAIT)
            continue
        if resp.status_code in (404, 413):
            log.warning("HTTP %d on %s %s", resp.status_code, dataset_code, filters)
            return []
        resp.raise_for_status()
        break

    data = resp.json()
    dim_ids   = data["id"]          # ordered dimension names e.g. ['freq','indic_de','geo','time']
    dim_sizes = data["size"]
    dimensions = data["dimension"]
    values    = data.get("value", {})
    statuses  = data.get("status", {})

    # Build index → category label maps for each dimension
    dim_labels = {}
    for dim in dim_ids:
        cat = dimensions[dim]["category"]
        # index maps category_key → position; invert to position → key
        idx_to_key = {v: k for k, v in cat["index"].items()}
        dim_labels[dim] = idx_to_key

    # Compute strides for flat-index → per-dimension index conversion
    strides = [1] * len(dim_ids)
    for i in range(len(dim_ids) - 2, -1, -1):
        strides[i] = strides[i + 1] * dim_sizes[i + 1]

    rows = []
    for flat_idx_str, value in values.items():
        flat_idx = int(flat_idx_str)
        coords   = {}
        remainder = flat_idx
        for i, dim in enumerate(dim_ids):
            pos = remainder // strides[i]
            remainder %= strides[i]
            coords[dim] = dim_labels[dim].get(pos, str(pos))

        obs_geo = coords.get("geo", GEO)
        period  = coords.get("time", "")
        dim_key = _dimension_key(coords)
        status  = statuses.get(flat_idx_str)

        rows.append({
            "dataset_code":  dataset_code,
            "geo":           obs_geo,
            "period":        period,
            "dimension_key": dim_key,
            "value":         float(value) if value is not None else None,
            "obs_status":    status,
        })

    if regional:
        rows = [r for r in rows if r["geo"].startswith("PL")]
        log.info("  Regional filter: kept %d PL* rows", len(rows))
    elif all_geos:
        log.info("  ALL_GEOS mode: keeping all %d rows", len(rows))

    return rows


# ── DuckDB upsert ─────────────────────────────────────────────────────────────

def _db():
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path)


def upsert(conn: duckdb.DuckDBPyConnection, rows: list[dict]) -> int:
    if not rows:
        return 0
    conn.executemany(
        """
        INSERT OR REPLACE INTO raw.eurostat_observations
            (dataset_code, geo, period, dimension_key, value, obs_status, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?, NOW())
        """,
        [(r["dataset_code"], r["geo"], r["period"], r["dimension_key"],
          r["value"], r["obs_status"]) for r in rows],
    )
    return len(rows)


def validate(conn: duckdb.DuckDBPyConnection) -> None:
    row = conn.execute(
        "SELECT COUNT(*), COUNT(DISTINCT dataset_code), MIN(period), MAX(period) "
        "FROM raw.eurostat_observations"
    ).fetchone()
    log.info(
        "Validation: %d observations across %d datasets, periods %s – %s",
        row[0], row[1], row[2], row[3],
    )
    nulls = conn.execute(
        "SELECT COUNT(*) FROM raw.eurostat_observations WHERE value IS NULL AND obs_status IS NULL"
    ).fetchone()[0]
    if nulls:
        log.warning("%d rows with null value and no status flag", nulls)
    log.info("Validation passed")


# ── Main ──────────────────────────────────────────────────────────────────────

def run(dataset_filter: str | None = None, backfill: bool = False) -> None:
    series_map = verified_series(dataset_filter)
    if not series_map:
        log.warning("No verified Eurostat series found in catalogue. Run Phase 0 first.")
        return

    log.info("Fetching %d datasets: %s", len(series_map), list(series_map.keys()))
    conn = _db()
    total = 0

    for dataset_code, filter_list in series_map.items():
        for filters, geo in filter_list:
            log.info("Fetching %s %s (geo=%s) ...", dataset_code, filters, geo)
            rows = fetch_dataset(dataset_code, filters, geo=geo, backfill=backfill)
            n = upsert(conn, rows)
            total += n
            log.info("  %s: %d observations upserted", dataset_code, n)

    log.info("Total upserted: %d observations", total)
    if total:
        validate(conn)
    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest Eurostat data into raw.eurostat_observations")
    parser.add_argument("--dataset", help="Fetch a single dataset code only")
    parser.add_argument("--backfill", action="store_true", help="Fetch full history (no period limit)")
    args = parser.parse_args()
    run(dataset_filter=args.dataset, backfill=args.backfill)


if __name__ == "__main__":
    main()
