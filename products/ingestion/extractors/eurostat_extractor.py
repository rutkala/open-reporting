#!/usr/bin/env python3
"""
Eurostat Data Extractor
Fetches JSON-stat data from the Eurostat API, parses it using pandas, and stores
it into warehouse.duckdb inside a generic raw_eurostat table.
"""

import os
import json
import argparse
import logging
import requests
import pandas as pd
import duckdb

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

EUROSTAT_API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"


def _db() -> duckdb.DuckDBPyConnection:
    """Connect to DuckDB warehouse."""
    db_path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(db_path)


def fetch_dataset(dataset_code: str, params: dict | None = None) -> pd.DataFrame:
    """
    Download and parse JSON-stat data from Eurostat into a pandas DataFrame.
    """
    url = f"{EUROSTAT_API}{dataset_code}"
    req_params = {"format": "JSON", "lang": "en"}
    if params:
        req_params.update(params)

    logger.info("Fetching Eurostat dataset %s", dataset_code)
    resp = requests.get(url, params=req_params, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    dim_ids = data["id"]
    dim_sizes = data["size"]
    dimensions = data["dimension"]
    values = data.get("value", {})
    statuses = data.get("status", {})

    # Invert index maps for fast lookup
    dim_labels = {}
    for dim in dim_ids:
        cat = dimensions[dim]["category"]
        dim_labels[dim] = {v: k for k, v in cat["index"].items()}

    # Compute strides for flat-index to multi-dimensional index
    strides = [1] * len(dim_ids)
    for i in range(len(dim_ids) - 2, -1, -1):
        strides[i] = strides[i + 1] * dim_sizes[i + 1]

    rows = []
    for flat_idx_str, val in values.items():
        flat_idx = int(flat_idx_str)
        row = {
            "dataset_code": dataset_code,
            "value": float(val) if val is not None else None,
            "obs_status": statuses.get(flat_idx_str)
        }
        
        remainder = flat_idx
        for i, dim in enumerate(dim_ids):
            pos = remainder // strides[i]
            remainder %= strides[i]
            row[dim] = dim_labels[dim].get(pos, str(pos))
            
        rows.append(row)

    df = pd.DataFrame(rows)
    return df


def load_to_duckdb(df: pd.DataFrame, table_name: str = "raw_eurostat"):
    """
    Store the parsed DataFrame into DuckDB generic table.
    """
    if df.empty:
        logger.warning("DataFrame is empty. Nothing to insert.")
        return

    # Ensure essential columns exist
    for col in ["geo", "time", "obs_status"]:
        if col not in df.columns:
            df[col] = None

    # Identify dimension columns (everything that's not standard)
    standard_cols = {"dataset_code", "geo", "time", "value", "obs_status"}
    dim_cols = [c for c in df.columns if c not in standard_cols]

    # Convert dimension columns to a JSON string
    if dim_cols:
        df["dimensions"] = df[dim_cols].to_dict(orient="records")
        df["dimensions"] = df["dimensions"].apply(lambda x: json.dumps(x))
        df = df.drop(columns=dim_cols)
    else:
        df["dimensions"] = "{}"

    # Reorder columns
    df = df[["dataset_code", "geo", "time", "dimensions", "value", "obs_status"]]

    conn = _db()
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            dataset_code VARCHAR,
            geo VARCHAR,
            time VARCHAR,
            dimensions VARCHAR,
            value DOUBLE,
            obs_status VARCHAR
        )
    """)
    
    # We clear the previous data for the dataset to prevent duplicates
    # Alternatively, we just insert. The simplest is a DELETE/INSERT pattern if generic.
    dataset_code = df["dataset_code"].iloc[0]
    conn.execute(f"DELETE FROM {table_name} WHERE dataset_code = ?", (dataset_code,))
    
    logger.info("Inserting %d rows for %s into %s", len(df), dataset_code, table_name)
    conn.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    
    # Validation count
    count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    logger.info("Total rows in %s: %d", table_name, count)
    
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Eurostat Data Extractor")
    parser.add_argument("dataset_code", help="Eurostat dataset code to fetch (e.g., nama_10_gdp)")
    parser.add_argument("--geo", help="Filter by geography (e.g., PL)", default=None)
    parser.add_argument("--time", help="Filter by time (e.g., 2022)", default=None)
    args = parser.parse_args()

    params = {}
    if args.geo:
        params["geo"] = args.geo
    if args.time:
        params["time"] = args.time

    df = fetch_dataset(args.dataset_code, params)
    load_to_duckdb(df)


if __name__ == "__main__":
    main()
