# AGENTS.md — Open Reporting Code Standards

Code conventions for AI coding agents. For project vision, architecture, and workflow see `docs/`.

---

## Code Standards

### General
- Use `#!/usr/bin/env python3` shebang
- Module docstrings with purpose and usage
- `logging.getLogger(__name__)` for logging — no `print()` in scripts
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
except Exception:
    log.exception("Unexpected error")
    raise
```

### Logging Levels
- `debug()` — Detailed debugging
- `info()` — Normal operation milestones
- `warning()` — Unexpected but recoverable
- `error()` — Serious problem
- `exception()` — Error with traceback

---

## Database

- **Always parameterised** — never string-concatenate SQL
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

1. **Never commit `.env`** — contains secrets
2. **Use env vars** for all secrets (passwords, API keys)
3. **Never log secrets** — no passwords or keys in log output
4. **Parameterised queries** — no string concatenation in SQL
5. **Validate external data** — sanitise before storing

---

## Testing

```bash
# DB connection
python3 -c "from charts.lib.db import query; print(query('SELECT 1'))"

# API availability
python3 -c "import requests; print(requests.get('https://bdl.stat.gov.pl/api/v1').status_code)"

# Pytest (when tests exist)
pytest tests/ -v
```

### Ingestion Validation Checklist
- [ ] Row count before/after matches expected
- [ ] Date ranges complete (no gaps)
- [ ] Spot-check 3-5 values against source
- [ ] No nulls in required columns
- [ ] Validation results logged at `info` level
