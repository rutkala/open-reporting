# Data Architecture Knowledge Base

Agent reference for warehouse architecture decisions, schema design, and layer enforcement.
Read at the start of `/plan` for any task involving ingestion, transformation, new tables, new
dbt models, schema changes, or architectural review. The `architecture-critic` agent reads this
file as its primary theory backing.

**Sources:** Kimball Group (kimballgroup.com), Databricks Medallion Architecture documentation,
dbt Labs Developer Hub (docs.getdbt.com), DuckDB official documentation (duckdb.org),
Data Vault 2.0 canonical literature, Wikipedia dimensional modeling, dbt blog surrogate key guide.

---

## 1. Medallion Architecture

### 1.1 Origin and Purpose

The medallion (bronze-silver-gold) architecture was formalised by Databricks as a lakehouse
design pattern. Its core guarantee: data quality increases monotonically as rows move from
bronze through silver to gold. Each layer makes an explicit contract with its consumers.
The pattern maps directly to the DWH principle that raw source data must be preserved
separately from the transformed analytical layer — a principle present in Kimball's staging
area concept and in Inmon's ODS pattern before the term "medallion" was coined.

### 1.2 Layer Contracts

**Bronze / Raw — source fidelity layer**

Contract: "I contain exactly what the source system produced."

- Data is ingested as-received. No cleaning, no reshaping, no type coercion beyond what is
  required to land the row in a SQL table.
- Source structure is preserved. Column names, codes, and values match the upstream API or file.
- Every row carries `fetched_at TIMESTAMPTZ` — the wall-clock time when the row was ingested.
  This is the audit trail. Without it, you cannot determine whether a stale dashboard is caused
  by a data source issue or a pipeline failure.
- Raw data is append-only or upsert-only. It is NEVER modified retroactively unless the source
  issued a correction and the re-ingestion is fully documented.
- Raw tables are the ingest target. They are NOT query targets for analytical consumers.

What is FORBIDDEN in the raw layer:
- Business logic (rounding, categorisation, computed ratios)
- Joins to other sources
- Aggregation
- Renaming columns to match a house standard (that belongs in staging/silver)
- Boolean flags derived from business rules

**Silver / Curated staging — integration and conformance layer**

Contract: "I have validated, typed, and conformed this data to the house schema.
Every row is a single observable measurement at a declared grain."

- Business keys are resolved. External codes are mapped to internal identifiers.
- Data types are enforced. Nulls are explicit (`null::varchar`, never empty string).
- Dimensions are named semantically (e.g. `dim_sex`, `dim_nace_sector`), not positionally.
- The grain is explicitly declared. Every staging model header should state:
  "Output grain: one row per (detail_id, geo, period_date, [dim_*])."
- Source-specific dimension slots that are not applicable are `null`, not a placeholder.
- Multiple sources are unioned into a single integration table at this layer
  (`all_indicators` in this project). This is the integration bus.

What is FORBIDDEN in the silver layer:
- Domain-specific business logic (e.g. "is_poland", "fiscal_category") — these belong in gold
- Pre-aggregation across the grain
- UI labels (Polish column names, display strings) — these belong in gold or the dashboard
- Direct queries from domain dashboards (Explorer is the one documented exception because it
  exposes the raw indicator catalogue — this is intentional, not a violation)

**Gold / Mart — business-ready layer**

Contract: "I contain pre-joined, labelled, domain-relevant rows that a dashboard or analyst
can query with minimal additional logic."

- One mart per domain. A mart selects from silver, filters to its domain, joins to dimension
  seeds for labels, pre-computes derived metrics, and drops inapplicable dim columns.
- Polish user-facing labels (country names, indicator names, axis labels) belong here.
- Boolean convenience flags (`is_poland`, `is_projection`, `is_eu_aggregate`) belong here.
- Derived metrics (YoY change, % of GDP) belong here when they are universally used by the
  domain dashboard; otherwise compute in the dashboard layer.
- Domain dashboards (Labour, Finance, etc.) query ONLY gold marts.
- The grain of a gold mart must be explicitly declared and consistent with its silver source.

What is FORBIDDEN in the gold layer:
- Raw table references (no `from raw.*` in a mart model)
- Metrics from a different domain (Finance mart must not contain Labour indicators)
- Cross-domain joins at the mart level — use conformed dimensions instead

### 1.3 Layer Violation Consequences

Bypassing layers causes structural coupling. A dashboard that queries `raw.*` directly:
1. Depends on the ingestion schema — any source format change breaks the dashboard
2. Bypasses all data quality validation applied in staging
3. Cannot benefit from performance optimisations applied in gold (pre-joins, type coercions)
4. Makes the ingestion contract and the query contract the same contract — impossible to
   evolve one without breaking the other

The same failure mode applies to transform logic in ingestion scripts. When a Python ingestor
cleans, aggregates, or reshapes data before loading to raw, the raw layer no longer contains
the source truth. Debugging a pipeline discrepancy requires guessing what the script did.

---

## 2. Dimensional Modelling (Kimball)

### 2.1 Core Concepts

Dimensional modelling (Ralph Kimball, *The Data Warehouse Toolkit*, 1996) organises analytical
data into two table types: **fact tables** and **dimension tables**. This is not just a schema
convention — it encodes the epistemological structure of business measurement.

**Fact table** — a table where every row represents one measurement event at the declared grain.
Columns are: foreign keys to dimension tables, numeric additive measures, and degenerate
dimensions (codes that do not warrant their own dimension table). Fact tables are narrow in
measure columns, wide in foreign keys.

**Dimension table** — a table where every row describes one entity that provides context for
measurements. Columns are descriptive attributes: names, codes, hierarchies, labels.
Dimension tables are typically wide (many descriptive columns) and slowly changing.

**Grain declaration** — the most important decision in dimensional modelling. The grain is a
precise English statement of what one row in the fact table represents. Atomic grain (lowest
possible level of detail) is always preferred — you can always aggregate upward, but you cannot
decompose a pre-aggregated fact.

Example grain declarations:
- "One row per statistical indicator per geography per period per applicable dimension combination"
  → this is the grain of `curated.all_indicators`
- "One row per source per fiscal indicator per country per year"
  → this is the grain of `curated.mart_finance`

If you cannot state the grain precisely, the model is not ready to build.

### 2.2 Conformed Dimensions and the Bus Matrix

A **conformed dimension** is a dimension table that is defined once and referenced by multiple
fact tables. The key property: every attribute of a conformed dimension means the same thing in
every context where it is used. If `dim_geo` defines geography codes consistently, any two fact
tables that reference `dim_geo` can be joined — this is called **drill-across**.

Without conformed dimensions, cross-domain analysis requires bespoke joins with undocumented
assumptions. With them, you can ask "what is the employment rate in regions where GDP growth
exceeded X%?" without building a one-off integration.

The **bus matrix** is the planning tool: rows are business processes (domains), columns are
dimensions. A tick at the intersection means that dimension is used in that domain's fact table.
Conformed dimensions appear in multiple rows. A column with only one tick is either a local
dimension (acceptable) or a missed conformance opportunity (investigate).

In this project: `dim_source`, `dim_domain_detail`, `dim_geo`, `dim_calendar` are conformed
dimensions. They are defined as dbt seeds and referenced by all staging models that populate
`all_indicators`.

### 2.3 Slowly Changing Dimensions (SCDs)

Dimension attributes change over time. The SCD strategy determines what history is preserved.

| Type | Strategy | Use when |
|------|----------|----------|
| SCD Type 0 | Never update — retain original value | Attributes that should never change (birth year, accession year) |
| SCD Type 1 | Overwrite with new value — no history | Fixing errors; attributes where history is irrelevant |
| SCD Type 2 | Add a new row with effective dates — full history | Attributes where history matters (country classification changes) |
| SCD Type 3 | Add a "previous value" column | When only one prior value is needed and rows must not multiply |

**Default for this project:** Dimension seeds (`dim_domain_detail.csv`, `dim_source.csv`) are
SCD Type 1 — they are managed files that are rebuilt on `dbt seed --full-refresh`. For
geography codes (NUTS revisions), SCD Type 2 should be applied if a NUTS code is reassigned,
to preserve historical analysis.

### 2.4 Surrogate vs Natural Keys

**Natural key** — the identifier from the source system (NUTS code, Eurostat dataset code,
GUS variable ID). Natural keys are meaningful to the business but can change when source systems
change.

**Surrogate key** — a system-generated identifier (integer sequence or hash of natural key
components). Surrogate keys decouple fact table foreign keys from source system changes.

**Rule for this project:** In `all_indicators` and its staging inputs, the natural key
combination (`source_id`, `detail_id`, `geo`, `period_date`, applicable `dim_*` values) serves
as the composite grain key. There is no integer surrogate — this is intentional and correct for
a columnar analytical store. DuckDB performs well on composite key joins. Integer surrogates
add no performance benefit in DuckDB's vectorised execution model and create a dependency on
a sequence generator that is unnecessary in an ELT pipeline.

For dimension tables: natural keys from seeds are the primary keys (e.g. `detail_id`,
`source_id`). This is appropriate because seed data is controlled by the pipeline team, not
by an external source that might reassign keys.

---

## 3. Star Schema vs Snowflake Schema

### 3.1 Structural Difference

**Star schema** — fact table at the centre, each dimension fully denormalised into one wide
table. A four-dimension fact table joins to exactly four tables. Queries are simple.

**Snowflake schema** — dimension hierarchies are normalised into multiple linked tables.
A geography dimension might split into `dim_geo → dim_region → dim_country`. More joins
required per query.

### 3.2 Performance Implications for OLAP

Analytical queries scan many rows and filter on few columns. Column-store engines (DuckDB,
BigQuery, Snowflake, Redshift) exploit this with vectorised reads. The join count matters
more than storage efficiency in this context.

Star schema delivers 40-60% faster analytical query performance through fewer joins (DataCamp,
2024). Each additional join in a snowflake schema introduces CPU overhead and prevents certain
query plan optimisations (e.g. predicate pushdown through a single-hop join).

DuckDB's vectorised execution engine is specifically optimised for the scan-aggregate-join
pattern of star schema queries. Its zone map implementation (min/max metadata per column
chunk) also works most effectively on denormalised wide dimension tables.

### 3.3 Decision Rule

**Always use star schema for analytical marts in this project.**

The only valid reason to normalise a dimension (partial snowflaking) is:
- The dimension hierarchy has 4+ levels with large cardinality at each level, AND
- Storage is a genuine constraint (it is not — DuckDB single-file format on a modern server)

In practice: `dim_domain_detail` carries all indicator metadata in one wide table. It is not
split into `dim_domain → dim_indicator_group → dim_indicator`. That would be textbook
unnecessary snowflaking.

---

## 4. dbt Patterns for This Project

### 4.1 The Staging Contract (one-to-one with source)

Each staging model is a one-to-one reflection of one source entity. It selects from
`{{ source('raw', 'table_name') }}`, not from another model. It does not join two sources
— that happens in the integration layer (`all_indicators.sql`).

Staging model responsibilities (and nothing else):
1. Select from the raw source table
2. Rename columns to match the house schema (`source_id`, `detail_id`, `geo`, etc.)
3. Cast types explicitly (`value::double`, `period::date`)
4. Map source-specific dimension codes to named `dim_*` columns
5. Apply `null::varchar as dim_{name}` for all 24 dim columns not populated by this source
6. Filter out rows that cannot be staged (e.g. `where value is not null`)

What staging models must NOT do:
- Join to another source's raw table
- Apply business categorisation logic
- Aggregate or pivot
- Apply Polish labels

**Naming:** `stg_{source}.sql` → outputs to `curated.stg_{source}`. Single file per source.
If a source has multiple entity types that need separate staging logic, use CTEs within the
single file rather than splitting into multiple staging models (keeps the union in
`all_indicators.sql` manageable).

### 4.2 The All-Indicators Integration Model

`all_indicators.sql` is a UNION ALL of all `stg_*` models. Its sole job is to union.
No filtering, no joining, no transformations. Any logic belongs upstream (in stg_) or
downstream (in mart_).

This model materialises as a `table` in `curated` schema. It is the Silver layer.

### 4.3 Mart Model Pattern

A mart model:
1. Selects from `{{ ref('all_indicators') }}` (Silver) filtered to its domain
2. Joins to dimension seeds for labels (`{{ ref('dim_domain_detail') }}`, etc.)
3. Derives domain-specific computed columns
4. Drops inapplicable dim columns (reduces output width)
5. Assigns Polish display labels

Every mart declares its grain explicitly in a SQL comment header (see `mart_finance.sql`).

**Naming:** `mart_{domain}.sql` → outputs to `curated.mart_{domain}`.

### 4.4 `ref()` vs `source()`

| Situation | Use |
|-----------|-----|
| Selecting from a raw table | `{{ source('raw', 'table_name') }}` |
| Selecting from another dbt model | `{{ ref('model_name') }}` |
| Never | Hardcoded schema.table strings in dbt SQL |

`source()` registers the dependency between the dbt project and the raw schema, enabling
dbt to compute freshness checks and lineage. `ref()` enables dbt to resolve cross-environment
table names (dev/prod) and build the DAG correctly.

### 4.5 Idempotency

A dbt model is idempotent if running it twice produces the same result as running it once.
All models in this project must be idempotent.

For `table` materialisation: DuckDB drops and recreates the table on every `dbt run`.
Idempotency is structural — it is guaranteed by the materialization.

For `incremental` materialisation: idempotency requires a `unique_key` parameter and a
`merge` or `delete+insert` strategy. Without `unique_key`, append strategy will duplicate rows
on re-run. The raw layer uses upsert (`ON CONFLICT DO UPDATE`) in the ingestion script —
this is the idempotency guarantee for bronze. dbt models inherit it if they read from raw
via `source()`.

**Rule:** Staging and mart models use `materialized='table'`. Incremental materialisation
is appropriate only for very large fact tables (>100M rows) where full rebuild time exceeds
acceptable pipeline SLA. At the current data volumes in this project, `table` is always correct.

### 4.6 Test Coverage Expectations

Minimum test coverage for every model:

| Test | Applies to | Required |
|------|-----------|---------|
| `unique` | grain key combination | Yes — on all stg_* and mart_* models |
| `not_null` | `detail_id`, `geo`, `period_date`, `value` | Yes |
| `accepted_values` | `source_id`, `domain_id` | Yes — prevents silent bad mappings |
| `relationships` | `detail_id` → `dim_domain_detail` | Yes for mart models |

Staging tests are more important than mart tests — a staging defect propagates to all downstream
marts and dashboards. Catching it at the source is always cheaper.

---

## 5. Schema Naming Conventions — What the Names Encode

Naming conventions are not cosmetic. They encode layer, source, and domain in the table
identifier, making architectural role immediately legible.

```
raw.{source}_{entity}
```
- `raw.` — bronze layer, source-fidelity guarantee, never modified
- `{source}` — the external data provider (eurostat, dbw, nbp, imf, openbudget)
- `{entity}` — the logical entity from that source (observations, exchange_rates, execution)

```
curated.stg_{source}
```
- `curated.` — this is a transformed/validated table
- `stg_` prefix — staging model; one-to-one with a source; intermediate, not a query target

```
curated.all_indicators
```
- No prefix — the integration bus; the Silver layer; one table for all sources

```
curated.mart_{domain}
```
- `mart_` prefix — gold layer; domain-specific; safe for dashboard queries
- `{domain}` — business domain (finance, labour, demographics, ...)

```
curated.dim_{entity}
```
- `dim_` prefix — conformed dimension; managed as a seed; reused across domains

```
curated.fact_{process}
```
- `fact_` prefix — reserved for future explicit fact tables if `all_indicators` is decomposed

**Anti-patterns to reject:**
- `curated.eurostat_gdp` — looks like a mart but has no domain prefix; ambiguous layer
- `raw.labour_employment` — looks like a domain mart in the raw schema; confusing
- `curated.data` — no source or entity context; meaningless
- `temp_*` or `staging_*` outside the dbt model namespace — ad-hoc tables in the warehouse

---

## 6. Data Quality at Layer Boundaries

### 6.1 Raw → Silver (Staging Boundary)

The staging model is the first data quality checkpoint. At this boundary, validate:

1. **Row count check** — staging output row count should be ≥ raw input row count after
   filtering nulls. A staging model that drops >10% of raw rows is suspicious.
2. **Key uniqueness** — `unique` test on the composite grain key. Duplicates at staging mean
   the grain declaration is wrong or the source has duplicate rows.
3. **Null rate on `value`** — staging filters `where value is not null`. Log the null rate
   before filtering. Null rates >50% may indicate a mapping error in the dimension_key join.
4. **`detail_id` referential integrity** — every `detail_id` in the staging output must exist
   in `dim_domain_detail.csv`. A missing `detail_id` means a catalogue mapping is missing.
5. **`source_id` and `domain_id` accepted values** — unexpected values indicate a mapping
   error in the staging SQL.

### 6.2 Silver → Gold (Mart Boundary)

At the mart boundary, validate:

1. **Domain filter completeness** — the mart's `where domain_id = 'XYZ'` should capture
   all expected indicators. Row count vs `all_indicators` filtered to that domain should
   match (minus intentional exclusions).
2. **Grain preservation** — if the mart re-grains (e.g. drops some dim columns), ensure
   the resulting combination remains unique. Run `unique` test on the mart grain.
3. **Dimension join coverage** — `LEFT JOIN` to `dim_domain_detail` should produce zero
   unmatched `detail_id` rows. An unmatched join produces a NULL `detail_name` — silent
   data loss in the dashboard.
4. **No new nulls in label columns** — `detail_name`, `country_name`, and other derived
   label columns should be NOT NULL. A null label in the dashboard is a user-visible defect.
5. **Temporal completeness** — the date range in the mart should match the expected coverage
   for the domain's sources. Missing recent periods indicate a pipeline gap.

### 6.3 Gold → Dashboard (Query Boundary)

This is not a transformation boundary but an access boundary. Validate:

1. **Schema reference** — dashboard imports query `curated.mart_{domain}`, not `raw.*` or
   `curated.all_indicators` (except Explorer).
2. **Filter pushdown** — dashboard filters (year range, geography, indicator) should
   correspond to indexed columns in the mart. Filtering on non-indexed columns on large marts
   causes full scans.
3. **No analytical logic in dashboard layer** — if a dashboard callback computes a ratio,
   running total, or YoY change that is universally needed, it should be promoted to the mart.

---

## 7. Data Vault 2.0 — Where It Fits and Why We Don't Use It

Data Vault 2.0 (Dan Linstedt) organises raw historical data into Hubs (business keys),
Links (relationships between hubs), and Satellites (descriptive attributes with full history).
It is append-only, source-driven, and maximally flexible.

**Why Data Vault is not appropriate for this project:**

1. **Scale mismatch** — Data Vault is designed for enterprise warehouses with dozens of
   source systems, complex many-to-many relationship tracking, and strict auditing requirements.
   This project has ~5 data sources with stable, well-understood schemas.

2. **Query complexity** — querying Data Vault requires joining Hub + Satellite (+ Link for
   cross-entity queries). Every analytical query becomes 3-5 joins. For a DuckDB analytical
   workload, this erases the columnar join performance advantage.

3. **No business vault benefit** — the Business Vault tier (where cross-source business logic
   lives) is equivalent to the silver/gold layers we already have. Adding a Raw Vault tier
   would duplicate the raw layer.

4. **Hybrid use case** — the one legitimate Data Vault pattern worth borrowing is hash-based
   integration keys for source-agnostic fact table joins. This project achieves the same
   outcome through natural composite keys (`detail_id`, `geo`, `period_date`) which are
   semantically richer than opaque hashes.

**Verdict:** Kimball dimensional modelling with a medallion layer structure is the correct
choice for this project. Data Vault adds auditing and flexibility overhead that is not needed
at this scale.

---

## 8. DuckDB Architectural Implications

### 8.1 Why DuckDB is the Right Warehouse Engine Here

DuckDB is an in-process OLAP engine with columnar-vectorised execution. For this project:

- **Single-file warehouse** — `warehouse.duckdb` is the entire warehouse. No server process,
  no network I/O, no connection pooling complexity. Simplicity is a feature.
- **Columnar storage** — analytical queries that scan millions of rows but read 3-5 columns
  pay I/O only for those columns. Exactly the access pattern of `all_indicators`.
- **Vectorised execution** — DuckDB processes batches of rows in CPU cache-friendly vectors,
  not row-by-row. 30-50x faster than SQLite on analytical aggregation workloads.
- **Automatic parallelisation** — multi-core joins and scans without configuration.
- **Zone maps** — DuckDB stores min/max metadata per column chunk, enabling selective skipping.
  This makes date range filters on `period_date` extremely fast on sorted data.

### 8.2 DuckDB-Specific Schema Decisions

These decisions are derived from DuckDB's architecture and are distinct from generic SQL advice:

- **No integer surrogate keys in fact tables** — DuckDB's vectorised hash join on string
  composite keys is fast. Integer surrogates would add a sequence generator dependency with
  no measurable performance benefit.
- **`TIMESTAMPTZ` not `TIMESTAMP`** — DuckDB stores TIMESTAMPTZ as UTC internally. Use it
  for all audit columns (`fetched_at`, `updated_at`).
- **`DOUBLE` not `NUMERIC` for analytical values** — `NUMERIC(18,2)` is appropriate for
  financial ledger values where exact decimal arithmetic is required. For statistical indicators
  (rates, indices, percentages) `DOUBLE` is correct and faster for aggregation.
- **Full overwrite pattern** — DuckDB cannot `DELETE FROM` a table with a compound primary key
  index without raising a FatalException. Use `DROP TABLE + recreate DDL + INSERT` for
  full-overwrite loads.
- **Indexes** — DuckDB uses zone maps for columnar predicate pushdown. Traditional B-tree
  indexes are less impactful than in row-store databases. Create indexes on `period_date` and
  `geo` for the most common dashboard filter patterns, but do not over-index.

---

## 9. Applied Rules for Architecture Review

The following rules are directly enforceable by the `architecture-critic` agent. Each rule
cites the theoretical principle it enforces.

### BLOCK — Reject the plan before implementation

**RULE BLOCK-01** — A dashboard model (Dash app callback, chart component) imports from or
queries `raw.*` tables directly.
→ Violates medallion layer contract. Raw is source-fidelity only; no consumer SLA.
→ Kimball principle: staging area is a mandatory intermediary between source and consumption.

**RULE BLOCK-02** — A new domain dashboard (not Explorer) queries `curated.all_indicators`
directly.
→ Violates gold layer contract. Dashboards must query `curated.mart_{domain}`.
→ Silver is an integration bus, not a query target. Business logic and labels are not present.
→ Exception: Explorer is documented and intentional — it exposes the indicator catalogue.

**RULE BLOCK-03** — An ingestion script applies transformations (cleaning, reshaping, joins,
aggregations, type casting to business types) before loading to raw.
→ Violates ELT principle. Ingestion is Extract + Load only. Transform belongs in dbt.
→ Consequence: raw no longer reflects the source truth; pipeline debugging becomes guesswork.

**RULE BLOCK-04** — A new data source is proposed without a `stg_{source}.sql` dbt staging
model conforming the source to the 33-column shared schema.
→ Violates the integration contract of `all_indicators`. Unmodelled sources cannot be unioned.
→ dbt Labs principle: every source must be represented by exactly one staging model.

**RULE BLOCK-05** — A mart model (`curated.mart_{domain}`) selects from `raw.*` instead of
`{{ ref('all_indicators') }}`.
→ Violates the medallion layer sequence: raw → silver → gold.
→ Marts must be built on silver, not raw. Data quality validation in staging is bypassed.

**RULE BLOCK-06** — A circular dependency is proposed (component A imports B, B imports A;
or a dashboard imports from `products/ingestion/` or `platform/processing/`).
→ Violates module boundary. The shared library between platform and products is
  the `complex_dashboard` skill (`.claude/skills/complex_dashboard/assets/`) only.

**RULE BLOCK-07** — A new column is added to `all_indicators.sql` that does not exist in
all existing `stg_*.sql` staging models.
→ Violates the union contract. All staged sources must output identical column sets.
→ When a new `dim_*` column is introduced, ALL staging models must emit it as `null::varchar`.

**RULE BLOCK-08** — An integration or mart model uses `SELECT *` from `all_indicators`.
→ The shared 33-column schema must be consumed explicitly by column name. `SELECT *` is
  fragile: any column addition or reordering breaks downstream consumers silently.

### CONDITIONAL — Flag and require justification

**RULE COND-01** — A new `raw.*` table is proposed without a `fetched_at TIMESTAMPTZ` column.
→ Audit trail requirement. Without `fetched_at`, pipeline staleness cannot be diagnosed.
→ Every raw table must carry the ingestion timestamp.

**RULE COND-02** — A new table's name does not follow `raw.{source}_{entity}` or
`curated.{domain}_{metric}` convention.
→ Names encode layer and origin. Deviations make architectural role ambiguous in code review.

**RULE COND-03** — A new ingestion script is proposed without catalogue verification step.
→ Ingestion standard requires verifying source existence in the catalogue before writing code.
→ Uncatalogued sources cannot be routed to the correct `domain_id` in staging.

**RULE COND-04** — A new dimension column (`dim_{name}`) is added to one staging model
without updating all other staging models.
→ Union contract violation. All stg_* must emit identical column sets for `all_indicators`.
→ Any stg_* that does not emit the new column will fail the UNION ALL at `dbt run` time.

**RULE COND-05** — A table that receives repeated ingestions has no upsert strategy defined.
→ Without `ON CONFLICT DO UPDATE`, repeated ingestion duplicates rows.
→ Storage standard requires explicit conflict target on all mutable tables.

**RULE COND-06** — A dashboard component imports functions directly from `products/ingestion/`
or `platform/processing/`.
→ Tight coupling: a product artefact depends on a platform artefact outside the shared library.
→ Shared surface is the `complex_dashboard` skill (`.claude/skills/complex_dashboard/assets/`) only.

**RULE COND-07** — A mart model uses `INNER JOIN` to a dimension seed without checking that
all `detail_id` values are present in the seed.
→ Inner join to dimension silently drops rows with unmapped keys.
→ Use LEFT JOIN; test for null `detail_name` post-join.

**RULE COND-08** — A staging model filters out rows using business logic (e.g.
`WHERE obs_status != 'deprecated'`) without documenting why.
→ Staging filters should be limited to structural nulls, not business rules.
→ Business filters belong in gold marts where the rationale is domain-visible.

**RULE COND-09** — A mart model's grain is not declared in a SQL comment.
→ Grain declaration is mandatory (Kimball four-step design process, step 2).
→ Without it, future maintainers cannot determine whether a schema change is safe.

**RULE COND-10** — An incremental dbt model is proposed without a `unique_key` parameter.
→ Without `unique_key`, re-runs append duplicate rows. Violates idempotency requirement.
→ dbt Labs: always set `unique_key` for incremental materialisation.

**RULE COND-11** — A new dbt model references a raw table with a hardcoded schema string
(`FROM raw.table_name`) instead of `{{ source('raw', 'table_name') }}`.
→ dbt cannot track freshness or lineage for hardcoded references.
→ All raw table references must use `source()` to register the dependency in the DAG.

**RULE COND-12** — A staging model's output row count is substantially lower than its
raw source row count without explanation.
→ Staging models should explain material row-count reductions (deduplications, null filters).
→ Silent row loss at staging propagates to silver and gold with no visibility.

### NOTE — Good practice, does not block

**RULE NOTE-01** — No index strategy mentioned for a new table with `period_date` or `geo`.
→ DuckDB benefits from zone map-compatible sorted storage on date columns.
→ Consider `CREATE INDEX ... ON (period_date)` for mart tables used in range queries.

**RULE NOTE-02** — No idempotency comment in a new dbt model.
→ Note in the model header whether full-refresh or incremental is used and why.

**RULE NOTE-03** — No dbt tests defined for a new staging or mart model.
→ Minimum: `unique` on grain key, `not_null` on `detail_id`/`geo`/`period_date`/`value`,
  `accepted_values` on `source_id` and `domain_id`.

**RULE NOTE-04** — A new mart model does not drop inapplicable `dim_*` columns.
→ Gold should carry only domain-relevant columns. Passing all 24 dim columns through to the
  mart makes dashboard SQL noisier and wastes memory during query execution.

**RULE NOTE-05** — No rollback plan for a schema change on a production table.
→ DuckDB single-file format: a failed ALTER on a production table may leave the warehouse in
  an inconsistent state. Always test schema changes on a copy before applying to production.

**RULE NOTE-06** — A staging model uses empty string `''` instead of `null::varchar` for
inapplicable dimension columns.
→ Empty strings break `IS NULL` checks in downstream models and dashboards.
→ Storage standard: always `null::varchar`, never empty string for missing dimensions.

---

## 10. Decision Reference

Quick lookup for common architectural questions.

| Question | Answer | Rule |
|----------|--------|------|
| Can a dashboard query `raw.*`? | Never | BLOCK-01 |
| Can a domain dashboard query `all_indicators`? | No (Explorer exception) | BLOCK-02 |
| Where does business logic live? | dbt mart models (gold) | Layer contracts §1.2 |
| Where do Polish labels live? | Gold mart + dashboard layer | Layer contracts §1.2 |
| Where does data cleaning live? | dbt staging models (silver) | BLOCK-03 |
| Should I use star or snowflake schema? | Star schema always | §3.3 |
| Should I use integer surrogate keys? | No — composite natural keys | §2.4, §8.2 |
| Can I use SELECT * from all_indicators? | No | BLOCK-08 |
| Should staging models use incremental? | No — use table | §4.5 |
| What is the shared library between platform and products? | `complex_dashboard` skill (`.claude/skills/complex_dashboard/assets/`) only | BLOCK-06 |
| Where do derived metrics (YoY) live? | Gold mart if universal; dashboard if local | §1.2 |
| How do I add a new data source? | raw → stg_* → all_indicators union | §4.1, BLOCK-04 |
| What if a source doesn't have a dimension? | `null::varchar as dim_{name}` | NOTE-06 |
```

---

**Research complete. Here is the synthesis.**

The knowledge base covers all eight requested sections plus an applied rules section and a decision reference table. Key synthesis points:

1. **Medallion contracts are grounded** in Databricks documentation plus Kimball's original staging area concept — the theory shows these are not arbitrary conventions but consequences of the coupling/auditability problem.

2. **Dimensional modelling section** covers grain declaration (the most important concept), conformed dimensions mapped to the actual project seeds (`dim_source`, `dim_domain_detail`, `dim_geo`, `dim_calendar`), SCD types with the project-specific default, and surrogate vs natural key rationale explicitly tuned for DuckDB's vectorised execution model.

3. **Star schema recommendation** is grounded in the 40-60% query performance advantage through fewer joins, with DuckDB's zone map implementation as the secondary reason.

4. **The 25 applied rules** (8 BLOCK, 12 CONDITIONAL, 6 NOTE) are directly derived from the theoretical principles and are in the same format as the architecture-critic's existing evaluation output. They extend the critic's current ruleset with theoretical backing and additional cases (BLOCK-07 on union contract, BLOCK-08 on SELECT *, COND-07 on inner join dimension trap, COND-11 on source() vs hardcoded references, NOTE-06 on empty string vs null).

5. **Data Vault section** is included as a negative justification — establishing why the current Kimball + medallion approach is correct, not a gap to fill.

6. **DuckDB section** captures the engine-specific decisions that deviate from generic SQL advice: no integer surrogates, DOUBLE vs NUMERIC for indicators, the DROP TABLE full-overwrite workaround, and zone map behaviour.

Sources:
- [Kimball Dimensional Modeling Techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [Enterprise Data Warehouse Bus Architecture - Kimball Group](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/kimball-data-warehouse-bus-architecture/)
- [What is the medallion lakehouse architecture? | Databricks](https://www.databricks.com/glossary/medallion-architecture)
- [Staging: Preparing our atomic building blocks | dbt Developer Hub](https://docs.getdbt.com/best-practices/how-we-structure/2-staging)
- [Marts: Business-defined entities | dbt Developer Hub](https://docs.getdbt.com/best-practices/how-we-structure/4-marts)
- [A complete guide to surrogate keys and why they matter | dbt Labs](https://www.getdbt.com/blog/guide-to-surrogate-key)
- [Configure incremental models | dbt Developer Hub](https://docs.getdbt.com/docs/build/incremental-models)
- [Why DuckDB – DuckDB](https://duckdb.org/why_duckdb)
- [Star Schema vs Snowflake Schema | DataCamp](https://www.datacamp.com/blog/star-schema-vs-snowflake-schema)
- [Data vault modeling - Wikipedia](https://en.wikipedia.org/wiki/Data_vault_modeling)
- [Building a Kimball dimensional model with dbt | dbt Developer Blog](https://docs.getdbt.com/blog/kimball-dimensional-model)
- [Modeling - dbt_project_evaluator](https://dbt-labs.github.io/dbt-project-evaluator/latest/rules/modeling/)