# Data Model

Architecture decision record for the Open Reporting analytical warehouse.

---

## Architecture: Medallion + standard dbt layout + MetricFlow semantic layer

The warehouse follows the **medallion pattern** (raw → curated) with Kimball-style conformed dimensions, organised inside the dbt project (`products/warehouse/`) using the standard dbt convention (`staging/intermediate/marts/dim/semantic`). Dashboards never query the warehouse directly — they go through **MetricFlow** (the semantic layer), which the dbr framework wraps.

```
raw.*                                Source-aligned, untouched, reproducible
    ↓  models/staging/<source>/stg_*.sql
curated.stg_*                        Conformed staging — one model per source
    ↓  models/intermediate/{int_*,  by_domain/<X>_indicators.sql}
curated.int_*                        Cross-source consolidations (e.g. int_finance_consolidated)
curated.{agr,bus,…}_indicators       Per-domain wide views over curated.all_indicators
    ↓  models/marts/<domain>/fact_*.sql
curated.fact_*                       Star-schema facts ready for the semantic layer
curated.dim_*                        Shared dimensions (dim_geo, dim_calendar, dim_cofog)
    ↓  models/semantic/*.yml         MetricFlow semantic_models + metrics (no SQL)
MetricFlow (in-process engine)       Metric name → SQL, run by dbr.semantic at dashboard render
    ↓
dbr visual factory (Plotly figure)
```

### The two-table type — wide vs star

The warehouse has **two distinct fact-table shapes**:

- **Wide cross-source integration:** `curated.all_indicators` (the legacy "silver" integration layer — one row per source × detail × geo × period, with 24 sparse `dim_*` columns). Still produced by `models/staging/eurostat/all_indicators.sql` for use by cross-domain discovery (Explorer-style tools).
- **Domain star-schema facts:** `curated.fact_<domain>_<topic>` (Kimball-style, narrow). Joined by their foreign-key entities to `curated.dim_*` tables. Consumed by MetricFlow semantic models. This is what dashboards see.

The Explorer (cross-domain discovery) reads `curated.all_indicators`; domain dashboards read facts via the semantic layer. Both patterns coexist.

### Conformed dimensions (Kimball-style)

The `curated.dim_*` tables are Kimball-style conformed dimensions — managed once, shared across all facts:

| Table | Rows | Purpose |
|-------|------|---------|
| `curated.dim_geo` | 34 | Eurostat country codes (EU-27 + EFTA + non-European peers), Polish/English names, EU membership, continent |
| `curated.dim_calendar` | ~25,900 | Day-grain calendar 1980–2050 with year/quarter/month/year_quarter/year_month columns. Also serves as MetricFlow time spine. |
| `curated.dim_cofog` | 10 | COFOG-10 functional spending classification (Polish/English labels) |
| `curated.dim_domain_detail` | 305 | Indicator catalogue — all valid `detail_id` values, labels, domains, units |
| `curated.dim_source` | 3 | Source registry (eurostat, nbp, dbw) |
| `curated.dim_primary_source` | small | Primary-source registry |

---

## Central Fact Table: `curated.all_indicators`

One row per: `source_id + detail_id + geo + period_date + [all populated dim columns]`

### Schema (33 columns)

| Column | Type | Description |
|--------|------|-------------|
| `source_id` | VARCHAR | Data source: `eurostat`, `nbp`, `dbw` |
| `domain_id` | VARCHAR | 18 domain codes: MAC, LAB, PUB, POP, PRC, etc. |
| `detail_id` | VARCHAR | Indicator key from `curated.dim_domain_detail` |
| `geo` | VARCHAR | NUTS code (`PL`, `PL1`, `PL11`, etc.) |
| `period_date` | DATE | All granularities truncated to first day of period |
| `dim_sex` | VARCHAR | Sex breakdown — NULL if not applicable |
| `dim_age_group` | VARCHAR | Age group |
| `dim_type_of_locality` | VARCHAR | Urban / rural classification |
| `dim_nace_sector` | VARCHAR | NACE economic sector |
| `dim_employment_status` | VARCHAR | Employment status |
| `dim_education_level` | VARCHAR | ISCED education level |
| `dim_prodcom_product` | VARCHAR | PRODCOM product category |
| `dim_hicp_category` | VARCHAR | HICP price category |
| `dim_pollutant_type` | VARCHAR | Environmental pollutant type |
| `dim_waste_category` | VARCHAR | Waste category |
| `dim_healthcare_function` | VARCHAR | Healthcare function (HC.1–HC.9) |
| `dim_health_provider` | VARCHAR | Health service provider type |
| `dim_health_financing` | VARCHAR | Health financing scheme |
| `dim_govt_sector` | VARCHAR | Government sector (S.13, S.1311, etc.) |
| `dim_institutional_sector` | VARCHAR | Institutional sector (ESA 2010) |
| `dim_asset_classification` | VARCHAR | Fixed asset type |
| `dim_tourist_origin` | VARCHAR | Tourist country/region of origin |
| `dim_trip_direction` | VARCHAR | Inbound / outbound |
| `dim_trip_duration` | VARCHAR | Trip duration category |
| `dim_quintile_group` | VARCHAR | Income quintile group |
| `dim_citizenship` | VARCHAR | Citizenship category |
| `dim_resources_uses` | VARCHAR | National accounts resources/uses side |
| `dim_transport_mode` | VARCHAR | Transport mode |
| `dim_accommodation_type` | VARCHAR | Tourist accommodation type |
| `value` | DOUBLE | Observed numeric value |
| `obs_status` | VARCHAR | Data quality flag from source |
| `fetched_at` | TIMESTAMPTZ | When the raw row was ingested |
| `updated_at` | TIMESTAMPTZ | When the curated row was last transformed |

### Sparsity is expected and correct

Eurostat and NBP rows have all 24 dim columns as NULL — these sources provide pre-aggregated
national series with no breakdown dimensions. DBW rows populate 1–3 dim columns per indicator.
This sparsity is intentional: DuckDB's columnar storage makes NULL columns essentially free.
The named columns exist to accommodate all current and future sources in a consistent schema.

| Source | Rows | Dimensions populated |
|--------|------|---------------------|
| `eurostat` | ~2,500 | None (all NULL) |
| `nbp` | ~24,000 | None (all NULL) |
| `dbw` | ~568,000 | 1–3 per indicator |

---

## Staging Layer

Each source has a `stg_{source}.sql` dbt model that:
1. Reads from `raw.*` (bronze)
2. Conforms column names, types, and grain to the shared 33-column schema
3. Maps source dimension slots to named semantic columns (NULL for absent dims)

`curated.all_indicators` unions all three:
```sql
select * from {{ ref('stg_eurostat') }}
union all
select * from {{ ref('stg_nbp') }}
union all
select * from {{ ref('stg_dbw') }}
```

### DBW dimension mapping

DBW has up to 3 dimension slots per observation (`dim1`, `dim2`, `dim3`), each identified by
a `dim_id` that encodes the semantic type. The staging model routes each slot to the correct
named column via CASE expressions on `dim_id` — slot position does not matter:

```sql
CASE
    WHEN o.dim1_type_id IN (1, 67, 339) THEN o.dim1_pos_name
    WHEN o.dim2_type_id IN (1, 67, 339) THEN o.dim2_pos_name
    WHEN o.dim3_type_id IN (1, 67, 339) THEN o.dim3_pos_name
END AS dim_sex
```

---

## Star-schema fact layer (`marts/<domain>/`)

Domain dashboards query the warehouse exclusively through MetricFlow metrics defined on star-schema facts. Each fact lives in `products/warehouse/models/marts/<domain>/` with shape:

```
marts/finance/
├── fact_finance_overview.sql              ← measures fact (wide, one column per measure)
├── fact_finance_overview.yml              ← schema + tests
├── fact_finance_cofog.sql                 ← long-format fact (one row per geo/period/function)
├── fact_finance_imf.sql                   ← annual wide, with is_projection flag
├── fact_finance_revenue_expenditure.sql   ← annual wide
└── schema.yml
```

A fact in this project is:
- **Domain-scoped** — only the indicators relevant to one domain
- **Star-schema** — narrow tables with foreign-key entities (`geo`, `date_key`, `cofog_function`) that join to `curated.dim_*`
- **MetricFlow-ready** — exposes measures (raw aggregations) that the semantic layer wraps as metrics
- **Built from intermediate consolidations** — uses `{{ ref('int_*') }}`, not raw or all_indicators directly

### Intermediate layer (`intermediate/`)

The intermediate layer holds two patterns:

- **`int_finance_consolidated.sql`** — cross-source consolidation. Brings Eurostat + IMF + DBW finance data into one long-format intermediate. Facts in `marts/finance/` pivot this into wide MetricFlow-ready shapes.
- **`intermediate/by_domain/<X>_indicators.sql`** (18 files) — per-domain filtered views over `all_indicators`. Used by cross-domain discovery (Explorer-style) and as inputs to domain consolidations.

### Semantic layer (`semantic/`)

MetricFlow YAMLs define **measures** (raw aggregations on a fact) and **metrics** (named, formatted business KPIs). Dashboards reference metrics by name only — they never see SQL.

```
models/semantic/
├── finance_overview.yml          ← semantic_model + 3 metrics (fiscal_balance, public_debt, govt_revenue)
├── finance_cofog.yml             ← 1 metric (cofog_expenditure) over the long-format fact
├── finance_imf.yml               ← 5 IMF WEO metrics + is_projection dimension
└── finance_revenue_expenditure.yml  ← 9 revenue/expenditure metrics
```

Polish labels, format (`% PKB`, `mld zł`), scale, and thresholds (SGP −3%, Maastricht 60%) live in `metric.config.meta` blocks and are read by dbr at render time.

---

## Rules

1. **Dashboards consume metrics, not tables** — `semantic_query()` / `semantic_query_data()` in dbr, never raw SQL against `curated.*`.
2. **Cross-domain discovery (Explorer-style) reads `curated.all_indicators`** — intentional bypass of the semantic layer for "show me everything" UX.
3. **Raw tables (`raw.*`) are never queried by anything except staging** — strict layer discipline.
4. **NULL for absent dimensions** in `all_indicators` — do not use empty string or placeholder values.
5. **Adding a new dimension column** — if a new source introduces a dim not in the current 24, add a new `dim_{name} VARCHAR` column to `models/staging/<source>/` and update this document.
6. **Dashboards open warehouse read-only** — via the `dashboard` dbt target (`config_options.access_mode: READ_ONLY`) so multiple dashboard services can hold concurrent MetricFlow engines.

---

## Adding a New Source (checklist)

1. Ingest to `raw.{source}_{entity}` — follow `team/standards/build/ingestion.md`. Raw-table DDL is co-located: `products/ingestion/to_raw/<source>.sql` next to `<source>.py`, loaded via `ensure_table()` at runtime.
2. Create `products/warehouse/models/staging/{source}/stg_{source}.sql` — conform to the 33-column shape if joining `all_indicators`, otherwise design for the source's natural shape and let `int_*` consolidate later.
3. Map source dimension slots to named semantic columns; `null::varchar` for unpopulated dims.
4. If source has a new dimension type not in the current 24: add `dim_{name} VARCHAR` to all staging models that feed `all_indicators`.
5. (If integrating with `all_indicators`) Union `select * from {{ ref('stg_{source}') }}` into `models/staging/eurostat/all_indicators.sql`.
6. Add source row to `dim_source.csv` seed.
7. Add indicator rows to `dim_domain_detail.csv` seed.
8. Run `dbt seed --full-refresh && dbt run`.
9. Validate: row counts per source, NULL rates per dim column.

## Adding a New Domain Dashboard (checklist)

1. Build the dimensions you need in `models/dim/` (or reuse existing).
2. Consolidate source data into `models/intermediate/int_{domain}_consolidated.sql` if multi-source.
3. Build star-schema fact(s) in `models/marts/{domain}/fact_{domain}_{topic}.sql` — wide for headline KPIs, long for breakdowns (see `fact_finance_cofog.sql`).
4. Define semantic model in `models/semantic/{domain}_{topic}.yml` — measures + metrics with Polish labels.
5. Author the dashboard YAML in `products/dashboards/{domain}/` following the `public_finance` pattern.
6. `dbr validate` then `dbr run`.
