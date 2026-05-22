# Brief Review Rules

**Derived from:** `team/knowledge-base/business-analysis/kpi-indicator-design.md` ✓ + `team/knowledge-base/analytical-methods/analytical-thinking.md` ✓ (SMART+FABRIC indicator design, aggregation correctness, stock/flow, leading/lagging, Polish structural breaks, balanced framing, qualified causal claims)
**Used by:** `.claude/agents/brief-reviewer.md`
**Does NOT cover:** chart-call correctness in code (see `evaluation/visualization-image.md`), aggregation in SQL (see `evaluation/analytical-review.md`), semantic-layer measure DDL (see `evaluation/measures-review.md`), domain-specific KPI selection theory beyond what the KB covers (see `domain-specialist` agent)

Rules applied by the `brief-reviewer` agent on analytical briefs produced by the `business-analyst` agent. Briefs are reviewed in plan-phase, before they become the foundation of a dashboard plan. The goal is to catch indicator design errors at the earliest possible stage, before they propagate through the build pipeline.

These rules are ADDITIVE to a domain-specialist review when one runs. Both agents may run in parallel.

---

## P1 — Blocks Acceptance

### Indicator design

- **Indicator named without an explicit definition** — every recommended indicator must state exactly how it is calculated (numerator, denominator, source series). A bare name like "unemployment rate" with no definition is a P1.
- **Indicator declared with no source** — every indicator must name the data series and the publishing organisation (Eurostat code, GUS BDL series, NBP table, etc.). Without a source the indicator is unbuildable.
- **Aggregation rule missing or wrong for indicator type** — every indicator must declare how it aggregates across time, region, and group. A wage/salary/income/rent measure must declare median or percentile (mean is wrong for skewed distributions). A rate, ratio, or percentage must declare that it cannot be summed across dimensions. A stock measure must declare that it cannot be summed across time. A flow measure must declare that it sums across time. Missing or contradictory aggregation rules are P1.
- **Stock vs flow misclassified** — calling population, employment level, debt outstanding, or reserves a "flow", or calling revenue, GDP, births, or transactions a "stock", is a P1. The two are different mathematical objects.

### Framing

- **Causal claim unsupported by the brief's data** — language like "X causes Y", "X drives Y", "X is responsible for Y" requires either an experimental setup or a quoted authoritative source. Correlational data does not justify causal language. Flag as P1.
- **Unbalanced framing on a politically charged indicator** — for politically sensitive indicators (deficit, debt, immigration, unemployment, inflation), the brief must recommend showing both level and change, both nominal and real where applicable, both absolute and relative. Recommending only the framing that supports a single narrative is a P1.

---

## P2 — Should Fix Before Use

### Polish context

- **Known Polish structural break not acknowledged** — when an indicator has a documented structural break in the time series (EU accession 2004, ESA 2010 transition, GUS LFS methodology change, currency redenomination 1995, EU agricultural subsidy onset), the brief must note it. Missing acknowledgement on a long-run series is P2.
- **Wrong unit convention for Polish data** — Polish convention uses comma as decimal separator, space as thousand separator, `mln zł` and `mld zł` as currency abbreviations, and `pp` for percentage-point deltas. A brief recommending `M PLN` or `B PLN` or using `%` for a pp-delta is P2.
- **Polish indicator label missing diacritics or mixing languages** — `Srednia` instead of `Średnia`, `Stopa unemployment` instead of `Stopa bezrobocia`. Polish labels must be correct Polish.

### Benchmarks and analytical angles

- **Benchmark named vaguely** — "compare to the EU" without specifying EU-27, EU-11, EU-15, eurozone, or a specific peer group is P2. The brief must say which benchmark and why.
- **Benchmark inappropriate for Poland's structural position** — comparing Polish wages to EU-15 average without context, or Polish public debt to EU-27 average without noting Poland's position in the new member state cohort, is P2. Peer selection must justify why this comparison is meaningful.
- **Leading/lagging not declared where it matters** — for indicators that are clearly leading (PMI, sentiment, vacancies) or clearly lagging (unemployment, GDP final estimates), the brief should note the lag. Missing on a forecast-relevant indicator is P2.
- **Time periodicity not declared** — every indicator must state monthly / quarterly / annual / irregular. Missing periodicity is P2.

### Coverage

- **Brief lists fewer than three analytical angles** — a useful brief explores multiple ways into the data. A brief with only one angle is incomplete.
- **No aggregation warnings section** — the brief must include a "what NOT to do with this data" section. Missing entirely is P2.

---

## P3 — Noted

- **No reference value provided** — recommending an indicator without naming a target, EU average, or anchor year for comparison. Note as a clarity gap.
- **No chart type recommendation tied to analytical angle** — the brief should connect each analytical angle to a chart type from the visualization KB. Missing is a P3 improvement.
- **Indicator name in English only when a standard Polish term exists** — note as a content/language consistency item.
- **Brief does not cite which KB section grounds each recommendation** — note as traceability improvement.

---

## What this standard does NOT cover

- Whether the dashboard built from the brief actually renders correctly — that is `visual-screenshot-reviewer`'s scope.
- Whether the SQL queries in the resulting build sum correctly — that is `analytical-validator`'s scope at PR phase.
- Whether the semantic-layer measure DDL declared `agg`, `format_type`, and `scale` correctly — that is `measures-reviewer`'s scope.
- Whether the indicator is the absolute best KPI for the domain (vs another reasonable choice) — that is `domain-specialist`'s scope.
- Generic prose quality, grammar, formatting — out of scope.
