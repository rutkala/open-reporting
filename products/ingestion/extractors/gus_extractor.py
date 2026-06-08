#!/usr/bin/env python3
"""
GUS BDL Extractor
Downloads data for a specific metric across Poland into raw_gus.
"""
import os
import time
import logging
import requests
import pandas as pd
import duckdb
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def _db() -> duckdb.DuckDBPyConnection:
    """Follows the _db() loader pattern for connection."""
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path)

def fetch_data(metric_id: str, limit_pages: int = None) -> pd.DataFrame:
    """Download data for a specific metric across Poland from GUS BDL."""
    base_url = f"https://bdl.stat.gov.pl/api/v1/data/By-Variable/{metric_id}"
    page = 0
    page_size = 100
    all_results = []
    
    headers = {"Accept": "application/json"}
    api_key = os.environ.get("BDL_API_KEY")
    if api_key:
        headers["X-ClientId"] = api_key
        
    log.info(f"Fetching metric {metric_id} from GUS BDL...")
    while True:
        try:
            resp = requests.get(
                base_url, 
                params={"page": page, "page-size": page_size}, 
                headers=headers,
                timeout=30
            )
        except requests.exceptions.Timeout:
            log.warning("Timeout, retrying...")
            time.sleep(5)
            continue
            
        if resp.status_code == 429:
            log.warning("Rate limit hit, sleeping 5s")
            time.sleep(5)
            continue
            
        resp.raise_for_status()
        data = resp.json()
        
        results = data.get("results", [])
        if not results:
            break
            
        for row in results:
            unit_id = row.get("id")
            unit_name = row.get("name")
            for val_obj in row.get("values", []):
                all_results.append({
                    "metric_id": str(metric_id),
                    "unit_id": unit_id,
                    "unit_name": unit_name,
                    "year": int(val_obj.get("year")),
                    "value": val_obj.get("val"),
                    "fetched_at": datetime.now()
                })
                
        if "next" not in data.get("links", {}):
            break
        page += 1
        if limit_pages and page >= limit_pages:
            break
        
    log.info(f"Fetched {len(all_results)} observations for metric {metric_id}.")
    return pd.DataFrame(all_results)

def load_data(df: pd.DataFrame):
    """Load pandas DataFrame into duckdb generic raw_gus table."""
    if df.empty:
        log.warning("DataFrame is empty, nothing to load.")
        return
    conn = _db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_gus (
            metric_id VARCHAR,
            unit_id VARCHAR,
            unit_name VARCHAR,
            year INTEGER,
            value DOUBLE,
            fetched_at TIMESTAMP
        )
    """)
    metric_id = df["metric_id"].iloc[0]
    conn.execute("DELETE FROM raw_gus WHERE metric_id = ?", [metric_id])
    conn.execute("INSERT INTO raw_gus SELECT * FROM df")
    log.info(f"Loaded {len(df)} rows into raw_gus for metric {metric_id}.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="GUS Extractor")
    parser.add_argument("--metric", type=str, default="72305", help="BDL Metric ID")
    parser.add_argument("--limit-pages", type=int, default=None, help="Limit fetched pages")
    args = parser.parse_args()
    
    df = fetch_data(args.metric, args.limit_pages)
    load_data(df)
