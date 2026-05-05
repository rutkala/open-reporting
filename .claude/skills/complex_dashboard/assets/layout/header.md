# Header

## What it is
The top bar of the main content area. Contains the dashboard title, subtitle (date range
or domain), and action buttons (settings, user). Separated from the content area by a divider.

## Usage in `app.py`

```python
from complex_dashboard.assets.layout.header import build_header

html.Main(style=S["main"], children=[
    *build_header(
        title="TODO: Dashboard title (Polish)",
        subtitle="TODO: Subtitle — e.g. 'Rynek pracy — GUS 2018–2024'",
        domain="TODO_DOMAIN",
    ),
    # ... content area ...
])
```

`build_header(...)` returns `[header_div, divider_hr]` — spread the
list into `html.Main` so the divider sits as a sibling of the header.

## What `build_header` does

| Argument | Type | Purpose |
|---|---|---|
| `title` | `str` | Polish dashboard title — H1 text, no "Dashboard" suffix |
| `subtitle` | `str` | Domain + date range, e.g. "Rynek pracy — GUS 2018–2024" |
| `domain` | `str` | URL prefix, must match `make_app(domain=...)` — used for asset `src` paths |
| `extra_actions` | `list \| None` | Optional list of extra header buttons appended after settings + user |

Returns the `html.Div(id="main-header", ...)` plus the trailing
`html.Hr(style=S["main-divider"])`.

## Rules
- Title: dashboard name in Polish — concise, no "Dashboard" suffix
- Subtitle: domain + date range (e.g. "Rynek pracy — dane GUS 2018–2024")
- Standard action buttons (`btn-settings`, `btn-user`) always present — no callbacks required by default
- `extra_actions` for dashboard-specific buttons (export, theme toggle, etc.) — keep ≤ 2 to avoid header clutter
- `src` paths use the dashboard's URL prefix: `/TODO_DOMAIN/assets/images/` — `build_header` constructs them from `domain=`
