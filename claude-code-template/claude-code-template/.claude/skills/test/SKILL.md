---
name: test
description: "Detect the project's test framework and run relevant tests. Can run all tests, tests for a specific file, or tests matching a pattern. Reports results with failure analysis."
disable-model-invocation: true
user-invocable: true
argument-hint: "[all | file-path | pattern | --coverage]"
---

# Test Runner

Detect the test framework, run tests, and report results with failure analysis.

## Arguments
`$ARGUMENTS`

- No argument: Run tests related to recently changed files (use `git diff --name-only` to find them)
- `all`: Run the full test suite
- A file path: Run tests for that specific file
- A pattern (e.g., `auth`, `user`): Run tests matching that pattern
- `--coverage`: Run with coverage reporting if supported

## Step 1 — Detect Test Framework

Check for these in order:

| Check | Framework | Run Command |
|-------|-----------|-------------|
| `jest` in package.json | Jest | `npx jest` |
| `vitest` in package.json | Vitest | `npx vitest run` |
| `mocha` in package.json | Mocha | `npx mocha` |
| `pytest` importable | pytest | `pytest` |
| `unittest` in code | Python unittest | `python -m unittest` |
| `go test` files exist | Go testing | `go test ./...` |
| `cargo test` Cargo.toml | Rust | `cargo test` |
| `mix test` mix.exs | Elixir | `mix test` |
| `rspec` in Gemfile | RSpec | `bundle exec rspec` |
| `phpunit` in composer.json | PHPUnit | `vendor/bin/phpunit` |
| `test` script in package.json | npm test | `npm test` |
| `Makefile` with test target | Make | `make test` |

If multiple frameworks exist (e.g., monorepo), identify which one applies to the target.

## Step 2 — Determine What to Run

### No arguments (smart mode)
1. Run `git diff --name-only HEAD` to find changed files
2. For each changed file, find its corresponding test file:
   - `src/foo.js` → `tests/foo.test.js`, `__tests__/foo.test.js`, `src/foo.spec.js`
   - `app/models/user.py` → `tests/test_user.py`, `tests/models/test_user.py`
   - `pkg/auth/auth.go` → `pkg/auth/auth_test.go`
3. Run only those test files
4. If no test files found for changed files, tell the user and offer to run all

### Specific file
- If the argument IS a test file → run it directly
- If the argument is a source file → find and run its corresponding test file
- If no test file found → tell the user

### Pattern
- Pass the pattern to the framework's filter flag:
  - Jest: `--testPathPattern=pattern`
  - pytest: `-k pattern`
  - Go: `-run Pattern`
  - RSpec: `--tag pattern` or path filter

### `all`
- Run the full suite with the framework's default command

### `--coverage`
- Append coverage flag:
  - Jest: `--coverage`
  - pytest: `--cov`
  - Go: `-cover`
  - Vitest: `--coverage`

## Step 3 — Run and Report

Run the tests and present results:

```
## Test Results

**Framework:** Jest
**Command:** `npx jest --testPathPattern=auth`
**Status:** ✗ 2 failed, 14 passed, 16 total
**Duration:** 3.2s

### Failures

1. **auth.test.js:42** — `should reject expired tokens`
   - Expected: `401`
   - Received: `200`
   - Likely cause: [analysis of why it failed based on the test code and recent changes]

2. **auth.test.js:67** — `should refresh token before expiry`
   - Error: `TypeError: refreshToken is not a function`
   - Likely cause: [analysis]

### Suggestions
- [ ] Fix `refreshToken` export in `src/auth.js`
- [ ] Check token expiry logic in `src/middleware/auth.js:31`
```

## Step 4 — Failure Analysis

For each failure:
1. Read the failing test file at the reported line number
2. Read the source file being tested
3. Check if recent changes (git diff) could have caused the failure
4. Provide a specific diagnosis and suggested fix

## Rules
- **NEVER modify test files** unless the user explicitly asks to fix tests
- **NEVER skip or disable failing tests** to make them pass
- If tests require environment setup (database, API keys), tell the user what's needed
- If the test suite is very large (>5 min), warn the user before running `all`
- Read `.claude/languages.json` → `agent_language` for report language
