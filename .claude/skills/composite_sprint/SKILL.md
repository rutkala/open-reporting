---
name: composite_sprint
description: "Sprint planning — review the backlog, decide which issues to work on this cycle, and move them to Todo."
user-invocable: true
argument-hint: ""
---

# Sprint Planning

Review the backlog and decide what goes into the current sprint. Lightweight — no ceremony, just prioritisation.

## Step 1 — Fetch backlog issues

List all Linear issues with status **Backlog** that do NOT have the **Idea** label.

If the backlog is empty, say so and stop.

## Step 2 — Present backlog

Group by milestone (Phase 1, Phase 2, etc.), show label and priority:

```
## Backlog — Sprint Planning

### Phase 1 — Content & Data Depth

| # | ID | Title | Label | Priority |
|---|----|-------|-------|----------|
| 1 | OR-78 | Set up Ghost admin account | Infra | Urgent |
| 2 | OR-85 | Automate daily ingestion cron | Infra | Urgent |
| 3 | OR-81 | MAC domain dashboard | Feature | High |
...
```

## Step 3 — Recommend

Based on priority, dependencies, and logical sequencing, recommend a focused set for the sprint (typically 2–4 issues for a one-person team).

Explain your reasoning briefly — e.g. "OR-78 blocks OR-79 and OR-80, so it should go first."

Then ask: *"Which issues do you want in this sprint?"*

## Step 4 — Feasibility gate + move to Todo

For each confirmed issue, run `/composite_feasibility {issue ID}` before moving to Todo.

- **FEASIBLE** → set status → **Todo**, add comment: *"Feasibility: PASS. Added to sprint [date]."*
- **PARTIAL** → set status → **Todo** with conditions noted, add comment with the conditional findings
- **BLOCKED** → do NOT move to Todo; add blocking finding as comment; present to user before proceeding

After feasibility passes:
- Set status → **Todo**
- Add comment: *"Added to sprint [date]."*

## Step 5 — Summary

```
## Sprint Started

**Active this sprint:**
- OR-XX — Title (Label, Priority)
- OR-XX — Title (Label, Priority)

**Suggested order:** OR-XX → OR-XX → OR-XX

When ready to start: `/composite_kickoff` (I'll detect the first Todo issue or show the list)
```
