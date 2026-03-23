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

## System Architecture

```
/opt/open-reporting/
├── charts/              → Plotly dashboards (static HTML output)
│   ├── dashboards/      → Dashboard modules (one file per dashboard)
│   └── lib/             → Shared utilities: db.py, theme.py
├── ingestion/           → ETL scripts (fetch → raw schema)
├── processing/          → Data transformations (raw → public schema)
├── nginx/               → Nginx config + SSL certs + static HTML output
│   ├── conf.d/          → Virtual host configs
│   └── html/            → Served files (dashboards go here)
├── content/             → Ghost CMS data volume
├── .claude/             → Claude Code config (agents, hooks, skills)
├── docs/                → Project documentation
└── docker-compose.yml   → All services defined here
```

**Docker services:**
- `nginx` — Reverse proxy, serves dashboards (port 80/443)
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
| `dashboard-dev` | `charts/` | Full dev | Plotly dashboard building (follows DDF) |
| `data-engineer` | `ingestion/`, `processing/` | Full dev | ETL pipeline building |

**When to delegate:**
- Bug investigation → `debug` (read-only, safe)
- Dashboard work entirely in `charts/` → `dashboard-dev`
- ETL/ingestion work → `data-engineer`
- Architecture decisions, schema changes, git ops → orchestrator handles directly

## Linear Workflow

Claude Code has MCP access to Linear for the `ORE` project.

**Standard flow:**
1. Brainstorm in Claude.ai → draft concept
2. Create Linear issues (manually or via MCP)
3. In Claude Code: `"implement Linear issue ORE-123"` → read issue → build

**Linear MCP tools available:** `get_issue`, `save_issue`, `list_issues`, `save_comment`, `get_project`

**When implementing a Linear issue:**
1. Read the issue with `get_issue`
2. Confirm scope with user before starting
3. Update status to "In Progress" when starting
4. Add implementation notes as comments
5. Update status to "Done" when complete

## Skills (Slash Commands)

| Skill | Description |
|-------|-------------|
| `/commit [hint]` | Smart conventional commit with auto-generated message |
| `/review [scope]` | Code review current changes for quality, security, correctness |
| `/plan <task>` | Design implementation plan before coding, get approval first |
| `/status-check` | Quick diagnostic of git state + running processes |

## Development Commands

```bash
# Infrastructure
docker compose up -d              # Start all services
docker compose ps                 # Check service status
docker compose logs -f postgres   # View logs

# Dashboards
POSTGRES_PASSWORD=xxx python3 charts/generate.py          # Generate all dashboards

# Ingestion
POSTGRES_PASSWORD=xxx python3 ingestion/gpw_ingest.py --backfill
BDL_API_KEY=xxx POSTGRES_PASSWORD=xxx python3 ingestion/budget_ingest.py

# DB quick test
python3 -c "from charts.lib.db import query; print(query('SELECT 1'))"
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

See `AGENTS.md` for full Python conventions, SQL patterns, and security rules.

Key rules:
- Parameterised queries always (no string concatenation in SQL)
- Never commit `.env` — use env vars for all secrets
- 100 char line length, 4-space indent
- `logging.getLogger(__name__)` — no print() in scripts
