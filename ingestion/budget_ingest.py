"""
Ingests Polish voivodship budget data from GUS BDL API into PostgreSQL raw schema.

Variables pulled:
  6454 - Dochody budżetów województw (total revenues)
  6476 - Wydatki z budżetu (total expenditures)

Budget balance is calculated as revenues - expenditures.

Usage:
  pip install requests psycopg2-binary python-dotenv
  BDL_API_KEY=your_key python ingestion/budget_ingest.py
"""

import os
import time
import logging
import requests
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# --- Config ---
API_BASE = "https://bdl.stat.gov.pl/api/v1"
API_KEY  = os.environ.get("BDL_API_KEY", "")

VARIABLES = {
    "revenues":     6454,
    "expenditures": 6476,
}

DB_DSN = (
    f"host={os.environ.get('POSTGRES_HOST', 'localhost')} "
    f"port={os.environ.get('POSTGRES_PORT', '5432')} "
    f"dbname={os.environ.get('POSTGRES_DB', 'reporting')} "
    f"user={os.environ.get('POSTGRES_USER', 'reporting')} "
    f"password={os.environ.get('POSTGRES_PASSWORD', '')}"
)

# Voivodship unit IDs (NUTS-2 level, 16 regions)
# These are the BDL unit codes for each voivodship
VOIVODSHIP_LEVEL = 2  # administrative level = województwo


def bdl_get(path, params=None):
    """GET from BDL API with retry on rate limit."""
    headers = {"X-ClientId": API_KEY} if API_KEY else {}
    params = params or {}
    params["format"] = "json"

    for attempt in range(3):
        r = requests.get(f"{API_BASE}{path}", headers=headers, params=params, timeout=30)
        if r.status_code == 429:
            wait = 10 * (attempt + 1)
            log.warning(f"Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"Failed after retries: {path}")


def fetch_variable_data(variable_id):
    """Fetch all pages of data for a variable at voivodship level."""
    rows = []
    page = 0
    page_size = 100

    while True:
        data = bdl_get(
            f"/data/by-variable/{variable_id}",
            params={"unit-level": VOIVODSHIP_LEVEL, "page": page, "page-size": page_size},
        )

        results = data.get("results", [])
        if not results:
            break

        for unit in results:
            unit_id   = unit["id"]
            unit_name = unit["name"]
            for val in unit.get("values", []):
                rows.append({
                    "variable_id": variable_id,
                    "unit_id":     unit_id,
                    "unit_name":   unit_name,
                    "year":        val["year"],
                    "value":       val.get("val"),
                    "flag":        val.get("attrId"),
                })

        total_pages = data.get("totalPages", 1)
        log.info(f"  variable {variable_id}: page {page+1}/{total_pages}, {len(results)} units")
        page += 1
        if page >= total_pages:
            break
        time.sleep(0.3)

    return rows


def setup_schema(cur):
    cur.execute("CREATE SCHEMA IF NOT EXISTS raw")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.bdl_budget (
            id            SERIAL PRIMARY KEY,
            variable_id   INTEGER      NOT NULL,
            variable_name TEXT         NOT NULL,
            unit_id       TEXT         NOT NULL,
            unit_name     TEXT         NOT NULL,
            year          INTEGER      NOT NULL,
            value         NUMERIC,
            flag          TEXT,
            loaded_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
            UNIQUE (variable_id, unit_id, year)
        )
    """)


def upsert_rows(cur, variable_name, rows):
    if not rows:
        return 0

    records = [
        (
            r["variable_id"],
            variable_name,
            r["unit_id"],
            r["unit_name"],
            r["year"],
            r["value"],
            r["flag"],
        )
        for r in rows
    ]

    execute_values(
        cur,
        """
        INSERT INTO raw.bdl_budget
            (variable_id, variable_name, unit_id, unit_name, year, value, flag)
        VALUES %s
        ON CONFLICT (variable_id, unit_id, year)
        DO UPDATE SET
            value     = EXCLUDED.value,
            flag      = EXCLUDED.flag,
            loaded_at = NOW()
        """,
        records,
    )
    return len(records)


def main():
    log.info("Starting GUS BDL budget ingestion")
    if not API_KEY:
        log.warning("BDL_API_KEY not set — requests may be rate-limited")

    conn = psycopg2.connect(DB_DSN)
    conn.autocommit = False

    with conn:
        with conn.cursor() as cur:
            setup_schema(cur)
            log.info("Schema ready")

            for name, var_id in VARIABLES.items():
                log.info(f"Fetching {name} (variable {var_id})...")
                rows = fetch_variable_data(var_id)
                count = upsert_rows(cur, name, rows)
                log.info(f"  Upserted {count} rows for {name}")

    conn.close()
    log.info("Done.")


if __name__ == "__main__":
    main()
