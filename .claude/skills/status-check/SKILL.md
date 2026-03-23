---
name: status-check
description: "Quick diagnostic of the project — git state, Docker services, recent changes, and open items from session memory."
user-invocable: true
---

# Status Check

Run a quick diagnostic across the project.

## Git Status

!`git status --short 2>/dev/null`

Current branch:
!`git branch --show-current 2>/dev/null`

Last 5 commits:
!`git log --oneline -5 2>/dev/null`

## Docker Services

!`docker compose ps 2>/dev/null || echo "docker compose not available"`

## Report

Present a clear plain-language summary:

1. **Git state** — Any uncommitted changes? What branch?
2. **Recent work** — What was last committed?
3. **Services** — Are nginx, postgres, and ghost running? Any stopped or unhealthy?
4. **Open items** — Read `.claude/session-memory.md` and list any open items
5. **Issues** — Anything that looks wrong or needs attention?
