# Open Reporting — Shared Agent Instructions

One-person data media company turning Polish public data into accessible, beautiful, and useful products.

**Root:** `/opt/open-reporting` | **Warehouse:** `data/warehouse.duckdb` | **Live:** `portal.open-reporting.dev`

## Token Efficiency Rules

These rules apply every session, every task:
- Never read a file unless specifically needed for the current task
- Prefer `grep`/`glob` over reading full files — search before reading
- When reading files, use line ranges; never load an entire large file
- Never spawn subagents for tasks that can be done inline
- Prefer one targeted bash command over multiple broad searches
- After heavy tool use (large file reads, multi-step searches), suggest `/clear` before continuing
- One session per task — do not accumulate unrelated context across tasks
- Avoid re-reading files already in context

## Key Paths

Two-plane architecture — see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full contract.

```
products/           → declarative work (you + cheap AI edit here)
  ingestion/        → Per-source Python fetchers + dlt pipelines
  warehouse/        → dbt project — staging/intermediate/marts/dim/semantic
  database/         → PostgreSQL operational schema + loader
  dashboards/       → dbr YAML dashboards (one folder per dashboard)
  blog/ social/ research/ mobile/ domain-briefs/
docs/               → ARCHITECTURE.md (target), refactor-plan.md, DATA_MODEL.md, …
  archive/          → Superseded docs
team/               → knowledge base, standards, playbooks, agent memory
  knowledge-base/   → KB modules — read on demand, see INDEX.md
  standards/        → build + evaluation standards — see INDEX.md

packages/           → engine code (Opus only)
  dbr/              → Dashboard framework
  screenshot/       → Screenshot CLI
infra/              → nginx + systemd + certs
.claude/            → Claude Code config

data/               → git-ignored runtime data
  warehouse.duckdb  → DuckDB analytical warehouse
```

## Language Rules

- **Code, config, DB, filenames, logs:** English always, no exceptions
- **User-facing content** (chart labels, axis labels, portal copy, tooltips): Polish
- **Agent responses, commits, reviews:** English
- Formal Polish — proper diacritics, no machine-translation

## Development Commands

```bash
# Services
docker compose up -d                         # start all
docker compose ps                            # status
docker compose up -d --force-recreate nginx  # reload nginx

# Dashboards
PYTHONPATH=/opt/open-reporting python3 products/dashboards/labour/app.py    # port 8050
PYTHONPATH=/opt/open-reporting python3 products/dashboards/explorer/app.py  # port 8051

# dbt
cd products/warehouse && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .
cd products/warehouse && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt test --profiles-dir .
```

## Workflow Overview

```
Ideas → /capture-idea → /review-ideas → /kickoff OR-XXX → PR → Done
```

- Normal chat = explore, advise, explain — no code, no commits
- `/kickoff` is the only gate into implementation
- Any idea from chat → `/capture-idea` first, never implement directly

## Code Standards

- Parameterised queries always — no string concatenation in SQL
- Never commit `.env`
- 100 char line length, 4-space indent
- `logging.getLogger(__name__)` — no `print()` in scripts
- `load_dotenv(override=True)` + lazy `_dsn()` for DB connections
