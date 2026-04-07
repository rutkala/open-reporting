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

Also read `team/standards/build/requirements.md` to check the issue meets Definition of Ready for its type.

## Step 3 — Feasibility + cost

Run `/feasibility {issue ID}` — spawns architecture-critic, analytical-validator, and cost-estimator in parallel against the issue description. This runs silently; surface findings in Step 4.

## Step 4 — Present to user

Plain business language. No code, no jargon. Include feasibility findings.

```
## {ID} — {Title}

### What this task is
{1–2 paragraphs: what needs to be built and why}

### Feasibility
{FEASIBLE / PARTIAL / BLOCKED — from /feasibility output}
{Plain explanation of any blocking or conditional findings}

### Cost estimate
{Range from cost-estimator: e.g. "120–250k tokens, Medium risk"}
{If split recommended: suggest how to split}

### Dependencies
{List, or "None."}

### Open questions
{List, or "None — I have everything I need."}

### Proposed approach
{"/research [topic]" if approach is unclear, or "/plan [task]" if ready to design}
```

If BLOCKED → stop here. Document the blocker on the Linear issue. Do not proceed.

## Step 5 — Wait for confirmation

Present the summary, then wait for user confirmation. If FEASIBLE and no open questions: user confirmation is a brief "yes" or equivalent — do not require more.

## Step 6 — Update Linear

Once confirmed:
- Set issue status → **In Progress**
- Add comment: *"Kickoff confirmed. Starting [research / planning]."*

## Step 7 — Drive the pipeline

Execute the appropriate next steps in sequence, pausing for user approval at each gate:

1. `/research` — if data source or approach is unclear
2. `/plan` — design the solution, present for approval before any code
3. **Implement** — create feature branch, write code (use `data-architect` for `platform/` work, `dashboard-dev` for `products/dashboards/` and `products/visuals/` work)
4. `/review` — runs all evaluator agents in parallel; auto-commits, pushes, and opens PR when all pass; loops to fix when blocked (no human involvement during review loop)
5. **Merge** — present PR URL to user; wait for merge approval (only human gate in the pipeline)
6. `/document` — update affected docs, RELEASE_NOTES.md
7. **Lessons learned (mandatory)** — after every issue, reflect on what went wrong or could go better. Update standards, skills, or playbooks based on findings. See `/document` Step 5.
8. **Close** — Linear issue → **Done** (only after PR is merged), delete feature branch
