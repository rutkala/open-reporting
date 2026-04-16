---
name: qa
description: "Quality assurance for a completed dashboard. Tests the built product against the requirements document. Called from /dashboard Step 7."
user-invocable: false
---

# Quality Assurance

Tests the built dashboard against the requirements document from Step 3.
Every acceptance criterion must be verified. Failures return to /dashboard-code for fixes.

## Inputs

- Requirements document from Step 3 (acceptance criteria, KPI definitions)
- Architecture design from Step 4 (KPI calculation logic, data model)
- Built dashboard at `products/dashboards/{domain}/app.py`

## Standards and knowledge

- Read `team/standards/evaluation/analytical-review.md` — KPI correctness, aggregation rules
- Read `team/standards/evaluation/visualization-image.md` — visual QA rules

## Agents (run in parallel)

- **analytical-validator** — checks KPI calculations, aggregation correctness, statistical validity
- **visual-screenshot-reviewer** — checks rendered output against UX/UI design spec
- **code-reviewer** — final code quality pass
- **domain-specialist** — checks domain correctness (KPI interpretation, benchmarks)

## Test checklist

### Data correctness
- Each KPI value matches its definition and calculation method
- Aggregations are correct (no double-counting, correct grain)
- Filters apply correctly to all charts on the relevant page
- Time period handling is correct (fiscal vs calendar year if relevant)
- Null and zero values handled gracefully

### Visual correctness
- Chart types match UX/UI design specification
- Axis labels are in Polish and match the spec
- Colours match the palette specified in UX/UI design
- KPI cards display correct format and unit
- Layout matches the design on desktop resolution

### Acceptance criteria
Go through each criterion from the requirements document one by one.
Mark each: PASS / FAIL / NOT TESTABLE (with reason).

### Edge cases
- No data available for selected filters
- Single data point
- Very large values (formatting)
- All-zero series

## Outcome

**All PASS:** proceed to /release.

**Any FAIL:** return to /dashboard-code with a specific list of what failed and what the
correct behaviour should be. Re-run QA after fixes — do not proceed until all pass.

## Output

QA report summarising: criteria tested, results, any caveats or known limitations.
