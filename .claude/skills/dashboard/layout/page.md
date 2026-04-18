# Page / Section

## What it is
A named section within the dashboard content area. Each section answers exactly one
analytical question. Sections are separated by headings and stack vertically in the
scrollable content area.

## Template — section block
```python
# Each section:
# 1. H2 heading with id= matching the sidebar nav href
# 2. Optional description paragraph
# 3. KPI row (if applicable)
# 4. Chart grid

html.H2("TODO: Section title (Polish)", id="TODO_SECTION_ID",
        style={**S["section-heading"], "marginTop": 0}),   # first section: marginTop 0
        # subsequent sections: use S["section-heading"] as-is (has marginTop: 48px)

html.P("TODO: One sentence describing what this section shows.",
       style=S["section-desc"]),

# KPI row — always before charts
kpi_row([...]),

# Charts in a grid
html.Div(style=S["grid-2"], children=[
    html.Div(style=S["card"], children=[...]),
    html.Div(style=S["card"], children=[...]),
]),

# Full-width chart
html.Div(style=S["card"], children=[...]),
```

## Grid options
```python
S["grid-2"]   # 2 columns equal width
S["grid-3"]   # 3 columns equal width
S["grid-4"]   # 4 columns equal width
```

## Rules
- One analytical question per section — never mix unrelated topics
- Section `id=` must match the `href="#id"` in sidebar nav
- First section: `"marginTop": 0`; all others: use `S["section-heading"]` (marginTop 48px built in)
- KPI row always above charts in its section
- Max 2 charts side by side (grid-2) — grid-3 only for KPI-sized tiles or narrow charts
