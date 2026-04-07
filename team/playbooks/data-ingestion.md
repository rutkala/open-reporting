# Playbook: Data Ingestion

Covers sub-products #1 (Data ingested) and #2 (Data curated — silver).

## Recipe

### Sub-product #1 — Data ingested into environment

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Research (source, indicators, format, cadence) | Data Research | `data-researcher` | `data-research-reviewer` | data-research-review.md |
| Design (raw DDL, ELT approach, upsert strategy) | Data Architecture | `data-architect` | `architecture-critic` | storage.md, ingestion.md → architecture-review.md |
| Build (ingestion script, DDL, sources.yml, tests) | Data Engineering | `data-engineer` | `data-engineer-reviewer` | ingestion.md → data-engineering-review.md |

### Sub-product #2 — Data curated (silver)

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Design (staging model structure, conformed dims) | Data Architecture | `data-architect` | `architecture-critic` | storage.md, processing.md → architecture-review.md |
| Build (dbt staging SQL, schema.yml, all_indicators union) | Data Engineering | `data-engineer` | `data-engineer-reviewer` | processing.md → data-engineering-review.md |

---

## Phase 1 — Research

Before any schema design or code, research the source:

1. **Identify the source** — official organisation, dataset name, publication URL
2. **Understand the data format** — API (REST/SDMX), file download (CSV/Excel/Parquet), manual export
3. **Map available indicators** — list all series/variables available; identify which are relevant to the warehouse domains
4. **Check update cadence** — how often is the data refreshed? Monthly, quarterly, annual?
5. **Check data quality flags** — does the source publish observation status codes (provisional, final, revised)?
6. **Check licence** — is the data open/public? Any attribution requirements?
7. **Check for existing ingestion** — is any part of this source already ingested? Look in `platform/ingestion/` and `platform/warehouse/raw/`

**Output:** A source summary (title, URL, format, cadence, relevant indicators, known quality issues) documented in the Linear issue comment before proceeding to design. Reviewed by `data-research-reviewer`.

---

## Phase 2 — Design (raw layer)

Read these before designing:
- `team/standards/build/storage.md` — schema naming, types, upsert pattern
- `team/standards/build/ingestion.md` — ELT phases, raw loading rules

Design decisions to document:
1. **Table name** — `raw.{source}_{entity}` following naming convention
2. **Primary key** — which columns form the natural key? (e.g. source_id + geo + period_date + dimension columns)
3. **Column types** — use DuckDB-appropriate types: `VARCHAR`, `DOUBLE`, `DATE`, `TIMESTAMPTZ`
4. **Update method** — upsert (`ON CONFLICT DO UPDATE`) vs append-only (if source is immutable)
5. **Fetched_at** — always `TIMESTAMPTZ NOT NULL DEFAULT NOW()`
6. **Indexes** — primary key + date index + geo index where applicable

Write the DDL in `platform/warehouse/raw/{source}_{entity}.sql`.

---

## Phase 3 — Build (ingestion script)

Follow `team/standards/build/ingestion.md` exactly. Key rules:

- **ELT only** — land data as-is. No business logic, no joins, no derived columns.
- **Script location** — `platform/ingestion/to_raw/{source}_{entity}.py`
- **Structure** — `#!/usr/bin/env python3`, `load_dotenv(override=True)`, lazy `_dsn()`, `logging.getLogger(__name__)`
- **DuckDB patterns** — use `read_csv()` / `read_parquet()` with explicit `columns=` schema; never iterate rows
- **Upsert** — `INSERT OR REPLACE` or `ON CONFLICT DO UPDATE` on all tables with unique keys
- **Idempotency** — running twice must produce the same result as running once
- **Test** — run the script once; query the raw table; verify row count and sample values

---

## Phase 4 — Design (staging model)

Read `team/standards/build/processing.md` and `team/standards/build/storage.md` shared staging schema (33-column output).

Design decisions:
1. **Grain** — what is one row? (source_id + detail_id + geo + period_date + dimension columns)
2. **Dimension mapping** — which of the 24 `dim_*` columns does this source populate? Use `null::varchar` for all others.
3. **detail_id values** — map source series codes to `dim_domain_detail.detail_id` values. Add new rows to the seed if needed.
4. **obs_status** — map source quality flags to the standard obs_status values

---

## Phase 5 — Build (staging model and seeds)

1. Create `platform/processing/dbt/models/{source}/stg_{source}.sql` — conform to 33-column shared schema
2. Add entry to `platform/processing/dbt/models/{source}/sources.yml` with `loaded_at_field: fetched_at`
3. Add `not_null` + `unique` tests on the grain key in `schema.yml`
4. Add `select * from {{ ref('stg_{source}') }}` to `all_indicators.sql`
5. Add source row to `platform/processing/dbt/seeds/dim_source.csv`
6. Add new indicator rows to `platform/processing/dbt/seeds/dim_domain_detail.csv` for any new detail_ids
7. Run: `dbt seed --full-refresh && dbt run --select stg_{source} all_indicators && dbt test --select stg_{source}`
8. Validate: row counts per source, NULL rates per dim column, sample values match raw table

---

## Checklist

- [ ] Source researched and documented in Linear
- [ ] Raw DDL written (`platform/warehouse/raw/{source}_{entity}.sql`)
- [ ] Raw DDL applied to warehouse
- [ ] Ingestion script written and idempotent
- [ ] Script runs without error; raw table has expected rows
- [ ] Staging model written with all 33 columns (null for unused dims)
- [ ] sources.yml entry added
- [ ] schema.yml tests added
- [ ] all_indicators.sql updated
- [ ] dim_source.csv updated
- [ ] dim_domain_detail.csv updated for new indicators
- [ ] dbt seed + run + test all pass
- [ ] Row counts and sample values validated
