#!/usr/bin/env python3
"""
Dynamic Ingestion Engine
Daemon that automatically checks GUS (BDL) and Eurostat APIs for newly published datasets.
If new data is detected for our tracked domains, it triggers the respective ingestion script
to pull it into data/warehouse.duckdb.
"""
import logging
import os
import subprocess
import sys
import time
from datetime import datetime

import duckdb
import requests
from dotenv import load_dotenv

from products.ingestion.to_raw.bdl_observations import VARIABLES as BDL_VARIABLES
from products.ingestion.to_raw.eurostat_observations import verified_series as eurostat_series

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

CHECK_INTERVAL = 3600  # Check every hour

def _db() -> duckdb.DuckDBPyConnection:
    """Open DuckDB connection lazily — reads DUCKDB_PATH only at call time."""
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path)

def check_bdl():
    log.info("Checking BDL API for new data...")
    try:
        conn = _db()
    except Exception as e:
        log.error("Could not connect to DuckDB: %s", e)
        return
        
    for var_id in BDL_VARIABLES:
        try:
            url = f"https://bdl.stat.gov.pl/api/v1/variables/{var_id}"
            headers = {"X-ClientId": os.environ["BDL_API_KEY"], "Accept": "application/json"}
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code != 200:
                log.warning("BDL variable %s returned %d", var_id, resp.status_code)
                continue
            
            data = resp.json()
            years = data.get("years", [])
            if not years:
                continue
                
            api_max_year = max(years)
            
            try:
                db_max_year_row = conn.execute(
                    "SELECT max(year) FROM raw.bdl_observations WHERE variable_id = ?",
                    [var_id]
                ).fetchone()
                db_max_year = db_max_year_row[0] if db_max_year_row else None
            except duckdb.CatalogException:
                # Table doesn't exist, we should ingest
                db_max_year = None
            
            if db_max_year is None or api_max_year > db_max_year:
                log.info("BDL variable %s has new data (API max: %s, DB max: %s). Triggering ingestion...", var_id, api_max_year, db_max_year)
                subprocess.run(
                    [sys.executable, "products/ingestion/to_raw/bdl_observations.py", "--variable", str(var_id)],
                    check=True,
                    env=dict(os.environ, PYTHONPATH="/opt/open-reporting")
                )
            else:
                log.debug("BDL variable %s is up to date", var_id)
                
        except Exception as e:
            log.error("Error checking BDL variable %s: %s", var_id, e)
            
    conn.close()

def check_eurostat():
    log.info("Checking Eurostat API for new data...")
    try:
        conn = _db()
    except Exception as e:
        log.error("Could not connect to DuckDB: %s", e)
        return

    try:
        datasets = eurostat_series()
    except Exception as e:
        log.error("Could not fetch Eurostat verified series from catalogue: %s", e)
        conn.close()
        return

    for dataset_code in datasets.keys():
        try:
            url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset_code}"
            params = {"format": "JSON", "lang": "en", "lastTimePeriod": 1}
            resp = requests.get(url, params=params, timeout=30)
            if resp.status_code != 200:
                # 404 or 413 or others might mean dataset moved or requires specific params, handled in ingestion script
                log.warning("Eurostat dataset %s returned %d on metadata check", dataset_code, resp.status_code)
                continue
                
            data = resp.json()
            updated_str = data.get("updated")
            if not updated_str:
                continue
            
            try:
                api_updated = datetime.strptime(updated_str, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                log.warning("Eurostat dataset %s returned unknown date format: %s", dataset_code, updated_str)
                continue
            
            try:
                db_fetched_row = conn.execute(
                    "SELECT max(fetched_at) FROM raw.eurostat_observations WHERE dataset_code = ?",
                    [dataset_code]
                ).fetchone()
                db_fetched_at = db_fetched_row[0] if db_fetched_row else None
            except duckdb.CatalogException:
                # Table doesn't exist, we should ingest
                db_fetched_at = None
                
            if db_fetched_at is None or api_updated > db_fetched_at:
                log.info("Eurostat dataset %s has new data (API updated: %s, DB max fetched: %s). Triggering ingestion...", dataset_code, api_updated, db_fetched_at)
                subprocess.run(
                    [sys.executable, "products/ingestion/to_raw/eurostat_observations.py", "--dataset", dataset_code],
                    check=True,
                    env=dict(os.environ, PYTHONPATH="/opt/open-reporting")
                )
            else:
                log.debug("Eurostat dataset %s is up to date", dataset_code)
                
        except Exception as e:
            log.error("Error checking Eurostat dataset %s: %s", dataset_code, e)
            
    conn.close()

def main():
    log.info("Starting Dynamic Ingestion Engine daemon...")
    while True:
        try:
            check_bdl()
            check_eurostat()
        except Exception as e:
            log.error("Unhandled error in ingestion loop: %s", e)
            
        log.info("Sleeping for %d seconds...", CHECK_INTERVAL)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
