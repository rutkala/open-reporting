---
name: composite_standards_review
description: "Self-improvement cycle. Reads lessons-learned history, identifies recurring patterns, and proposes updates to standards and skills. Run after every 10 issues or when explicitly requested."
user-invocable: true
argument-hint: ""
---

# Standards Review

Reads the lessons-learned log for recurring patterns and proposes concrete updates to evaluation standards, build standards, and skills. This is the self-improvement loop.

---

## Step 1 — Read lessons learned

Read `team/lessons-learned.md` in full.

Look for:
- **Recurring finding types** — if the same type of issue appears 3+ times (e.g. "missing type hints", "bare except", "non-standard KPI"), it should become a P1/P2 rule
- **False positives** — if agents are flagging things that were deliberately acceptable, the rule may need scoping
- **Missing rules** — issues that recurred but are not covered by any evaluation standard
- **Outdated rules** — rules that reference paths, tools, or patterns that no longer exist in the codebase
- **Process failures** — steps that were skipped because a skill made them easy to miss

## Step 2 — Read current standards

Read all evaluation standards:
- `team/standards/evaluation/code-review.md`
- `team/standards/evaluation/visualization-diff.md`
- `team/standards/evaluation/visualization-image.md`

Read relevant build standards if process failures were noted:
- `team/standards/build/requirements.md`
- `team/standards/build/ingestion.md`
- `team/standards/build/processing.md`

## Step 3 — Cross-reference KB

For any proposed new rule, check whether there is KB backing:
- `team/knowledge-base/analytical-methods/analytical-thinking.md`
- `team/knowledge-base/visualization/`
- `team/knowledge-base/ux-perception/` (if built)
- `team/knowledge-base/data-architecture/` (if built)
- `team/knowledge-base/data-engineering/` (if built)
- `team/knowledge-base/business-analysis/` (if built)

A new rule without KB backing should be marked "experience-based — KB not yet built" in the standard.

## Step 4 — Produce proposals

For each proposed change:

```
### Proposal {N}: {one-line description}

**Type:** New rule | Rule update | Rule removal | Process update
**Affects:** {standard or skill file path}
**Trigger:** {what in lessons-learned prompted this — cite specific entry dates}

**Proposed change:**
{exact text to add, update, or remove — show as a diff if modifying existing text}

**KB backing:** {KB section that supports this, or "Experience-based — KB not yet built"}
**Severity if added:** P1 | P2 | P3 (for code-review) | HIGH | MEDIUM | LOW (for others)
```

Present all proposals at once.

## Step 5 — Wait for approval

Ask: *"Which proposals should I apply?"* — user can say "all", "N, N, N", or "none".

## Step 6 — Apply approved proposals

For each approved proposal:
1. Edit the relevant standard or skill file directly
2. Update `team/standards/INDEX.md` if a new standard is added
3. Add a note to `team/lessons-learned.md`: *"Standards review applied: {proposal summary}"*

## Step 7 — Summary

```
## Standards Review Complete

**Applied:** {list of proposals applied}
**Deferred:** {list of proposals deferred by user}
**Files updated:** {list of files changed}
```
