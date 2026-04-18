# Sidebar Navigation

## When to use
Every dashboard. The collapsible sidebar provides page/section navigation and the
Open Reporting logo. It collapses to an icon strip on narrow screens or when toggled.

## Template — full sidebar structure
```python
from dash import html, callback, Input, Output, State

SIDEBAR_W         = "240px"
SIDEBAR_COLLAPSED = "44px"

# Add to S dict in app.py:
# S["sidebar"], S["sidebar-logo"], S["sidebar-divider"], S["sidebar-nav"],
# S["nav-item"], S["nav-item-active"], S["toggle-btn"], S["toggle-icon"], S["logo"]

html.Aside(id="sidebar", style=S["sidebar"], children=[

    # Logo
    html.Div(id="sidebar-logo", style=S["sidebar-logo"], children=[
        html.A(
            html.Img(id="sidebar-logo-img",
                     src="/TODO_DOMAIN/assets/images/logo.svg",
                     style=S["logo"]),
            href="/",
        ),
    ]),

    html.Hr(id="sidebar-divider", style=S["sidebar-divider"]),

    # Navigation links — one per dashboard section
    # First link uses nav-item-active style; rest use nav-item
    html.Nav(id="sidebar-nav", style=S["sidebar-nav"], children=[
        html.A("TODO: Section 1", href="#TODO_SECTION_1_ID", style=S["nav-item-active"]),
        html.A("TODO: Section 2", href="#TODO_SECTION_2_ID", style=S["nav-item"]),
        html.A("TODO: Section 3", href="#TODO_SECTION_3_ID", style=S["nav-item"]),
        # Add one html.A per section — href must match the id= of the section H2
    ]),

    # Collapse toggle button
    html.Button(id="btn-toggle", style=S["toggle-btn"], children=[
        html.Img(id="toggle-icon",
                 src="/TODO_DOMAIN/assets/images/sidebar.svg",
                 style=S["toggle-icon"]),
    ]),
])
```

## Collapse callback — copy verbatim
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

## Rules
- One `html.A` per section — `href="#section-id"` must match the `id=` of the section `html.H2`
- First link always `nav-item-active`; rest `nav-item` (no JS needed — anchor scrolling)
- Copy collapse callback verbatim — it is identical for all dashboards
- `src` path must use the dashboard's URL prefix: `/TODO_DOMAIN/assets/images/`
