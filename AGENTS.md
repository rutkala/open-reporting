# AGENTS.md — Open Reporting

## Overview

This file contains rules and guidelines for AI coding agents. Follow these instructions precisely.

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `docker compose up -d` | Start all services |
| `docker compose logs -f` | View logs |
| `python3 -c "from charts.lib.db import query; print(query('SELECT 1'))"` | Test DB connection |
| `POSTGRES_PASSWORD=xxx python3 charts/generate.py` | Generate dashboards |

---

## Project Vision

**Open Reporting** is a one-person data media company turning Polish public data into accessible, beautiful, and useful products.

### Four Product Lines
1. **Analytical Portal** — Interactive dashboards (portal.open-reporting.dev)
2. **Content Portal / Blog** — Data-driven articles (www.open-reporting.dev)
3. **Mobile App** — Future phase
4. **Social Media** — Short-form content (LinkedIn, X, Instagram)

### Tech Stack
- Infrastructure: Docker Compose on Hetzner VPS
- Database: PostgreSQL 16
- Dashboards: Python + Plotly (static HTML)
- Blog: Ghost CMS
- Key Libraries: psycopg2, pandas, requests, plotly

---

## Code Standards

### General
- Use `#!/usr/bin/env python3` shebang
- Module docstrings with purpose and usage
- `logging.getLogger(__name__)` for logging
- f-strings for formatting
- `load_dotenv()` at module level

### Imports (ordered)
```
1. Standard library (os, sys, time, logging, typing)
2. Third-party (psycopg2, pandas, requests, plotly)
3. Local imports (charts.lib, ingestion)
```

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Modules | snake_case | `budget_ingest.py` |
| Classes | PascalCase | `AgentState` |
| Functions | snake_case | `fetch_data` |
| Constants | UPPER_SNAKE | `API_BASE` |
| Private | _leading | `_config` |
| Type vars | PascalCase | `T = TypeVar('T')` |

### Formatting
- Line length: 100 characters max
- Indentation: 4 spaces (no tabs)
- Trailing commas in multi-line collections
- Blank lines: 2 between top-level definitions, 1 inside functions

### Type Hints
```python
from typing import Optional, List, Dict, Any

def process_data(
    items: List[Dict[str, Any]],
    config: Optional[Dict[str, str]] = None
) -> tuple[int, List[str]]:
    ...
```

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
except Exception as e:
    log.exception("Unexpected error")
    raise
```

### Logging Levels
- `debug()` — Detailed debugging
- `info()` — Normal operation milestones
- `warning()` — Unexpected but recoverable
- `error()` — Serious problem
- `exception()` — Error with traceback

### Database
- **Always parameterized** — prevent SQL injection
- `execute_values()` for bulk inserts
- `ON CONFLICT DO UPDATE` for upserts
- Connection cleanup with `finally` block

```python
conn = None
try:
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute("SELECT %s, %s", (value1, value2))
    return cur.fetchall()
finally:
    if conn:
        conn.close()
```

---

## Security Rules

1. **Never commit .env** — contains API keys
2. **Use env vars** for all secrets
3. **Never log secrets** — API keys, passwords
4. **Parameterized queries** — no string concatenation in SQL
5. **Validate input** — sanitize external data

---

## Testing

### Manual Testing
```bash
# Database connection
python3 -c "from charts.lib.db import query; print(query('SELECT 1'))"

# API availability
python3 -c "import requests; print(requests.get('https://bdl.stat.gov.pl/api/v1').status_code)"

# Single module (if pytest exists)
pytest tests/test_budget.py -v

# Single test
pytest tests/test_budget.py::test_fetch_data -v
```

### Ingestion Validation
- Check row counts before/after
- Verify date ranges
- Compare totals against source
- Log all validation results

---

## Dashboard Development Framework (DDF)

Every dashboard follows these stages. **Do not skip stages.**

### Stage 1: Source Research
- Identify data sources (GUS BDL, Eurostat, etc.)
- Evaluate API availability, rate limits, authentication
- Document data structure, variables, time range
- **Gate: Present findings, get approval**

### Stage 2: Metric Definition
- Define KPIs based on domain taxonomy
- Specify calculations, aggregations, comparisons
- Identify data transformations needed
- **Gate: Review metrics, get approval**

### Stage 3: Ingestion Implementation
- Build ETL script following code standards
- Create database schema (raw schema for source data)
- Implement error handling, retries, logging
- Validate data quality
- **Gate: Test ingestion, get approval**

### Stage 4: UI/Presentation
- Design dashboard layout
- Build charts following theme standards
- Add interactivity (filters, selectors)
- Write source attribution
- **Gate: Review dashboard, get approval**

### Dashboard Code Pattern
```python
from charts.lib.theme import C, apply, page
import plotly.graph_objects as go
import plotly.io as pio

def build():
    df = query("SELECT ...")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.col, y=df.val))
    apply(fig, title, subtitle, height=400)
    html = page(title, body=pio.to_html(fig))
    with open(out_path, "w") as f:
        f.write(html)
```

---

## Project Structure

```
/opt/open-reporting/
├── charts/              # Plotly dashboards
│   ├── dashboards/      # Dashboard modules
│   └── lib/             # Shared utilities (db.py, theme.py)
├── ingestion/           # ETL scripts
├── processing/          # Data processing
├── nginx/               # Nginx, SSL
├── content/             # Ghost CMS
├── .opencode/           # Agent configurations
│   ├── agents/          # Custom agents
│   └── commands/        # Slash commands
└── docker-compose.yml
```

---

## Useful Commands

```bash
# Start services
docker compose up -d

# Generate dashboards
POSTGRES_PASSWORD=xxx python3 charts/generate.py

# Run ingestion
POSTGRES_PASSWORD=xxx python3 ingestion/gpw_ingest.py --backfill
BDL_API_KEY=xxx POSTGRES_PASSWORD=xxx python3 ingestion/budget_ingest.py
```

---

## Agent Configuration

Custom agents in `.opencode/agents/`:
- `dashboard-dev.md` — Builds dashboards following DDF
- `data-engineer.md` — Builds ingestion pipelines
- `reviewer.md` — Reviews code quality

Custom commands in `.opencode/commands/`:
- `/dash <domain>` — Start dashboard development
- `/ingest <source>` — Start data ingestion
- `/review` — Code review

---

## Remember

- **Approval gates** — Do not skip stages without approval
- **Budget aware** — Use free-tier models (Gemini, Groq)
- **Document everything** — Comment code, update README
- **Test thoroughly** — Manual validation before claiming done
- **Git workflow** — Commit after each stage, push regularly
