---
name: test
description: >
  Test a completed product against its requirements document. Use when /evaluate invokes
  it for code products, when acceptance criteria need functional verification, or when
  the PO says "run the tests" or "does this work correctly". Every acceptance criterion
  must be verified — nothing is assumed. Failures return to /build with an exact list.
  Triggers when: "run tests", "verify the product works", "check acceptance criteria",
  or when /evaluate reaches the functional testing step for a code product.
user-invocable: false
---

# Test

Tests the completed product against the requirements document.
Every acceptance criterion must be verified. Failures return to `/build` with a specific list.

Applies to: dashboard, portal, mobile, article, research, social content.

## Input

- Requirements document (acceptance criteria, deliverables, content requirements)
- Design document (for data products — KPI calculation logic, semantic model spec)
- Built product (running code, written content, or other output)

## Output

- Test report: criteria tested, results (PASS / FAIL / NOT TESTABLE), known limitations
- PASS → proceeds to `/release`
- FAIL → returns to `/build` with specific failure list

## Components

Select agents relevant to the product type. Run in parallel.

| Agent | When to use |
|-------|-------------|
| analytical-validator | Dashboards, research — KPI correctness, aggregation, statistical claims |
| visual-screenshot-reviewer | Dashboards, portal — rendered output vs design spec |
| code-reviewer | Any product with code — final quality pass |
| domain-specialist | Any product — domain correctness, KPI interpretation, benchmarks |
| content-reviewer | Articles, social content — accuracy, tone, structure |
| research-reviewer | Research products — methodology, claims, reproducibility |

## Steps

1. Read requirements document in full — note every acceptance criterion
2. Spawn relevant evaluator agents in parallel
3. Work through test checklist (see Instructions)
4. Compile test report
5. If any FAIL: return to `/build` with specific failure list; re-run after fixes
6. If all PASS: proceed to `/release`

## Instructions

**Acceptance criteria**
Go through each criterion from the requirements document one by one.
Mark each: **PASS** / **FAIL** / **NOT TESTABLE** (with reason).

**Deliverables check**
Confirm every deliverable listed in requirements is present and complete.

**Content requirements check**
Verify each content requirement is met (KPIs shown, key analytical angles covered, etc.).

**Product-specific edge cases**

*Dashboards:*
- No data for selected filter combination
- Single data point
- Large values (number formatting)
- Filter interactions (page-scoped vs global)
- KPI values match calculation logic from design document
- Semantic layer measures match what is displayed

*Articles / social content:*
- All factual claims are verifiable from cited sources
- No unsupported conclusions
- Polish is correct (diacritics, formal register)

*Research:*
- Methodology matches what was specified in requirements
- Results reproducible from provided data and code
- Claims proportionate to evidence

**On failure**
Return to `/build` with:
- Exactly what failed (criterion reference number)
- What was observed vs what was expected
- What needs to change

## Standards

- `team/standards/evaluation/analytical-review.md` (data products)
- `team/standards/evaluation/visualization-image.md` (visual products)
- `team/standards/evaluation/content-review.md` (content products)
- `team/standards/evaluation/research-review.md` (research products)

Load only the standards relevant to the product type being tested.
