# `assets/` — opinionated dashboard starter kit

This folder is the practitioner's starter kit for any Open Reporting
Dash dashboard. It is grouped by **file lifecycle** — the question
"do I import this, copy this, or read this?" is answered by the
folder name, not by guessing.

## Tri-modal map

| Folder | Lifecycle | What you do with it |
|---|---|---|
| `runtime/` | **imported** at app startup | `from complex_dashboard.assets.runtime import make_app, S, build_header, build_footer, build_sidebar, register_toggle_callback, configure_logging, register_healthcheck, build_page_layout` |
| `scaffolds/` | **copied** into the dashboard | `cp scaffolds/*.template products/dashboards/<domain>/` then strip `.template`, replace `TODO_*`, commit your version |
| `specs/` | **read** as authoring docs | Markdown only — never imported or copied. Open in your editor when you need the chart-type guide, the layout grid, or the data-loader contract |
| `example/` | **runs** as a demo | `python3 example/app.py` (single-page, port 8060) and `python3 example/app_multipage.py` (multi-page, port 8061) — proof both shapes work |
| `static/` | **served** by Dash | Canonical SVG icon set (logo, sidebar, toggle, user). Domain dashboards copy these into their own `assets/images/` |

Everything at the top level (`app.py.template`,
`app_multipage.py.template`, `requirements*.txt.template`,
`pyproject.toml.template`, `start.sh.template`, `.env.example`,
`walkthrough.md`) is also lifecycle = copied — they live at the root
because that is where a contributor opening the folder expects to
find the entry points.

## Folder shape

```
assets/
├── README.md                      ← this file
├── walkthrough.md                 ← narrated tour of example/
│
├── app.py.template                ← single-page dashboard starter
├── app_multipage.py.template      ← multi-page (use_pages=True) variant
├── requirements.txt.template      ← runtime deps
├── requirements-dev.txt.template  ← test/lint extras
├── pyproject.toml.template        ← ruff / mypy / pytest config
├── start.sh.template              ← local dev launcher
├── .env.example                   ← env-var contract
│
├── runtime/                       ← imported helpers (the only Python that runs at startup)
│   ├── app_init.py                ← make_app(domain, title, *, use_pages=False)
│   ├── styles.py                  ← S, SIDEBAR_W, GAP, RADIUS tokens
│   ├── header.py                  ← build_header(...)
│   ├── footer.py                  ← build_footer(name, *, source, updated)
│   ├── sidebar_nav.py             ← build_sidebar(...) + register_toggle_callback(app)
│   ├── page_shell.py              ← build_page_layout(...)
│   ├── healthcheck.py             ← register_healthcheck(app)
│   └── log.py                     ← configure_logging() + get_logger() + require_env()
│
├── scaffolds/                     ← copied per dashboard
│   ├── data_loaders.py.template
│   ├── measures.py.template
│   ├── pages/                     ← only relevant for multi-page apps
│   │   ├── _README.md
│   │   ├── overview.py.template
│   │   └── _section.py.template
│   └── tests/
│       ├── conftest.py.template
│       ├── test_smoke.py.template
│       ├── test_data_contract.py.template
│       └── test_page_overview.py.template
│
├── specs/                         ← read-only authoring documentation
│   ├── _index.md                  ← what's where, link map
│   ├── load_map.md                ← when to load each spec
│   ├── page_layout.md             ← section block (H2 + KPI row + chart grid)
│   ├── chart_types.md             ← chart-type decision guide
│   ├── testing.md                 ← walkthrough of test scaffolds
│   ├── config.md                  ← env-var policy
│   ├── visuals/                   ← per-chart-family rules
│   ├── controls/                  ← slicers + navigation
│   ├── layout/                    ← header / footer / styles specs
│   ├── data/                      ← loader interface contract
│   ├── theme/                     ← colour / typography / icon tokens
│   └── deploy/                    ← app_init / deploy / observability
│
├── example/                       ← runnable demo
│   ├── app.py                     ← single-page (port 8060)
│   ├── app_multipage.py           ← multi-page (port 8061)
│   ├── smoke_test.py
│   ├── data_loaders.py
│   ├── measures.py
│   └── pages/
│       ├── overview.py            ← register_page(path="/")
│       └── regional.py            ← register_page(path="/regional")
│
└── static/                        ← canonical SVG icons
    ├── logo.svg
    ├── sidebar.svg
    ├── settings.svg
    └── user.svg
```

## Quickstart — single-page dashboard

```bash
cp .claude/skills/complex_dashboard/assets/app.py.template \
   products/dashboards/<domain>/app.py

cp .claude/skills/complex_dashboard/assets/scaffolds/data_loaders.py.template \
   products/dashboards/<domain>/data_loaders.py

cp .claude/skills/complex_dashboard/assets/scaffolds/measures.py.template \
   products/dashboards/<domain>/measures.py

cp .claude/skills/complex_dashboard/assets/.env.example \
   products/dashboards/<domain>/.env

cp -r .claude/skills/complex_dashboard/assets/static/* \
   products/dashboards/<domain>/assets/images/
```

Then strip `.template` from every filename, replace every `TODO_*`,
and run `python3 products/dashboards/<domain>/app.py` (with
`PYTHONPATH` and `DUCKDB_PATH` set — see `start.sh.template`).

For a multi-page dashboard, swap `app.py.template` for
`app_multipage.py.template` and additionally copy
`scaffolds/pages/overview.py.template` into a new `pages/` directory
inside the dashboard.

## Power BI mental map

If you arrive from Power BI Desktop:

| Power BI artifact | Lives in |
|---|---|
| `.Report/` (visuals, slicers, canvas) | `runtime/` (frame) + `specs/visuals/` (chart-type rules) + `static/` (icons) |
| `.SemanticModel/` (tables, measures) | `scaffolds/measures.py.template` (dashboard-local display) — semantic measures defined upstream in the `semantic-model` skill |
| `reportExtensions.json` (report-level measures) | `scaffolds/measures.py.template` |
| StaticResources / RegisteredResources | `static/` + `specs/theme/` |
| `definition.pbir` settings (HTML shell, theme registration) | `runtime/app_init.py` + `specs/deploy/app_init.md` |

The folder names follow lifecycle, not PBIP. The Power BI analogy is
documentation, not folder structure — the scaffold stays recognisable
to any Dash developer who has never opened a `.pbip` project.
