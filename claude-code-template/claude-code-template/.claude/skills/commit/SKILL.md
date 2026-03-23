---
name: commit
description: "Create a conventional git commit with auto-generated message from current changes. Analyzes the diff, determines the correct commit type (feat/fix/refactor/docs/chore), and generates a descriptive message."
disable-model-invocation: true
user-invocable: true
argument-hint: "[optional message hint]"
---

# Smart Commit

Create a well-formatted conventional commit for the current changes.

## Current State

Git status:
!`git status --short 2>/dev/null`

Staged changes:
!`git diff --cached --stat 2>/dev/null || echo "Nothing staged"`

Unstaged changes:
!`git diff --stat 2>/dev/null || echo "Nothing unstaged"`

Recent commit messages (for style reference):
!`git log --oneline -5 2>/dev/null`

## Instructions

1. **Check language** — Read `.claude/languages.json` → `agent_language` for commit message language. Default to English if file does not exist.
2. **Analyze changes** — Read the diff to understand what was changed and why
3. **Pick commit type** based on the nature of changes:
   - `feat:` — New feature or capability
   - `fix:` — Bug fix
   - `refactor:` — Code restructuring without behavior change
   - `docs:` — Documentation only
   - `chore:` — Build, config, tooling changes
4. **Generate message** — Concise, descriptive, focuses on "why" not "what"
5. **Present to user** — Show the proposed commit message and files to be committed
6. **Wait for approval** — NEVER auto-commit. Always wait for user to confirm

If user provided a hint: `$ARGUMENTS` — use it to inform the commit message.

## Commit Format

```
type: short description (max 72 chars)

Optional longer description if the change is complex.
Explain the "why" behind the change.

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Safety Rules

- **NEVER** auto-commit without user approval
- **NEVER** use `--no-verify` to skip hooks
- **NEVER** amend existing commits unless explicitly asked
- **NEVER** commit files that may contain secrets (.env, credentials)
- **ALWAYS** stage specific files (not `git add -A` or `git add .`)
- **ALWAYS** create NEW commits (don't amend unless asked)
