"""Shared database connection helper."""
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

_CONFIG = dict(
    host=os.environ.get("POSTGRES_HOST", "localhost"),
    port=int(os.environ.get("POSTGRES_PORT", "5432")),
    dbname=os.environ.get("POSTGRES_DB", "reporting"),
    user=os.environ.get("POSTGRES_USER", "reporting"),
    password=os.environ["POSTGRES_PASSWORD"],
)


def query(sql: str, params=None) -> pd.DataFrame:
    with psycopg2.connect(**_CONFIG) as conn:
        return pd.read_sql(sql, conn, params=params)
