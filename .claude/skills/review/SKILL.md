---
name: review
description: "Review completed implementation for quality, security, and correctness. Presents both a technical code review and a plain-language business summary for user approval before committing."
user-invocable: true
argument-hint: "[scope or directory]"
---

# Code Review

Review the completed implementation — first technically, then present a plain-language summary for user approval.

## Context

Current changes:
!`git diff HEAD --stat 2>/dev/null || echo "No changes found"`

Detailed diff:
!`git diff HEAD 2>/dev/null | head -500`

Review scope: `$ARGUMENTS` (if provided, focus here only — otherwise review all changes)

---

## Part 0 — Independent agent passes

Before running any internal checks, spawn all three review agents **in parallel** using three Agent tool calls in the same message:

**Agent A — `code-reviewer`**
- Runs `git diff HEAD` independently
- Reads `team/standards/code-review.md`, applies rules to the diff
- Returns P1 / P2 / P3 findings with BLOCK / CONDITIONAL / PASS verdict

**Agent B — `visualization-reviewer`**
- Runs `git diff HEAD` independently
- Reads `team/standards/evaluation/visualization-diff.md`, checks chart/KPI calls in domain dashboards
- Returns HIGH / MEDIUM / LOW findings with BLOCK / CONDITIONAL / PASS verdict
- Scoped to `products/dashboards/` (excl. template) and `products/visuals/components/`

**Agent C — `analytical-validator`**
- Runs `git diff HEAD` independently (diff-phase mode — leave $PLAN empty)
- Reads `team/knowledge-base/analytical-methods/analytical-thinking.md`, checks SQL aggregation, CAGR, labelling, and causal language
- Returns MISLEADING / QUESTIONABLE / NOTED findings with BLOCK / CONDITIONAL / PASS verdict
- Scoped to SQL files, Python data queries, and chart call string literals

Wait for all three agents to complete, then map findings to review output:
- code-reviewer P1 / visualization-reviewer HIGH / analytical-validator MISLEADING → **CRITICAL**
- code-reviewer P2 / visualization-reviewer MEDIUM / analytical-validator QUESTIONABLE → **WARNING**
- code-reviewer P3 / visualization-reviewer LOW / analytical-validator NOTED → **SUGGESTION**

If any agent returns BLOCK → overall review is blocked.

---

## Part 0.5 — Screenshot review (dashboard changes only)

After Part 0 completes, check whether the diff touches `products/dashboards/` (excluding template) or `products/visuals/`. If yes, spawn **`visual-screenshot-reviewer`**:

- Starts each affected dashboard from branch code on a temp port
- Takes a Playwright screenshot at 1440×900
- Reads the PNG image and evaluates against `team/standards/visual-screenshot-review.md`
- Returns HIGH / MEDIUM / LOW findings with BLOCK / CONDITIONAL / PASS verdict

Map findings to review output:
- HIGH → **CRITICAL**
- MEDIUM → **WARNING**
- LOW → **SUGGESTION**

If the agent returns BLOCK → overall review is blocked.
If the dashboard could not be started (agent notes startup failure) → flag as WARNING, do not block.

Skip this step if the diff contains only non-dashboard changes (config, docs, platform code).

---

## Part 1 — Technical Review (internal)

After the agent pass, run this checklist for concerns the rules file does not cover — architectural intent, domain correctness, plan alignment.

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

---

## Part 2 — Business Summary (present to user)

Combine agent findings (Part 0) and internal checks (Part 1) into one summary:

```
## Review: {what was built}

### What was built
{1-2 sentences describing what was implemented, in plain language}

### Does it match the plan?
{Yes / Mostly (with minor differences) / No (explain)}

### Technical issues found
CRITICAL: {agent P1 findings + any Part 1 blockers — "None" if clean}
WARNING:  {agent P2 findings + Part 1 warnings — "None" if clean}
SUGGESTION: {agent P3 findings — "None" if clean}

### Ready to commit?
{Yes — all clear | No — fix required first (explain what)}
```

## Step 3 — Wait for Approval

- If issues found: fix them, then run `/review` again
- If clean: wait for user to say "commit" or `/commit`
- **Never commit without explicit user approval**
