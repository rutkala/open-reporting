---
name: review
description: "Review completed implementation for quality, security, and correctness. Presents both a technical code review and a plain-language business summary for user approval before committing."
user-invocable: true
argument-hint: "[scope or directory]"
---

# Code Review

Review the completed implementation — first technically, then present a plain-language summary for user approval.

## Context

Current changes:
!`git diff HEAD --stat 2>/dev/null || echo "No changes found"`

Detailed diff:
!`git diff HEAD 2>/dev/null | head -500`

Review scope: `$ARGUMENTS` (if provided, focus here only — otherwise review all changes)

---

## Part 1 — Technical Review (internal)

Work through this checklist internally before presenting to the user.

### Code Quality
- [ ] Functions are well-named and single-purpose
- [ ] No duplicated logic
- [ ] Error handling follows project patterns (try/except with logging, not bare except)
- [ ] No leftover debug code, print statements, TODOs, or FIXMEs
- [ ] Logging uses `logging.getLogger(__name__)`, not `print()`

### Security
- [ ] No hardcoded secrets, passwords, or API keys
- [ ] SQL queries use parameterised queries — no string concatenation
- [ ] External data is validated before storing
- [ ] `.env` not committed

### Python Conventions
- [ ] `#!/usr/bin/env python3` shebang on scripts
- [ ] Imports ordered: stdlib → third-party → local
- [ ] Type hints present on function signatures
- [ ] Line length ≤ 100 characters
- [ ] f-strings used for formatting

### Data & Database
- [ ] Raw data lands in `raw.` schema, processed data in `public.` schema
- [ ] `ON CONFLICT DO UPDATE` used for upserts
- [ ] `fetched_at` timestamp included in ingestion tables
- [ ] Connection closed in `finally` block

### Dashboard Output
- [ ] Output HTML written to `nginx/html/dashboards/`
- [ ] Theme applied via `apply()` and `page()` from `charts.lib.theme`
- [ ] Source attribution visible in the dashboard
- [ ] `include_plotlyjs="cdn"` used (not bundled)

### Content Language
- [ ] User-facing text (chart titles, labels, tooltips) is in Polish
- [ ] Polish diacritics correct (ą, ć, ę, ł, ń, ó, ś, ź, ż)

---

## Part 2 — Business Summary (present to user)

After the technical review, present this — in plain language, no code:

```
## Review: {what was built}

### What was built
{1-2 sentences describing what was implemented, in plain language}

### Does it match the plan?
{Yes / Mostly (with minor differences) / No (explain)}

### Technical issues found
{CRITICAL: must fix before committing — list if any, "None" if clean}
{WARNING: should fix — list if any, "None" if clean}
{SUGGESTION: optional improvements — list if any}

### Ready to commit?
{Yes — all clear | No — fix required first (explain what)}
```

## Step 3 — Wait for Approval

- If issues found: fix them, then run `/review` again
- If clean: wait for user to say "commit" or `/commit`
- **Never commit without explicit user approval**
