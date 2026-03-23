---
name: kickoff
description: "Start work on a task or issue. Reads the task from Linear, assesses feasibility, identifies blockers and ambiguities, and presents a plain-language summary for user confirmation before any work begins."
user-invocable: true
argument-hint: "<issue ID e.g. ORE-123>"
---

# Task Kickoff

Read a task, assess feasibility, and confirm understanding before starting any work.

## Step 1 — Read the Task

Read the Linear issue: `$ARGUMENTS`

Use the Linear MCP tool to fetch the full issue including description, comments, and any attachments.

## Step 2 — Feasibility Assessment

Before presenting to the user, assess internally:

- **Data**: Does the required data exist in the DB? If not, does a known source exist?
- **Dependencies**: Does this task depend on something not yet built?
- **Scope**: Is this one task or multiple tasks in disguise?
- **Ambiguity**: Is anything unclear, underspecified, or open to interpretation?
- **Complexity**: How large is this — small (hours), medium (a day), large (multiple sessions)?

## Step 3 — Present to User

Present in plain business language. No code. No technical jargon unless necessary.

```
## Task: {ID} — {Title}

### What I understand this task to be
{1-2 paragraph plain-language description of what needs to be built and why}

### Feasibility
{FEASIBLE / PARTIALLY FEASIBLE / BLOCKED}
{Plain explanation — what can be done now, what is blocked and why}

### Dependencies
{List anything that must exist before this can be built. If none, say "None."}

### Questions before I start
{List any ambiguities that need your decision. If none, say "None — I have everything I need."}

### Proposed next step
{"/research [specific question]" or "/plan [task]" if straightforward enough to skip research}
```

## Step 4 — Wait for Confirmation

Do NOT proceed to research or planning until the user:
- Confirms the understanding is correct
- Answers any open questions
- Explicitly says "proceed" or similar

## Step 5 — Update Linear

Once confirmed, update the Linear issue:
- Set status to **In Progress**
- Add comment: *"Starting work. Feasibility confirmed. Proceeding to research/planning."*
