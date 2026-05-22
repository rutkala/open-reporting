---
name: complex_dashboard
description: >
  Dashboard report-layer skill. Open Reporting dashboards are now built
  declaratively with the `dbr` Python package — author writes
  YAML, the engine renders a Dash app. Theme, layout, and visual library
  ship with the package. Load this skill when building, modifying, or
  reviewing a dashboard. For metrics and aggregation rules, load the
  `semantic-model` skill instead.
  Triggers when: "build the dashboard", "design the dashboard", "add a
  visual", "review the dashboard", or when /composite_develop reaches a
  dashboard product.
user-invocable: true
---

# Dashboard (Report Layer) — `dbr`

A small BI framework alongside Power BI / Lightdash / Rill Data.
**Authors write YAML; the engine renders Dash.** Theme, chrome (sidebar,
header, footer), and a library of pre-configured visuals all ship with
the installed package. Each visual binds to a MetricFlow metric by name —
no SQL, no DAX, no callbacks for static dashboards.

## Power BI mental model

| Power BI | Open Reporting | This skill |
|---|---|---|
| Visualization pane (visuals, layout, theme) | `dbr` report layer | **here** |
| Tabular model + DAX measures | dbt + MetricFlow semantic layer | `semantic-model` skill |
| Power Query (ETL) | dbt models | `data-engineer` skill |
| `theme.json` | `theme.yaml` (in the package; per-project override optional) | here |
| Visual format pane | per-visual YAML overrides | here |
| .pbip / .pbir project files | PBIP-shape folder of YAMLs | here |

This skill owns the **report layer only.** Metrics are defined in
MetricFlow YAML and referenced by name; visuals never see SQL.

## Project shape — what every dashboard looks like

```
<dashboard>/
├── app.py                          ← 2-line shim (sets env var, calls run_dashboard)
├── dashboard.yml                    ← root: domain, port, title
├── theme.yaml                       ← OPTIONAL: project-level brand overrides
├── layout.yaml                      ← OPTIONAL: project-level chrome overrides
└── pages/
    ├── pages.yml                    ← order: [overview, trend, ...]
    └── <page>/
        ├── page.yml                 ← title + anchor
        └── visuals/
            ├── visuals.yml          ← layout: rows of items
            ├── <visual_a>.yml       ← type + metric + filter + per-visual overrides
            ├── <visual_b>.yml
            └── ...
```

Each YAML file starts with a `# yaml-language-server: $schema=...` header
so editors with yaml-language-server give live auto-complete and
inline validation against the packaged JSON Schemas.

## Override layering — `theme.json` style

```
1. Package defaults     ← ships with dbr, immutable
2. Project overrides    ← optional <project>/theme.yaml + <project>/layout.yaml,
                          deep-merged on top of defaults
3. Per-visual options   ← inside each pages/.../visuals/<name>.yml
```

A project file lists **only the keys it wants to change**; everything
else inherits defaults. No `theme.yaml` at all in a project = full
defaults apply.

## CLI workflow

```bash
dbr init <name>          # scaffold a new project at ./<name>/
dbr validate <path>      # schema-check every YAML in the project tree
dbr compile <path>       # print resolved layout tree as JSON (debug)
dbr run <path>           # start the Dash server
```

systemd units run `dbr run /opt/.../<dashboard>` instead of
`python3 app.py`. Local development can use either.

**Validation is your friend.** Run `dbr validate <path>`
before every commit — it catches:
- Missing required fields (`'metric' is a required property`)
- Wrong types (`'eight-thousand' is not of type 'integer'`)
- Unknown visual types (`unknown visual 'kpi_stadnard'. Available: …`)
- Typo'd visual options (`Additional properties are not allowed ('show_perido' was unexpected)`)
- Out-of-range values (`500 is greater than the maximum of 100`)

## Visual library (`VISUAL_REGISTRY`)

Six visuals registered today. Each binds to a metric by name; the
metric's label, unit, format, and threshold metadata come from the
semantic layer.

| Type | Data | Output | Key options |
|---|---|---|---|
| `kpi_standard` | single latest value | big stacked card (label, value, period) | `show_period` |
| `kpi_compact` | single latest value | inline card (label + value side-by-side) | — |
| `line_chart` | history of N periods | Plotly line+markers | `years` |
| `area_chart` | history of N periods | Plotly area | `years` |
| `bar_chart` | history of N periods | Plotly bars | `years` |
| `table` | history of N periods | HTML table | `rows` |

Minimal visual YAML:

```yaml
# yaml-language-server: $schema=https://open-reporting.dev/dbr/schemas/visual.schema.json
type:   kpi_standard
metric: fiscal_balance
filter:
  geo: PL
```

That's the entire visual. The metric's Polish label, unit, format, and
threshold metadata come from `products/warehouse/.../*.yml`.

## Layout shape — rows-and-items (Rill canvas-style)

Two equivalent shapes:

```yaml
# Short — one column, stacks vertically
order:
  - kpi_balance
  - trend_chart
```

```yaml
# Explicit — multi-column rows
rows:
  - items:
      - { visual: kpi_balance,  width: "33%" }
      - { visual: kpi_debt,     width: "33%" }
      - { visual: kpi_revenue,  width: "33%" }
  - items:
      - { visual: trend_chart,  width: "100%" }
```

Bare strings (`items: [a, b, c]`) get auto-equal widths.

## What changes when you add features

| To add… | Touch |
|---|---|
| A new visual on a page | one YAML file under `pages/<page>/visuals/`, one line in `visuals.yml` |
| A new page | a folder under `pages/`, an entry in `pages.yml` |
| A new dashboard | `dbr init <name>`, fill in metric bindings |
| Override the brand for this dashboard | drop `<project>/theme.yaml` with the keys to change |
| Define a new metric | MetricFlow YAML — that's a `semantic-model` skill task, NOT here |
| Add a new visual TYPE to the library | `packages/dbr/src/dbr/visuals/<name>.py` + register in `VISUAL_REGISTRY` + add `SCHEMA` constant + add tokens to `theme.yaml` |

## Core rules

- **Dashboards are YAML, not Python.** A dashboard's `app.py` is 10
  lines of boilerplate (env var + `run_dashboard(__file__)`). Everything
  else lives in YAML.
- **Visuals bind to metrics by name.** No SQL in dashboards. If the
  number you want isn't a metric yet, define it in MetricFlow first
  (`semantic-model` skill), then reference it.
- **Theme is locked to the brand.** Per-project overrides exist but are
  rare — they're for one-off variants (mobile, accent colour). Most
  dashboards inherit defaults entirely.
- **Validate before committing.** `dbr validate <path>` catches
  schema, type, and reference errors before they hit production.

## Reference paths

| What | Where |
|---|---|
| The installed engine | `/opt/open-reporting/packages/dbr/src/dbr/` |
| JSON Schemas | `dbr/schemas/*.schema.json` |
| Theme defaults | `dbr/theme/theme.yaml` |
| Layout defaults | `dbr/layout/layout.yaml` |
| Visual factories | `dbr/visuals/*.py` |
| Working example dashboard | `products/dashboards/_template/` |
| Legacy Python kit (reference only) | `.claude/skills/complex_dashboard/assets_legacy/` |
| Visualisation principles (IBCS, Gestalt, colour) | `team/knowledge-base/visualization/` |
| Polish editorial conventions | `team/knowledge-base/content/` |

## What this skill no longer covers

The old Python-composition pattern (`from complex_dashboard.assets.runtime
import build_page_layout`) is **deprecated.** It survives at
`assets_legacy/` for reference, but new dashboards do not import from it
and AI agents should not learn it. If you see code resembling the
legacy pattern, treat it as historical context, not a model to follow.
