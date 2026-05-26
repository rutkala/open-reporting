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

Also read `docs/process/requirements.md` to check the issue meets Definition of Ready for its type.

## Step 3 — Feasibility check

Spawn `architecture-critic` and `analytical-validator` in parallel against the issue description. This runs silently; surface findings in Step 4.

## Step 4 — Present to user

Plain business language. No code, no jargon. Include feasibility findings.

```
## {ID} — {Title}

### What this task is
{1–2 paragraphs: what needs to be built and why}

### Feasibility
{FEASIBLE / PARTIAL / BLOCKED — from evaluator output}
{Plain explanation of any blocking or conditional findings}

### Dependencies
{List, or "None."}

### Open questions
{List, or "None — I have everything I need."}

### Proposed approach
{"/basic_research [topic]" if approach is unclear, or "/plan [task]" if ready to design}
```

If BLOCKED → stop here. Document the blocker on the Linear issue. Do not proceed.

## Step 5 — Wait for confirmation

Present the summary, then wait for user confirmation. If FEASIBLE and no open questions: user confirmation is a brief "yes" or equivalent — do not require more.

## Step 6 — Update Linear

Once confirmed:
- Set issue status → **In Progress**
- Add comment: *"Kickoff confirmed. Starting [research / planning]."*

## Step 7 — Route to the right pipeline

Identify the product type from the Linear issue labels or description, then route:

**Code products (dashboard, portal, mobile):**
Run `/develop {issue ID}` — this drives the full pipeline:
document → design → build → test → release

**Platform / data / infra work** (no product orchestrator exists for these yet):
1. `/basic_research` — if data source or approach is unclear
2. `/plan` — design the solution, present for approval before any code
3. Create feature branch, write code (`data-engineer` for `platform/` and infra)
4. `/review` — auto-commits, pushes, opens PR when clean; loops to fix when blocked
5. **Merge** — present PR URL; wait for merge approval
6. **Close** — Linear issue → **Done**, delete feature branch
