# Playbook: Data Mart and Semantic Layer

Covers sub-products #3 (Data mart — gold) and #4 (Semantic layer).

## Recipe

### Sub-product #3 — Data mart (gold)

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Design (star schema, derived metrics, bus matrix) | Data Architecture | `data-architect` *(gap — main Claude)* | `architecture-critic` | storage.md, processing.md → architecture-review.md |
| Build (dbt mart SQL, incremental models) | Data Engineering | `data-engineer` | `data-engineer-reviewer` | processing.md → data-engineering-review.md |

### Sub-product #4 — Semantic layer

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Domain brief (indicator selection, aggregation rules) | Business Analysis | `business-analyst` | `brief-reviewer` | — → brief-review.md |
| Design (MetricFlow entities, measures, dimensions, metrics) | Data Architecture + Semantic Modelling | `data-architect` *(gap — main Claude)* | `architecture-critic` | measures.md → architecture-review.md |
| Build (MetricFlow YAML, agg, format_type, Polish labels) | Semantic Modelling | `data-engineer` | `measures-reviewer` | measures.md → measures-review.md |

---

## Part 1 — Data Mart (Gold)

### What a domain mart is

A gold mart (`curated.mart_{domain}`) is a pre-joined, domain-scoped star schema built on top of `curated.all_indicators` (silver). It contains:
- Only indicators relevant to the domain
- Pre-joined dimension labels (Polish names, codes, descriptions)
- Pre-computed derived metrics (growth rates, per-capita figures, year-over-year changes)
- A grain of one row per observable (period × geography × indicator × relevant dimensions)

Domain dashboards query gold marts. They do not query silver directly.

### Phase 1 — Design

Read before designing:
- `team/standards/build/storage.md` — schema naming, types
- `team/standards/build/processing.md` — dbt mart model pattern
- `platform/warehouse/bus_matrix.md` — existing fact × dimension map

Design decisions:
1. **Domain scope** — which domain_ids from `dim_domain_detail` belong in this mart?
2. **Fact columns** — which silver columns are retained (period_date, geo, value, obs_status, relevant dim_* columns)?
3. **Dimension joins** — which `dim_*` tables to join for Polish labels?
4. **Derived metrics** — which computations to pre-calculate (YoY %, growth index, real vs nominal)?
5. **Bus matrix update** — does this mart introduce new fact × dimension combinations? Update `platform/warehouse/bus_matrix.md`.

### Phase 2 — Build

1. Create `platform/processing/dbt/models/mart/mart_{domain}.sql`
   - Filter `all_indicators` to domain scope
   - Join `dim_domain_detail`, `dim_geo`, `dim_calendar`, `dim_source` for labels
   - Compute derived metrics as SQL expressions
   - Declare `unique_key` for incremental materialisation
2. Add `not_null` + `unique` tests on the grain key in `schema.yml`
3. Run: `dbt run --select mart_{domain} && dbt test --select mart_{domain}`
4. Validate: compare row counts vs silver source, check derived metric values, verify Polish labels

### Mart checklist

- [ ] Bus matrix reviewed; updated if new combinations introduced
- [ ] All domain_ids mapped and filtered correctly
- [ ] Polish labels joined from seed dimensions
- [ ] Derived metrics have correct aggregation (not summing rates; not averaging stocks across time)
- [ ] unique_key declared for idempotency
- [ ] schema.yml tests added
- [ ] dbt run + test pass

---

## Part 2 — Semantic Layer

The semantic layer exposes curated data to dashboards and analysts through a formal measure catalogue. It declares what each measure means, how it aggregates, and how it renders — so dashboards cannot misuse the data by mistake.

### Phase 1 — Domain brief

Run `/domain-brief` before designing any semantic model. The brief determines:
- Which indicators to expose as measures
- Whether each is a stock or flow (determines aggregation)
- Whether it is a rate, ratio, or absolute value (determines what operations are valid)
- What the Polish user-facing label should be

The brief must pass `brief-reviewer` before proceeding to design.

### Phase 2 — Design

Read `team/standards/build/measures.md` in full.

Design decisions:
1. **Semantic model scope** — which mart does this model sit on?
2. **Entities** — what is the primary entity (e.g. `labour_indicator` keyed on period_date + geo + detail_id)?
3. **Dimensions** — which columns become queryable dimensions (geo, period, indicator type)?
4. **Measures** — for each indicator exposed:
   - `agg` — SUM for flows, LAST or AVERAGE_OVER_TIME for stocks (never SUM for stocks)
   - `expr` — SQL expression referencing the mart column
   - `format_type` — currency / percent / pp / count / ratio / rate
   - `scale` — for currency: raw / tys / mln / mld
   - `label` — Polish, correct diacritics, no English mixing
5. **Metrics** — higher-order calculations (YoY growth, share of total) built on measures

### Phase 3 — Build

1. Create `platform/processing/dbt/models/{domain}/semantic_models/{domain}.yml` (MetricFlow)
2. Create `platform/processing/dbt/models/{domain}/metrics/{domain}.yml`
3. Run: `dbt compile` to check YAML syntax
4. Validate: check each measure's agg against the stock/flow classification in the brief

### Semantic layer checklist

- [ ] Domain brief completed and passed brief-reviewer
- [ ] Every measure declares agg, expr, format_type, label
- [ ] No AVG on wages/incomes/rents without explicit justification
- [ ] No SUM on stock measures
- [ ] No SUM on rate/ratio/percentage measures across dimensions
- [ ] Currency measures declare scale (raw / tys / mln / mld)
- [ ] Polish labels have correct diacritics
- [ ] Percentage-point deltas use format_type: pp, not percent
- [ ] dbt compile passes without errors
- [ ] measures-reviewer PASS on PR
