# Footer

## What it is
The fixed bottom bar of the main content area. Contains the dashboard name (left) and a
link to open-reporting.dev (right). Separated from the content area by a divider. Mandatory
on every dashboard — omitting it breaks the branding contract.

## Usage in `app.py`

```python
from complex_dashboard.assets.pages.layout.footer import build_footer

html.Main(style=S["main"], children=[
    *build_header(...),
    html.Div(style=S["main-content-area"], children=[ ... ]),
    *build_footer(name="TODO: Dashboard name (Polish)"),
])
```

`build_footer(...)` returns `[divider_hr, footer]` — spread the list
into `html.Main` so the divider sits as a sibling of the footer.

## What `build_footer` does

| Argument | Type | Purpose |
|---|---|---|
| `name` | `str` | Polish dashboard name — left slot. Should match the header H1 text. |
| `link_label` | `str` | Right-slot link text. Default `"open-reporting.dev"`. |
| `link_href` | `str` | Right-slot link target. Default `"https://open-reporting.dev"`. |

Returns the `html.Hr(style=S["footer-divider"])` plus the
`html.Footer(style=S["main-footer"], ...)`.

## Rules
- Left slot: dashboard name in Polish — same text as the `html.H1` in the header
- Right slot defaults: `open-reporting.dev` linking to `https://open-reporting.dev` — only override for branded variants
- `footer-divider` and `main-footer` styles are in the `S` dict — do not override inline
- Footer is outside the scrollable content area — it sits below `main-content-area`
