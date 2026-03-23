---
name: deps
description: "Audit project dependencies for outdated packages, known vulnerabilities, and unused imports. Supports npm, pip, cargo, go, composer, and bundler. Run /deps to get a full report."
disable-model-invocation: true
user-invocable: true
argument-hint: "[outdated | security | unused | all]"
---

# Dependency Audit

Check project dependencies for issues: outdated versions, security vulnerabilities, and unused packages.

## Arguments
`$ARGUMENTS`

- No argument or `all`: Run all checks
- `outdated`: Only check for outdated packages
- `security`: Only check for known vulnerabilities
- `unused`: Only scan for unused imports/dependencies

## Step 1 — Detect Package Manager

| Check | Manager | Lock File |
|-------|---------|-----------|
| `package.json` | npm/yarn/pnpm | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |
| `requirements.txt` or `pyproject.toml` | pip/poetry | `requirements.txt`, `poetry.lock` |
| `Cargo.toml` | cargo | `Cargo.lock` |
| `go.mod` | go modules | `go.sum` |
| `composer.json` | composer | `composer.lock` |
| `Gemfile` | bundler | `Gemfile.lock` |

If multiple exist (monorepo), run for each.

## Step 2 — Outdated Check

Run the appropriate command:

| Manager | Command |
|---------|---------|
| npm | `npm outdated --json 2>/dev/null` |
| yarn | `yarn outdated --json 2>/dev/null` |
| pip | `pip list --outdated --format=json 2>/dev/null` |
| cargo | `cargo outdated 2>/dev/null` (if installed) |
| go | `go list -u -m all 2>/dev/null` |
| composer | `composer outdated --format=json 2>/dev/null` |
| bundler | `bundle outdated 2>/dev/null` |

If the command is not available, fall back to reading the lock file and checking versions manually.

## Step 3 — Security Audit

Run the appropriate command:

| Manager | Command |
|---------|---------|
| npm | `npm audit --json 2>/dev/null` |
| yarn | `yarn audit --json 2>/dev/null` |
| pip | `pip-audit --format=json 2>/dev/null` or `safety check 2>/dev/null` |
| cargo | `cargo audit 2>/dev/null` |
| go | `govulncheck ./... 2>/dev/null` |
| composer | `composer audit --format=json 2>/dev/null` |
| bundler | `bundle audit check 2>/dev/null` |

If the audit tool is not installed, note it and suggest installation.

## Step 4 — Unused Dependencies (code scan)

For each dependency in the manifest:
1. Search the codebase for imports/requires of that package
2. Flag packages that have zero import references
3. Exclude known config-only packages (e.g., `eslint`, `prettier`, `typescript`, `@types/*`, `babel-*`, build tools)

**Be careful with:**
- Packages used only in config files (e.g., `tailwindcss` in `tailwind.config.js`)
- Packages used as CLI tools (e.g., `rimraf`, `cross-env`)
- Peer dependencies
- Plugins loaded by name (e.g., babel plugins, eslint plugins)

## Step 5 — Report

```markdown
# Dependency Audit Report

**Project:** {name from manifest}
**Manager:** {npm/pip/cargo/etc}
**Date:** {today}
**Total dependencies:** {count}

## Security Vulnerabilities

| Severity | Package | Version | Vulnerability | Fix |
|----------|---------|---------|---------------|-----|
| CRITICAL | lodash | 4.17.20 | Prototype Pollution (CVE-xxxx) | Upgrade to 4.17.21 |
| HIGH | ... | ... | ... | ... |

**Action needed:** {count} vulnerabilities found. Run `{fix command}` to auto-fix.

## Outdated Packages

| Package | Current | Latest | Type | Breaking? |
|---------|---------|--------|------|-----------|
| react | 17.0.2 | 18.2.0 | major | Yes — see migration guide |
| axios | 0.27.0 | 1.6.0 | major | Yes — response format changed |
| lodash | 4.17.20 | 4.17.21 | patch | No |

### Major updates (breaking changes likely):
- **react** 17 → 18: Requires concurrent mode migration
- **axios** 0.x → 1.x: Response data structure changed

### Minor/patch updates (safe to upgrade):
- Run `{upgrade command}` to update {count} packages

## Potentially Unused

| Package | Last import found | Suggestion |
|---------|-------------------|------------|
| moment | None | Remove — consider `date-fns` if needed |
| underscore | None | Remove — `lodash` already installed |

**Note:** Verify these are truly unused before removing. Some may be used dynamically.

## Recommendations
1. [ ] Fix {count} security vulnerabilities immediately
2. [ ] Update {count} patch-level packages (safe)
3. [ ] Plan migration for {count} major updates
4. [ ] Investigate {count} potentially unused packages
```

## Rules
- **NEVER auto-remove or auto-upgrade** packages without user approval
- **NEVER run `npm audit fix --force`** — it can break things. Always show the plan first
- If a vulnerability has no fix available, note it as "No fix yet — monitor"
- Read `.claude/languages.json` → `agent_language` for report language
- For monorepos, run per-package and combine into one report
