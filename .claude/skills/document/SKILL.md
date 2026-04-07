---
name: document
description: "Update project documentation after completing implementation. Reviews what was built and updates the relevant docs/ files, README.md, and inline code comments."
user-invocable: true
argument-hint: "[what was built]"
---

# Documentation Update

Update documentation to reflect what was just built. Run after `/commit`.

## Context

What was just built: `$ARGUMENTS`

Recent commit:
!`git log --oneline -3 2>/dev/null`

Changed files:
!`git diff HEAD~1 --name-only 2>/dev/null`

## Step 1 — Identify What Needs Updating

Based on what was built, determine which documents are affected:

| What changed | Documents to update |
|---|---|
| New data source added | `docs/DATA_SOURCES.md` |
| New domain or product area | `docs/DOMAINS.md` |
| Architecture change (new service, new folder) | `docs/ARCHITECTURE.md`, `README.md` |
| New workflow or process | `docs/WORKFLOW.md` |
| Project direction or goals changed | `docs/PROJECT.md` |
| New ingestion script | Inline docstring in the script itself |
| New dashboard | Inline docstring in the script itself |

## Step 2 — Update Documents

For each document that needs updating:
- Add new information in the right section
- Remove or correct anything that is now outdated
- Keep language plain — these docs are also used as context in Claude.ai

## Step 3 — Update Inline Docstrings

For any new Python scripts, ensure the module docstring includes:
```python
"""
{What this script does in one sentence}
Source: {data source name and URL}
Schema: {DB schema.table it writes to}
Usage: python3 {path/to/script.py} [--flags]
"""
```

## Step 4 — Present Summary

Tell the user:
- Which documents were updated and what was added
- Whether anything in the docs is now outdated and was corrected
- Whether any documentation gaps remain

## Step 5 — Lessons Learned (mandatory after every issue)

Reflect on the issue that was just completed. Ask:
- What went wrong or took longer than expected?
- What was discovered about the data, tools, or architecture that wasn't known at the start?
- What would have made this issue go faster or smoother?
- Did any process steps get skipped, and why?

For each lesson, decide where it belongs and update it immediately:

| Type of lesson | Where to write it |
|---|---|
| Technical pattern or pitfall (data types, tool quirk, API behaviour) | `team/standards/build/` — relevant standard |
| Process failure (step skipped, wrong order, wrong gate) | `.claude/skills/` — relevant skill |
| Architecture decision or constraint | `docs/ARCHITECTURE.md` or inline in relevant script |
| Tooling or environment fact | `.claude/session-memory.md` Key Technical Facts |
| Behaviour rule for future sessions | `memory/feedback_*.md` |

Present the lessons and where they were written. If no lessons — explicitly state "No lessons identified." Do not silently skip this step.

## Rules
- **Plain language** — docs are read by both Claude.ai and Claude Code
- **Don't over-document** — update only what actually changed
- **No new files** unless genuinely needed — update existing docs first
- **Keep docs concise** — a good doc is one that gets read
- **Lessons learned is not optional** — always run Step 5, even for small issues
