"""
Database access for dashboard generation.
Connects to DuckDB using DUCKDB_PATH env var (default: data/reporting.duckdb).
Always queries the curated schema — never raw.
"""
import logging
import os

import duckdb
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)


def _db_path() -> str:
    return os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/reporting.duckdb")


def query(sql: str, params: tuple = ()) -> pd.DataFrame:
    """Execute a parameterised SELECT and return a DataFrame."""
    try:
        conn = duckdb.connect(_db_path(), read_only=True)
        return conn.execute(sql, list(params)).df()
    except Exception:
        log.exception("Query failed: %s", sql[:120])
        raise
    finally:
        conn.close()
