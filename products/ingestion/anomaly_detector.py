#!/usr/bin/env python3
"""
Anomaly Detector
Scans recently inserted observations in DuckDB for spikes or sudden drops
(2+ standard deviations from the historical mean) across Eurostat and BDL metrics.

Usage:
  PYTHONPATH=/opt/open-reporting python3 products/ingestion/anomaly_detector.py
"""
import argparse
import logging
import os
import sys

import duckdb
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def _db() -> duckdb.DuckDBPyConnection:
    """Open DuckDB connection lazily — reads DUCKDB_PATH only at call time."""
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    try:
        # We only need read access for detection
        return duckdb.connect(path, read_only=True)
    except duckdb.IOException:
        # Fallback if there's an issue with read_only or lock
        log.warning("Could not connect read-only. Retrying standard connect...")
        return duckdb.connect(path)


def check_bdl_anomalies(conn: duckdb.DuckDBPyConnection, hours: int):
    """
    Finds 2+ standard deviation anomalies in BDL data for rows fetched in the last `hours`.
    """
    query = f"""
    WITH stats AS (
        SELECT 
            variable_id, 
            unit_id,
            AVG(value) as mean_val,
            STDDEV_SAMP(value) as std_val,
            COUNT(*) as n_obs
        FROM raw.bdl_observations
        WHERE value IS NOT NULL
        GROUP BY variable_id, unit_id
        HAVING COUNT(*) >= 4 AND STDDEV_SAMP(value) > 0
    ),
    recent_data AS (
        SELECT 
            b.variable_id,
            b.unit_id,
            b.unit_name,
            b.year,
            b.value,
            b.fetched_at
        FROM raw.bdl_observations b
        WHERE b.fetched_at >= NOW() - INTERVAL '{hours} HOURS'
          AND b.value IS NOT NULL
    )
    SELECT 
        r.variable_id,
        r.unit_id,
        r.unit_name,
        r.year,
        r.value AS current_value,
        s.mean_val,
        s.std_val,
        ABS(r.value - s.mean_val) / s.std_val AS z_score,
        r.fetched_at
    FROM recent_data r
    JOIN stats s ON r.variable_id = s.variable_id AND r.unit_id = s.unit_id
    WHERE ABS(r.value - s.mean_val) / s.std_val >= 2.0
    ORDER BY z_score DESC
    """
    try:
        return conn.execute(query).fetchall()
    except duckdb.CatalogException:
        log.warning("Table raw.bdl_observations does not exist yet.")
        return []


def check_eurostat_anomalies(conn: duckdb.DuckDBPyConnection, hours: int):
    """
    Finds 2+ standard deviation anomalies in Eurostat data for rows fetched in the last `hours`.
    """
    query = f"""
    WITH stats AS (
        SELECT 
            dataset_code,
            geo,
            dimension_key,
            AVG(value) as mean_val,
            STDDEV_SAMP(value) as std_val,
            COUNT(*) as n_obs
        FROM raw.eurostat_observations
        WHERE value IS NOT NULL
        GROUP BY dataset_code, geo, dimension_key
        HAVING COUNT(*) >= 4 AND STDDEV_SAMP(value) > 0
    ),
    recent_data AS (
        SELECT 
            e.dataset_code,
            e.geo,
            e.dimension_key,
            e.period,
            e.value,
            e.fetched_at
        FROM raw.eurostat_observations e
        WHERE e.fetched_at >= NOW() - INTERVAL '{hours} HOURS'
          AND e.value IS NOT NULL
    )
    SELECT 
        r.dataset_code,
        r.geo,
        r.dimension_key,
        r.period,
        r.value AS current_value,
        s.mean_val,
        s.std_val,
        ABS(r.value - s.mean_val) / s.std_val AS z_score,
        r.fetched_at
    FROM recent_data r
    JOIN stats s 
      ON r.dataset_code = s.dataset_code 
     AND r.geo = s.geo 
     AND r.dimension_key = s.dimension_key
    WHERE ABS(r.value - s.mean_val) / s.std_val >= 2.0
    ORDER BY z_score DESC
    """
    try:
        return conn.execute(query).fetchall()
    except duckdb.CatalogException:
        log.warning("Table raw.eurostat_observations does not exist yet.")
        return []


def main():
    parser = argparse.ArgumentParser(description="Find 2+ std dev anomalies in recently ingested data.")
    parser.add_argument("--hours", type=int, default=24, help="Scan data fetched in the last N hours.")
    args = parser.parse_args()

    log.info("Starting anomaly detection scan for data fetched in the last %d hours...", args.hours)
    
    try:
        conn = _db()
    except Exception as e:
        log.error("Failed to connect to DuckDB: %s", e)
        sys.exit(1)

    # Scan BDL
    log.info("Scanning BDL observations...")
    bdl_anomalies = check_bdl_anomalies(conn, args.hours)
    if bdl_anomalies:
        log.info("Found %d BDL anomalies:", len(bdl_anomalies))
        for row in bdl_anomalies:
            var_id, unit_id, unit_name, year, val, mean, std, z, fetched_at = row
            direction = "SPIKE" if val > mean else "DROP"
            log.info("  [BDL] %s (Unit: %s '%s', Year: %s) -> %s! Value: %.2f (Mean: %.2f, z-score: %.2f)", 
                     var_id, unit_id, unit_name, year, direction, val, mean, z)
    else:
        log.info("No BDL anomalies found.")

    # Scan Eurostat
    log.info("Scanning Eurostat observations...")
    eurostat_anomalies = check_eurostat_anomalies(conn, args.hours)
    if eurostat_anomalies:
        log.info("Found %d Eurostat anomalies:", len(eurostat_anomalies))
        for row in eurostat_anomalies:
            ds_code, geo, dim_key, period, val, mean, std, z, fetched_at = row
            direction = "SPIKE" if val > mean else "DROP"
            log.info("  [Eurostat] %s (Geo: %s, Period: %s, Dims: %s) -> %s! Value: %.2f (Mean: %.2f, z-score: %.2f)", 
                     ds_code, geo, period, dim_key, direction, val, mean, z)
    else:
        log.info("No Eurostat anomalies found.")

    conn.close()
    log.info("Anomaly scan complete.")


if __name__ == "__main__":
    main()
