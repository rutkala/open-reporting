# Testing

## What ships in `scaffolds/tests/`

Four templates — copy into `products/dashboards/<domain>/tests/` and
strip the `.template` suffix. They cover three layers in increasing
cost:

| Template | Layer | Needs warehouse? | Needs browser? |
|---|---|---|---|
| `conftest.py.template` | fixtures | no | no |
| `test_smoke.py.template` | HTTP / layout assigned | no | no |
| `test_data_contract.py.template` | DIMS / MEASURES / loaders | yes | no |
| `test_page_overview.py.template` | per-page render | yes | no |

`pip install -r requirements-dev.txt` brings in `pytest` and
`dash[testing]`. Run with `pytest -q` from the dashboard directory
(`PYTHONPATH=/opt/open-reporting` set so the dashboard package
resolves).

## Fixture model

`conftest.py` imports the dashboard's `app` once per session and
exposes:

- `app` — the Dash instance
- `client` — `app.server.test_client()` for HTTP-level tests
- `dash_duo` — provided by `dash[testing]` for browser-driven E2E

We deliberately import the real app rather than constructing a
mocked one. Smoke tests catch import-time failures and missing
`app.layout` — the most common breakage class — and a mocked app
would not catch them.

## What the smoke test covers

- The Dash app builds (no exception on import).
- `app.layout` is not `None`.
- `GET /` serves the Dash index HTML with HTTP 200.
- `GET /health` returns `{"status": "ok"}`
  (requires `register_healthcheck(app)` in `app.py`).
- For multi-page apps: `dash.page_registry` is populated and a
  page is registered at `path="/"`. The test no-ops on
  single-page apps.

## What the data contract test covers

- `DIMS` and `MEASURES` are non-empty registries of `Dimension` /
  `Measure` instances.
- Column names follow the `dim_*` / `val_*` convention so the
  loader-to-component wiring works.
- Every label is non-empty (Polish required by the visualisation
  standard).
- `load_by_year()` returns a `DataFrame` with `dim_year` and at
  least one row.
- `load_scalars()` keys are all defined in `MEASURES` — catches the
  drift where a loader returns `"unemploymnt"` (typo) but the
  `kpi_row` reads `MEASURES["unemployment"]`.

## What the per-page test covers

For multi-page dashboards, calls `layout()` directly and walks the
returned tree for the elements every page must carry — the section
heading, the page anchor id, and any KPI/chart slots that load at
import. Add one `test_page_<slug>.py` per page.

For single-page dashboards, replace this file with a test that walks
`app.layout` itself.

## What we deliberately do not scaffold

- **Visual regression.** Percy / Playwright snapshot tests catch real
  rendering bugs but cost more setup time than the value/regression
  ratio currently justifies. The screenshot reviewer agent (see
  `team/standards/evaluation/visualization-image.md`) covers this in
  PR review instead.
- **Browser-driven E2E with `dash_duo`.** The fixture is wired so it
  is one `pytest` import away when needed, but the default test set
  does not depend on a browser binary.
- **Mocked DuckDB.** Better to skip data-contract tests in CI when
  the warehouse is unavailable than to maintain a fixture warehouse
  that drifts from production.
