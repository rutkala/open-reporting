#!/usr/bin/env python3
"""
Ingestion: NBP Exchange Rates
Tool: Python / requests
API: https://api.nbp.pl/api/exchangerates/rates/A/{code}/{startDate}/{endDate}/?format=json
Update method: upsert on (currency_code, rate_date)
Schema: raw.nbp_exchange_rates
Catalogue:
  detail_id  : fin.exchange_rate_usd_pln   series_id: exchangerates/rates/A/USD  verified: true
  detail_id  : fin.exchange_rate_eur_pln   series_id: exchangerates/rates/A/EUR  verified: true
  detail_id  : fin.exchange_rate_chf_pln   series_id: exchangerates/rates/A/CHF  verified: true
  detail_id  : fin.exchange_rate_gbp_pln   series_id: exchangerates/rates/A/GBP  verified: true
  source_id  : nbp
Usage:
  PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/nbp_exchange_rates.py
  PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/nbp_exchange_rates.py --backfill
Notes:
  - NBP API max window: 93 days per request. Backfill paginates in 90-day chunks.
  - Exchange rates are published on business days only (Mon–Fri, no public holidays).
  - Default (no flag): fetches from last loaded date to today, or last 30 days if table empty.
"""
import argparse
import logging
import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import duckdb
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

API_BASE = "https://api.nbp.pl/api/exchangerates/rates/A"
CURRENCIES = ["USD", "EUR", "CHF", "GBP"]
CHUNK_DAYS = 90          # stay under NBP's 93-day hard limit
BACKFILL_FROM = {        # year_from per currency from catalogue
    "USD": date(2002, 1, 2),
    "EUR": date(2004, 1, 2),
    "CHF": date(2002, 1, 2),
    "GBP": date(2002, 1, 2),
}
RETRY_WAIT = 2           # seconds between retries on 429


def _db() -> duckdb.DuckDBPyConnection:
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path)


def _date_chunks(start: date, end: date) -> list[tuple[date, date]]:
    """Split [start, end] into CHUNK_DAYS-sized intervals."""
    chunks = []
    current = start
    while current <= end:
        chunk_end = min(current + timedelta(days=CHUNK_DAYS - 1), end)
        chunks.append((current, chunk_end))
        current = chunk_end + timedelta(days=1)
    return chunks


def fetch_rates(code: str, start: date, end: date) -> list[dict]:
    """Fetch NBP Table A rates for one currency over a date range."""
    url = f"{API_BASE}/{code}/{start.isoformat()}/{end.isoformat()}/?format=json"
    for attempt in range(3):
        resp = requests.get(url, timeout=30)
        if resp.status_code == 404:
            # No data published for this period (e.g. all public holidays)
            return []
        if resp.status_code == 429:
            log.warning("Rate limited — waiting %ds", RETRY_WAIT)
            time.sleep(RETRY_WAIT)
            continue
        resp.raise_for_status()
        data = resp.json()
        return [
            {
                "currency_code": code,
                "rate_date": r["effectiveDate"],
                "mid_rate": r["mid"],
                "table_no": r["no"],
            }
            for r in data["rates"]
        ]
    resp.raise_for_status()
    return []


def last_loaded_date(conn: duckdb.DuckDBPyConnection, code: str) -> date | None:
    """Return the most recent rate_date for this currency, or None if empty."""
    row = conn.execute(
        "SELECT MAX(rate_date) FROM raw.nbp_exchange_rates WHERE currency_code = ?",
        [code],
    ).fetchone()
    return row[0] if row and row[0] else None


def upsert(conn: duckdb.DuckDBPyConnection, rows: list[dict]) -> int:
    if not rows:
        return 0
    conn.executemany(
        """
        INSERT OR REPLACE INTO raw.nbp_exchange_rates
            (currency_code, rate_date, mid_rate, table_no, fetched_at)
        VALUES (?, ?, ?, ?, NOW())
        """,
        [(r["currency_code"], r["rate_date"], r["mid_rate"], r["table_no"]) for r in rows],
    )
    return len(rows)


def validate(conn: duckdb.DuckDBPyConnection) -> None:
    row = conn.execute(
        "SELECT COUNT(*), MIN(rate_date), MAX(rate_date) FROM raw.nbp_exchange_rates"
    ).fetchone()
    log.info("Validation: %d rows, dates %s – %s", row[0], row[1], row[2])
    for code in CURRENCIES:
        row = conn.execute(
            "SELECT COUNT(*), MAX(rate_date) FROM raw.nbp_exchange_rates WHERE currency_code = ?",
            [code],
        ).fetchone()
        log.info("  %s: %d rows, latest %s", code, row[0], row[1])
    nulls = conn.execute(
        "SELECT COUNT(*) FROM raw.nbp_exchange_rates WHERE mid_rate IS NULL OR rate_date IS NULL"
    ).fetchone()[0]
    if nulls:
        log.error("Validation FAILED: %d rows with null required columns", nulls)
        sys.exit(1)
    log.info("Validation passed")


def run(backfill: bool = False) -> None:
    conn = _db()
    today = date.today()
    total_upserted = 0

    for code in CURRENCIES:
        if backfill:
            start = BACKFILL_FROM[code]
        else:
            last = last_loaded_date(conn, code)
            start = (last + timedelta(days=1)) if last else (today - timedelta(days=30))

        if start > today:
            log.info("%s: already up to date (last loaded: %s)", code, start - timedelta(days=1))
            continue

        chunks = _date_chunks(start, today)
        log.info("%s: fetching %s → %s (%d chunks)", code, start, today, len(chunks))

        for chunk_start, chunk_end in chunks:
            rows = fetch_rates(code, chunk_start, chunk_end)
            n = upsert(conn, rows)
            total_upserted += n
            log.info("  %s %s–%s: %d rows upserted", code, chunk_start, chunk_end, n)

    log.info("Total upserted: %d rows", total_upserted)
    validate(conn)
    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest NBP exchange rates into raw.nbp_exchange_rates")
    parser.add_argument("--backfill", action="store_true", help="Fetch full history from catalogue year_from")
    args = parser.parse_args()
    run(backfill=args.backfill)


if __name__ == "__main__":
    main()
