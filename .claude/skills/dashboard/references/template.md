# Dashboard Template — Structure and Patterns

The template at `products/dashboards/template/` is the canonical starting point for
every new dashboard. It is a live developer reference: all chart types displayed
with sample data, all components exercised, all patterns demonstrated.

Run it before building to see what each component looks like:

```bash
PYTHONPATH=/opt/open-reporting \
DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
python3 products/dashboards/template/app.py
# → http://localhost:8055
```

---

## File structure

```
products/dashboards/{domain}/
├── app.py           → Dash app — layout + callbacks (copy from template, adapt)
├── measures.py      → Dimension + Measure display config (rename, replace labels)
├── data.py          → Data loaders: template uses sample data; domain uses warehouse
│                      (replace with semantic_service.py calls in real dashboards)
└── assets/
    └── images/
        ├── logo.svg         → Portal logo (shared from template)
        ├── icon.svg         → Favicon
        ├── sidebar.svg      → Sidebar toggle icon
        ├── settings.svg     → Settings button icon
        └── user.svg         → User button icon
```

For domain dashboards, `data.py` is typically replaced by `semantic_service.py`,
which queries the warehouse using `products/visuals/lib/db.py`.

---

## Three-file contract

| File | What it contains | What it does NOT contain |
|------|-----------------|--------------------------|
| `measures.py` | `DIMS` + `MEASURES` dicts of Dimension/Measure objects | Any SQL, aggregation, or data loading |
| `data.py` / `semantic_service.py` | Data loaders returning pre-aggregated DataFrames | Any chart config, labels, or formatting |
| `app.py` | Layout, chart calls, callbacks | Aggregation logic or raw SQL |

This separation means: updating a Polish label touches only `measures.py`. Updating
a SQL query touches only `semantic_service.py`. Layout changes touch only `app.py`.

---

## app.py layout pattern

### Bootstrap

```python
import products.visuals.lib.theme as _theme   # registers 'teal' Plotly template
from products.visuals.lib.theme import (
    BG_PAGE, BG_SURFACE, BORDER, TEXT, SUBTEXT, FONT_FAMILY,
    POSITIVE, NEGATIVE, WARNING, COLORWAY,
    TEAL_1, TEAL_2, TEAL_3, TEAL_4, TEAL_PALE,
    AZURE_1, AZURE_2, AZURE_3, AZURE_4, AZURE_PALE,
    SLATE_1, SLATE_2, SLATE_3, SLATE_4,
)

import products.dashboards.{domain}.measures as m
import products.dashboards.{domain}.data as _data   # or semantic_service
```

### Style dictionary

All inline styles live in a single `S = {}` dict at module level. Never hardcode
hex values or pixel sizes in layout calls — reference `S["key"]` or theme tokens.

```python
SIDEBAR_W         = "240px"
SIDEBAR_COLLAPSED = "44px"
GAP    = "4px"
RADIUS = "10px"

S = {
    "body": {
        "fontFamily": FONT_FAMILY,
        "background": BG_PAGE, "color": TEXT,
        "height": "100vh", "display": "flex", "margin": 0,
        "padding": f"{GAP} 0 {GAP} {GAP}",
        "boxSizing": "border-box", "overflow": "hidden",
    },
    "sidebar": {
        "width": SIDEBAR_W, "flexShrink": 0,
        "background": BG_SURFACE, "borderRadius": RADIUS,
        "boxShadow": "0 2px 8px rgba(0,0,0,0.06), 0 0 1px rgba(0,0,0,0.08)",
        "display": "flex", "flexDirection": "column",
        "height": f"calc(100vh - {GAP} * 2)", "overflow": "hidden",
        "transition": "width 0.25s ease", "position": "relative",
    },
    "main": {
        "flex": 1, "minWidth": 0,
        "overflowY": "auto", "overflowX": "hidden",
        "height": f"calc(100vh - {GAP} * 2)",
        "boxSizing": "border-box", "display": "flex", "flexDirection": "column",
    },
    "main-content-area": {
        "flex": 1, "padding": "28px 32px 32px",
        "overflowY": "auto", "width": "100%", "boxSizing": "border-box",
    },
    "card": {
        "background": BG_SURFACE, "border": f"1px solid {BORDER}",
        "borderRadius": "8px", "padding": "16px",
        "overflow": "hidden", "minWidth": 0,
    },
    "grid-2": {"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "alignItems": "start"},
    "grid-3": {"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "20px", "alignItems": "start"},
    "grid-4": {"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "16px", "alignItems": "start"},
    "section-heading": {"fontSize": "18px", "fontWeight": "700", "color": TEXT, "marginBottom": "6px", "marginTop": "48px"},
    "section-desc": {"fontSize": "13px", "color": SUBTEXT, "marginBottom": "24px"},
}
```

### Full layout structure

```python
app.layout = html.Div(style=S["body"], children=[

    # ── Sidebar ───────────────────────────────────────────────────────────────
    html.Aside(id="sidebar", style=S["sidebar"], children=[
        # Logo
        html.Div(id="sidebar-logo", style=S["sidebar-logo"], children=[
            html.A(html.Img(src="/{domain}/assets/images/logo.svg"), href="/"),
        ]),
        html.Hr(style=S["sidebar-divider"]),
        # Navigation links — one per dashboard section
        html.Nav(id="sidebar-nav", style=S["sidebar-nav"], children=[
            html.A("Overview", href="#overview", style=S["nav-item-active"]),
            html.A("Trends",   href="#trends",   style=S["nav-item"]),
            html.A("Regions",  href="#regions",  style=S["nav-item"]),
        ]),
        # Collapse toggle
        html.Button(id="btn-toggle", style=S["toggle-btn"], children=[
            html.Img(src="/{domain}/assets/images/sidebar.svg", style=S["toggle-icon"]),
        ]),
    ]),

    # ── Main ─────────────────────────────────────────────────────────────────
    html.Main(id="main-content", style=S["main"], children=[

        # Header
        html.Div(style=S["main-header"], children=[
            html.Div(children=[
                html.H1("Dashboard title", style={...}),
                html.P("Subtitle or date range", style={...}),
            ]),
            html.Div(style=S["header-actions"], children=[
                html.Button(html.Img(src="/{domain}/assets/images/settings.svg"), id="btn-settings", style=S["header-btn"]),
                html.Button(html.Img(src="/{domain}/assets/images/user.svg"),     id="btn-user",     style=S["header-btn"]),
            ]),
        ]),
        html.Hr(style=S["main-divider"]),

        # Content area
        html.Div(style=S["main-content-area"], children=[

            # Section
            html.H2("Overview", id="overview", style={**S["section-heading"], "marginTop": 0}),
            html.P("Section description", style=S["section-desc"]),

            # KPI row
            kpi_row([
                kpi_standard(label=..., value=..., unit=..., trend=..., trend_color=...),
                ...
            ]),

            # Chart in a card
            html.Div(style=S["grid-2"], children=[
                html.Div(style=S["card"], children=[line(...)]),
                html.Div(style=S["card"], children=[clustered_column(...)]),
            ]),

            # Next section
            html.H2("Trends", id="trends", style=S["section-heading"]),
            ...
        ]),

        html.Hr(style=S["footer-divider"]),

        # Footer — source attribution (mandatory)
        html.Footer(style=S["main-footer"], children=[
            html.Span(f"Dane: {SOURCE} — aktualizacja: {DATE}", style=S["footer-text"]),
        ]),
    ]),
])
```

### Sidebar collapse callback

Copy verbatim from the template — it is identical for all dashboards:

```python
@callback(
    Output("sidebar", "style"),
    Output("btn-toggle", "style"),
    Output("sidebar-logo", "style"),
    Output("sidebar-nav", "style"),
    Output("sidebar-logo-img", "style"),
    Input("btn-toggle", "n_clicks"),
    State("sidebar", "style"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, sidebar_style):
    is_expanded = sidebar_style.get("width", SIDEBAR_W) == SIDEBAR_W
    btn_open   = {**S["toggle-btn"], "right": "10px", "transform": "none"}
    btn_closed = {**S["toggle-btn"], "right": "50%", "transform": "translateX(50%)"}
    if is_expanded:
        return ({**sidebar_style, "width": SIDEBAR_COLLAPSED},
                btn_closed, {"display": "none"}, {"display": "none"}, {"display": "none"})
    else:
        return (S["sidebar"], btn_open, S["sidebar-logo"], S["sidebar-nav"], S["logo"])
```

---

## data.py / semantic_service.py pattern

Template `data.py` uses synthetic data. Real domain dashboards replace it with
`semantic_service.py` that queries the warehouse.

### Standard loaders

Every dashboard exposes the same loader interface:

| Function | Returns | Used by |
|----------|---------|---------|
| `load_by_year()` | `DataFrame` with `dim_year` + measure columns | Time-series charts |
| `load_by_category()` | `DataFrame` with dim column + measure columns | Category charts |
| `load_scalars()` | `dict` of `{measure_name: float}` | KPI cards |
| `load_geo()` | `DataFrame` with `dim_iso3`, `dim_label`, `dim_lat`, `dim_lon` | Map charts |

### Column naming conventions

- Dimension columns: `dim_*` — e.g. `dim_year`, `dim_region`, `dim_category`
- Measure columns: `val_*` — e.g. `val_employment`, `val_rate`, `val_gdp`
- Derived columns: `val_*_pct` (YoY %), `val_*_cum` (cumulative)
- Geographic: `dim_iso3` (ISO-3 code), `dim_label` (display name), `dim_lat`, `dim_lon`
- Date/time: `dim_date` (OHLC), `dim_year`, `dim_period` (Q1–Q4)

### Domain semantic_service.py pattern

```python
from products.visuals.lib.db import query

def load_by_year() -> pd.DataFrame:
    return query("""
        SELECT year                        AS dim_year,
               AVG(employment_thousands)   AS val_employment,
               AVG(unemployment_rate)      AS val_rate
        FROM   curated.mart_labour
        GROUP  BY year
        ORDER  BY year
    """)

def load_scalars() -> dict:
    df = load_by_year()
    return {
        "employment": float(df["val_employment"].iloc[-1]),
        "rate":       float(df["val_rate"].iloc[-1]),
    }
```

---

## Dash app registration

Every domain dashboard runs on its own port and prefix:

```python
PORT = 8050  # labour, 8051 = explorer, 8052 = mobile, 8053 = finance, …

app = Dash(
    __name__,
    title="Labour — Open Reporting",
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/{domain}/",
    routes_pathname_prefix="/{domain}/",
    index_string="""<!DOCTYPE html>
<html>
    <head>
        {%metas%}<title>{%title%}</title>{%favicon%}{%css%}
        <style>
            html, body { margin: 0; padding: 0; height: 100vh; }
            #react-entry-point { height: 100%; }
            .js-plotly-plot .plotly { width: 100% !important; }
            .js-plotly-plot .plotly .main-svg { width: 100% !important; }
        </style>
    </head>
    <body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body>
</html>""",
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
```

---

## How to copy and adapt the template

1. Copy `products/dashboards/template/` to `products/dashboards/{domain}/`
2. Copy `products/dashboards/template/assets/` to the new directory
3. In `measures.py`: rename labels to Polish domain terms; keep `Dimension`/`Measure` structure
4. In `data.py` (or rename to `semantic_service.py`): replace sample data with warehouse queries
5. In `app.py`:
   - Update `title=`, `requests_pathname_prefix=`, `routes_pathname_prefix=`, `PORT`
   - Update sidebar nav links to match dashboard sections
   - Replace chart calls with domain-specific charts (keep the S-dict and layout shell)
   - Update footer source attribution
6. Register in `nginx` config and `docker-compose.yml` if deploying
