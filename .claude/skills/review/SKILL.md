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

## Part 0 — Independent Code Review (agent pass)

Before running any internal checks, spawn the `code-reviewer` agent:

- The agent runs `git diff HEAD` independently (fresh context — no knowledge of why the code was written this way)
- It reads `team/standards/code-review.md` and applies rules to the diff
- It returns structured P1 / P2 / P3 findings with a BLOCK / CONDITIONAL / PASS verdict

Use the Agent tool to launch `code-reviewer`. Wait for its findings before proceeding to Part 1.

Map agent findings to review output:
- Agent P1 → **CRITICAL** (must fix before committing)
- Agent P2 → **WARNING** (should fix)
- Agent P3 → **SUGGESTION** (optional)

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
