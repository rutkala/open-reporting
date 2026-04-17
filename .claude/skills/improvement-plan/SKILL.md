---
name: improvement-plan
description: "Improvement plan artifact. Defines what a structured improvement proposal is — specific changes to standards, skills, or processes derived from lessons learned. Produced by /improve."
user-invocable: false
---

# Improvement Plan

An improvement plan is a structured proposal of specific changes to make to standards,
skills, or processes based on observed patterns from completed work.

Produced by: `/improve` (via `/write`)
Consumed by: PO review, then applied to `.claude/skills/` and `team/standards/`

---

## Location

`team/improvement-plans/{date}-{topic}.md`
Or as a section in `team/lessons-learned.md`.

---

## Structure

```markdown
# Improvement Plan — {Topic}

**Date:** {date}
**Source:** Lessons from OR-XXX, OR-YYY

## Observed patterns

| Pattern | How often | Impact |
|---------|-----------|--------|
| {what went wrong or could be better} | {count/frequency} | {rework / delay / quality issue} |

## Proposed changes

### 1. {Change title}

**File:** `.claude/skills/{skill}/SKILL.md` or `team/standards/build/{standard}.md`
**Change:** {exactly what to add, remove, or modify}
**Rationale:** {why this prevents recurrence}

### 2. {Next change}
...

## What this will NOT fix

{Limitations of this plan — issues that require a larger structural change or PO decision.}

## Approval required

- [ ] PO approves scope and priority of changes
- [ ] Changes applied and verified
```

---

## Quality criteria

- Every proposed change must be specific — file, section, and exact content
- Rationale must explain recurrence prevention, not just describe the problem
- Changes to CLAUDE.md or PLATFORM.md require explicit PO approval note
- "Will NOT fix" section is mandatory — prevents scope creep
