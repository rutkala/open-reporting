---
name: kickoff
description: "Start the full implementation pipeline for a Linear issue. Reads the issue, assesses feasibility, and drives the work end-to-end: research → plan → implement → review → PR."
user-invocable: true
argument-hint: "<optional: issue ID e.g. OR-123>"
---

# Task Kickoff

Entry point for Stage 3 — implementation. Drives the full pipeline from issue to merged PR.

## Step 1 — Identify the issue

**If `$ARGUMENTS` is provided:** use that issue ID directly.

**If `$ARGUMENTS` is empty:**
1. Check the current git branch name for a pattern like `OR-123` or `feat/OR-123-description` — if found, use that issue ID
2. If no branch match, fetch all Linear issues with status **Todo** and present them as a numbered list for the user to pick from

Do not proceed until an issue is identified.

## Step 2 — Read the issue

Fetch the full Linear issue: title, description, acceptance criteria, comments, linked sub-issues.

Also read `.claude/standards/requirements.md` to check the issue meets Definition of Ready for its type.

## Step 3 — Feasibility assessment

Assess internally before presenting:
- **Data**: Does required data exist in the warehouse? If not, is there a known source?
- **Dependencies**: Does this depend on something not yet built?
- **Scope**: Is this one task or multiple in disguise?
- **Ambiguity**: Anything unclear or open to interpretation?
- **Complexity**: Small (hours) / Medium (a day) / Large (multiple sessions)?

## Step 4 — Present to user

Plain business language. No code, no jargon.

```
## {ID} — {Title}

### What this task is
{1–2 paragraphs: what needs to be built and why}

### Feasibility
{FEASIBLE / PARTIALLY FEASIBLE / BLOCKED}
{Plain explanation}

### Dependencies
{List, or "None."}

### Open questions
{List, or "None — I have everything I need."}

### Proposed approach
{"/research [topic]" if approach is unclear, or "/plan [task]" if ready to design}
```

## Step 5 — Wait for confirmation

Do NOT proceed until the user confirms understanding and answers any open questions.

## Step 6 — Update Linear

Once confirmed:
- Set issue status → **In Progress**
- Add comment: *"Kickoff confirmed. Starting [research / planning]."*

## Step 7 — Drive the pipeline

Execute the appropriate next steps in sequence, pausing for user approval at each gate:

1. `/research` — if data source or approach is unclear
2. `/plan` — design the solution, present for approval before any code
3. **Implement** — create feature branch, write code, commit
4. `/review` — standards compliance check before PR
5. **Open PR** — push branch, create PR with review output and acceptance criteria checklist
6. **Codex review loop (when available)** — Codex triggers when a PR is opened or when you comment `@codex review`. After each review, read findings with `gh api repos/rutkala/open-reporting/pulls/{N}/comments` and `gh api repos/rutkala/open-reporting/pulls/{N}/reviews`. Fix every P1, push, then comment `@codex review` to trigger re-review. Repeat until no new P1s. P2s can be fixed in the same PR or captured as follow-up issues. If Codex is rate-limited or unavailable, proceed to merge — do not block on it.
7. **Merge** — after approval and Codex findings addressed, merge to main
8. `/document` — update affected docs, RELEASE_NOTES.md
9. **Lessons learned (mandatory)** — after every issue, reflect on what went wrong or could go better. Update standards, skills, or playbooks based on findings. See `/document` Step 5.
10. **Close** — Linear issue → **Done** (only after PR is merged), delete feature branch
