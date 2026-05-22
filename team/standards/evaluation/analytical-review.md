# Analytical Review Rules

**Derived from:** `team/knowledge-base/analytical-methods/analytical-thinking.md` *(KB complete)*
**Used by:** `.claude/agents/analytical-validator.md`
**Does NOT cover:** code quality (see `evaluation/code-review.md`), architecture layer violations (see `evaluation/architecture-review.md`), visual design (see `evaluation/visualization-image.md`)

Rules applied by the `analytical-validator` agent at plan phase and diff phase.
A chart or SQL query can be technically correct and architecturally compliant while still communicating a false or misleading picture.

---

## MISLEADING — Block (BLOCK)

A single MISLEADING finding must be fixed before merge. These produce analyses that actively mislead users.

### Plan-phase rules

- **Mean on skewed distribution** — wages, income, rent, wealth, or any strongly right-skewed variable. If a plan proposes `AVG()` / mean without explicit justification, flag it. KB rule: "the median is almost always preferred over mean for skewed distributions."
- **CAGR across structural break** — any plan proposing CAGR over a period crossing 2008–09 (financial crisis), 2020 (COVID), or 2004 (EU accession). KB rule: "Do not use CAGR across these periods."
- **Non-comparable populations directly contrasted** — comparing registered unemployment to LFS/BAEL without harmonisation; comparing pre-2012 to post-2012 Polish wage survey data without noting the coverage change.
- **Causal claim from correlational evidence** — any plan using "drives", "causes", "results in" based solely on co-movement. KB rule: "No correlation is evidence of causation."
- **Percentage change on a value already expressed as percent** — "unemployment rose X%" when the correct framing is "rose X percentage points."

### Diff-phase rules

- **`AVG()` / `mean()` on wage, income, or salary columns** — flag `AVG(value)` or `.mean()` on any column named `wage`, `salary`, `income`, `earnings`, `wynagrodzenie`, `płaca`.
- **CAGR formula spanning a structural break** — CAGR where start year ≤ 2007 and end ≥ 2010 (2008–09 crisis), or start ≤ 2019 and end ≥ 2021 (COVID), or start ≤ 2003 and end ≥ 2005 (EU accession).
- **Causal language in chart strings** — string literals containing "spowodowany", "wynika z", "napędza", "caused by", "driven by", "due to" in chart titles, subtitles, or KPI labels without explicit qualification ("correlated with", "associated with").
- **Percentage change label on a percentage-point difference** — "%" suffix on a value representing a difference between two percentage values, without labelling as "pp" or "percentage points."

---

## QUESTIONABLE — Conditional (CONDITIONAL)

These degrade analytical quality without actively misleading. Fix before merge where practical.

### Plan-phase rules

- **Aggregate change without compositional decomposition** — reporting aggregate change (e.g., rising average wages) without checking for Simpson's paradox / compositional shift.
- **Per capita normalisation without proportionality check** — per capita cross-country comparisons without noting the proportionality assumption; particularly relevant for small-country comparisons.
- **Level without rate-of-change (or vice versa)** — reporting only the level when the rate is more interesting, or vice versa.
- **EU27 comparison without V4 for structural stories** — for structural analysis of Poland's labour or fiscal position, V4 is the appropriate first-order peer. EU27-only comparisons may mislead by mixing structurally dissimilar economies.
- **Seasonal series without adjustment note** — period-over-period change for a series with known seasonal patterns (employment, construction, retail) without mentioning seasonal adjustment.
- **Period average where end-of-period is more appropriate** — or vice versa. Annual averages hide intra-year movement; end-of-period values ignore intra-year trajectory.

### Diff-phase rules

- **Aggregate query without compositional awareness** — `AVG()` or `SUM()` across a group dimension without a corresponding decomposition query or comment.
- **Hard-coded date range** — a filter like `WHERE year >= 2020` that selects post-event data without a comment explaining the structural reason.
- **Division without zero-guard** — ratio calculations (`a / b`) without `NULLIF(b, 0)` or equivalent.

---

## NOTED — Log only (NOTE)

Minor issues that do not meaningfully affect correctness.

- No named policy threshold referenced for a value near one (e.g., debt near 55%, unemployment near 5%)
- Missing long-run trend context anchored to 2004 baseline for labour/fiscal indicators
- CAGR used without a note that it smooths intra-period volatility
- SQL ordering or filtering that could silently exclude outliers without documentation
- `ROUND()` applied inconsistently in the same query
- Missing `FILTER` clause on a window function where conditional aggregation is likely intended

---

## Cannot evaluate from code or plan

Always include this section in the review output so the reviewer knows the limits:

- Aggregation intent for non-wage indicators (requires knowing analytical purpose)
- Comparison validity across populations (requires knowing data lineage)
- Causation vs correlation in narrative text outside chart calls
- Outlier handling in upstream data preparation
- Whether the chosen indicator is the right one for the analytical question (domain-specialist's job)
