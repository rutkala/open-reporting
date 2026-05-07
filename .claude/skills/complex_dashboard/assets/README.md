# `assets/` — opinionated dashboard starter kit

This folder is the practitioner's starter kit for any Open Reporting Dash
dashboard. It is grouped by Plotly-vocabulary concern so that anyone
familiar with Dash can navigate it without translation.

## Shape

```
assets/
├── app.py.template    ← copy to products/dashboards/<domain>/app.py
├── example_app.py     ← runnable end-to-end example (port 8060)
├── walkthrough.md     ← narrated tour of example_app.py
├── smoke_test.py      ← end-to-end HTTP-200 check
│
├── pages/             ← what the user sees: chart specs, controls, layout
├── components/        ← placeholder for dashboard-local components
├── data/              ← loader interface + DIMS / MEASURES registry
├── theme/             ← colour, typography, icon tokens
├── images/            ← canonical SVG icon set (logo, sidebar, settings, user)
└── deploy/            ← Dash app factory + systemd / nginx / portal config
```

Top-level entry points (`app.py.template`, `example_app.py`,
`smoke_test.py`, `walkthrough.md`) sit at the root because that is where
every Dash tutorial puts them — a contributor opening this folder finds
them immediately.

## Why this shape

Plotly Dash has no single canonical layout, but the community
conventions are well established:

- **`pages/`** is the Dash Pages convention (≥ v2.5). Even though this
  scaffold catalogues sections rather than registering Dash Pages, the
  folder name is the recognised home for "what the user sees."
- **`assets/`** is the Dash auto-served static directory. The skill
  itself lives under that name; visual tokens live under `theme/` and
  `images/` to avoid nested `assets/`.
- **`data/`** is the convention used by Plotly's own sample apps and by
  every cookiecutter Dash template. It also matches `data.py` in the
  Open Reporting `template/` dashboard.
- **`deploy/`** carries operational glue (Dash factory, systemd unit,
  nginx route). It is skill-only — domain dashboards do not copy this
  folder; they import `make_app` from it.

## For Power BI users

If you arrive from Power BI Desktop, the mental model is:

| Power BI artifact | Lives in |
|---|---|
| `.Report/` (visuals, slicers, canvas) | `pages/` + `components/` + `theme/` + `images/` |
| `.SemanticModel/` (tables, measures) | `data/` (loader contract) — measures defined upstream in the `semantic-model` skill |
| `reportExtensions.json` (report-level measures) | `data/measures_template.py` |
| StaticResources / RegisteredResources | `theme/` + `images/` |
| `definition.pbir` settings (HTML shell, theme registration) | `deploy/app.md` + `deploy/app_init.py` |

The folder names follow Plotly conventions, not PBIP. The Power BI
analogy is preserved here as documentation, not as folder structure —
this is so the scaffold stays recognisable to any Dash developer who
has never opened a `.pbip` project.
