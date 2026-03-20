# AGENTS.md — Open Reporting

## Overview

This file contains rules and guidelines for AI coding agents working in this repository. Follow these instructions precisely.

---

## Source of Truth

| What | Where |
| :--- | :--- |
| Tasks, issues, roadmap | GitHub Issues |
| Code | GitHub |
| This file | Root: AGENTS.md |

**Linear is no longer used.**

---

## Project Vision

**Open Reporting** is a one-person data media company turning Polish public data into accessible, beautiful, and useful products.

### Four Product Lines

1. **Analytical Portal** — Interactive dashboards by domain (portal.open-reporting.dev)
2. **Content Portal / Blog** — Data-driven articles (www.open-reporting.dev)
3. **Mobile App** — Future phase
4. **Social Media** — Short-form content (LinkedIn, X, Instagram)

### Audience
- Polish citizens curious about their country
- Analysts, researchers, journalists, academics
- Professionals: consultants, financial analysts, policy makers
- International: EU researchers, investors, expats

### Language
Polish-first. English available. Write once, publish in both.

---

## Domain Taxonomy (18 Categories)

All dashboards, data ingestion, and articles are organized by these domains:

| ID | Domain | Data Sources |
| :--- | :--- | :--- |
| 1 | Public Finance | GUS BDL, MF, NIK |
| 2 | National Accounts & Macro | GUS BDL, Eurostat |
| 3 | Prices & Inflation | GUS BDL, NBP |
| 4 | Financial Markets | stooq.com, NBP, KNF |
| 5 | Population & Demographics | GUS BDL, GUS DBW |
| 6 | Labour Market | GUS BDL, GUS DBW |
| 7 | Health | GUS BDL, NFZ, MZ |
| 8 | Education | GUS BDL, MEN |
| 9 | Income, Living & Social | GUS BDL, GUS DBW, ZUS |
| 10 | Crime & Justice | GUS BDL, MS |
| 11 | Culture, Tourism & Sport | GUS BDL, MKiDN |
| 12 | Business & Industry | GUS BDL, GUS DBW |
| 13 | Agriculture & Forestry | GUS BDL, MRiRW |
| 14 | International Trade | GUS BDL, NBP, Eurostat |
| 15 | Transport | GUS BDL, UTK, ULC |
| 16 | Environment & Climate | GUS BDL, GIOŚ, Eurostat |
| 17 | Energy | GUS BDL, URE, Eurostat |
| 18 | Science, Tech & Digital | GUS BDL, GUS DBW, Eurostat |

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| Infrastructure | Hetzner VPS CX22, Docker Compose |
| Database | PostgreSQL 16 |
| Dashboards | Python + Plotly (static HTML) |
| Blog | Ghost CMS |
| Reverse proxy | Nginx + Let's Encrypt |
| Data ingestion | Python scripts |
| Project management | GitHub Issues |
| Code hosting | GitHub |

### Key Libraries
- psycopg2, pandas (database)
- plotly (charts)
- requests (API calls)
- langgraph, litellm (agents - experimental)

### API Keys (in .env)
- BDL_API_KEY: GUS BDL API
- DBW_API_KEY: GUS DBW API
- POSTGRES_PASSWORD: PostgreSQL
- GHOST_KEY_ID, GHOST_KEY_SECRET: Ghost CMS
- LLM keys: GEMINI_API_KEY, etc.

---

## Project Structure

```
/opt/open-reporting/
├── agent-team/          # AI agent infrastructure (experimental)
├── charts/             # Plotly dashboards
│   ├── dashboards/      # Dashboard modules
│   └── lib/            # Shared utilities (db.py, theme.py)
├── content/            # Ghost CMS publishing
├── docs/               # Reference docs
├── ingestion/           # Data ingestion scripts
├── nginx/              # Nginx, SSL
├── processing/          # Data processing
├── .opencode/          # Agent configurations
│   ├── agents/         # Custom agents
│   ├── commands/       # Slash commands
│   └── templates/      # File templates
└── docker-compose.yml
```

---

## Dashboard Development Framework (DDF)

### Mandatory Stages

Every dashboard follows this sequence. **Do not skip stages.**

#### Stage 1: Source Research
- Identify data sources (GUS BDL, Eurostat, etc.)
- Evaluate API availability, rate limits, authentication
- Document data structure, variables, time range
- **Gate: Present findings, get approval**

#### Stage 2: Metric Definition
- Define KPIs based on domain taxonomy
- Specify calculations, aggregations, comparisons
- Identify data transformations needed
- **Gate: Review metrics, get approval**

#### Stage 3: Ingestion Implementation
- Build ETL script following code standards
- Create database schema (raw schema for source data)
- Implement error handling, retries, logging
- Validate data quality
- **Gate: Test ingestion, get approval**

#### Stage 4: UI/Presentation
- Design dashboard layout
- Build charts following theme standards
- Add interactivity (filters, selectors)
- Write source attribution
- **Gate: Review dashboard, get approval**

### Agent Responsibilities

| Agent | Owns Stages |
|-------|-------------|
| **Data Engineer** | Stage 1, Stage 3 |
| **Analytics Lead** | Stage 2 |
| **Presenter** | Stage 4 |

---

## Agent Workflow

### How to Work with Agents

1. **Create GitHub Issue** for the dashboard domain
2. **Assign issue** to yourself (agent)
3. **Use DDF stages** - complete each stage in order
4. **Request approval** at each gate
5. **Update issue status** when complete

### Stage Workflow Example

```
GitHub Issue: OPE-XX: Dashboard: Energy

Agent: "Stage 1 complete. Sources identified:
- GUS BDL: variable 6450 (energy production)
- URE: electricity prices API
Shall I proceed to Stage 2?"

Radek: "Yes, approved. Define metrics."

Agent: "Stage 2 complete. KPIs defined:
- Primary: Energy mix (coal %, renewable %)
- Secondary: Production vs consumption
Proceed to Stage 3?"

Radek: "Approved. Build ingestion."

Agent: *builds ingestion script*

Agent: "Stage 3 complete. Script ready. 
Tested with 10 years of data. Proceed to Stage 4?"

Radek: "Approved. Build dashboard."

Agent: *builds dashboard*

Agent: "Dashboard complete. Here is the final result.
Please review and close the issue if satisfactory."
```

---

## Code Standards

### General
- Use `#!/usr/bin/env python3` shebang
- Module docstrings with purpose and usage
- `logging.getLogger(__name__)` for logging
- f-strings for formatting
- `load_dotenv()` at module level

### Imports
```
1. Standard library (os, sys, time, logging)
2. Third-party (psycopg2, pandas, requests)
3. Local imports
```

### Naming
| Type | Convention | Example |
| :--- | :--- | :--- |
| Modules | snake_case | `budget_ingest.py` |
| Classes | PascalCase | `AgentState` |
| Functions | snake_case | `fetch_data` |
| Constants | UPPER_SNAKE | `API_BASE` |
| Private | _leading | `_config` |

### Database
- **Always parameterized** - prevent SQL injection
- `execute_values()` for bulk inserts
- `ON CONFLICT DO UPDATE` for upserts

### Error Handling
```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
except requests.Timeout:
    log.error(f"Timeout: {url}")
    raise
except requests.HTTPError as e:
    log.error(f"HTTP {e.response.status_code}: {url}")
    raise
```

### Logging Levels
- `debug()` - Detailed debugging
- `info()` - Normal operation
- `warning()` - Unexpected but recoverable
- `error()` - Serious problem
- `exception()` - Error with traceback

---

## Dashboard Code Standards

### Theme Usage
```python
from charts.lib.theme import C, apply, page, kpi_card

# Colors from theme
C["blue"]   # Primary data color
C["red"]    # Negative/spending
C["green"]  # Positive/revenue
C["bg"]     # Background
C["text"]   # Text color
```

### Chart Pattern
```python
def build():
    # 1. Query data
    df = query("SELECT ...")
    
    # 2. Create figure
    fig = go.Figure()
    fig.add_trace(go.Bar(...))
    
    # 3. Apply theme
    apply(fig, title, subtitle, height=400)
    
    # 4. Save HTML
    html = page(title, body=pio.to_html(fig))
    with open(out_path, "w") as f:
        f.write(html)
```

---

## Security Rules

1. **Never commit .env** - contains API keys
2. **Use env vars** for all secrets
3. **Never log secrets** - API keys, passwords
4. **Parameterized queries** - prevent injection
5. **Validate input** - sanitize external data

---

## Testing

### Manual Testing
```bash
# Database
python3 -c "from charts.lib.db import query; print(query('SELECT 1'))"

# API
python3 -c "import requests; print(requests.get('https://bdl.stat.gov.pl/api/v1').status_code)"
```

### Ingestion Validation
- Check row counts
- Verify date ranges
- Compare totals against source
- Log all validation results

---

## Docker Commands

```bash
docker compose up -d          # Start
docker compose logs -f         # View logs
docker compose restart nginx   # Restart
docker compose down           # Stop
docker compose up -d --build  # Rebuild
```

---

## Useful Commands

```bash
# Start OpenCode in project
cd /opt/open-reporting && opencode

# Initialize (create/update AGENTS.md)
/init

# Generate dashboards
POSTGRES_PASSWORD=xxx python3 charts/generate.py

# Ingest GPW data
POSTGRES_PASSWORD=xxx python3 ingestion/gpw_ingest.py --backfill

# Ingest BDL data
BDL_API_KEY=xxx POSTGRES_PASSWORD=xxx python3 ingestion/budget_ingest.py
```

---

## Agent Configuration

Custom agents are configured in `.opencode/agents/`:
- `dashboard-dev.md` - Builds dashboards following DDF
- `data-engineer.md` - Builds ingestion pipelines
- `reviewer.md` - Reviews code quality

Custom commands are in `.opencode/commands/`:
- `/dash <domain>` - Start dashboard development
- `/ingest <source>` - Start data ingestion
- `/review` - Code review

---

## VPS Access

- **IP:** 91.98.118.153
- **Specs:** Hetzner CX22, 4GB RAM, Ubuntu
- **Repo:** `/opt/open-reporting`

---

## Starting a New Dashboard

1. Create GitHub issue: "Dashboard: [Domain Name]"
2. Use `/dash energy` to invoke dashboard-dev agent
3. Follow DDF stages with approval gates
4. Commit code after each stage
5. Close issue when complete

---

## Starting Data Ingestion

1. Create GitHub issue: "Ingest: [Data Source]"
2. Use `/ingest gusz_bdl` to invoke data-engineer agent
3. Follow ingestion patterns in `ingestion/`
4. Test with small dataset first
5. Document variables and schema

---

## Remember

- **Approval gates** - Do not skip stages without approval
- **Budget aware** - Use free-tier models (Gemini, Groq)
- **Document everything** - Comment code, update README
- **Test thoroughly** - Manual validation before claiming done
- **Git workflow** - Commit after each stage, push regularly
