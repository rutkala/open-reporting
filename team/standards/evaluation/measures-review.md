# Measures Review Rules

**Derived from:** `team/knowledge-base/business-analysis/kpi-indicator-design.md` ✓, `team/knowledge-base/analytical-methods/analytical-thinking.md` ✓, `team/standards/build/measures.md`
**Used by:** `.claude/agents/measures-reviewer.md`
**Does NOT cover:** SQL aggregation correctness in queries outside the semantic layer (see `evaluation/analytical-review.md`), general code quality (see `evaluation/code-review.md`), layer violations (see `evaluation/architecture-review.md`)

Rules applied by the `measures-reviewer` agent on PR diffs touching the semantic layer:
- `products/semantic/` (legacy)
- `products/warehouse/**/semantic_models/*.yml` (MetricFlow)
- `products/warehouse/**/metrics/*.yml` (MetricFlow)

These rules are ADDITIVE to `code-review.md`. Both agents run in parallel. Do not duplicate findings.

---

## P1 — Blocks Merge

### Aggregation correctness

- **`AVG` / `mean` declared for a wage, income, salary, rent, or wealth measure** — the business-analysis KB and analytical-methods KB mandate median (or a percentile-based summary) for strongly right-skewed distributions. A measure named `avg_wage`, `mean_salary`, `avg_income`, `srednie_wynagrodzenie`, `srednia_pensja`, or any semantic measure whose label contains "średni/średnia/średnie" combined with wage/salary/income is a P1 violation unless accompanied by an explicit justification comment citing the data shape.
- **`SUM` over a ratio, rate, or percentage measure** — rates (unemployment rate, inflation rate, interest rate), ratios (debt-to-GDP), and percentages cannot be summed across a dimension and stay meaningful. A `agg: sum` declaration on a measure whose `format_type` is percent/rate is a P1.
- **`SUM` over a stock measure across time** — stock measures (population, headcount, debt outstanding, reserves) are point-in-time values. Summing them across months/quarters/years produces a meaningless number. Flag `agg: sum` on any measure the KB classifies as a stock (population, employment level, debt, reserves, balance sheet entries).
- **`AVG` over a flow measure where `SUM` is appropriate** — flow measures (monthly revenue, quarterly GDP, annual births) should sum across time; averaging them loses the totality and is almost always wrong unless the intent is explicitly "per-period average" and is labelled as such.

### Definition integrity

- **Measure missing `agg` declaration** — every semantic-layer measure must declare an aggregation type explicitly. Implicit aggregation is a silent correctness risk.
- **Measure missing `expr` or equivalent SQL body** — a measure name declared with no formula is a dead reference.
- **Duplicate measure name within the same semantic model** — two measures with the same name across entities cause undefined resolution. Flag any new measure whose name collides with an existing one in the same `semantic_models/*.yml`.
- **Measure references a column that does not exist in the entity's source model** — if the `expr` references `{column}` and that column is not in the parent dbt model's `schema.yml` columns list, flag as P1 (will fail at runtime).

---

## P2 — Should Fix

### Formatting and units

- **Measure missing `format_type`** — every published measure should declare how it renders (currency, percent, count, ratio). Without `format_type` the downstream dashboard must guess.
- **Currency measure missing `scale` or unit abbreviation** — a `zł` measure at raw scale vs `mln zł` vs `mld zł` renders completely differently. Scale must be declared.
- **Percentage measure declared with unit `%` but expressing a percentage-point delta** — e.g. a measure called `unemployment_rate_change` with `format_type: percent` instead of `format_type: pp`. The analytical-methods KB treats these as different units.

### Polish labelling

- **User-facing `label` missing Polish diacritics** — if the label is Polish and contains `a/c/e/l/n/o/s/z` where `ą/ć/ę/ł/ń/ó/ś/ź/ż` is required (e.g. `Srednia pensja` instead of `Średnia pensja`), flag as P2.
- **User-facing `label` mixing English and Polish** — a Polish dashboard should have Polish labels; stray English tokens leak across the content/code language boundary.
- **Measure `description` missing** — published measures that will appear in dashboards should carry a one-sentence description explaining what the measure represents. Missing `description` on new measures is a P2.

### Consistency

- **New measure duplicates a measure that already exists elsewhere in the semantic layer** — even under a different name. Flag suspected duplicates (e.g. `headcount` in one file, `employment_level` in another, both pointing to the same underlying column).
- **Inconsistent aggregation across similar measures** — if three existing wage measures use median and the new one uses mean without justification, flag.

---

## P3 — Noted

- **No unit/metadata comment explaining non-obvious business meaning** — e.g. a measure named `ess_index` with no comment explaining what "ESS" stands for.
- **Measure defined but not yet referenced by any metric or dashboard** — dead measures accumulate. Note, do not block.
- **Format scale inconsistency within a domain** — e.g. some finance measures in `mln zł`, others in `mld zł`, within the same dashboard. Note as a consistency concern.
- **Stock/flow type not indicated in measure name or description** — the KB distinguishes stock from flow explicitly; names like `balance` are ambiguous. Note as a clarity improvement.

---

## What this standard does NOT cover

- SQL aggregation correctness inside dbt models or ad-hoc queries — that is `analytical-validator`'s scope.
- Whether a measure is the right KPI for a domain — that is `domain-specialist`'s scope.
- Whether the semantic model is well-structured architecturally (which entity owns which measure) — that is `architecture-critic`'s scope at plan phase.
- Number formatting at render time in chart/KPI component calls — that is `visual-screenshot-reviewer`'s scope.
