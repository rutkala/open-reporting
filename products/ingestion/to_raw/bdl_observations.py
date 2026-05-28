#!/usr/bin/env python3
"""
Ingestion: GUS BDL (Bank Danych Lokalnych) REST API → raw.bdl_observations
Tool: Python / requests
API: https://bdl.stat.gov.pl/api/v1/
Update method: upsert on (variable_id, unit_id, year)
Schema: raw.bdl_observations
Catalogue: reads hard-coded VARIABLES list (BDL variable IDs)
Usage:
  PYTHONPATH=/opt/open-reporting python3 products/ingestion/to_raw/bdl_observations.py
  PYTHONPATH=/opt/open-reporting python3 products/ingestion/to_raw/bdl_observations.py --variable 72305
  PYTHONPATH=/opt/open-reporting python3 products/ingestion/to_raw/bdl_observations.py --backfill
Notes:
  - Authentication: X-ClientId header, key from BDL_API_KEY env var.
  - Unit levels fetched: 5 (national aggregate) and 2 (voivodeship / NUTS2).
  - Default run fetches the last DEFAULT_YEARS calendar years (fast daily refresh).
  - --backfill fetches the full available history for each variable.
  - --variable restricts to a single BDL variable ID.
  - Pagination: BDL API returns max PAGE_SIZE rows per page; loop until exhausted.
  - Missing variables (404 from the API) are skipped with a warning — do not hard-fail.
  - Register a free API key at: https://api.stat.gov.pl/Home/BdlApi
"""
import argparse
import logging
import os
import sys
import time
from datetime import date

import duckdb
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

BDL_BASE    = "https://bdl.stat.gov.pl/api/v1"
PAGE_SIZE   = 100
RETRY_WAIT  = 5      # seconds to wait after HTTP 429
MAX_RETRIES = 3

# Initial set of high-value BDL variable IDs.
# Keys are variable_id (int); comments describe subject and indicator name.
VARIABLES = [
    72305,    # Ludność — Ludność ogółem (total population)
    76498,    # Rynek pracy — Stopa bezrobocia rejestrowanego (registered unemployment rate)
    64428,    # Wynagrodzenia — Przeciętne wynagrodzenie brutto (average gross wage)
    454571,   # Urodzenia — Urodzenia żywe na 1000 ludności (live births per 1000)
    454576,   # Zgony — Zgony na 1000 ludności (deaths per 1000)
]

# Unit levels to fetch in every run.
# 5 = national aggregate (Poland as a whole)
# 2 = voivodeship (NUTS2 equivalent, 16 units)
UNIT_LEVELS = [5, 2]

DEFAULT_YEARS = 5   # how many recent calendar years to fetch in normal (non-backfill) mode


# ── DuckDB connection ──────────────────────────────────────────────────────────

def _db() -> duckdb.DuckDBPyConnection:
    """Open DuckDB connection lazily — reads DUCKDB_PATH only at call time."""
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path)


# ── DDL bootstrap ──────────────────────────────────────────────────────────────

def ensure_table(conn: duckdb.DuckDBPyConnection) -> None:
    """Create raw.bdl_observations if it does not already exist."""
    ddl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bdl_observations.sql")
    with open(ddl_path) as fh:
        conn.execute(fh.read())
    log.info("Table raw.bdl_observations ensured")


# ── BDL API helpers ────────────────────────────────────────────────────────────

def _headers() -> dict[str, str]:
    """Return request headers with BDL API key."""
    return {"X-ClientId": os.environ["BDL_API_KEY"], "Accept": "application/json"}


def _get(url: str, params: dict | None = None) -> dict | None:
    """
    HTTP GET with retry on 429 (rate limit) and graceful handling of 404.
    Returns the parsed JSON body, or None on 404 (variable/unit not found).
    Raises for all other non-2xx responses after MAX_RETRIES attempts.
    """
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=_headers(), params=params, timeout=30)
        except requests.exceptions.Timeout:
            log.warning("Request timed out (attempt %d/%d): %s", attempt + 1, MAX_RETRIES, url)
            if attempt + 1 == MAX_RETRIES:
                raise
            time.sleep(RETRY_WAIT)
            continue

        if resp.status_code == 404:
            return None
        if resp.status_code == 429:
            log.warning("Rate limited — waiting %ds (attempt %d/%d)", RETRY_WAIT, attempt + 1, MAX_RETRIES)
            time.sleep(RETRY_WAIT)
            continue
        resp.raise_for_status()
        return resp.json()

    # Exhausted retries without a successful response
    resp.raise_for_status()
    return None


# ── Fetching units ─────────────────────────────────────────────────────────────

def fetch_units(unit_level: int) -> list[dict]:
    """
    Return all administrative units at the given level.
    Each dict has: {id, name, nuts_code (may be None)}.
    Paginates until all units are collected.
    """
    units: list[dict] = []
    page = 0
    while True:
        data = _get(f"{BDL_BASE}/units", params={"level": unit_level, "page": page, "pageSize": PAGE_SIZE})
        if data is None:
            log.warning("Units endpoint returned 404 for level %d", unit_level)
            break
        results = data.get("results", [])
        for u in results:
            units.append({
                "id":        str(u["id"]),
                "name":      u.get("name"),
                # NUTS code field name varies across BDL API versions; try both.
                "nuts_code": u.get("nutsId") or u.get("nuts") or None,
            })
        total = data.get("totalRecords", 0)
        log.debug("Units level=%d page=%d: got %d of %d", unit_level, page, len(units), total)
        if len(units) >= total or not results:
            break
        page += 1
    log.info("Fetched %d units at level %d", len(units), unit_level)
    return units


# ── Fetching observations ──────────────────────────────────────────────────────

def fetch_variable_for_level(
    variable_id: int,
    unit_level: int,
    year_from: int | None = None,
) -> list[dict]:
    """
    Fetch all observations for one variable × unit_level combination.

    Returns a flat list of dicts:
      {variable_id, unit_id, unit_name, nuts_code, year, value}

    year_from: if provided, only include observations where year >= year_from.
    The BDL API does not support server-side year filtering on this endpoint,
    so filtering is applied client-side.

    Returns empty list if the variable does not exist (404).
    """
    # First fetch the unit metadata for this level so we have nuts_code per unit.
    units_meta = {u["id"]: u for u in fetch_units(unit_level)}
    if not units_meta:
        return []

    rows: list[dict] = []
    page = 0
    total_records: int | None = None

    while True:
        data = _get(
            f"{BDL_BASE}/data/by-variable/{variable_id}",
            params={"unitLevel": unit_level, "page": page, "pageSize": PAGE_SIZE},
        )
        if data is None:
            log.warning("Variable %d not found at unitLevel=%d (404) — skipping", variable_id, unit_level)
            return []

        results = data.get("results", [])
        if total_records is None:
            total_records = data.get("totalRecords", 0)

        for result in results:
            uid = str(result["id"])
            unit_info = units_meta.get(uid, {})
            unit_name = result.get("name") or unit_info.get("name")
            nuts_code = unit_info.get("nuts_code")

            for entry in result.get("values", []):
                yr = entry.get("year")
                val = entry.get("val")
                if yr is None:
                    continue
                if year_from is not None and yr < year_from:
                    continue
                rows.append({
                    "variable_id": variable_id,
                    "unit_id":     uid,
                    "unit_name":   unit_name,
                    "nuts_code":   nuts_code,
                    "year":        yr,
                    # val can be None (suppressed/missing) — preserve as NULL
                    "value":       float(val) if val is not None else None,
                })

        collected_units = (page + 1) * PAGE_SIZE
        log.debug(
            "  variable=%d level=%d page=%d: %d rows so far (total_records=%d)",
            variable_id, unit_level, page, len(rows), total_records,
        )
        if not results or (total_records is not None and collected_units >= total_records):
            break
        page += 1

    return rows


# ── DuckDB upsert ──────────────────────────────────────────────────────────────

def upsert(conn: duckdb.DuckDBPyConnection, rows: list[dict]) -> int:
    """Upsert rows into raw.bdl_observations. Returns number of rows processed."""
    if not rows:
        return 0
    conn.executemany(
        """
        INSERT INTO raw.bdl_observations
            (variable_id, unit_id, unit_name, nuts_code, year, value, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?, NOW())
        ON CONFLICT (variable_id, unit_id, year) DO UPDATE SET
            unit_name  = EXCLUDED.unit_name,
            nuts_code  = EXCLUDED.nuts_code,
            value      = EXCLUDED.value,
            fetched_at = NOW()
        """,
        [
            (r["variable_id"], r["unit_id"], r["unit_name"],
             r["nuts_code"], r["year"], r["value"])
            for r in rows
        ],
    )
    return len(rows)


# ── Validation ─────────────────────────────────────────────────────────────────

def validate(conn: duckdb.DuckDBPyConnection) -> None:
    """Log basic quality metrics for raw.bdl_observations after ingestion."""
    row = conn.execute(
        "SELECT COUNT(*), COUNT(DISTINCT variable_id), MIN(year), MAX(year) "
        "FROM raw.bdl_observations"
    ).fetchone()
    log.info(
        "Validation: %d observations, %d variables, years %s – %s",
        row[0], row[1], row[2], row[3],
    )
    nulls = conn.execute(
        "SELECT COUNT(*) FROM raw.bdl_observations WHERE value IS NULL"
    ).fetchone()[0]
    if nulls:
        log.info("%d rows with NULL value (suppressed/missing at source — expected)", nulls)
    log.info("Validation passed")


# ── Main pipeline ──────────────────────────────────────────────────────────────

def run(variable_filter: int | None = None, backfill: bool = False) -> None:
    """
    Fetch BDL observations and upsert into raw.bdl_observations.

    variable_filter: if provided, only this variable_id is fetched.
    backfill: if True, fetch full history; otherwise only the last DEFAULT_YEARS years.
    """
    api_key = os.environ.get("BDL_API_KEY", "").strip()
    if not api_key:
        log.error(
            "BDL_API_KEY is not set. Register a free key at https://api.stat.gov.pl/Home/BdlApi "
            "and add it to .env as BDL_API_KEY=<your_key>"
        )
        sys.exit(1)

    variables = [variable_filter] if variable_filter is not None else VARIABLES
    year_from = None if backfill else (date.today().year - DEFAULT_YEARS + 1)

    conn = _db()
    ensure_table(conn)

    total_upserted = 0
    mode = "backfill (full history)" if backfill else f"last {DEFAULT_YEARS} years (from {year_from})"
    log.info("Starting BDL ingestion: %d variable(s), mode=%s", len(variables), mode)

    for var_id in variables:
        log.info("Variable %d: fetching...", var_id)
        variable_total = 0

        for level in UNIT_LEVELS:
            log.info("  variable=%d unitLevel=%d", var_id, level)
            try:
                rows = fetch_variable_for_level(var_id, level, year_from=year_from)
            except requests.exceptions.HTTPError as exc:
                log.warning("HTTP error for variable=%d level=%d: %s — skipping", var_id, level, exc)
                continue

            if not rows:
                log.info("  variable=%d level=%d: no data returned", var_id, level)
                continue

            n = upsert(conn, rows)
            variable_total += n
            log.info("  variable=%d level=%d: %d rows upserted", var_id, level, n)

        log.info("Variable %d complete: %d rows total", var_id, variable_total)
        total_upserted += variable_total

    log.info("BDL ingestion complete — total upserted: %d rows", total_upserted)
    if total_upserted:
        validate(conn)
    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest GUS BDL observations into raw.bdl_observations"
    )
    parser.add_argument(
        "--variable",
        type=int,
        metavar="VARIABLE_ID",
        help="Fetch a single BDL variable ID only (e.g. --variable 72305)",
    )
    parser.add_argument(
        "--backfill",
        action="store_true",
        help=f"Fetch full history (default: last {DEFAULT_YEARS} years)",
    )
    args = parser.parse_args()
    run(variable_filter=args.variable, backfill=args.backfill)


if __name__ == "__main__":
    main()
