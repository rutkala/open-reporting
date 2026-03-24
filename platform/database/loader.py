#!/usr/bin/env python3
"""
Catalogue loader — upserts domains, sources, and source_domains into PostgreSQL.
Run after any change to platform/database/data/*.csv

Usage:
    PYTHONPATH=/opt/open-reporting python3 platform/database/loader.py
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
        return list(csv.DictReader(f))


def apply_schema(conn) -> None:
    cur = conn.cursor()
    for sql_file in sorted(DDL_DIR.glob("*.sql")):
        log.info("Applying %s", sql_file.name)
        cur.execute(sql_file.read_text())
    conn.commit()
    log.info("Schema ready")


def load_domains(conn) -> int:
    rows = _read_csv("domains.csv")
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO catalogue.domains (domain_id, name, group_name, description)
        VALUES %s
        ON CONFLICT (domain_id) DO UPDATE SET
            name        = EXCLUDED.name,
            group_name  = EXCLUDED.group_name,
            description = EXCLUDED.description,
            updated_at  = NOW()
    """, [(r["domain_id"], r["name"], r["group_name"], r["description"] or None)
          for r in rows])
    conn.commit()
    log.info("Upserted %d domains", len(rows))
    return len(rows)


def load_sources(conn) -> int:
    rows = _read_csv("sources.csv")
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO catalogue.sources
            (source_id, name, provider, tier, url, api_url,
             auth_type, auth_env_var, format, update_frequency, notes)
        VALUES %s
        ON CONFLICT (source_id) DO UPDATE SET
            name             = EXCLUDED.name,
            provider         = EXCLUDED.provider,
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
        r["source_id"], r["name"], r["provider"], int(r["tier"]),
        r["url"] or None, r["api_url"] or None,
        r["auth_type"] or None, r["auth_env_var"] or None,
        r["format"] or None, r["update_frequency"] or None,
        r["notes"] or None,
    ) for r in rows])
    conn.commit()
    log.info("Upserted %d sources", len(rows))
    return len(rows)


def load_source_domains(conn) -> int:
    rows = _read_csv("source_domains.csv")
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO catalogue.source_domains
            (source_id, domain_id, geo_levels, year_from, year_to, coverage_notes)
        VALUES %s
        ON CONFLICT (source_id, domain_id) DO UPDATE SET
            geo_levels     = EXCLUDED.geo_levels,
            year_from      = EXCLUDED.year_from,
            year_to        = EXCLUDED.year_to,
            coverage_notes = EXCLUDED.coverage_notes,
            updated_at     = NOW()
    """, [(
        r["source_id"], r["domain_id"],
        r["geo_levels"] or None,
        int(r["year_from"]) if r["year_from"] else None,
        int(r["year_to"]) if r["year_to"] else None,
        r["coverage_notes"] or None,
    ) for r in rows])
    conn.commit()
    log.info("Upserted %d source_domain mappings", len(rows))
    return len(rows)


def main() -> None:
    conn = None
    try:
        conn = psycopg2.connect(_dsn())
        apply_schema(conn)
        load_domains(conn)
        load_sources(conn)
        load_source_domains(conn)
        log.info("Catalogue load complete")
    except Exception:
        log.exception("Catalogue load failed")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
