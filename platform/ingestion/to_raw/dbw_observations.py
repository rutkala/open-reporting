#!/usr/bin/env python3
"""
Raw load: data/landing/dbw_hvd/ → raw.dbw_observations + raw.dbw_positions
Reads all *_data.csv files from the landing zone in one bulk DuckDB operation.
Run AFTER platform/ingestion/to_landing/dbw_hvd.py.
Usage:
  PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/dbw_observations.py
Notes:
  - Drops and recreates raw.dbw_observations on every run (full overwrite).
  - Positions (raw.dbw_positions) are loaded from *_dict.csv files — also full overwrite.
  - DuckDB reads all CSVs natively via read_csv glob — no Python row iteration.
  - Data CSV: semicolon delimited, comma decimal separator, no_value_id!=0 → NULL value.
"""
import csv
import glob
import logging
import os

import duckdb
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

LANDING_DIR = os.path.join(
    os.environ.get("REPO_ROOT", "/opt/open-reporting"),
    "data/landing/dbw_hvd"
)


def _db() -> duckdb.DuckDBPyConnection:
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path)


def load_observations(conn: duckdb.DuckDBPyConnection) -> int:
    """Drop and recreate raw.dbw_observations from all *_data.csv files in landing."""
    pattern = os.path.join(LANDING_DIR, "*_data.csv")
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No data CSV files found in {LANDING_DIR}. Run to_landing/dbw_hvd.py first.")

    log.info("Loading %d data CSV files from landing...", len(files))

    conn.execute("DROP TABLE IF EXISTS raw.dbw_observations")
    ddl_path = os.path.join(
        os.environ.get("REPO_ROOT", "/opt/open-reporting"),
        "platform/warehouse/raw/dbw_observations.sql"
    )
    with open(ddl_path) as f:
        ddl = f.read()
    conn.execute(ddl)

    glob_pattern = os.path.join(LANDING_DIR, "*_data.csv")
    conn.execute(f"""
        INSERT OR REPLACE INTO raw.dbw_observations
            (variable_id, section_id, year, period_id,
             dim1_id, dim2_id, dim3_id, dim4_id, dim5_id, dim6_id,
             value, precision, fetched_at)
        SELECT
            Indicator_id,
            cross_section_id,
            data_id,
            period_id,
            COALESCE(TRY_CAST(dimension_1_position_id AS BIGINT), 0),
            COALESCE(TRY_CAST(dimension_2_position_id AS BIGINT), 0),
            COALESCE(TRY_CAST(dimension_3_position_id AS BIGINT), 0),
            COALESCE(TRY_CAST(dimension_4_position_id AS BIGINT), 0),
            COALESCE(TRY_CAST(dimension_5_position_id AS BIGINT), 0),
            COALESCE(TRY_CAST(dimension_6_position_id AS BIGINT), 0),
            TRY_CAST(REPLACE(value, ',', '.') AS DOUBLE),
            TRY_CAST(precision AS INTEGER),
            NOW()
        FROM read_csv(
            '{glob_pattern}',
            delim=';',
            header=true,
            ignore_errors=true,
            columns={{
                'rowNumber':               'VARCHAR',
                'Indicator_id':            'INTEGER',
                'cross_section_id':        'INTEGER',
                'dimension_1_id':          'VARCHAR',
                'dimension_1_position_id': 'VARCHAR',
                'dimension_2_id':          'VARCHAR',
                'dimension_2_position_id': 'VARCHAR',
                'dimension_3_id':          'VARCHAR',
                'dimension_3_position_id': 'VARCHAR',
                'dimension_4_id':          'VARCHAR',
                'dimension_4_position_id': 'VARCHAR',
                'dimension_5_id':          'VARCHAR',
                'dimension_5_position_id': 'VARCHAR',
                'dimension_6_id':          'VARCHAR',
                'dimension_6_position_id': 'VARCHAR',
                'dimension_7_id':          'VARCHAR',
                'dimension_7_position_id': 'VARCHAR',
                'dimension_8_id':          'VARCHAR',
                'dimension_8_position_id': 'VARCHAR',
                'dimension_9_id':          'VARCHAR',
                'dimension_9_position_id': 'VARCHAR',
                'period_id':               'INTEGER',
                'way_of_presentation_id':  'VARCHAR',
                'data_id':                 'INTEGER',
                'no_value_id':             'VARCHAR',
                'confidentionality_id':    'VARCHAR',
                'flag_id':                 'VARCHAR',
                'value':                   'VARCHAR',
                'precision':               'VARCHAR'
            }}
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM raw.dbw_observations").fetchone()[0]
    log.info("Loaded %d observations from %d files", count, len(files))
    return count


def load_positions(conn: duckdb.DuckDBPyConnection) -> int:
    """Load all *_dict.csv files into raw.dbw_positions."""
    dict_files = glob.glob(os.path.join(LANDING_DIR, "*_dict.csv"))
    if not dict_files:
        log.warning("No dict CSV files found — skipping positions load")
        return 0

    conn.execute("DELETE FROM raw.dbw_positions")

    total = 0
    for dict_path in dict_files:
        # Extract section_id from the data CSV sibling
        file_id   = os.path.basename(dict_path).replace("_dict.csv", "")
        data_path = dict_path.replace("_dict.csv", "_data.csv")
        if not os.path.exists(data_path):
            continue

        # Get section_id from first data row
        with open(data_path, encoding="utf-8", errors="replace") as fh:
            first = next(csv.DictReader(fh, delimiter=";"), None)
        if not first:
            continue
        section_id = int(first["cross_section_id"])

        with open(dict_path, encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f, delimiter=";", quotechar='"')
            dim_names: dict[int, tuple[int, str]] = {}
            rows = []
            for r in reader:
                col  = (r.get("column_name") or "").strip()
                eid  = (r.get("element_id")  or "").strip()
                desc = (r.get("description") or "").strip().strip('"')
                if not eid:
                    continue
                eid = int(eid)
                for n in range(1, 10):
                    if col == f"dimension_{n}_id":
                        dim_names[n] = (eid, desc)
                        break
                    if col == f"dimension_{n}_position_id":
                        dim_id, dim_name = dim_names.get(n, (n, ""))
                        rows.append((section_id, dim_id, dim_name, eid, desc))
                        break

        if rows:
            conn.executemany(
                "INSERT OR REPLACE INTO raw.dbw_positions "
                "(section_id, dim_id, dim_name, position_id, position_name, fetched_at) "
                "VALUES (?, ?, ?, ?, ?, NOW())",
                rows,
            )
            total += len(rows)

    log.info("Loaded %d position labels from %d dict files", total, len(dict_files))
    return total


def validate(conn: duckdb.DuckDBPyConnection) -> None:
    r = conn.execute(
        "SELECT COUNT(*), COUNT(DISTINCT variable_id), COUNT(DISTINCT section_id), "
        "MIN(year), MAX(year) FROM raw.dbw_observations"
    ).fetchone()
    log.info(
        "Validation: %d observations, %d variables, %d sections, years %s–%s",
        r[0], r[1], r[2], r[3], r[4],
    )
    p = conn.execute(
        "SELECT COUNT(*), COUNT(DISTINCT section_id) FROM raw.dbw_positions"
    ).fetchone()
    log.info("Positions: %d labels across %d cross-sections", p[0], p[1])


def run() -> None:
    conn = _db()
    load_observations(conn)
    load_positions(conn)
    validate(conn)
    conn.close()


if __name__ == "__main__":
    run()
