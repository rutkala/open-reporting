---
name: status-check
description: "Quick diagnostic check of the project — git status, running processes, recent changes, and potential issues."
disable-model-invocation: true
user-invocable: true
---

# System Status Check

Run a quick diagnostic across the project.

## Git Status

Root repo:
!`git status --short 2>/dev/null`

Current branch:
!`git branch --show-current 2>/dev/null`

## Recent Changes

Last 5 commits:
!`git log --oneline -5 2>/dev/null`

## Process Check

Node processes running:
!`tasklist /FI "IMAGENAME eq node.exe" 2>/dev/null || ps aux | grep node 2>/dev/null | head -10 || echo "Cannot check processes"`

## Report

Present a clear summary:
1. **Git state** — Any uncommitted changes? Current branch?
2. **Recent work** — What was last committed?
3. **Running services** — Are expected processes active?
4. **Potential issues** — Anything that looks wrong?
