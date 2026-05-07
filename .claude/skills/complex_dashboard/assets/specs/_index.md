# `specs/` index

Read-only authoring documentation for the `complex_dashboard` skill.
Markdown only — nothing in this folder is imported or copied; open
the relevant file in your editor when you are working on the
matching part of the dashboard.

## Top-level docs

| File | Read when |
|---|---|
| [page_layout.md](page_layout.md) | Designing the section block (H2 + KPI row + chart grid) |
| [chart_types.md](chart_types.md) | Choosing the right chart for an analytical question |
| [testing.md](testing.md) | Writing tests for a dashboard (smoke / data contract / per-page) |
| [config.md](config.md) | Adding env vars or revisiting the config policy |
| [load_map.md](load_map.md) | Deciding which spec to read for a given task |

## Visuals — chart-family specs

| Family | Files | Read when |
|---|---|---|
| [`visuals/cards/`](visuals/cards/) | KPI card variants | Building any KPI tile |
| [`visuals/bar/`](visuals/bar/) | Clustered, stacked, 100% stacked, horizontal | Categorical comparison |
| [`visuals/line/`](visuals/line/) | Line, area, sparkline | Time series |
| [`visuals/combo/`](visuals/combo/) | Combo charts | Two measures with different units |
| [`visuals/scatter/`](visuals/scatter/) | Scatter, bubble | Two-variable relationships |
| [`visuals/distribution/`](visuals/distribution/) | Box, violin, histogram | Distribution shape |
| [`visuals/waterfall/`](visuals/waterfall/) | Waterfall | Decomposition of a delta |
| [`visuals/maps/`](visuals/maps/) | Choropleth, point map | Geography matters analytically |
| [`visuals/tables/`](visuals/tables/) | Data table | Reader needs to look up exact values |
| [`visuals/other/`](visuals/other/) | Edge cases | Default off the canonical chart families |

## Controls

| File | Read when |
|---|---|
| [`controls/slicers/`](controls/slicers/) | Adding a dropdown / range / multi-select slicer |
| [`controls/navigation/sidebar_nav.md`](controls/navigation/sidebar_nav.md) | Adjusting the sidebar nav (sections, ordering, multi-page) |

## Layout

| File | Read when |
|---|---|
| [`layout/header.md`](layout/header.md) | Customising the header (title, subtitle, logo) |
| [`layout/footer.md`](layout/footer.md) | Source attribution — `source` / `updated` are required |
| [`layout/styles.md`](layout/styles.md) | Picking a token from the `S` dict, adding a new one |

## Data

| File | Read when |
|---|---|
| [`data/data_loaders.md`](data/data_loaders.md) | Writing or wiring a `load_*` function in `data_loaders.py` |

## Theme

| File | Read when |
|---|---|
| [`theme/colours.md`](theme/colours.md) | Picking a chart colour — Nordic palette, semantic roles |
| [`theme/typography.md`](theme/typography.md) | Font choices and sizes |
| [`theme/icons.md`](theme/icons.md) | Adding or replacing an SVG icon |

## Deploy

| File | Read when |
|---|---|
| [`deploy/app_init.md`](deploy/app_init.md) | Calling `make_app(...)` — kwargs and conventions |
| [`deploy/deploy.md`](deploy/deploy.md) | Wiring systemd + nginx for a new dashboard |
| [`deploy/observability.md`](deploy/observability.md) | Logging, healthcheck, optional Sentry |

## Public-import surface

For Python imports, do not read into `specs/` — read into `runtime/`.
The single import line is:

```python
from complex_dashboard.assets.runtime import (
    make_app, S, SIDEBAR_W, SIDEBAR_COLLAPSED,
    build_header, build_footer,
    build_sidebar, register_toggle_callback,
    build_page_layout,
    configure_logging, get_logger, require_env,
    register_healthcheck,
)
```
