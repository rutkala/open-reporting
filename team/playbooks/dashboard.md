# Playbook: Domain Dashboard

## Recipe (sub-product #15)

*For the full routing rationale see `team/PLATFORM.md §3.7`.*

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Domain brief | Business Analysis | `business-analyst` | `brief-reviewer` | brief-review.md |
| Domain review | Domain Specialist | — *(evaluator only)* | `domain-specialist` | — |
| Design (layout, tabs, filters) | UX / UI Design + Dashboard Dev | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md → visualization-image.md |
| Build (Dash app, queries) | Dashboard Development | `dashboard-dev` | `visualization-reviewer` | visualisation.md → visualization-diff.md |
| Analytical review | Analytical Methods | — *(evaluator only)* | `analytical-validator` | analytical-review.md |

*Note: if new data is needed, first complete sub-products #1–#3 (ingest → silver → gold) via the data-ingestion and data-mart playbooks.*

---

## Overview

This playbook defines the complete process for building a **domain dashboard** — one dashboard per business domain (Public Finance, Labour, Health, etc.), covering the full pipeline from raw data sources to a published dashboard.

Each domain is an **epic** in Linear with sub-issues per phase. This is the reusable template — the pattern established for the first domain (Public Finance, OR-102) is followed for every subsequent domain.

```
/kickoff → Phase 1 (Research) → Phase 2 (Ingest) → Phase 3 (Silver) → Phase 4 (Gold) → Phase 5 (Dashboard) → Phase 6 (Publish)
```

---

## Principles

These are guiding principles, not rigid rules. Evaluate whether they fit the domain and situation — if a principle does not apply or a better approach emerges from research, adapt and document why.

- **Multi-source by default**: aim to identify all available parallel sources in the research phase. Some domains will have many; others may have only one authoritative source. The goal is to not miss obvious sources — not to artificially create parallel ingestion where it adds no value.
- **Keep parallel sources**: where multiple sources exist for the same domain, keep them in the warehouse simultaneously. This supports comparison and quality assessment. When one source is clearly superior or redundant, document it and consider pruning.
- **Full pipeline per domain**: the complete pipeline (research → bronze → silver → gold → dashboard) produces the best outcome. Jumping layers can be justified in specific circumstances (e.g., a domain already well-covered in bronze) — document the rationale.
- **Domain Explorer in every dashboard**: including a domain-scoped Explorer tab gives power users flexibility. Evaluate whether this fits the domain's audience — a specialist dashboard for a narrow audience may not benefit from it.
- **Gold queries from domain dashboards**: domain dashboards querying the gold mart (not silver) is the default. Evaluate whether a gold mart is needed or whether silver is sufficient for the domain's needs.
- **Update this playbook**: if a phase works differently than expected, update this playbook before moving to the next domain.

---

## Linear Structure

Each domain is one **epic** with 5 sub-issues:

| Sub-issue | Label | Description |
|-----------|-------|-------------|
| `OR-XXX-a` Research | Data | Identify all parallel data sources |
| `OR-XXX-b` Ingest | Data | Ingest each source to bronze |
| `OR-XXX-c` Silver | Data | Stage each source into `curated.all_indicators` via dbt |
| `OR-XXX-d` Gold | Data | Build `curated.mart_{domain}` star schema |
| `OR-XXX-e` Dashboard | Feature | Build `products/dashboards/{domain}/app.py` |

Each sub-issue goes through its own `/kickoff` when it is pulled into a sprint.

---

## Phase 0: Kickoff

**Skill:** `/kickoff <OR-XXX>` (for the sub-issue being started)

1. Read the Linear sub-issue
2. Confirm which phase this is and what the deliverable is
3. Check blockers: confirm previous phase is done (data available)
4. **No user approval needed** — proceed directly from kickoff

---

## Phase 1: Data Source Research

**Deliverable:** Research document listing all available sources for this domain.

**Steps:**
1. Use web search to find ALL public data sources covering this domain:
   - Start with Polish national statistics: GUS/DBW HVD, BDL, GUS BDL API
   - EU-level: Eurostat (identify the specific dataset code)
   - Sector-specific: Ministry of Finance (MF), NBP, sectoral regulators
   - Any other Level 1-3 official source (see `docs/DATA_SOURCES.md`)
2. For each source document:
   - URL and access method (API, file download, SPARQL)
   - Geographic granularity (national / NUTS2 / NUTS3 / gmina)
   - Time granularity (annual / quarterly / monthly)
   - Key variables available
   - Overlap with other sources (where they measure the same thing)
   - Unique value this source adds
3. **Do not select a single winner** — all identified sources proceed to ingestion
4. Document findings in a comment on the research sub-issue in Linear

**Rule:** Never limit research to what is already ingested. The question is "what exists in the world for this domain?" not "what do we already have?"

---

## Phase 2: Ingestion → Bronze

**Deliverable:** `raw.{source}_{domain}` table(s) for each newly identified source.

**Standard:** `team/standards/build/ingestion.md`

**Steps (for each new source):**
1. Create `platform/ingestion/to_landing/fetch_{source}_{domain}.py` — download raw files to `data/landing/{source}_{domain}/`
2. Create `platform/ingestion/to_raw/load_{source}_{domain}.py` (dlt pipeline) — parse and load to `raw.{source}_{domain}`
3. Create DDL at `platform/warehouse/raw/{source}_{domain}.sql`
4. Follow ingestion standard: upsert pattern, `fetched_at` column, BIGINT for external IDs
5. Validate: row counts, date range, key variable coverage — post results as Linear comment

**Rule:** Keep all ingested sources in `raw.*` simultaneously. Parallel sources for the same domain are intentional. Never overwrite one source with another.

Note: If a source was already ingested in a prior issue (e.g., DBW HVD for Public Finance), skip it here — it is already in bronze. Focus only on new sources identified in Phase 1.

---

## Phase 3: Silver Staging

**Deliverable:** dbt staging model(s) for each new source, unioned into `curated.all_indicators`.

**Standard:** `team/standards/build/storage.md` — 33-column schema

**Steps (for each new source):**
1. Create `platform/processing/dbt/models/{source}/stg_{source}_{domain}.sql`
2. Map source variables to `detail_id` values in `curated.dim_domain_detail`
3. Map source dimensions to named semantic columns (`dim_govt_sector`, `dim_resources_uses`, etc.)
4. Use `null::varchar as dim_{name}` for all unpopulated dimension columns
5. Add new indicator rows to `dim_domain_detail.csv` seed if source introduces new indicators
6. Union `select * from {{ ref('stg_{source}_{domain}') }}` into `all_indicators.sql`
7. Run: `dbt seed --full-refresh && dbt run`
8. Validate: row counts per `source_id`, NULL rates per dim column, date range

**Rule:** All parallel sources must coexist in `curated.all_indicators`. Use `source_id` to distinguish them. Do not deduplicate across sources at this layer.

---

## Phase 4: Gold Mart

**Deliverable:** `curated.mart_{domain}` — a domain-specific star schema built from silver.

**Standard:** Kimball star schema (one fact table per domain business process)

**Steps:**
1. Create `platform/processing/dbt/models/mart/mart_{domain}.sql`
2. Filter `curated.all_indicators` to domain-relevant `domain_id` and `detail_id` values
3. Pre-join Polish labels from `curated.dim_domain_detail` — no runtime joins in dashboard
4. Include only dimension columns relevant to this domain; drop unpopulated dims
5. Add domain hierarchy column (e.g., `budget_category` for Public Finance)
6. Pre-compute derived metrics (YoY change, ratios, gaps)
7. Keep `source_id` — dashboard must be able to filter and compare by source
8. Add DDL to `platform/warehouse/curated/mart_{domain}.sql`
9. Run `dbt run --select mart_{domain}`
10. Validate:
    - Row counts per `source_id` match silver layer
    - Polish labels populated for all indicators
    - Domain hierarchy correctly classifies all indicators
    - Derived metrics are numerically correct

---

## Phase 5: Dashboard

**Deliverable:** `products/dashboards/{domain}/app.py` — Dash application.

**Standard:** `team/standards/build/visualisation.md`

### Phase 5a — Domain Research (mandatory before any design)

Run `/domain-brief {domain}` to produce a domain brief. This brief defines:
- What KPIs practitioners use in this domain
- What analytical angles are standard
- What visualization conventions are used in authoritative publications
- How the domain data maps to what is available in `curated.mart_{domain}`

**The dashboard design is derived from the domain brief — not from IT patterns or PO specifications.**

Never ask the PO what tabs, KPIs, or charts the dashboard should contain. Research it, design it based on the brief, build it, then present the result.

### Phase 5b — Dashboard Design (based on brief)

Translate the domain brief into a Dash application structure. The standard pattern below is a reasonable starting point — evaluate whether it fits the domain and adjust based on what the domain brief reveals about how practitioners structure their analysis.

**Standard pattern (evaluate for each domain):**

| Tab | Purpose | When to include |
|-----|---------|----------------|
| Explorer | Domain-scoped indicator browser, dimension filtering, source toggle | Generally useful — may be less relevant for narrow specialist audiences |
| Overview | Headline KPIs + trend for the domain's primary question | Almost always — every domain has a headline metric |
| [Domain-specific] | One tab per major analytical angle from the domain brief | Include when the domain has distinct sub-questions (e.g. Revenue vs Expenditure vs Debt for Public Finance) |
| Source Comparison | Same metric across all `source_id` values | Include when multiple sources are available; skip or defer if only one source exists at this stage |

The brief may suggest a completely different structure — a single scrollable page, a map-first layout, or a time-series-only view. Follow the evidence from the research, not the template.

### Phase 5c — Implementation

1. Create `products/dashboards/{domain}/app.py`
2. Query `curated.mart_{domain}` only — never raw or silver
3. Use `products/visuals/lib/theme.py` Nordic template
4. All user-facing text in Polish (labels, KPI titles, axis labels, tooltips)
5. Add `or-{domain}.service` systemd unit (next available port starting from 8053)
6. Register in `docker-compose.yml` and nginx reverse proxy
7. Restart service, verify at `portal.open-reporting.dev/{domain}`

### Phase 5d — Present to PO

After building, present:
- What the dashboard shows and why (grounded in the domain brief)
- Which KPIs and analytical angles were included, with brief justification
- Any gaps (standard KPIs not yet in data — note for future ingestion)

The PO challenges the design, provides feedback, and approves or requests changes. The PO does not specify what to build — they react to what was built.

---

## Phase 6: Publish

**Steps:**
1. `/commit` — commit all changes across all phases (can be one PR per sub-issue or one PR for the full epic)
2. Update Linear: each sub-issue → Done; epic → Done when all sub-issues complete
3. `/document`:
   - Update `docs/DATA_SOURCES.md` with any new sources documented in research
   - Update `docs/DATA_MODEL.md` if new dim columns were added to silver
   - Update `docs/RELEASE_NOTES.md` under Unreleased
   - Add lessons-learned entries for anything that deviated from this playbook
4. Update `.claude/session-memory.md`
5. Verify dashboard is live: `curl -I https://portal.open-reporting.dev/{domain}`

---

## Quick Reference

| Phase | Input | Output | Standard |
|-------|-------|--------|----------|
| 1: Research | Domain name | Source inventory (Linear comment) | DATA_SOURCES.md |
| 2: Ingest | Source inventory | `raw.{source}_{domain}` tables | ingestion.md |
| 3: Silver | Bronze tables | Rows in `curated.all_indicators` | storage.md |
| 4: Gold | Silver rows | `curated.mart_{domain}` | Kimball star schema |
| 5: Dashboard | Gold mart | Running Dash app | visualisation.md |
| 6: Publish | All outputs | Live dashboard, docs updated | — |

---

## Guidance

These are default positions — evaluate each one for the specific domain and context:

- **Prefer gold over silver in domain dashboards** — querying `curated.mart_{domain}` is cleaner and more performant than querying silver directly. If a gold mart does not yet exist and the domain is simple, silver may be acceptable as an interim step.
- **Identify parallel sources in research** — aim to find all meaningful sources, not just the first one. Some domains will have many; for some, one authoritative source is enough.
- **Consider a gold mart when the domain has specific needs** — pre-computed labels, domain hierarchy, derived metrics. If the domain is thin or early-stage, silver may suffice.
- **Update this playbook** when something works differently than described here — before moving to the next domain.
