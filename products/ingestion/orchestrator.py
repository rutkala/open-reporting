#!/usr/bin/env python3
import os
import time
import yaml
import random
import logging
from datetime import datetime
import duckdb

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def _db() -> duckdb.DuckDBPyConnection:
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path)


import subprocess

def fetch_data(source: dict) -> int:
    """Fetch data using real extractors where available."""
    source_id = source["id"]
    
    if source_id == "eurostat_api":
        cmd = ["python3", "/opt/open-reporting/products/ingestion/extractors/eurostat_extractor.py", "nama_10_gdp"]
        logger.info(f"Running Eurostat Extractor: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Eurostat extraction failed: {result.stderr}")
        # Parse stdout to find row count if possible, else default
        rows = 0
        for line in result.stdout.split("\\n"):
            if "Total rows in raw_eurostat:" in line:
                rows = int(line.split(":")[-1].strip())
        return rows
        
    elif source_id == "gus_bdl_api":
        cmd = ["python3", "/opt/open-reporting/products/ingestion/extractors/gus_extractor.py", "--metric", "72305"]
        logger.info(f"Running GUS Extractor: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"GUS extraction failed: {result.stderr}")
        rows = 0
        for line in result.stdout.split("\\n"):
            if "Total rows in raw_gus:" in line:
                rows = int(line.split(":")[-1].strip())
        return rows
        
    else:
        # Mock for remaining until extractors are built
        time.sleep(0.5)
        if random.random() < 0.1:
            raise Exception("Not yet implemented - Mock simulated error")
        return random.randint(100, 5000)


def main():
    yaml_path = "/opt/open-reporting/products/ingestion/to_landing/sources.yaml"
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    conn = _db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_status (
            source_id VARCHAR PRIMARY KEY,
            last_sync TIMESTAMP,
            status VARCHAR,
            rows_fetched INTEGER,
            error_message VARCHAR
        )
    """)
    conn.close()

    for source in data.get("sources", []):
        source_id = source["id"]
        logger.info(f"Fetching data for {source_id}...")
        
        status = "SUCCESS"
        rows_fetched = 0
        error_message = None
        
        try:
            rows_fetched = fetch_data(source)
        except Exception as e:
            status = "FAILED"
            error_message = str(e)
            logger.error(f"Failed to fetch {source_id}: {error_message}")
            
        last_sync = datetime.now()

        conn = _db()
        conn.execute("""
            INSERT INTO ingestion_status (
                source_id, last_sync, status, rows_fetched, error_message
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (source_id) DO UPDATE SET
                last_sync = excluded.last_sync,
                status = excluded.status,
                rows_fetched = excluded.rows_fetched,
                error_message = excluded.error_message
        """, (source_id, last_sync, status, rows_fetched, error_message))
        conn.close()
        
        logger.info(f"Finished {source_id} with status: {status}")


if __name__ == "__main__":
    main()
