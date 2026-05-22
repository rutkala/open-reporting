# Contributing & Project Management

This document defines how all post-MVP work is planned, tracked, and delivered.

---

## Guiding Rule

**No idea goes directly to code.**

Every piece of work — feature, bug fix, data pipeline, article, infrastructure change — must start as a documented issue in Linear before any implementation begins.

---

## Workflow Overview

Four stages, four skills:

```
Stage 1 — Collect          Stage 2 — Convert          Stage 3 — Prioritise       Stage 4 — Implement
───────────────────        ───────────────────        ────────────────────        ───────────────────
Chat idea                  /review-ideas              /sprint                     /kickoff
  → /capture-idea            Review ideas board         Review backlog              Plan → approve
                             Accept → issue             Pick sprint issues          Branch → code
Direct Linear entry          Reject → archive           Move to Todo                /review → PR
  (Backlog + Idea label)     Defer → leave                                          Merge → Done
```

---

## Issue Lifecycle

### 1. Create the issue
Create in Linear (`OR` project). Issue must meet the **Definition of Ready** defined in `team/standards/build/requirements.md` before work starts.

Issue types and required fields are defined in `team/standards/build/requirements.md`:
- **Feature** — new product capability
- **Bug** — something broken that worked before
- **Data** — new ingestion pipeline or data transformation
- **Content** — article, social post, copy
- **Infra** — infrastructure, configuration, deployment

### 2. Kickoff
In Claude Code: `/kickoff OR-XXX`

Claude reads the issue, checks requirements completeness, assesses feasibility, identifies blockers, and presents a plan for user confirmation. No work starts until the user approves.

Claude updates the Linear issue status to **"In Progress"**.

### 3. Feature branch
Create a branch from `main` before writing any code:

```bash
git checkout main
git pull origin main
git checkout -b feat/OR-123-short-description
```

Branch naming convention:
- `feat/OR-XXX-description` — new feature
- `fix/OR-XXX-description` — bug fix
- `data/OR-XXX-description` — data pipeline
- `infra/OR-XXX-description` — infrastructure
- `docs/OR-XXX-description` — documentation only

### 4. Implementation
- Commits on the feature branch reference the issue: `feat: OR-123 short description`
- Follow all standards in `team/standards/`
- Never commit `.env` or secrets
- Keep commits logical — one change per commit

### 5. Review
Before opening a PR, run `/review` in Claude Code.

Claude produces a structured review covering:
- Standards compliance (ingestion, processing, storage, visualisation — whichever apply)
- Security (no hardcoded secrets, no injection risks)
- Code quality (line length, naming, logging)
- Acceptance criteria met (checked against Linear issue)

Fix any issues raised before opening the PR.

### 6. Pull Request
Push the branch and open a PR on GitHub:

```bash
git push -u origin feat/OR-123-short-description
gh pr create --title "OR-123: Short description" --body "..."
```

PR description must include:
- Link to Linear issue (`OR-XXX`)
- Summary of changes
- How to test / verify
- `/review` output (paste the Claude review)
- Checklist of acceptance criteria from the Linear issue

### 7. Approval
The PR requires at least one approval before merging.

The reviewer checks:
- [ ] `/review` output is included and issues are addressed
- [ ] Standards compliance (see PR Review Checklist below)
- [ ] Acceptance criteria from the Linear issue are met
- [ ] No secrets or `.env` changes committed
- [ ] `RELEASE_NOTES.md` updated under "Unreleased"

### 8. Merge
Merge to `main` (squash or merge commit — keep history readable).

After merge:
- Linear issue → **Done**
- Delete the feature branch
- Update any affected documentation (see step 9)

### 9. Documentation update
After every merge, review and update any docs affected by the change:

| Change type | Docs to update |
|-------------|---------------|
| Any change | `docs/RELEASE_NOTES.md` — move from "Unreleased" or add entry |
| New data source | `docs/DATA_SOURCES.md` |
| New domain / indicator | `docs/DOMAINS.md` |
| Infrastructure change | `docs/ARCHITECTURE.md` |
| New product / URL | `README.md` + `docs/ARCHITECTURE.md` |
| New playbook or standard | `README.md` doc index |

If the change invalidates something in `.claude/session-memory.md`, update that too.

### 10. Lessons learned
After any non-trivial issue — especially where something went wrong, took longer than expected, or revealed a process gap — add an entry to `.claude/lessons-learned.md`.

See that file for format. This is how the process improves over time.

---

## PR Review Checklist

Paste this into every PR and check off before requesting review:

```markdown
## Standards Compliance

### All PRs
- [ ] No secrets committed (.env, API keys, passwords)
- [ ] English-only backend (names, variables, logs, SQL columns)
- [ ] Polish user-facing strings (labels, titles, tooltips)
- [ ] 100 char line length, 4-space indent
- [ ] logging.getLogger(__name__) — no print() in scripts

### Ingestion PRs (products/ingestion/)
- [ ] Parameterised queries — no string concatenation in SQL
- [ ] load_dotenv(override=True) + lazy _dsn() pattern
- [ ] Idempotent — safe to re-run without duplicating data
- [ ] Landing zone used for raw files before warehouse load
- [ ] Source documented in catalogue (catalogue.domain_detail_sources)

### Processing PRs (products/warehouse/)
- [ ] dbt model follows curated schema naming
- [ ] Data quality checks included (DQ framework — 6 categories)
- [ ] Seeds use --full-refresh when schema changes

### Visualisation PRs (products/)
- [ ] Nordic theme imported from complex_dashboard.assets.theme
- [ ] No hardcoded colours
- [ ] All chart labels in Polish
- [ ] Source attribution visible
- [ ] Mobile-responsive layout

### Acceptance criteria
- [ ] All acceptance criteria from the Linear issue are met
- [ ] RELEASE_NOTES.md updated under "Unreleased"
```

---

## Sprint Cadence

- **2-week cycles** in Linear
- Start of cycle: review backlog, assign issues to cycle
- End of cycle: review what shipped, update ROADMAP.md
- No ceremony required for a one-person team — keep it lightweight

---

## Release Process

When a meaningful set of features ships:

1. Move items from "Unreleased" to a new version section in `docs/RELEASE_NOTES.md`
2. Tag the commit: `git tag v0.2.0 -m "v0.2.0 — Phase 1 content and data"`
3. Push the tag: `git push origin v0.2.0`
4. Update `docs/ROADMAP.md` — check off completed items

Version format: `MAJOR.MINOR.PATCH`
- MAJOR — breaking change or major product shift
- MINOR — new feature or domain added
- PATCH — bug fix or small improvement

---

## Claude Code's Role

Claude Code (this tool) acts as the implementation partner:

- Reads Linear issues via MCP (`/kickoff OR-XXX`)
- Creates feature branches, implements, commits
- Runs `/review` before opening PRs
- Updates Linear status and adds implementation notes as comments
- Never pushes directly to `main`
- Never auto-commits or auto-pushes without user instruction
- Follows all standards in `team/standards/`
