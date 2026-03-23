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

## Rules
- **Plain language** — docs are read by both Claude.ai and Claude Code
- **Don't over-document** — update only what actually changed
- **No new files** unless genuinely needed — update existing docs first
- **Keep docs concise** — a good doc is one that gets read
