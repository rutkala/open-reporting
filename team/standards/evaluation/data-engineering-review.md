# Data Engineering Review Rules

**Derived from:** `team/knowledge-base/data-engineering/engineering.md` ✓, `team/knowledge-base/data-architecture/architecture.md` ✓
**Used by:** `.claude/agents/data-engineer-reviewer.md`
**Does NOT cover:** general code quality (see `evaluation/code-review.md`), layer violations at plan level (see `evaluation/architecture-review.md`), statistical correctness (see `evaluation/analytical-review.md`)

Rules applied by the `data-engineer-reviewer` agent on every PR diff touching `platform/`. These rules are ADDITIVE to `code-review.md` — both agents run in parallel. Do not duplicate findings already in code-review scope.

---

## P1 — Blocks Merge

### ELT violations

- **Transform logic in ingestion script** — any Python code in `products/ingestion/` that derives new columns, filters rows based on domain criteria, joins to reference tables, applies business rules about data validity, or aggregates before loading. Ingestion must land raw data only. The permitted boundary: strip whitespace, parse dates, add `fetched_at`. Everything else belongs in dbt.
- **Python row iteration over DuckDB insert** — using `for row in data: conn.execute("INSERT ...")` instead of a single `INSERT ... SELECT FROM read_csv(...)`. Row-by-row Python inserts bypass DuckDB's vectorised engine and are orders of magnitude slower.

### dbt correctness

- **Mart or staging model querying `raw.*` directly without a `source()` reference** — dbt models must reference raw tables via `{{ source('raw', 'table_name') }}`, not `FROM raw.table_name` as a literal string. Literal raw references bypass dbt's lineage graph and dependency tracking.
- **`ref()` used to reference a staging model that does not exist in the project** — a `{{ ref('stg_something') }}` call where no `stg_something.sql` file exists in the dbt project. This will fail at runtime.
- **`sources.yml` missing entry for a new raw table referenced by a staging model** — every `{{ source() }}` call requires a corresponding entry in `sources.yml`. Absence means dbt cannot resolve the lineage or run `dbt source freshness`.

### Type safety

- **Raw cast without `TRY_CAST` on external data** — using `CAST(value AS DOUBLE)` directly on columns ingested from external sources (CSV, API responses). External data contains nulls, empty strings, and unexpected formats. `TRY_CAST` returns `NULL` on failure instead of throwing a runtime error.

---

## P2 — Should Fix

### Idempotency

- **Incremental dbt model without `unique_key`** — any dbt model using `materialized='incremental'` must declare `unique_key` in its config. Without it, incremental runs append duplicates rather than merge. Every incremental model must be safe to re-run.
- **`INSERT INTO` on a raw table without upsert strategy** — bare `INSERT INTO` on a table that receives repeated ingestions will produce duplicates. Use `INSERT OR REPLACE` or `ON CONFLICT DO UPDATE`. Append-only tables (audit logs, event streams) are the only exception — document the intent with a comment.
- **New ingestion script without idempotency guarantee** — if a script is run twice, it should produce the same result as running it once. If it does not, document explicitly why (e.g. append-only by design).

### Schema conventions

- **New raw table without `fetched_at TIMESTAMPTZ`** — every raw table must include `fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`. This is the audit trail for when data was ingested.
- **New raw table without `NOT NULL` constraints on key columns** — the primary key columns of a raw table (source_code, period_date, or equivalent) must be `NOT NULL`. Allows the upsert `ON CONFLICT` clause to function correctly.
- **Schema naming deviation** — new raw tables should follow `raw.{source}_{entity}` (e.g. `raw.gus_population`, `raw.eurostat_gdp`). New curated tables should follow `curated.{domain}_{metric}` for marts or `curated.stg_{source}` for staging.

### dbt quality

- **New dbt model without test coverage** — every new dbt model should have at least `not_null` + `unique` tests on its primary key in `schema.yml`. Models without tests produce undetected silent failures.
- **Staging model missing grain declaration comment** — every staging model should open with a comment stating: `-- Output grain: one row per (dimension1, dimension2, period_date)`. This documents the intended uniqueness constraint.
- **New `sources.yml` entry without `loaded_at_field`** — Eurostat, NBP, and GUS sources should specify `loaded_at_field: fetched_at` to enable `dbt source freshness` monitoring.

### Python conventions

- **`read_csv` / `read_parquet` without explicit `columns` schema** — production ingestion should declare expected column types in the DuckDB file function call. Relying on auto-detection allows schema drift to go undetected.
- **Database connection not using the `_dsn()` lazy pattern** — new scripts should follow the project's lazy DSN pattern: `_dsn()` function that reads env vars, called only when a connection is actually needed. Eager DSN construction at import time breaks CLI tooling and unit tests.

---

## P3 — Noted

- New dbt model without a `description` field in `schema.yml` (makes the dbt docs site incomplete)
- No `dbt test` invocation mentioned in the PR description for a new model
- Ingestion script missing `--dry-run` flag or equivalent for safe local testing
- `ignore_errors=true` in `read_csv` without a comment explaining why silent errors are acceptable
- Hardcoded `/opt/open-reporting/` path in a script that should use a config var

---

## What this agent does NOT flag

- General Python style issues not listed above — covered by `code-reviewer`
- SQL injection (parameterised queries) — covered by `code-reviewer` P1
- Missing `fetched_at` in general — covered by `code-reviewer` P2 (do not duplicate)
- Architectural layer violations at plan level — `architecture-critic`'s job
- Statistical correctness of aggregations — `analytical-validator`'s job
- Whether the source data actually exists or matches expectations — requires data access, not code review
