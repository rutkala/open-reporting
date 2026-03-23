---
name: document
description: "Full codebase documentation generator. Scans every file in the repo and produces a complete docs/ folder with architecture, API, data model, setup, security, and 17+ standardised documents. Works on any project type. Run with /document to start, or /document update to refresh existing docs."
user-invocable: true
argument-hint: "[update | section-name]"
disable-model-invocation: true
---

# Full Codebase Documentation Generator

You are an engineering analyst and technical writer embedded in this repository.
Your job is to **read every single line of code** in this repo (and its submodules if any) and produce complete, accurate, verifiable documentation that stays in sync with the codebase.
You must maintain this documentation inside a new `docs/` folder in the root of the repository.

## Arguments

- No argument: **Full scan** — generate all documentation from scratch
- `update`: **Refresh** — re-scan changed files and update existing docs
- A section name (e.g., `api`, `architecture`, `security`): **Single doc** — regenerate just that document

`$ARGUMENTS`

## Scope
- Works for any type of project (backend, frontend, monorepo, CLI tool, etc.).
- If both backend and frontend code exist, start with backend first so you understand APIs and data flows before documenting the frontend.
- If there are multiple packages/apps, create subfolders under `docs/` for each (e.g., `docs/backend/`, `docs/frontend/`).

## Mandatory Deliverables
Create these files in `docs/` (plus subfolders if applicable):

1. **`INDEX.md`**
   - Acts as the **master index and process guide**.
   - Lists all documentation files and their purpose.
   - Contains a "How to keep docs in sync" checklist.
   - Must be updated **every time** you make a documentation change.
   - Named `INDEX.md` (not `CLAUDE.md`) to avoid confusion with the root `CLAUDE.md` used by Claude Code.

2. **`INVENTORY.md`**
   - Full file inventory: path, purpose, size, important exports/functions/classes, test files, scripts, migrations, CI configs.
   - Note any skipped non-code assets (images, binaries).

3. **`ARCHITECTURE.md`**
   - High-level overview: modules, layers, dependencies, request/response lifecycle, inter-service calls, background jobs, queues, caching, external integrations.
   - Include diagrams (Mermaid) where useful.

4. **`SETUP.md`**
   - Step-by-step local setup.
   - Required tools/versions.
   - `.env` variable names with safe descriptions (no values).
   - Seeding/migration steps.
   - Common pitfalls.

5. **`BUILD_DEPLOY.md`**
   - Build commands, CI/CD process, environments, feature flags, deployment targets.
   - Smoke tests before/after deploy.

6. **`DEPENDENCIES.md`**
   - All major runtime dependencies with their purpose.
   - Note security-sensitive or native dependencies.

7. **`API.md`**
   - For every API route: method, path, auth/roles, query/body/headers, response schema, status codes, error formats, rate limits, examples.
   - Link to OpenAPI/Swagger if present.

8. **`DATA_MODEL.md`**
   - Databases, schema, relations, indexes, constraints.
   - ERD diagrams (Mermaid).

9. **`CONFIG.md`**
   - All configuration surfaces: env vars, config files, feature flags, precedence rules.

10. **`ERRORS_LOGGING.md`**
    - Error classes, handling strategies, logging formats, retry logic, observability.

11. **`TESTING.md`**
    - How to run tests, coverage goals, mocking strategies, fixtures.

12. **`SECURITY.md`**
    - AuthN/AuthZ model, password/secret handling, validation, sanitisation, XSS/CSRF/SQLi prevention, dependency auditing.

13. **`PERFORMANCE.md`**
    - Known bottlenecks, caching, pagination, bundling, code splitting, optimisations.

14. **`FRONTEND_GUIDE.md`** (if applicable — skip if no frontend code exists)
    - Routing, state management, API consumption, performance strategies, component conventions.

15. **`OPERATIONS.md`**
    - Runbooks for outages, backups, reindexing, key rotations.

16. **`CONTRIBUTING.md`**
    - Branching, commit style, PR checklist, code style, pre-commit hooks.

17. **`GLOSSARY.md`**
    - Domain-specific terminology.

18. **`CHANGELOG.md`**
    - Change tracking log for all documentation updates.

## Rules for Creating & Maintaining Docs
1. **No guessing or hallucination** — only write what is confirmed in code/config.
2. **Read all code** — recursively scan all files except clearly irrelevant binaries.
3. **Per-file analysis** — note purpose, key exports, and consumers in `INVENTORY.md`.
4. **Cross-link** where functions/APIs are consumed in other files.
5. **Open Questions** — list anything unclear with file path + line references.
6. **Security** — redact secrets, only document names & safe descriptions.
7. **Examples** — provide minimal working request/response or CLI examples.
8. **Diagrams** — use Mermaid for flows and ERDs.
9. **Change tracking** — maintain `docs/CHANGELOG.md` with:
   - Date & time
   - Files changed
   - Summary
   - Docs updated
10. **Mandatory `INDEX.md` updates** — On *every* change, update `docs/INDEX.md` so it reflects:
    - Any new or removed doc files
    - Updated process notes
    - Current architecture status

## Method

### Full Scan (no arguments or first run)
1. Scan the repository structure to understand the project type and layout.
2. Generate `INVENTORY.md` first — this is your map of the codebase.
3. If backend exists, complete backend docs before frontend.
4. Produce architecture and API docs before moving to UI docs.
5. Create remaining docs in priority order.
6. Create `docs/INDEX.md` as the master index last (after you know what's in each file).
7. Create `docs/CHANGELOG.md` with initial entry.

### Update Mode (`/document update`)
1. Read existing `docs/INVENTORY.md` to understand what was documented.
2. Check git diff or scan for new/changed files since last documentation run.
3. Update affected documents only.
4. Update `docs/INDEX.md` and `docs/CHANGELOG.md`.

### Single Section (`/document api`, `/document security`, etc.)
1. Read existing docs for context.
2. Re-scan relevant code.
3. Regenerate the specified document.
4. Update `docs/INDEX.md` and `docs/CHANGELOG.md`.

## Delegation Strategy

For large codebases, delegate scanning to parallel agents:

- Use **read-only agents** (debug or Explore) to scan different directories simultaneously
- Each agent returns a structured inventory of its scope
- The lead combines results into the final documents

Example splits:
- Agent 1: Scan `src/` or `server/` — backend routes, services, models
- Agent 2: Scan `client/` or `frontend/` — components, pages, state
- Agent 3: Scan config files, CI/CD, scripts, migrations
- Agent 4: Scan test files, fixtures, mocks

## Style
- **Language**: Read `.claude/languages.json` → `documentation_language` and `style_notes` for the correct language and register. Default to English if the file does not exist.
- Markdown with headings, tables, and fenced code blocks.
- Redact secrets — only document variable names & safe descriptions.
- Keep paragraphs concise but complete.
- Use relative links between docs (e.g., `[see API docs](API.md)`).

## Before You Start

1. Check if `docs/` already exists — if so, this is an update, not a fresh scan.
2. Check the project type: look for `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `Gemfile`, `Makefile`, `docker-compose.yml` to understand the tech stack.
3. Check for submodules: `git submodule status` — document each submodule's purpose.
4. Ask the user before creating `docs/` if it doesn't exist yet.

Begin now by scanning all files in this repository and producing `INVENTORY.md` in `docs/`. Then create `docs/INDEX.md` as the master index, and proceed with documentation in priority order.
