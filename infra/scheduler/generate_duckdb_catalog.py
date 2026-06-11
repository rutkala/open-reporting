#!/usr/bin/env python3
"""
generate_duckdb_catalog.py — Generate duckdb_catalog.json for the admin portal.

Inspects information_schema in the DuckDB warehouse and writes a structured JSON
summary to infra/nginx/html/data/duckdb_catalog.json.

Usage:
    python3 generate_duckdb_catalog.py
"""
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import duckdb

from catalog_common import OUT, atomic_write, human_size, iso, now_iso

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

DB_PATH = Path("/opt/open-reporting") / "data/warehouse.duckdb"

# Schemas shown first in this fixed order; others follow alphabetically.
_SCHEMA_ORDER = ["raw", "staging", "curated", "main"]

# Column names that indicate a "last loaded" timestamp (checked in priority order).
_LOADED_AT_COLS = ["loaded_at", "ingested_at", "updated_at"]


def _connect() -> duckdb.DuckDBPyConnection:
    """Connect read-only; retry once after 30 s on IOException."""
    try:
        return duckdb.connect(str(DB_PATH), read_only=True)
    except duckdb.IOException:
        log.warning("DuckDB locked, retrying in 30 s…")
        time.sleep(30)
        try:
            return duckdb.connect(str(DB_PATH), read_only=True)
        except duckdb.IOException as exc:
            log.error("Failed to open DuckDB after retry: %s", exc)
            raise


def _fetch_columns(conn: duckdb.DuckDBPyConnection) -> dict[tuple[str, str], list[str]]:
    """Return {(schema, table): [col1, col2, ...]} limited to first 25 cols."""
    rows = conn.execute("""
        SELECT table_schema, table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY table_schema, table_name, ordinal_position
    """).fetchall()

    columns_map: dict[tuple[str, str], list[str]] = {}
    col_count_map: dict[tuple[str, str], int] = {}

    for schema, table, col_name, _dtype in rows:
        key = (schema, table)
        col_count_map[key] = col_count_map.get(key, 0) + 1
        if key not in columns_map:
            columns_map[key] = []
        if len(columns_map[key]) < 25:
            columns_map[key].append(col_name)

    # Attach full column count as a side-table (returned separately via col_count_map)
    # We store count directly in columns_map by packing it: caller uses both dicts.
    return columns_map, col_count_map  # type: ignore[return-value]


def _row_count(
    conn: duckdb.DuckDBPyConnection,
    schema: str,
    name: str,
    object_type: str,
) -> "int | None":
    """Run SELECT count(*) for a table or view; return None on failure."""
    safe_schema = schema.replace('"', '""')
    safe_name = name.replace('"', '""')
    query = f'SELECT count(*) FROM "{safe_schema}"."{safe_name}"'

    t0 = time.monotonic()
    try:
        result = conn.execute(query).fetchone()
        elapsed = time.monotonic() - t0
        if elapsed > 5:
            log.warning("Slow row count (%0.1f s) for %s.%s", elapsed, schema, name)
        return result[0] if result else None
    except Exception as exc:
        if object_type.upper() == "VIEW":
            log.info("Row count failed for view %s.%s: %s", schema, name, exc)
            return None
        log.warning("Row count failed for %s.%s: %s", schema, name, exc)
        return None


def _last_loaded(
    conn: duckdb.DuckDBPyConnection,
    schema: str,
    name: str,
    col_names: list[str],
) -> "str | None":
    """Return the max date of the best available timestamp column as a date string."""
    safe_schema = schema.replace('"', '""')
    safe_name = name.replace('"', '""')

    # Check priority timestamp columns
    for col in _LOADED_AT_COLS:
        if col in col_names:
            safe_col = col.replace('"', '""')
            try:
                row = conn.execute(
                    f'SELECT max("{safe_col}")::DATE FROM "{safe_schema}"."{safe_name}"'
                ).fetchone()
                return str(row[0]) if row and row[0] is not None else None
            except Exception as exc:
                log.info("last_loaded(%s.%s, %s) failed: %s", schema, name, col, exc)
                return None

    # Fallback: _dlt_load_id epoch
    if "_dlt_load_id" in col_names:
        try:
            row = conn.execute(
                f'SELECT max(epoch_ms(CAST(_dlt_load_id AS DOUBLE) * 1000)::TIMESTAMPTZ)::DATE'
                f' FROM "{safe_schema}"."{safe_name}"'
            ).fetchone()
            return str(row[0]) if row and row[0] is not None else None
        except Exception as exc:
            log.info("last_loaded(%s.%s, _dlt_load_id) failed: %s", schema, name, exc)
            return None

    return None


def generate() -> Path:
    """Build duckdb_catalog.json and write it atomically to html/data/."""
    conn = _connect()

    try:
        # Tables + views
        tables_rows = conn.execute("""
            SELECT table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_schema, table_name
        """).fetchall()

        # Columns
        columns_map, col_count_map = _fetch_columns(conn)

        # Build per-schema grouping
        schema_tables: dict[str, list[dict]] = {}
        total_rows_sum = 0

        for schema, table_name, table_type in tables_rows:
            key = (schema, table_name)
            col_names = columns_map.get(key, [])
            col_count = col_count_map.get(key, 0)
            obj_type = "table" if table_type.upper() == "BASE TABLE" else "view"

            row_count = _row_count(conn, schema, table_name, table_type)
            if row_count is not None:
                total_rows_sum += row_count

            last_loaded = _last_loaded(conn, schema, table_name, col_names)

            entry: dict = {
                "name": table_name,
                "object_type": obj_type,
                "row_count": row_count,
                "column_count": col_count,
                "columns": col_names,
                "last_loaded": last_loaded,
            }

            if schema not in schema_tables:
                schema_tables[schema] = []
            schema_tables[schema].append(entry)

    finally:
        conn.close()

    # Sort schemas: fixed order first, then alphabetical for remainder
    all_schemas = list(schema_tables.keys())
    ordered: list[str] = []
    for s in _SCHEMA_ORDER:
        if s in all_schemas:
            ordered.append(s)
    for s in sorted(all_schemas):
        if s not in ordered:
            ordered.append(s)

    schemas_out: list[dict] = []
    table_count_total = 0
    for schema_name in ordered:
        tables = schema_tables.get(schema_name, [])
        if not tables:
            continue
        schema_rows = sum(t["row_count"] for t in tables if t["row_count"] is not None)
        schemas_out.append({
            "name": schema_name,
            "table_count": len(tables),
            "row_count": schema_rows,
            "tables": tables,
        })
        table_count_total += len(tables)

    # DB file stats
    try:
        db_stat = DB_PATH.stat()
        db_size_bytes: "int | None" = db_stat.st_size
        db_file_modified: "str | None" = iso(
            datetime.fromtimestamp(db_stat.st_mtime, tz=timezone.utc)
        )
    except OSError as exc:
        log.warning("Could not stat DuckDB file: %s", exc)
        db_size_bytes = None
        db_file_modified = None

    output: dict = {
        "generated_at": now_iso(),
        "db_path": "data/warehouse.duckdb",
        "db_size_bytes": db_size_bytes,
        "db_file_modified": db_file_modified,
        "table_count": table_count_total,
        "total_rows": total_rows_sum,
        "schemas": schemas_out,
    }

    out_path = OUT / "duckdb_catalog.json"
    atomic_write(out_path, output)

    log.info(
        "duckdb_catalog: %d schemas, %d tables/views, %d total rows, db %s",
        len(schemas_out),
        table_count_total,
        total_rows_sum,
        human_size(db_size_bytes or 0),
    )
    return out_path


if __name__ == "__main__":
    generate()
    sys.exit(0)
