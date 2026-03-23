---
name: review
description: "Review current code changes for quality, security, and correctness before committing. Analyzes git diff, checks for common pitfalls, and provides actionable feedback."
disable-model-invocation: true
user-invocable: true
argument-hint: "[scope or directory]"
---

# Code Review

Review the current uncommitted changes for quality, security, and correctness.

## Context

Current git diff (staged + unstaged):
!`git diff HEAD --stat 2>/dev/null || echo "No changes found"`

Detailed diff:
!`git diff HEAD 2>/dev/null | head -500`

## Review Scope

If argument provided, focus on `$ARGUMENTS` only. Otherwise review all changes.

## Review Checklist

For each changed file, check:

### Code Quality
- [ ] Functions are well-named and single-purpose
- [ ] No duplicated logic (check if a utility already exists)
- [ ] Error handling follows project patterns
- [ ] No leftover debug code (console.log, TODO, FIXME)

### Security
- [ ] No hardcoded secrets, tokens, or credentials
- [ ] User input is validated/sanitized
- [ ] SQL queries use parameterized queries (never string concatenation)
- [ ] Auth/authorization checks are present where needed

### Best Practices
- [ ] No unnecessary dependencies added
- [ ] Tests cover new functionality (if test framework exists)
- [ ] API responses follow project conventions
- [ ] No breaking changes without migration path

### Translations (if applicable)
- [ ] User-facing strings use i18n calls (not hardcoded)
- [ ] Translation keys added for ALL languages listed in `.claude/languages.json` → `content_languages`
- [ ] Translations follow the `style_notes` register (formal/informal, spelling conventions)

### {PROJECT-SPECIFIC CHECKLIST}
<!-- ADD YOUR PROJECT-SPECIFIC CHECKS HERE -->
<!-- Examples: -->
<!-- - [ ] Database migrations included for schema changes -->
<!-- - [ ] Socket event names match between server and client -->

## Output Format

Organize feedback by priority:
1. **CRITICAL** — Must fix before committing (security issues, broken logic)
2. **WARNING** — Should fix (pattern violations, missing validation)
3. **SUGGESTION** — Nice to have (style, minor improvements)

For each item, include the file path, line reference, and specific fix.
