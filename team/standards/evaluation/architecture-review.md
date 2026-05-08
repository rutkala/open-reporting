# Architecture Review Rules

**Derived from:** `team/knowledge-base/data-architecture/architecture.md` ✓ (KB complete — medallion, Kimball, dbt patterns, schema naming, SCD types)
**Used by:** `.claude/agents/architecture-critic.md`
**Does NOT cover:** code quality (see `evaluation/code-review.md`), statistical correctness (see `evaluation/analytical-review.md`), visual design (see `evaluation/visualization-diff.md`)

Rules applied by the `architecture-critic` agent on every implementation plan, before any code is written.

---

## BLOCK — Must Fix Before Implementing

A single BLOCK finding must be resolved before the plan is presented to the user or implemented.

### Layer violations

- **Raw schema queried from dashboard** — any plan proposing a dashboard or app reading from `raw.*` tables directly. Dashboards must query `curated.mart_*` (gold). Explorer querying `curated.all_indicators` (silver) is the one documented exception — do not flag it.
- **Transform logic in ingestion scripts** — any plan proposing Python code that cleans, reshapes, joins, or aggregates data before loading to raw. Ingestion lands data only; transforms belong in dbt.
- **New source without dbt staging model** — if a new data source is proposed and the plan does not mention a `stg_{source}.sql` dbt model to conform it to the shared schema.
- **Domain dashboard querying silver directly** — a new domain dashboard (not Explorer) proposed to query `curated.all_indicators` instead of a `curated.mart_{domain}` gold table.
- **Circular dependency** — component A importing from B while B imports from A; a dashboard importing from ingestion/processing code.

### Coupling violations

- **Dashboard importing from platform code** — `products/dashboards/` directly importing functions from `platform/ingestion/` or `platform/processing/`. The only shared layer between platform and products is the `complex_dashboard` skill (`.claude/skills/complex_dashboard/assets/`).

---

## CONDITIONAL — Address Before or During Implementation

These should be resolved or explicitly acknowledged before proceeding.

- **New raw table without `fetched_at`** — every raw table requires a `fetched_at TIMESTAMPTZ` column populated at ingest time.
- **Schema naming deviation** — new tables should follow `raw.{source}_{entity}` and `curated.{domain}_{metric}`. Flag significant deviations; minor variations are acceptable.
- **New ingestion without catalogue verification** — the ingestion standard requires verifying the source in `catalogue.sources` before writing code. Flag if the plan skips this step.
- **New dimension column without updating all staging models** — if the plan adds a new `dim_*` column to the shared silver schema, all existing staging models must also be updated. Flag if this cross-cutting change is not mentioned.
- **No upsert strategy for mutable data** — if a new table will receive repeated ingestions, it needs an `ON CONFLICT DO UPDATE` upsert pattern. Flag if not mentioned for non-append-only tables.
- **New dbt model without idempotency strategy** — new models should be either full-refresh or incremental with explicit `unique_key`. Flag if neither is mentioned.

---

## NOTE — Good to Address

Log in review output. Does not block.

- No index strategy mentioned for a new table with time or geography dimensions
- No idempotency strategy mentioned for new dbt models
- Missing rollback plan for schema changes on production tables
- No test coverage mentioned for new dbt models (not_null, unique, accepted_values)

---

## What This Agent Cannot Check

Be explicit about these — do not invent findings for things that require implementation detail:

- Whether the proposed data transformation logic is statistically correct (analytical-validator's job)
- Whether the SQL syntax is correct (only visible after implementation)
- Whether the chosen data source actually contains the required data (requires data inspection)
- Whether existing tables have the right indexes (requires warehouse introspection)
- Performance characteristics of proposed queries
