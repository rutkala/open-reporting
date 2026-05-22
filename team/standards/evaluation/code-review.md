# Code Review Rules

**Derived from:** `team/knowledge-base/data-engineering/engineering.md` ✓ (KB complete — ELT, DuckDB, dbt, Python ETL, DAMA quality)
**Used by:** `.claude/agents/code-reviewer.md`
**Does NOT cover:** architectural layer compliance (see `evaluation/architecture-review.md`), statistical correctness (see `evaluation/analytical-review.md`), visual design (see `evaluation/visualization-diff.md`)

Rules applied by the `code-reviewer` agent on every PR diff.
Organised by severity — P1 blocks merge, P2 should be fixed, P3 is noted.

---

## P1 — Blocks Merge

These are non-negotiable. A single P1 finding must be resolved before the PR can merge.

### Security
- **No hardcoded secrets** — API keys, passwords, tokens, DSNs must come from env vars or `.env`. Flag any string that looks like a credential.
- **No SQL string concatenation** — f-strings, `%` formatting, or `.format()` used to build SQL queries is a SQL injection risk. All dynamic values must use parameterised queries (`?` or `%s` placeholders with a values tuple).
- **No `.env` in diff** — `.env` must never appear in a staged commit. `.env.example` is fine.

### Architecture — layer violations
- **No raw schema queries from dashboard/app layer** — `products/dashboards/` and `.claude/skills/complex_dashboard/assets/` must not contain SQL that references `raw.*` tables directly. Raw queries belong in `products/ingestion/` or `platform/processing/`.
- **No curated/mart logic in ingestion scripts** — `products/ingestion/` must land data only. Transformation belongs in `platform/processing/` (dbt models).

### Error handling
- **No bare `except:`** — catches everything including `KeyboardInterrupt` and `SystemExit`. Always catch a specific exception class (e.g. `except ValueError`, `except duckdb.Error`).

---

## P2 — Should Fix

Fix before merging where practical. If not fixed, explain why in the PR description.

### Logging
- **No `print()` in scripts** — use `logging.getLogger(__name__)`. `print()` is acceptable only in one-off CLI scripts explicitly marked as such.
- **Logger defined at module level** — `log = logging.getLogger(__name__)` at the top of the file, not inside functions.

### Database
- **`ON CONFLICT DO UPDATE` for upserts** — any INSERT that could produce duplicates must use upsert pattern. A bare `INSERT INTO` on a table with a unique key is a bug waiting to happen.
- **`fetched_at` in ingestion tables** — every raw table must include a `fetched_at TIMESTAMPTZ` column populated at ingest time.
- **Connection closed in `finally` block** — DB connections opened in a function must be closed in `finally`, not just at the end of the happy path.
- **`load_dotenv(override=True)` in scripts that need env vars** — must appear before any `os.getenv()` calls.

### Python conventions
- **No Polish strings in component library or template code** — `.claude/skills/complex_dashboard/assets/` and `products/dashboards/template/` are English-only. Polish strings belong in domain dashboard files only (user-facing content).
- **Line length ≤ 100 characters** — flag lines that exceed this. Docstrings and comments included.
- **Type hints on new function signatures** — every new function must have parameter and return type annotations. Existing functions without hints are not flagged unless they are being modified.
- **`#!/usr/bin/env python3` shebang on new scripts** — required on any new file in `products/ingestion/` or `platform/processing/` that is meant to be run directly.
- **Imports ordered: stdlib → third-party → local** — flag only if the order is clearly wrong (e.g. local imports before stdlib), not minor grouping issues.

### Visual / semantic layer
- **`format_type` on every new `Measure` definition** — new `Measure(...)` calls must specify `format_type` explicitly. The default (`"number"`) is acceptable only if it is clearly intentional.
- **`y_measure` passed to chart calls that support it** — new chart calls in domain dashboards should pass `y_measure` if the component accepts it. Template scaffold already enforces this pattern.

---

## P3 — Noted

Log these in the review output but do not block merge.

- Missing docstring on new public functions (functions not prefixed with `_`)
- Unused imports left in file
- Magic numbers without a comment explaining their meaning
- f-string / `.format()` / `%` formatting inconsistency within the same file
- Repeated identical logic that could be a helper (flag only if 3+ occurrences)
- Missing `subtitle` on chart calls in domain dashboards (not required but recommended)

---

## What is NOT flagged

- Style preferences not listed above
- Existing code that was not touched by the diff
- Test files (we have no formal test suite yet — when one exists, add rules here)
- One-off analysis scripts in `products/research/notebooks/`
