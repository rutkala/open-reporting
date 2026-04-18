# Grid & Card

## What it is
The CSS grid system and card container used to lay out charts within a section.
All charts live inside a `card`. Cards are arranged in a `grid-2`, `grid-3`, or `grid-4`
container, or placed full-width without a grid wrapper.

## S dict entries (copy into `app.py`)
```python
S = {
    # ...
    "grid-2":    {"display": "grid", "gridTemplateColumns": "1fr 1fr",           "gap": "20px", "alignItems": "start"},
    "grid-3":    {"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr",       "gap": "20px", "alignItems": "start"},
    "grid-4":    {"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)",    "gap": "16px", "alignItems": "start"},
    "grid-auto": {"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))", "gap": "16px", "maxWidth": "100%"},
    "card":      {"background": BG_SURFACE, "border": f"1px solid {BORDER}",
                  "borderRadius": "8px", "padding": "16px", "overflow": "hidden", "minWidth": 0},
}
```

## Template — two charts side by side
```python
html.Div(style=S["grid-2"], children=[
    html.Div(style=S["card"], children=[
        # chart component here
    ]),
    html.Div(style=S["card"], children=[
        # chart component here
    ]),
]),
```

## Template — full-width chart
```python
html.Div(style=S["card"], children=[
    # chart component here
]),
```

## Template — four KPI-sized tiles
```python
html.Div(style=S["grid-4"], children=[
    html.Div(style=S["card"], children=[...]),
    html.Div(style=S["card"], children=[...]),
    html.Div(style=S["card"], children=[...]),
    html.Div(style=S["card"], children=[...]),
]),
```

## Grid options
| Key | Columns | Gap | Use for |
|-----|---------|-----|---------|
| `grid-2` | 2 equal | 20px | Standard side-by-side charts |
| `grid-3` | 3 equal | 20px | Narrow charts or KPI tiles |
| `grid-4` | 4 equal | 16px | KPI tiles only |
| `grid-auto` | auto-fit ≥180px | 16px | Responsive KPI strips |

## Rules
- Every chart must be wrapped in `S["card"]` — never render a chart directly into a grid cell
- Max 2 charts per row (grid-2) — grid-3 and grid-4 only for KPI tiles or narrow bar charts
- Full-width charts: no grid wrapper — just `html.Div(style=S["card"], ...)`
- `minWidth: 0` on card prevents grid blowout from wide chart content
- KPI rows use `kpi_row()` component — not the grid system
