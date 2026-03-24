#!/usr/bin/env python3
"""
Processing: GUS BDL Labour → curated.labour_market_regional
Input:  raw.bdl_labour
Output: curated.labour_market_regional
Run:    python3 processing/bdl_labour_process.py

Transformations applied:
- Encoding normalisation (NFC, whitespace) on region names
- Null checks: variable_name, unit_name (region), year required
- Type casting: value as NUMERIC, year as INT
- Validity: unemployment_rate in [0, 100], avg_wages in [0, 100_000],
            gdp_per_capita in [0, 1_000_000], year in [1990, 2030]
- Pivot: one row per (region, year) with columns per metric
- Deduplication on (region, year)
"""
import json
import logging
import os
import sys
import unicodedata
from datetime import datetime, timezone

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

SOURCE = "bdl_labour"
TARGET_TABLE = "curated.labour_market_regional"
NATURAL_KEY = ["region", "year"]
REQUIRED_COLUMNS = ["variable_name", "unit_name", "year"]


def _dsn() -> str:
    return (
        f"postgresql://reporting:{os.environ['POSTGRES_PASSWORD']}"
        f"@localhost:5432/reporting"
    )

VALIDITY_RULES = {
    "unemployment_rate": {"min": 0.0, "max": 100.0},
    "avg_wages":         {"min": 0.0, "max": 100_000.0},
    "gdp_per_capita":    {"min": 0.0, "max": 1_000_000.0},
    "year":              {"min": 1990, "max": 2030},
}

_issue_buffer: list[dict] = []


# ── Quality helpers ───────────────────────────────────────────────────────────

def _log_quality_issues(issue_df: pd.DataFrame) -> None:
    for _, row in issue_df.iterrows():
        _issue_buffer.append({
            "source": SOURCE,
            "table_name": TARGET_TABLE,
            "issue_type": row.get("issue", "unknown"),
            "row_data": json.dumps(
                row.drop("issue", errors="ignore").to_dict(), default=str
            ),
            "detected_at": datetime.now(timezone.utc),
        })


def clean_string(value) -> str | None:
    if value is None:
        return None
    value = unicodedata.normalize("NFC", str(value))
    value = value.replace("\u00a0", " ").replace("\x00", "")
    value = " ".join(value.split())
    return value if value else None


def parse_year(value) -> int | None:
    try:
        y = int(value)
        return y if 1900 <= y <= 2100 else None
    except (ValueError, TypeError):
        return None


def apply_range_checks(df: pd.DataFrame, col: str, bounds: dict) -> pd.DataFrame:
    lo, hi = bounds.get("min"), bounds.get("max")
    if lo is not None:
        mask = df[col].notna() & (df[col] < lo)
        if mask.any():
            _log_quality_issues(df[mask].assign(issue=f"{col}_below_minimum"))
            log.warning("%d values in %s below minimum %s — set to NULL", mask.sum(), col, lo)
            df.loc[mask, col] = None
    if hi is not None:
        mask = df[col].notna() & (df[col] > hi)
        if mask.any():
            _log_quality_issues(df[mask].assign(issue=f"{col}_above_maximum"))
            log.warning("%d values in %s above maximum %s — set to NULL", mask.sum(), col, hi)
            df.loc[mask, col] = None
    return df


def deduplicate(df: pd.DataFrame, key_cols: list[str]) -> pd.DataFrame:
    duplicates = df.duplicated(subset=key_cols, keep=False)
    if duplicates.any():
        dup_count = df.duplicated(subset=key_cols, keep="last").sum()
        log.warning(
            "Found %d rows involved in duplicates on %s. Dropping %d.",
            duplicates.sum(), key_cols, dup_count,
        )
        _log_quality_issues(
            df[df.duplicated(subset=key_cols, keep="last")].assign(issue="duplicate_natural_key")
        )
        df = df.drop_duplicates(subset=key_cols, keep="last")
    return df


# ── Schema setup ──────────────────────────────────────────────────────────────

CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS curated;"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS curated.labour_market_regional (
    region             VARCHAR(100)   NOT NULL,
    year               INT            NOT NULL,
    unemployment_rate  NUMERIC(8,4),
    avg_wages          NUMERIC(18,2),
    gdp_per_capita     NUMERIC(18,2),
    updated_at         TIMESTAMPTZ    DEFAULT NOW(),
    CONSTRAINT labour_market_regional_pk PRIMARY KEY (region, year)
);
"""

CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS lmr_year_idx   ON curated.labour_market_regional (year);",
    "CREATE INDEX IF NOT EXISTS lmr_region_idx ON curated.labour_market_regional (region);",
]

CREATE_QUALITY_LOG = """
CREATE SCHEMA IF NOT EXISTS processing_log;
CREATE TABLE IF NOT EXISTS processing_log.quality_issues (
    id           BIGSERIAL PRIMARY KEY,
    source       VARCHAR(100)  NOT NULL,
    table_name   VARCHAR(100)  NOT NULL,
    issue_type   VARCHAR(100)  NOT NULL,
    row_data     JSONB,
    detected_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);
"""


def setup_schema(conn) -> None:
    cur = conn.cursor()
    cur.execute(CREATE_SCHEMA)
    cur.execute(CREATE_TABLE)
    for idx in CREATE_INDEXES:
        cur.execute(idx)
    cur.execute(CREATE_QUALITY_LOG)
    conn.commit()
    log.info("Schema ready")


# ── ETL ───────────────────────────────────────────────────────────────────────

def extract(conn) -> pd.DataFrame:
    return pd.read_sql(
        "SELECT variable_name, unit_name, year, value FROM raw.bdl_labour ORDER BY year",
        conn,
    )


def transform(df: pd.DataFrame) -> pd.DataFrame:
    input_count = len(df)

    # 1. Encoding — region names from unit_name column
    df["unit_name"] = df["unit_name"].apply(clean_string)
    df["variable_name"] = df["variable_name"].apply(clean_string)

    # 2. Completeness
    null_mask = df[REQUIRED_COLUMNS].isnull().any(axis=1)
    if null_mask.any():
        _log_quality_issues(df[null_mask].assign(issue="null_in_required_column"))
        log.warning("Dropped %d rows with null in required columns", null_mask.sum())
        df = df[~null_mask].copy()

    # 3. Type casting
    df["year"] = df["year"].apply(parse_year)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # 4. Validity per metric
    for metric, bounds in VALIDITY_RULES.items():
        if metric == "year":
            continue
        mask_metric = df["variable_name"] == metric
        sub = df[mask_metric].copy()
        sub = apply_range_checks(sub, "value", bounds)
        df.loc[mask_metric, "value"] = sub["value"]

    apply_range_checks(df, "year", VALIDITY_RULES["year"])

    # 5. Pivot: rows per metric → columns per metric, one row per (region, year)
    pivot = df.pivot_table(
        index=["unit_name", "year"],
        columns="variable_name",
        values="value",
        aggfunc="last",
    ).reset_index()
    pivot.columns.name = None
    pivot = pivot.rename(columns={"unit_name": "region"})

    # Ensure all expected metric columns exist
    for col in ["unemployment_rate", "avg_wages", "gdp_per_capita"]:
        if col not in pivot.columns:
            pivot[col] = None

    # 6. Deduplication
    pivot = deduplicate(pivot, NATURAL_KEY)

    log.info("Transform: %d raw rows → %d curated rows (%d removed)",
             input_count, len(pivot), input_count - len(pivot))
    return pivot


def load(conn, df: pd.DataFrame) -> int:
    now = datetime.now(timezone.utc)
    rows = [
        (
            row["region"],
            int(row["year"]),
            row.get("unemployment_rate"),
            row.get("avg_wages"),
            row.get("gdp_per_capita"),
            now,
        )
        for _, row in df.iterrows()
    ]
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO curated.labour_market_regional
            (region, year, unemployment_rate, avg_wages, gdp_per_capita, updated_at)
        VALUES %s
        ON CONFLICT (region, year) DO UPDATE SET
            unemployment_rate = EXCLUDED.unemployment_rate,
            avg_wages         = EXCLUDED.avg_wages,
            gdp_per_capita    = EXCLUDED.gdp_per_capita,
            updated_at        = EXCLUDED.updated_at
    """, rows)
    conn.commit()
    return cur.rowcount


def flush_quality_issues(conn) -> None:
    if not _issue_buffer:
        return
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO processing_log.quality_issues
            (source, table_name, issue_type, row_data, detected_at)
        VALUES %s
    """, [
        (r["source"], r["table_name"], r["issue_type"],
         json.dumps(r["row_data"]), r["detected_at"])
        for r in _issue_buffer
    ])
    conn.commit()
    log.info("Logged %d quality issues", len(_issue_buffer))


def validate(conn) -> None:
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*), MIN(year), MAX(year), COUNT(DISTINCT region)
        FROM curated.labour_market_regional
    """)
    count, min_year, max_year, regions = cur.fetchone()
    log.info("Validation: %d rows, years %s–%s, %d regions", count, min_year, max_year, regions)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    conn = None
    try:
        conn = psycopg2.connect(_dsn())
        setup_schema(conn)
        df = extract(conn)
        df = transform(df)
        count = load(conn, df)
        flush_quality_issues(conn)
        log.info("Loaded %d rows into %s", count, TARGET_TABLE)
        validate(conn)
    except Exception:
        log.exception("Processing failed")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
