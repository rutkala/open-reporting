---
name: composite_feasibility
description: "Multi-agent feasibility assessment for a Linear issue. Runs architecture-critic, analytical-validator, and cost-estimator in parallel. Returns FEASIBLE / PARTIAL / BLOCKED with a consolidated report."
user-invocable: true
argument-hint: "OR-XXX"
---

# Feasibility Assessment

Evaluate whether a Linear issue is ready to enter implementation. Runs three evaluators in parallel and consolidates their findings.

Called automatically from `/composite_review_ideas` (before converting an idea to a proper issue) and `/composite_sprint` (before moving a Backlog issue to Todo). Can also be invoked directly: `/composite_feasibility OR-XXX`.

---

## Step 1 — Read the issue

Fetch the full Linear issue: title, description, acceptance criteria, any comments.

## Step 2 — Spawn evaluators in parallel

Spawn all three agents simultaneously:

**Agent A — `architecture-critic`**
Pass the issue description as `$PLAN` (the critic works in plan-evaluation mode).
Evaluates: data model compatibility, schema conflicts, layer violations in the proposed approach.

**Agent B — `analytical-validator`**
Pass the issue description as `$PLAN` (plan-phase mode, leave diff empty).
Evaluates: analytical design validity, aggregation soundness, misleading framing risks.

**Agent C — `cost-estimator`**
Pass the issue description as `$ISSUE`.
Evaluates: token budget estimate, scope complexity, split recommendation.

Skip Agent A if the issue has no data layer component (pure UI, content, or config).
Skip Agent B if the issue has no analytical design (infra, config, content only).
Agent C runs for every issue.

## Step 3 — Consolidate findings

Map agent verdicts to feasibility outcome:

| Agent A | Agent B | Agent C | Feasibility |
|---------|---------|---------|-------------|
| APPROVE | PASS | Proceed | **FEASIBLE** |
| CONDITIONAL | CONDITIONAL | Proceed | **PARTIAL** |
| BLOCK | any | any | **BLOCKED** |
| any | any | Split recommended | **PARTIAL** (note split) |
| any | any | Warning: rate-limit risk | **PARTIAL** (note split) |

## Step 4 — Output

```
## Feasibility: {ID} — {Title}

### Verdict
FEASIBLE | PARTIAL | BLOCKED

### Architecture
{Agent A verdict + key findings, or "Skipped — no data layer"}

### Analytical
{Agent B verdict + key findings, or "Skipped — no analytical design"}

### Cost
{Agent C estimate range + risk level + recommendation}

### Actions required
{List of specific issues to resolve before kickoff, or "None — ready to start"}
```

## Step 5 — Update Linear

- **FEASIBLE** → add comment: *"Feasibility: PASS. Ready for kickoff."*
- **PARTIAL** → add comment with the conditional findings. Issue stays in Backlog until conditions are met.
- **BLOCKED** → add comment with the blocking finding. Issue status → Backlog (do not move to Todo). PO must resolve blocker before re-assessment.
