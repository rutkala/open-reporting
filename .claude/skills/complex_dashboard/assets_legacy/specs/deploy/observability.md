# Observability

## Logging

Every dashboard configures the root logger once at startup via
`runtime/log.py`:

```python
from complex_dashboard.assets.runtime import configure_logging, get_logger

configure_logging()
log = get_logger(__name__)
log.info("starting %s on port %d", __name__, PORT)
```

`configure_logging(level=logging.INFO)` installs a single stdout
`StreamHandler` with the format
`%(asctime)s %(levelname)s %(name)s %(message)s`. Idempotent — repeated
calls replace the prior handler so re-imports during testing do not
duplicate log lines.

`get_logger(name)` is a thin wrapper around `logging.getLogger`
present only so dashboards have a single import surface. Always use
`__name__` as the argument so log lines carry the module path.

### What we deliberately do not do

- **No JSON formatter.** Plain stdout is enough at current scale; systemd
  captures it into the journal, where `journalctl -u <unit>` is fine for
  inspection. Add a JSON formatter when log shipping to Loki/Elastic
  becomes real.
- **No structured context (`extra={}`) by default.** Add per-call when a
  request needs it (e.g. user_id, query_id) — do not write a generic
  context-injection middleware unless multiple dashboards need it.

## Healthcheck

`register_healthcheck(app)` mounts `GET /health` returning
`{"status": "ok"}`. Call once after `app = make_app(...)`:

```python
from complex_dashboard.assets.runtime import register_healthcheck

app = make_app(domain="labour", title="...", module_name=__name__)
register_healthcheck(app)
```

Use it for systemd `WatchdogSec`, nginx `proxy_next_upstream`, or
external uptime probes (UptimeRobot, Better Stack). Deliberately
trivial — does not query DuckDB or test downstream APIs. A readiness
probe with real dependency checks can be added per-dashboard if a
specific failure mode warrants it.

## Sentry (optional, not bundled)

Dashboards that need exception tracking add Sentry per-app. The skill
does not import or depend on `sentry-sdk`; do not add it to the runtime
dependency list. Reference setup:

```python
import os
import sentry_sdk

if dsn := os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(dsn=dsn, traces_sample_rate=0.1)
```

Place this above `make_app(...)` so init errors during app construction
are captured. The `SENTRY_DSN` env var is listed in `.env.example` as
optional.

## Required env vars (fail-fast)

`require_env(name)` reads an env var and raises `RuntimeError` if it is
unset or empty. Call it at module load — never inside a callback — for
every variable the app cannot start without:

```python
from complex_dashboard.assets.runtime import require_env

DUCKDB_PATH = require_env("DUCKDB_PATH")
```

Misconfiguration then surfaces at `python3 app.py` startup with a
clear message, not as a 500 on the first user request. Treats unset
and empty-string as the same failure.
