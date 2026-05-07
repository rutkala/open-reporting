# Configuration

## Policy

Dashboards read configuration from environment variables only. No
config files, no YAML, no `pydantic-settings`. The complete env-var
contract lives in `assets/.env.example`.

Locally, populate a `.env` next to `app.py` (gitignored) and let
`python-dotenv` load it (already imported by anything in
`products/`):

```bash
cp .claude/skills/complex_dashboard/assets/.env.example \
   products/dashboards/<domain>/.env
$EDITOR products/dashboards/<domain>/.env
```

Production injects values via the systemd unit's `Environment=` /
`EnvironmentFile=` directives — never via `.env` files on the
production host.

## Reading env vars

For startup-critical values (e.g. `DUCKDB_PATH`), use `require_env`
from `runtime/log.py` so the app fails fast at import:

```python
from complex_dashboard.assets.runtime import require_env

DUCKDB_PATH = require_env("DUCKDB_PATH")
```

For optional values, use `os.environ.get(...)` with a sensible default.

## What we deliberately do not do

- **No `pydantic-settings`.** Adds a dependency for a value handful
  this codebase does not realise — coercion to `int` / `bool` is one
  line per call site, not worth a config-class abstraction.
- **No nested config namespaces.** Flat env vars keep the systemd unit
  readable and the contract obvious.
- **No runtime config reload.** Dashboards are short-lived processes;
  restart the systemd unit to pick up new values.

## Standard env vars

| Name | Required | Purpose |
|---|---|---|
| `DUCKDB_PATH` | yes | Path to `data/warehouse.duckdb` |
| `LOG_LEVEL` | no | Python logging level (default `INFO`) |
| `SENTRY_DSN` | no | Sentry ingest URL — see `specs/deploy/observability.md` |
| `GHOST_TOKEN` | no | Ghost CMS API token, dashboards that pull editorial copy |

Add domain-specific variables to the dashboard's own `.env.example`
and document them in the dashboard's README — do not pollute the
shared template.
