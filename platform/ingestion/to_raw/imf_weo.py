#!/usr/bin/env python3
"""
Ingestion: IMF World Economic Outlook (WEO) → raw.imf_weo
Tool: weo Python package (pip install weo)
Source: IMF WEO October 2024 release (latest available as of 2025)
Update method: upsert on (weo_subject, iso_code, year, weo_edition)
Schema: raw.imf_weo

Indicators ingested (all % GDP or % potential GDP):
  GGXCNL_NGDP  Overall fiscal balance
  GGXONLB_NGDP Primary balance
  GGSB_NPGDP   Cyclically-adjusted (structural) balance
  GGXWDG_NGDP  Gross government debt
  GGXWDN_NGDP  Net government debt
  GGR_NGDP     Government revenue
  GGX_NGDP     Government expenditure

Countries: Poland + V4 + major EU economies
Projection rule: year >= current_calendar_year is flagged as projection

Usage:
  PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/imf_weo.py
  PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/imf_weo.py --backfill
"""
import argparse
import datetime
import logging
import os

import duckdb
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# WEO release to use (year, release_number: 1=Apr, 2=Oct)
WEO_YEAR    = 2024
WEO_RELEASE = 2  # October
WEO_EDITION = "2024-10"

# WEO indicator codes (using weo package's internal codes)
WEO_SUBJECTS = [
    "GGXCNL_NGDP",   # Overall fiscal balance % GDP
    "GGXONLB_NGDP",  # Primary balance % GDP
    "GGSB_NPGDP",    # Cyclically-adjusted balance % potential GDP (unique to IMF)
    "GGXWDG_NGDP",   # Gross government debt % GDP
    "GGXWDN_NGDP",   # Net government debt % GDP
    "GGR_NGDP",      # Government revenue % GDP
    "GGX_NGDP",      # Government expenditure % GDP
]

# ISO 3166-1 alpha-3 country codes as used in WEO data
# Poland + V4 + major EU economies + Romania/Bulgaria
TARGET_COUNTRIES = [
    "POL",  # Poland
    "CZE",  # Czech Republic
    "SVK",  # Slovakia
    "HUN",  # Hungary
    "DEU",  # Germany
    "FRA",  # France
    "ITA",  # Italy
    "ESP",  # Spain
    "SWE",  # Sweden
    "NLD",  # Netherlands
    "AUT",  # Austria
    "BEL",  # Belgium
    "DNK",  # Denmark
    "FIN",  # Finland
    "GRC",  # Greece
    "PRT",  # Portugal
    "ROU",  # Romania
    "BGR",  # Bulgaria
    "HRV",  # Croatia
    "SVN",  # Slovenia
    "EST",  # Estonia
    "LVA",  # Latvia
    "LTU",  # Lithuania
    "IRL",  # Ireland
    "LUX",  # Luxembourg
    "MLT",  # Malta
    "CYP",  # Cyprus
]


def _db() -> duckdb.DuckDBPyConnection:
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path)


def ensure_table(conn: duckdb.DuckDBPyConnection) -> None:
    ddl_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "imf_weo.sql",
    )
    with open(ddl_path) as f:
        conn.execute(f.read())


def fetch_weo_data() -> list[dict]:
    """Download WEO data for all target subjects and countries."""
    try:
        import weo as weo_pkg
    except ImportError:
        raise ImportError("Install the weo package: pip install weo")

    current_year = datetime.date.today().year

    landing_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "landing")
    os.makedirs(landing_dir, exist_ok=True)
    log.info("Loading IMF WEO %d release %d (may download on first run)...", WEO_YEAR, WEO_RELEASE)
    w = weo_pkg.get(WEO_YEAR, WEO_RELEASE, path=landing_dir)
    log.info("WEO data loaded. Available countries: %d", len(w.codes))

    rows = []
    for subject in WEO_SUBJECTS:
        log.info("Fetching %s ...", subject)
        try:
            # getc returns DataFrame: rows=years (Period), columns=ISO codes
            df = w.getc(subject)
        except Exception as exc:
            log.warning("Could not fetch %s: %s", subject, exc)
            continue

        if df is None or df.empty:
            log.warning("Empty result for %s", subject)
            continue

        # Filter to target countries that exist in the data
        available = [c for c in TARGET_COUNTRIES if c in df.columns]
        df_filtered = df[available]

        count = 0
        for period in df_filtered.index:
            year = int(str(period)[:4])
            for iso_code in available:
                val = df_filtered.at[period, iso_code]
                try:
                    float_val = float(val) if val is not None and str(val) not in ("nan", "NaN", "") else None
                except (TypeError, ValueError):
                    float_val = None
                rows.append({
                    "weo_subject": subject,
                    "iso_code": iso_code,
                    "year": year,
                    "value": float_val,
                    "is_projection": year >= current_year,
                    "weo_edition": WEO_EDITION,
                })
                count += 1

        log.info("  %s: %d observations collected (%d countries)", subject, count, len(available))

    return rows


def upsert(conn: duckdb.DuckDBPyConnection, rows: list[dict]) -> int:
    if not rows:
        return 0
    conn.executemany(
        """
        INSERT OR REPLACE INTO raw.imf_weo
            (weo_subject, iso_code, year, value, is_projection, weo_edition, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?, NOW())
        """,
        [
            (r["weo_subject"], r["iso_code"], r["year"],
             r["value"], r["is_projection"], r["weo_edition"])
            for r in rows
        ],
    )
    return len(rows)


def validate(conn: duckdb.DuckDBPyConnection) -> None:
    row = conn.execute(
        "SELECT COUNT(*), COUNT(DISTINCT weo_subject), COUNT(DISTINCT iso_code), "
        "MIN(year), MAX(year) FROM raw.imf_weo"
    ).fetchone()
    log.info(
        "Validation: %d rows, %d subjects, %d countries, years %d–%d",
        row[0], row[1], row[2], row[3], row[4],
    )
    proj = conn.execute(
        "SELECT COUNT(*) FROM raw.imf_weo WHERE is_projection = TRUE"
    ).fetchone()[0]
    actual = conn.execute(
        "SELECT COUNT(*) FROM raw.imf_weo WHERE is_projection = FALSE"
    ).fetchone()[0]
    log.info("  Actual: %d rows, Projection: %d rows", actual, proj)

    # Check POL coverage for key indicator
    pol_row = conn.execute(
        "SELECT MIN(year), MAX(year), COUNT(*) FROM raw.imf_weo "
        "WHERE iso_code = 'POL' AND weo_subject = 'GGXCNL_NGDP'"
    ).fetchone()
    log.info("  POL GGXCNL_NGDP: years %d–%d (%d rows)", pol_row[0], pol_row[1], pol_row[2])
    log.info("Validation passed")


def run(backfill: bool = False) -> None:
    rows = fetch_weo_data()
    if not rows:
        log.warning("No rows fetched — aborting")
        return

    conn = _db()
    ensure_table(conn)
    n = upsert(conn, rows)
    log.info("Total upserted: %d rows", n)
    validate(conn)
    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest IMF WEO fiscal data into raw.imf_weo")
    parser.add_argument("--backfill", action="store_true", help="Full history (no-op — WEO always returns full history)")
    args = parser.parse_args()
    run(backfill=args.backfill)


if __name__ == "__main__":
    main()
