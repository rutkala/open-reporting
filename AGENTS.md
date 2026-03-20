# AGENTS.md — Open Reporting

Comprehensive guidelines for agentic coding agents working in this repository.

## Source of Truth

| What | Where |
| :--- | :--- |
| **Tasks, issues, roadmap** | GitHub Issues (github.com/rutkala/open-reporting/issues) |
| **Code** | GitHub (github.com/rutkala/open-reporting) |
| **This file** | Root directory AGENTS.md |

**Note:** Linear is no longer used. All project management is via GitHub Issues.

---

## Project Vision

**Open Reporting** is a one-person data media company turning Polish public data into accessible, beautiful, and useful products.

### Four Product Lines

1. **Analytical Portal** — Interactive dashboards organized by domain. portal.open-reporting.dev
2. **Content Portal / Blog** — Data-driven articles and reports. www.open-reporting.dev
3. **Mobile App** — Same data pipeline, mobile-first interface. Future phase.
4. **Social Media** — High-frequency short-form content across LinkedIn, X, Instagram.

### Audience
- General public — Polish citizens curious about their country
- Analysts & researchers — journalists, academics, think tanks
- Professionals — consultants, financial analysts, policy makers
- International — EU researchers, investors, expats studying Poland and CEE

### Language Strategy
Polish-first. English available for key content and the portal. Write once, publish in both.

### Team
- **Radek** — ideas, planning, product decisions, editorial direction, approves outputs
- **AI Agents** — development, engineering, analytics. Work only on assigned GitHub issues

---

## Domain Taxonomy (18 Categories)

This is the master list of content domains. Domains drive everything: portal sections, dashboard groupings, article categories, data pipelines, and GitHub issue labels.

| ID | Domain | Eurostat Theme | GUS Equivalent |
| :--- | :--- | :--- | :--- |
| 1 | **Public Finance** | Economy and finance | Finanse publiczne |
| 2 | **National Accounts & Macro** | Economy and finance | Rachunki narodowe |
| 3 | **Prices & Inflation** | Economy and finance | Ceny |
| 4 | **Financial Markets** | Economy and finance | NBP, GPW, KNF |
| 5 | **Population & Demographics** | Population and social | Ludność |
| 6 | **Labour Market** | Population and social | Rynek pracy |
| 7 | **Health** | Population and social | Ochrona zdrowia |
| 8 | **Education** | Population and social | Edukacja |
| 9 | **Income, Living & Social** | Population and social | Warunki życia |
| 10 | **Crime & Justice** | Population and social | Wymiar sprawiedliwości |
| 11 | **Culture, Tourism & Sport** | Population and social | Kultura, Turystyka |
| 12 | **Business & Industry** | Industry, trade, services | Podmioty gospodarcze |
| 13 | **Agriculture & Forestry** | Agriculture, fisheries | Rolnictwo, Leśnictwo |
| 14 | **International Trade** | International trade | Handel zagraniczny |
| 15 | **Transport** | Transport | Transport |
| 16 | **Environment & Climate** | Environment and energy | Środowisko |
| 17 | **Energy** | Environment and energy | Energia |
| 18 | **Science, Tech & Digital** | Science, technology | Nauka i technika |

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| Infrastructure | Hetzner VPS CX22, Docker Compose |
| Database | PostgreSQL 16 |
| Dashboards | Python + Plotly (static HTML) |
| Blog | Ghost CMS |
| Reverse proxy | Nginx + Let's Encrypt |
| Data ingestion | Python scripts (GUS BDL API, stooq.com) |
| Project management | GitHub Issues |
| Code hosting | GitHub |

### API Keys (in .env)
- `BDL_API_KEY`: GUS BDL API
- `DBW_API_KEY`: GUS DBW API  
- `POSTGRES_PASSWORD`: PostgreSQL
- `GHOST_KEY_ID`, `GHOST_KEY_SECRET`: Ghost Admin API
- `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, etc.: LLM providers

---

## Project Structure

```
/opt/open-reporting/
├── agent-team/          # AI agent orchestration (LangGraph, litellm)
├── charts/              # Plotly dashboard generation
│   ├── dashboards/      # Individual dashboard modules
│   └── lib/             # Shared utilities (db.py, theme.py)
├── content/             # Ghost CMS publishing scripts
├── docs/                # Reference documentation
├── ingestion/           # Data ingestion scripts
├── nginx/               # Nginx config, SSL certificates
├── processing/          # Data processing scripts
└── docker-compose.yml   # Service orchestration
```

---

## Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Start services
docker compose up -d

# Verify services
docker compose ps
```

---

## Running Scripts

### Chart Generation
```bash
# All dashboards
POSTGRES_PASSWORD=xxx python3 charts/generate.py

# Single dashboard
POSTGRES_PASSWORD=xxx python3 charts/dashboards/state_budget.py
POSTGRES_PASSWORD=xxx python3 charts/dashboards/voivodship.py
POSTGRES_PASSWORD=xxx python3 charts/dashboards/gpw_market.py
```

### Data Ingestion
```bash
# GPW stock data
POSTGRES_PASSWORD=xxx python3 ingestion/gpw_ingest.py           # incremental
POSTGRES_PASSWORD=xxx python3 ingestion/gpw_ingest.py --backfill  # full history

# BDL budget data
BDL_API_KEY=xxx POSTGRES_PASSWORD=xxx python3 ingestion/budget_ingest.py

# National budget
POSTGRES_PASSWORD=xxx python3 processing/national_budget.py
```

### Agent Team (Experimental)
```bash
source agent-team/venv/bin/activate
python3 agent-team/test_foundation.py        # Test connectivity
python3 agent-team/agent_orchestrator.py    # Run orchestrator
```

---

## Testing

Manual testing only. No formal test framework.

```bash
# Test database
python3 -c "from charts.lib.db import query; print(query('SELECT 1'))"

# Test API
python3 -c "import requests; print(requests.get('https://bdl.stat.gov.pl/api/v1').status_code)"
```

---

## Code Style Guidelines

### General Rules
- Use `#!/usr/bin/env python3` shebang for executable scripts
- Add module-level docstrings with purpose and usage
- Use `logging` module with `logging.getLogger(__name__)` instead of print
- Use f-strings for string formatting
- Call `load_dotenv()` at module level

### Imports (order)
1. Standard library (os, sys, time, logging)
2. Third-party (psycopg2, pandas, requests)
3. Local imports (use relative paths)

### Type Hints
```python
def fetch_data(ticker: str, limit: int = 100) -> list[dict]:
    ...

from typing import Optional, List, Dict
def process(rows: List[Dict], threshold: Optional[float] = None) -> pd.DataFrame:
    ...
```

### Naming Conventions
| Type | Convention | Example |
| :--- | :--- | :--- |
| Modules | lowercase_with_underscores | `budget_ingest.py` |
| Classes | PascalCase | `AgentState` |
| Functions | lowercase_with_underscores | `fetch_data` |
| Constants | UPPERCASE_WITH_UNDERSCORES | `API_BASE` |
| Private | leading_underscore | `_config` |

### Database Operations
```python
# Always parameterized (prevent SQL injection)
cur.execute("INSERT INTO t (a, b) VALUES (%s, %s)", (val1, val2))

# Bulk inserts
execute_values(cur, "INSERT INTO t (a, b) VALUES %s", records)

# Upserts
cur.execute("""
    INSERT INTO t (id, name) VALUES (%s, %s)
    ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
""", (id, name))
```

### Error Handling
```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
except requests.Timeout:
    log.error(f"Request timed out: {url}")
    raise
except requests.HTTPError as e:
    log.error(f"HTTP error {e.response.status_code}: {url}")
    raise
except Exception:
    log.exception("Unexpected error")
    raise
```

### Logging Levels
- `log.debug()` — Detailed debugging info
- `log.info()` — Normal operation
- `log.warning()` — Unexpected but recoverable
- `log.error()` — Serious problem
- `log.exception()` — Error with traceback

---

## Security

- **Never commit .env files** — contain API keys and credentials
- Use environment variables for all sensitive config
- Never log sensitive data (API keys, passwords)
- Always use parameterized database queries
- Validate and sanitize external input

---

## Docker Commands

```bash
docker compose up -d          # Start all services
docker compose logs -f       # View logs
docker compose restart nginx # Restart service
docker compose down          # Stop services
docker compose up -d --build # Rebuild and restart
```

---

## VPS Access

- **IP:** 91.98.118.153
- **Specs:** Hetzner CX22, 4GB RAM, Ubuntu
- **Repo path:** `/opt/open-reporting`

---

## Agent Infrastructure (Experimental)

The `agent-team/` directory contains a LangGraph-based multi-agent system:

### Architecture
- **Orchestrator** — High-level planning, task routing
- **Data Engineer** — Data pipelines, ETL, validation
- **Analytics Lead** — Metrics, KPIs, transformations
- **Presenter** — UI, content, portal integration

### Agent Responsibilities
- **Orchestrator**: Manages the DDF flow and routes tasks based on current stage
- **Data Engineer**: Owns Stages 1 (Source Research) & 3 (Ingestion Implementation)
- **Analytics Lead**: Owns Stage 2 (Metric Definition)
- **Presenter**: Owns Stage 4 (UI/Presentation)

### Model Fallbacks
All agents use a fallback hierarchy: Gemini → Groq → DeepSeek

### Current Status
This is an experimental feature. Not validated in production. Use with caution.

---

## Dashboard Development Framework

When developing a new dashboard, follow this stage-gate process:

1. **Source Research** — Identify data sources, evaluate API/file availability
2. **Metric Definition** — Define KPIs, business logic, transformations
3. **Ingestion Implementation** — Build ETL scripts with validation
4. **UI/Presentation** — Design layout, build charts, integrate content

Each stage requires approval before proceeding to the next.

---

## Working with AI Agents

When you start a session:
1. Read AGENTS.md for project guidelines
2. Check GitHub Issues for the task queue
3. Assign the issue to yourself and move to "In Progress"
4. Work on the task
5. Commit changes and update the issue when done

Use the `/init` command in OpenCode to initialize the session with proper context.
