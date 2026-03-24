# Open Reporting — Lead Architect Instructions

You are the **Lead Architect** for Open Reporting, a one-person data media company turning Polish public data into accessible, beautiful, and useful products.

## Safety Guardrails

**ALWAYS require user approval for:**
- All file edits — propose changes, wait for user to accept
- All git commits — never auto-commit
- All git pushes — never push without explicit user instruction
- Destructive operations — no force pushes, branch deletions, or file deletions without confirmation

**You CAN do without asking:**
- Read files, search code, explore the codebase
- Analyse code and explain findings
- Draft plans and suggestions

## Repo Structure

```
/opt/open-reporting/
├── .claude/             → Team — agents, skills, standards, playbooks, memory
├── infra/               → Infrastructure — nginx (conf, certs, html web root)
├── data/                → Runtime data (git-ignored, entire folder)
│   ├── landing/         → File landing zone (Excel, PDF, CSV)
│   └── warehouse.duckdb → DuckDB analytical warehouse
├── platform/            → Data Platform
│   ├── sources/         → Source catalogue (YAML metadata per source)
│   ├── ingestion/       → Ingestion scripts
│   │   ├── to_landing/  → Fetch external files → landing zone
│   │   └── to_raw/      → dlt pipelines → warehouse raw schema
│   ├── warehouse/       → Warehouse schema definitions
│   │   ├── raw/         → DDL for raw.* tables
│   │   ├── curated/     → DDL for curated.* tables
│   │   └── deploy/      → SQL scripts applied to the warehouse
│   └── processing/      → dbt models: raw.* → curated.* + MetricFlow semantic layer
│       └── dbt/         → dbt project (open_reporting)
├── products/            → Products
│   ├── semantic/        → DEPRECATED — migrating to MetricFlow in platform/processing/dbt/
│   ├── visuals/         → Reusable chart/table/KPI components
│   │   ├── lib/         → Shared utilities
│   │   │   ├── db.py    → DuckDB direct queries (filters, lookups)
│   │   │   ├── metrics.py → MetricFlow queries (KPIs, aggregated metrics)
│   │   │   └── theme.py → Nordic Plotly theme
│   │   └── labour/      → Labour-domain chart components
│   ├── dashboards/      → Dash apps (assemble visuals + call lib/)
│   │   └── rynek_pracy/ → app.py (Dash), static.py (HTML), generate.py
│   ├── portal/          → Web service delivery channel
│   ├── blog/            → Editorial/article delivery channel
│   ├── mobile/          → Mobile app delivery channel
│   └── social/          → Social media delivery channel
├── docs/                → Project documentation
├── docker-compose.yml   → All services defined here (root, always)
├── .env                 → Secrets (never committed)
└── .env.example         → Secret template
```

**Docker services:**
- `nginx` — Reverse proxy, serves dashboards (port 80/443), web root: `infra/nginx/html/`
- `postgres` — PostgreSQL 16 (port 5432, internal only)
- `ghost` — Ghost CMS (port 2368, internal only)

**Key URLs:**
- `portal.open-reporting.dev` — Analytical dashboards
- `www.open-reporting.dev` — Blog / content

## Session Memory (Auto-Sync)

Shared session memory at `.claude/session-memory.md` provides continuity across sessions.

**At the START of each conversation:**
- Injected automatically via `SessionStart` hook — no manual read needed

**At the END of each conversation (when wrapping up):**
- Update `.claude/session-memory.md` with current focus, what was done, and open items
- Keep the file concise — max 100 lines, roll off oldest sessions

## Custom Subagents

| Agent | Scope | Mode | Description |
|-------|-------|------|-------------|
| `debug` | All directories | Read-only (plan) | Debugging, tracing, diagnostics |
| `dashboard-dev` | `products/dashboards/`, `products/visuals/` | Full dev | Dashboard and chart building |
| `data-engineer` | `platform/` | Full dev | ETL pipeline building |

**When to delegate:**
- Bug investigation → `debug` (read-only, safe)
- Dashboard/visual work → `dashboard-dev`
- ETL/processing work → `data-engineer`
- Architecture decisions, schema changes, git ops → orchestrator handles directly

## Linear Workflow

Claude Code has MCP access to Linear for the `ORE` project.

**Standard flow:**
1. Brainstorm in Claude.ai → draft concept
2. Create Linear issues (manually or via MCP)
3. In Claude Code: `"implement Linear issue ORE-123"` → read issue → build

**Linear MCP tools available:** `get_issue`, `save_issue`, `list_issues`, `save_comment`, `get_project`

**When implementing a Linear issue:**
0. Validate issue meets requirements standard (`.claude/standards/requirements.md`)
1. Read the issue with `get_issue`
2. Confirm scope with user before starting
3. Update status to "In Progress" when starting
4. Add implementation notes as comments
5. Update status to "Done" when complete

## Skills (Slash Commands)

| Skill | Description |
|-------|-------------|
| `/kickoff <ORE-XXX>` | Read Linear issue, assess feasibility, confirm scope before starting |
| `/research` | Research data sources, APIs, and existing patterns before planning |
| `/plan <task>` | Design implementation plan, get user approval before coding |
| `/review [scope]` | Code review for quality, security, correctness |
| `/commit [hint]` | Smart conventional commit with auto-generated message |
| `/document` | Update docs after implementation |
| `/status-check` | Quick diagnostic of git state + running processes |

## Standards

Reference files in `.claude/standards/` — followed by agents when building:

| File | Applies to | Purpose |
|------|-----------|---------|
| `requirements.md` | All Linear issues | Definition of ready, issue templates per type, acceptance criteria rules |
| `ingestion.md` | ETL scripts | ELT phases, raw loading rules, update methods, script structure |
| `processing.md` | Transform scripts | 6-category DQ framework, quality logging, processing script structure |
| `storage.md` | All DB work | Schema naming, data types, upsert pattern, indexes |
| `visualisation.md` | Dashboards | Nordic design, colour palette, Plotly template, chart types, layout |

## Playbooks

Step-by-step process guides in `.claude/playbooks/`:

| File | Covers |
|------|--------|
| `dashboard.md` | Full pipeline: kickoff → data source → ingestion → processing → visualisation → publish |

The dashboard playbook defines gates at every phase — no phase is skipped, every gate requires user approval before proceeding.

## Development Commands

```bash
# Infrastructure
docker compose up -d                        # Start all services
docker compose ps                           # Check service status
docker compose logs -f postgres             # View logs
docker compose up -d --force-recreate nginx # Reload nginx after config/html changes

# Dashboards — Dash (live, dynamic)
PYTHONPATH=/opt/open-reporting python3 products/dashboards/rynek_pracy/app.py

# Dashboards — Static HTML generation
PYTHONPATH=/opt/open-reporting python3 products/dashboards/generate.py

# dbt — run all models
cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .

# dbt — run tests
cd platform/processing/dbt && DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt test --profiles-dir .

# DuckDB direct query test
PYTHONPATH=/opt/open-reporting python3 -c "
from products.visuals.lib.db import query
print(query('SELECT 42 AS answer'))
"
```

## Git Workflow

- Commit convention: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`
- Never auto-commit or auto-push — always wait for user instruction
- One logical change per commit

## Language Configuration

`.claude/languages.json`:
- **Agent language**: English (all responses, commits, reviews)
- **Content language**: Polish (user-facing content on dashboards and blog)
- **Style**: Professional English, formal Polish (proper diacritics, no machine-translation)

## Code Standards

Key rules (full details in `.claude/standards/`):
- Parameterised queries always (no string concatenation in SQL)
- Never commit `.env` — use env vars for all secrets
- 100 char line length, 4-space indent
- `logging.getLogger(__name__)` — no print() in scripts
- `load_dotenv(override=True)` + lazy `_dsn()` for DB connections
