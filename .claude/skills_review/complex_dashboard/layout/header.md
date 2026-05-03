# Header

## What it is
The top bar of the main content area. Contains the dashboard title, subtitle (date range
or domain), and action buttons (settings, user). Separated from the content area by a divider.

## Template
```python
html.Div(id="main-header", style=S["main-header"], children=[

    # Title + subtitle
    html.Div(children=[
        html.H1(
            "TODO: Dashboard title (Polish)",
            style={"fontSize": "20px", "fontWeight": 700, "color": TEXT, "margin": 0},
        ),
        html.P(
            "TODO: Subtitle — e.g. 'Rynek pracy 2018–2024' or domain + date range",
            style={"fontSize": "13px", "color": SUBTEXT, "margin": "4px 0 0"},
        ),
    ]),

    # Action buttons (settings + user)
    html.Div(style=S["header-actions"], children=[
        html.Button(
            html.Img(src="/TODO_DOMAIN/assets/images/settings.svg", style=S["header-icon"]),
            id="btn-settings", style=S["header-btn"],
        ),
        html.Button(
            html.Img(src="/TODO_DOMAIN/assets/images/user.svg", style=S["header-icon"]),
            id="btn-user", style=S["header-btn"],
        ),
    ]),
]),

html.Hr(style=S["main-divider"]),
```

## Rules
- Title: dashboard name in Polish — concise, no "Dashboard" suffix
- Subtitle: domain + date range (e.g. "Rynek pracy — dane GUS 2018–2024")
- Action buttons: always present — `btn-settings` and `btn-user` (no callbacks required by default)
- `src` paths use the dashboard's URL prefix: `/TODO_DOMAIN/assets/images/`
