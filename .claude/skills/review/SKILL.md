---
name: review
description: "Review completed implementation for quality, security, and correctness. Runs parallel evaluator agents (code, visualization, analytical, domain). Auto-commits/pushes/opens PR when all pass. Loops autonomously to fix when blocked."
user-invocable: true
argument-hint: "[scope or directory]"
---

# Code Review

Review the completed implementation. Three specialist agents run in parallel. If all pass: auto-commit, push, open PR. If any block: fix and re-review — no human involvement until merge.

## Context

Current changes:
!`git diff HEAD --stat 2>/dev/null || echo "No changes found"`

Detailed diff:
!`git diff HEAD 2>/dev/null | head -500`

Review scope: `$ARGUMENTS` (if provided, focus here only — otherwise review all changes)

---

## Part 0 — Independent agent passes

Spawn all agents **in parallel** using Agent tool calls in the same message. Agents A–C always run. D and E are conditional.

**Agent A — `code-reviewer`**
- Runs `git diff origin/main...HEAD` independently
- Reads `team/standards/evaluation/code-review.md`, applies rules to the diff
- Returns P1 / P2 / P3 findings with BLOCK / CONDITIONAL / PASS verdict

**Agent B — `visualization-reviewer`**
- Runs `git diff origin/main...HEAD` independently
- Reads `team/standards/evaluation/visualization-diff.md`, checks chart/KPI calls in domain dashboards
- Returns HIGH / MEDIUM / LOW findings with BLOCK / CONDITIONAL / PASS verdict
- Scoped to `products/dashboards/` (excl. template) and `products/visuals/components/`

**Agent C — `analytical-validator`**
- Runs `git diff origin/main...HEAD` independently (diff-phase mode — leave $PLAN empty)
- Reads `team/knowledge-base/analytical-methods/analytical-thinking.md`, checks SQL aggregation, CAGR, labelling, and causal language
- Returns MISLEADING / QUESTIONABLE / NOTED findings with BLOCK / CONDITIONAL / PASS verdict
- Scoped to SQL files, Python data queries, and chart call string literals

**Agent D — `domain-specialist`** *(domain dashboard changes only)*
- Runs `git diff origin/main...HEAD` independently
- Reads `team/knowledge-base/domains/{domain}.md`, checks KPI selection, framing, benchmark correctness
- Pass diff as `$INPUT`
- Only spawn if diff touches `products/dashboards/{domain}/` (not template, not explorer)

**Agent E — `data-engineer-reviewer`** *(platform/ changes only)*
- Runs `git diff origin/main...HEAD` independently
- Reads `team/standards/evaluation/data-engineering-review.md`, checks ELT compliance, DuckDB patterns, dbt conventions, idempotency
- Returns P1 / P2 / P3 findings with BLOCK / CONDITIONAL / PASS verdict
- Only spawn if diff touches `platform/ingestion/`, `platform/processing/`, or `platform/warehouse/`

**Agent F — `measures-reviewer`** *(semantic layer changes only)*
- Runs `git diff origin/main...HEAD` independently
- Reads `team/standards/evaluation/measures-review.md`, checks measure definitions, aggregation correctness (stock vs flow, rate summation), `format_type`, unit/scale, Polish labels
- Returns P1 / P2 / P3 findings with BLOCK / CONDITIONAL / PASS verdict
- Only spawn if diff touches `products/semantic/`, `platform/processing/dbt/**/semantic_models/*.yml`, or `platform/processing/dbt/**/metrics/*.yml`

Wait for all agents to complete, then map findings to review output:
- code-reviewer P1 / data-engineer-reviewer P1 / measures-reviewer P1 / visualization-reviewer HIGH / analytical-validator MISLEADING → **CRITICAL**
- code-reviewer P2 / data-engineer-reviewer P2 / measures-reviewer P2 / visualization-reviewer MEDIUM / analytical-validator QUESTIONABLE → **WARNING**
- code-reviewer P3 / data-engineer-reviewer P3 / measures-reviewer P3 / visualization-reviewer LOW / analytical-validator NOTED → **SUGGESTION**

If any agent returns BLOCK → do NOT proceed to Part 0.5. Go to the **Autonomous Fix Loop** below.

---

## Part 0.5 — Screenshot review (dashboard changes only)

After Part 0 completes with no BLOCK, check whether the diff touches `products/dashboards/` (excluding template) or `products/visuals/`. If yes, spawn **`visual-screenshot-reviewer`**:

- Starts each affected dashboard from branch code on a temp port
- Takes a Playwright screenshot at 1440×900
- Reads the PNG image and evaluates against `team/standards/evaluation/visualization-image.md`
- Returns HIGH / MEDIUM / LOW findings with BLOCK / CONDITIONAL / PASS verdict

Map findings to review output:
- HIGH → **CRITICAL**
- MEDIUM → **WARNING**
- LOW → **SUGGESTION**

If the agent returns BLOCK → go to the Autonomous Fix Loop.
If the dashboard could not be started (agent notes startup failure) → flag as WARNING, do not block.

Skip this step if the diff contains only non-dashboard changes (config, docs, platform code).

---

## Part 1 — Internal checks

After all agent passes with no BLOCK, run this checklist:

### Architecture & intent
- [ ] Implementation matches the approved plan — no scope creep or silent changes
- [ ] No layer violations missed by the agent (dashboard calling raw schema, ingestion doing transformation)
- [ ] External data validated at system boundaries

### Dashboard output (if applicable)
- [ ] Source attribution visible in the dashboard
- [ ] `include_plotlyjs="cdn"` used (not bundled)

### Content language (if applicable)
- [ ] Polish strings only in domain dashboard user-facing content — not in component library or template
- [ ] Polish diacritics correct (ą, ć, ę, ł, ń, ó, ś, ź, ż)

If any Part 1 check fails: go to the Autonomous Fix Loop.

---

## Autonomous Fix Loop

When a BLOCK or Part 1 failure is found:

1. Fix the issue directly — read the failing file, apply the fix, verify
2. Re-run `/review` (all agents again)
3. Repeat up to 3 iterations for BLOCK findings, 2 for CONDITIONAL
4. If still failing after max iterations: escalate to user with a clear description of what was tried and what is still blocking

**No human involvement during the fix loop** — only escalate genuine deadlocks.

---

## Part 2 — Auto-proceed when clean

When all agents PASS and all Part 1 checks pass, proceed immediately — **no human approval needed for commit or push**:

1. **Stage and commit** — use `/commit` skill (or directly: stage changed files, commit with conventional message)
2. **Push** — `git push -u origin {branch}`
3. **Open PR** — `gh pr create` with summary of what was built and acceptance criteria checklist
4. **Present summary to user** — brief, shows PR URL, lists SUGGESTION items (not blocking)

```
## Review Complete

### What was built
{1-2 sentences}

### Review result
CRITICAL: None
WARNING: {warnings or "None"}
SUGGESTION: {suggestions or "None"}

### PR opened
{PR URL} — ready for your review and merge
```

The user's only required action is **PR merge approval**. Everything up to that point is autonomous.

---

## If invoked standalone (not from /kickoff)

Present the Part 2 summary and wait for the user to say "commit" before committing. The autonomous auto-commit only applies when `/review` is called from within `/kickoff` pipeline context.
