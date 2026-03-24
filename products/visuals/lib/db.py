"""
Database access for dashboard generation.
Connects to PostgreSQL using POSTGRES_PASSWORD env var.
Always queries the curated schema — never raw.
"""
import logging
import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)


def _dsn() -> str:
    return (
        f"postgresql://reporting:{os.environ['POSTGRES_PASSWORD']}"
        f"@localhost:5432/reporting"
    )


def query(sql: str, params: tuple = ()) -> pd.DataFrame:
    """Execute a parameterised SELECT and return a DataFrame."""
    conn = None
    try:
        conn = psycopg2.connect(_dsn())
        return pd.read_sql(sql, conn, params=params)
    except Exception:
        log.exception("Query failed: %s", sql[:120])
        raise
    finally:
        if conn:
            conn.close()
