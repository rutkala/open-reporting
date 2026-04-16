---
name: qa
description: "Quality assurance for any completed product. Tests the built product against its requirements document. Called from product orchestrator skills."
user-invocable: false
---

# Quality Assurance

Tests the completed product against the requirements document.
Every acceptance criterion must be verified before release.
Failures return to the build step for fixes.

Applies to any product type: dashboard, article, research, social content, portal, blog.

## Inputs

- Requirements document (acceptance criteria, deliverables, content requirements)
- Built product (code, written content, visual output — whatever was produced)

## Standards and knowledge

- Read `team/standards/evaluation/analytical-review.md` — for data-driven products
- Read `team/standards/evaluation/visualization-image.md` — for visual products
- Read `team/standards/evaluation/content-review.md` — for content products
- Read `team/standards/evaluation/research-review.md` — for research products

Load only the standards relevant to the product type being reviewed.

## Agents (select relevant ones, run in parallel)

| Agent | When to use |
|-------|-------------|
| **analytical-validator** | Dashboards, research — checks KPI correctness, aggregation, statistical claims |
| **visual-screenshot-reviewer** | Dashboards, portal — checks rendered output against UX/UI spec |
| **code-reviewer** | Any product with code — final code quality pass |
| **domain-specialist** | Any product — checks domain correctness, KPI interpretation, benchmarks |
| **content-reviewer** | Articles, social content — checks accuracy, tone, structure |
| **research-reviewer** | Research products — checks methodology, claims, reproducibility |

## Test procedure

### 1. Acceptance criteria
Go through each criterion from the requirements document one by one.
Mark each: **PASS** / **FAIL** / **NOT TESTABLE** (with reason).

### 2. Deliverables check
Confirm every deliverable listed in the requirements is present and complete.

### 3. Content requirements check
Verify each content requirement is met (KPIs defined, key points covered, etc.).

### 4. Edge cases (product-specific)
*Dashboards:* no data, single value, large numbers, filter interactions
*Articles:* factual claims verified, sources cited, no unsupported conclusions
*Social content:* platform format compliance, character limits, image specs

## Outcome

**All PASS → proceed to /release.**

**Any FAIL → return to the build step** with a specific list:
- What failed
- What the correct behaviour or content should be
- Which acceptance criterion it maps to

Re-run QA after fixes. Do not proceed to release until all criteria pass.

## Output

QA report: criteria tested, results (PASS/FAIL), any known limitations or caveats.
