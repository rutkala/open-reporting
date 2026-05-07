# Source: products/visuals/lib/db.py

DuckDB query utility. Single function: `query(sql, params) -> pd.DataFrame`.

- Connects read-only to path from `DUCKDB_PATH` env var
- Always queries curated schema — never raw
- Parameterised queries via tuple (prevents SQL injection)
- Opens and closes connection per call (no pooling)

```python
from complex_dashboard.assets.data.db import query
df = query("SELECT * FROM curated.mart_labour WHERE year = ?", (2023,))
```
