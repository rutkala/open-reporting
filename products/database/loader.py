#!/usr/bin/env python3
"""
Catalogue loader — upserts domains, domain_details, sources, and
domain_detail_sources into PostgreSQL from CSV files.

Run after any change to products/database/data/*.csv

Usage:
    PYTHONPATH=/opt/open-reporting python3 products/database/loader.py
"""
import csv
import logging
import os
import sys
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv(override=True)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DATA_DIR = Path(__file__).parent / "data"
DDL_DIR  = Path(__file__).parent / "catalogue"


def _dsn() -> str:
    return (
        f"postgresql://reporting:{os.environ['POSTGRES_PASSWORD']}"
        f"@localhost:5432/reporting"
    )


def _read_csv(filename: str) -> list[dict]:
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if any(r.values())]


def apply_schema(conn) -> None:
    cur = conn.cursor()
    for sql_file in sorted(DDL_DIR.glob("*.sql")):
        log.info("Applying %s", sql_file.name)
        cur.execute(sql_file.read_text())
    conn.commit()
    log.info("Schema ready")


def load_domains(conn) -> int:
    rows = _read_csv("domains.csv")
    if not rows:
        log.info("domains.csv is empty — skipping")
        return 0
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO catalogue.domains (domain_id, name, domain_group, description)
        VALUES %s
        ON CONFLICT (domain_id) DO UPDATE SET
            name         = EXCLUDED.name,
            domain_group = EXCLUDED.domain_group,
            description  = EXCLUDED.description,
            updated_at   = NOW()
    """, [(r["domain_id"], r["name"], r["domain_group"], r["description"] or None)
          for r in rows])
    conn.commit()
    log.info("Upserted %d domains", len(rows))
    return len(rows)


def load_domain_details(conn) -> int:
    rows = _read_csv("domain_details.csv")
    if not rows:
        log.info("domain_details.csv is empty — skipping")
        return 0
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO catalogue.domain_details
            (detail_id, domain_id, name, unit, frequency, description, notes)
        VALUES %s
        ON CONFLICT (detail_id) DO UPDATE SET
            domain_id   = EXCLUDED.domain_id,
            name        = EXCLUDED.name,
            unit        = EXCLUDED.unit,
            frequency   = EXCLUDED.frequency,
            description = EXCLUDED.description,
            notes       = EXCLUDED.notes,
            updated_at  = NOW()
    """, [(
        r["detail_id"], r["domain_id"], r["name"],
        r["unit"] or None, r["frequency"] or None,
        r["description"] or None, r["notes"] or None,
    ) for r in rows])
    conn.commit()
    log.info("Upserted %d domain details", len(rows))
    return len(rows)


def load_sources(conn) -> int:
    rows = _read_csv("sources.csv")
    if not rows:
        log.info("sources.csv is empty — skipping")
        return 0
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO catalogue.sources
            (source_id, name, provider, category, tier, url, api_url,
             auth_type, auth_env_var, format, update_frequency, notes)
        VALUES %s
        ON CONFLICT (source_id) DO UPDATE SET
            name             = EXCLUDED.name,
            provider         = EXCLUDED.provider,
            category         = EXCLUDED.category,
            tier             = EXCLUDED.tier,
            url              = EXCLUDED.url,
            api_url          = EXCLUDED.api_url,
            auth_type        = EXCLUDED.auth_type,
            auth_env_var     = EXCLUDED.auth_env_var,
            format           = EXCLUDED.format,
            update_frequency = EXCLUDED.update_frequency,
            notes            = EXCLUDED.notes,
            updated_at       = NOW()
    """, [(
        r["source_id"], r["name"], r["provider"], r["category"], int(r["tier"]),
        r["url"] or None, r["api_url"] or None,
        r["auth_type"] or None, r["auth_env_var"] or None,
        r["format"] or None, r["update_frequency"] or None,
        r["notes"] or None,
    ) for r in rows])
    conn.commit()
    log.info("Upserted %d sources", len(rows))
    return len(rows)


def load_domain_detail_sources(conn) -> int:
    rows = _read_csv("domain_detail_sources.csv")
    if not rows:
        log.info("domain_detail_sources.csv is empty — skipping")
        return 0
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO catalogue.domain_detail_sources
            (detail_id, source_id, geo_levels, year_from, year_to, coverage_notes,
             series_id, verified)
        VALUES %s
        ON CONFLICT (detail_id, source_id) DO UPDATE SET
            geo_levels     = EXCLUDED.geo_levels,
            year_from      = EXCLUDED.year_from,
            year_to        = EXCLUDED.year_to,
            coverage_notes = EXCLUDED.coverage_notes,
            series_id      = EXCLUDED.series_id,
            verified       = EXCLUDED.verified,
            updated_at     = NOW()
    """, [(
        r["detail_id"], r["source_id"],
        r["geo_levels"] or None,
        int(r["year_from"]) if r["year_from"] else None,
        int(r["year_to"]) if r["year_to"] else None,
        r["coverage_notes"] or None,
        r["series_id"] or None,
        r["verified"].lower() == "true" if r.get("verified") else False,
    ) for r in rows])
    conn.commit()
    log.info("Upserted %d domain_detail_source mappings", len(rows))
    return len(rows)


def main() -> None:
    conn = None
    try:
        conn = psycopg2.connect(_dsn())
        apply_schema(conn)
        load_domains(conn)
        load_domain_details(conn)
        load_sources(conn)
        load_domain_detail_sources(conn)
        log.info("Catalogue load complete")
    except Exception:
        log.exception("Catalogue load failed")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
