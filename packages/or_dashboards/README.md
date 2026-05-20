# or-dashboards

Declarative YAML dashboard framework for Open Reporting.

A small BI tool sitting next to Power BI / Lightdash / Rill Data. Authors write YAML;
the engine renders Dash apps. Theme, layout, and visuals are bundled and overridable.

## Architecture

```
┌─ Tool (this package — pip install) ─────────────────────────┐
│   - default theme (Nordic teal palette)                      │
│   - visual library (KPI cards, charts, tables)               │
│   - layout chrome (sidebar, page shell)                      │
│   - compiler (YAML → Dash app)                               │
│   - MetricFlow semantic-layer adapter                        │
└──────────────────────────────────────────────────────────────┘
                            ▲
                            │ pip install
            ┌───────────────┴────────────────┐
            ▼                                ▼
      finance-dashboard               labour-dashboard
      (YAML only)                     (YAML only)
```

## Project shape (what a dashboard repo looks like)

```
<domain>/
├── app.py                ← 2 lines: from or_dashboards.compiler import run_dashboard; run_dashboard(__file__)
├── dashboard.yml         ← root: domain, port, title
└── pages/
    ├── pages.yml         ← page order
    └── <page>/
        ├── page.yml      ← page title + anchor
        └── visuals/
            ├── visuals.yml
            └── <visual>.yml   ← type + metric + filter + overrides
```

## Override layering

1. Tool defaults (shipped with this package, immutable)
2. Project-root `theme.yaml` / `layout.yaml` (optional, override what you need)
3. Per-visual options inside `pages/.../visuals/*.yml`

If a project file doesn't exist, defaults apply.

## CLI (planned)

```bash
or-dashboard init <name>       # scaffold a new dashboard project
or-dashboard run <path>        # start the Dash server
or-dashboard validate <path>   # schema-check the YAMLs
or-dashboard compile <path>    # print the resolved layout tree (debug)
```

## Status

- [x] Compiler (YAML → Dash app)
- [x] Theme YAML + loader (Nordic teal palette)
- [x] Layout YAML + loader (sidebar position/enabled)
- [x] MetricFlow semantic-layer binding
- [x] First visual: `kpi_standard`
- [ ] CLI (`or-dashboard init/run/validate/compile`)
- [ ] Project-root theme.yaml override file
- [ ] Schema validation (jsonschema)
- [ ] Visual library breadth (line, bar, area, table, ...)
- [ ] Auto-generated docs
