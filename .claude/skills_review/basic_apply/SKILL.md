---
name: basic_apply
description: "Execute a prepared action — deploy, publish, migrate, or activate. Atomic action invoked by release. Reads an action plan and executes it without making new decisions."
user-invocable: false
---

# Apply

Execute a prepared, approved action. The calling skill (release) defines what to apply
and verifies the preconditions. This skill executes and confirms.

**Called by:** release.

## Input

- Action plan: exactly what to execute (from calling skill)
- Preconditions: what must be true before execution begins

## Steps

1. Confirm all preconditions are met — do NOT proceed if any are unmet; report back
2. Execute the action exactly as specified — no improvisation
3. Verify the action succeeded (check output, URL, service status, etc.)
4. If failure: stop immediately, report what happened, do not retry destructive actions
5. Return confirmation (success + verification evidence) to calling skill

## Action types

| Action | Verification |
|--------|-------------|
| Deploy dashboard | Service responds at its URL |
| Publish article | Appears at www.open-reporting.dev |
| Merge PR | Branch merged, CI green |
| Run migration | Rows present, schema matches DDL |
| Restart service | `docker compose ps` shows healthy |

## Rules

- Never execute if preconditions are unmet
- Never modify scope during execution — if something unexpected arises, stop and report
- Destructive actions (drop table, delete branch, overwrite production) require confirmation first
