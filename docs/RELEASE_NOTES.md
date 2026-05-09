# Release Notes

---

## Unreleased

### Analytics knowledge base
- **OR-119** — Analytical thinking framework: `team/analytics/analytical-thinking.md` — structured KB covering the five analytical moves (describe/compare/change/relate/rank) with failure modes, four-layer insight hierarchy (headline → evidence → context → caveats), six when-is-it-interesting tests (statistical significance, practical significance, deviation from expectation, named threshold crossing, rate vs level, human scale), Polish public data context (V4/EU27 peer groups, six historical anchors from 2004 accession to present, domain-specific analyst questions for labour and fiscal), and aggregation/ratio rules (pp vs %, base effect, index comparability, per capita fallacy, Simpson's paradox, CAGR limits, definitional break handling). Includes worked example (Q4 2024 LFS unemployment).

### Evaluation framework
- **OR-132** — Screenshot-based visual reviewer: `tools/screenshot.py` starts an affected dashboard on a temp port (19999), waits for React render, takes a Playwright full-page screenshot at 1440×900, then stops it. `visual-screenshot-reviewer` agent reads the PNG via Claude's multimodal Read tool and evaluates against `team/standards/visual-screenshot-review.md` (HIGH: broken render, semantic colour mismatch, contrast failure, truncated text; MEDIUM: F-pattern, competing elements, wrong chart type, palette inconsistency). `/review` Part 0.5 triggers this automatically when dashboard files change. All three dashboards updated to read port from `OR_PORT` env var.
- **OR-131** — Analytical Validator agent: `analytical-validator` subagent evaluates statistical and methodological correctness. Dual-mode: plan-phase checks analytical design intent ($PLAN text); diff-phase checks SQL/Python/chart code. BLOCK concerns: AVG() on wage/income columns, CAGR across structural breaks (2008–09, 2020, 2004), non-comparable population comparisons, causal language in chart strings, % label on pp difference. `/plan` Step 3.5 now runs architecture-critic and analytical-validator in parallel. `/review` Part 0 now runs three agents in parallel — MISLEADING maps to CRITICAL.
- **OR-130** — Architecture Critic agent: `architecture-critic` subagent evaluates implementation plans before any code is written. Reads `team/standards/` and checks for BLOCK (layer violations, raw-from-dashboard, transform-in-ingestion, missing dbt staging model, silver queried by domain dashboard, circular dependencies), CONDITIONAL (missing fetched_at, schema naming, catalogue verification, upsert strategy, tight coupling), and NOTE concerns. `/plan` skill updated with Step 3.5: critic runs after plan is drafted, before presenting to user — BLOCK findings are fixed before the user ever sees the plan.
- **OR-128** — Visualization Reviewer agent: `team/standards/visualization-review.md` (HIGH/MEDIUM/LOW
  rules: colour semantics, KPI reference completeness, series count, y_measure on domain calls,
  subtitle, pie slice limit, waterfall variant mismatch). `visualization-reviewer` subagent scoped
  to domain dashboards. `/review` Part 0 now runs both agents in parallel.
- **OR-127** — Code Reviewer agent: `team/standards/code-review.md` (P1/P2/P3 rules covering
  security, SQL injection, layer violations, logging, DB patterns, Python conventions, semantic
  layer). `code-reviewer` subagent runs independently on every PR diff. `/review` skill updated
  with mandatory Part 0 agent pass before internal checks.

### Visual components
- **OR-126** — Template dashboard: all chart calls now pass `y_measure` (axis title + tick unit
  driven by Measure metadata) and use `measure.to_series()` for series dicts. Polish colour
  palette labels translated to English. Stale `bar_diverging` import removed.
- **OR-125** — `kpi_row()` flex container: wraps multiple KPI cards in an equal-height responsive
  row with configurable `min_width` and `gap`. Template updated with 4-card `kpi_standard` row
  and 5-card `kpi_compact` row demonstrating the pattern.
- **OR-124** — Measure-driven value formatting: `Measure` dataclass redesigned with structured
  format metadata (`format_type`, `scale`, `decimals`, `currency_symbol`, `show_unit`).
  All chart components accept optional `y_measure` param that auto-configures axis title,
  tick format and tick suffix. `kpi_standard` gains `subtitle`, `reference_value`,
  `reference_label`. Polish strings removed from component library code.
- **Template dashboard** — All sample data and measure labels translated to English;
  waterfall split into contribution and variance variants (39 families total).
  Treemap fixed (branchvalues="total" consistency).

---

## v0.1.0 — MVP (2026-03-28)

### Products launched
- **Blog** — `open-reporting.dev` (Ghost 5, "Otwarte Raporty")
- **Data Portal** — `portal.open-reporting.dev` with Labour dashboard and Data Explorer
- **Mobile PWA** — `portal.open-reporting.dev/app/` — installable Android app
- **Instagram** — `@otwarteraporty` with data card publishing

### Data platform
- DuckDB analytical warehouse with 222 indicators across 18 domains
- Eurostat ingestion (73 verified series) including NUTS2 regional data
- NBP FX rates ingestion (EUR/PLN, USD/PLN, GBP/PLN, CHF/PLN)
- dbt project: 22 curated models, 6 seeds
- Geographic dimension expanded to include NUTS1 (7) + NUTS2 (17) Polish regions

### Explorer enhancements
- Dimension hierarchy drill-down (Period: Year/Quarter/Month; Domain: Group/Domain/Detail)
- Default aggregation per indicator (`default_agg` in `dim_domain_detail`)
- Power BI-style ◄/► drill buttons

### Brand
- Renamed from "Open Reporting" to "Otwarte Raporty" across all products

### Infrastructure
- Single Hetzner VPS, Docker Compose (nginx, PostgreSQL 16, Ghost 5)
- SSL/TLS via Let's Encrypt
- Systemd services for all three portal apps

---

## Unreleased

### Unified Explorer dashboard on curated layer (2026-03-29) — OR-99
- Removed DBW HVD tab (was querying `raw.dbw_observations` directly — architecture violation)
- All three sources (Eurostat, NBP, GUS DBW) now accessible through one unified Explorer view
- Source is a filter attribute in the sidebar, not a navigation tab — `dcc.Tabs` removed
- Dynamic dimension filter panel: selecting indicators reveals only dims with data for those indicators
- 24 named semantic columns (dim_sex, dim_age_group, dim_nace_sector, etc.) exposed as Polish-labelled filters
- `load_available_dims()` uses DuckDB `UNPIVOT` to discover populated dims in one query
- `WARNING` colour imported from Nordic theme (was hardcoded)

### Kimball dimensional model — named semantic columns (2026-03-29) — OR-100
- Replaced EAV generic `dim1_name/dim1_value` slots with 24 named semantic columns (`dim_sex`, `dim_age_group`, `dim_nace_sector`, etc.)
- `curated.all_indicators` fact table now has 33 columns: 5 core, 24 named dimensions, 4 metadata
- `stg_dbw.sql` rewritten: dim_id-based CASE routing ensures consistent dimension filtering across all indicators regardless of source slot position
- `stg_eurostat.sql` and `stg_nbp.sql` updated with 24 named null columns (column-order aligned)
- Added `docs/DATA_MODEL.md` — decision record: Kimball vs Inmon vs Data Vault evaluation, full schema, DBW mapping logic, new-source checklist
- Updated `standards/storage.md` with Kimball standard and 33-column schema reference

### DW architecture — unified conformed fact table (2026-03-29) — OR-97
- `curated.all_indicators` extended to wide fact table with 8 sparse dimension columns (dim1–dim4 name+value)
- GUS DBW HVD integrated as third source via new `stg_dbw.sql` dbt model: 69 indicators, 568k rows, annual data 1995–2025
- Dimension labels resolved from `raw.dbw_positions`; geographic dimensions mapped to NUTS codes
- 81 new indicator rows added to `dim_domain_detail` seed; `dbw` added to `dim_source` seed
- `storage.md` and `processing.md` standards updated with layer contracts and dbt-first rule
- `ARCHITECTURE.md` updated to reflect three-source fact table

### DBW HVD explorer tab (2026-03-29) — OR-95
- Added **DBW HVD** tab to the Explorer dashboard (`/explorer/`) — no new service or port
- Variable selector grouped by 18 HVD categories, dimension filter (sex/sector/region), time series chart, 4 KPI cards (latest value, YoY %, max, min)
- All UI labels in Polish; GUS DBW source attribution in footer
- New `raw.dbw_variables` lookup table (85 rows) — variable name + HVD category
- Ingestion script extended: populates `raw.dbw_variables` via dict CSVs + GUS catalogue API

### GUS DBW HVD ingestion pipeline (2026-03-29) — OR-93
- New ingestion pipeline: `to_landing/dbw_hvd.py` + `to_raw/dbw_observations.py`
- Loaded 756,626 observations across 85 variables, 82 cross-sections, years 1995–2026
- Raw tables: `raw.dbw_observations`, `raw.dbw_positions`

### Semantic-layer measures (MetricFlow) pilot (2026-05-09) — OR-144
- **Implementation of MetricFlow semantic-layer pilot** for the Finance dashboard.
- Introduced `semantic_query` helper in `.claude/skills/complex_dashboard/assets/runtime/` to wrap `mf query` CLI.
- Enables domain dashboards to query metrics by name (e.g., `fiscal_balance`) without knowing underlying source tables or SQL logic.
- Added semantic models and wide intermediate models in `platform/processing/dbt/models/finance/` to support MetricFlow.
- Refactored Finance Overview KPI cards to use semantic layer, removing raw SQL/pandas logic from the dashboard code.
- Improved maintainability: metric metadata (labels, formats, thresholds) now lives in dbt semantic models, not in dashboard code.

### Documentation & project hygiene (2026-03-28)
111: - Expanded `docs/DOMAINS.md` to full 18-domain catalogue with Eurostat themes, GUS equivalents, and subcategories
112: - Archived all three Linear documents (Domain Taxonomy, Tech Stack & Environment, Data Catalog) — GitHub is now single source of truth for all documentation
113: - Updated Linear project description (mobile live, Instagram-only social, Polish-first language)
114: - Rewrote `docs/ARCHITECTURE.md` to reflect current stack (DuckDB/PostgreSQL roles, systemd services, URL structure)
115: - Rewrote `README.md` with correct product list, live URLs, doc index
116: - Added `docs/MVP.md`, `docs/ROADMAP.md`, `docs/CONTRIBUTING.md`, `docs/RELEASE_NOTES.md`
117: - Added `.claude/playbooks/social.md` for Instagram publishing flow
118: - Added `.claude/lessons-learned.md` for continuous process improvement
