# Footer

## What it is
The fixed bottom bar of the main content area. Contains the dashboard name (left) and a
link to open-reporting.dev (right). Separated from the content area by a divider. Mandatory
on every dashboard — omitting it breaks the branding contract.

## Template
```python
html.Hr(style=S["footer-divider"]),

html.Footer(style=S["main-footer"], children=[
    html.Span("TODO: Dashboard name (Polish)", style=S["footer-text"]),
    html.A("open-reporting.dev", href="https://open-reporting.dev",
           style={**S["footer-text"], "textDecoration": "none"}),
]),
```

## Rules
- Left slot: dashboard name in Polish — same text as the `html.H1` in the header
- Right slot: always `open-reporting.dev` linking to `https://open-reporting.dev`
- `footer-divider` and `main-footer` styles are in the `S` dict — do not override inline
- Footer is outside the scrollable content area — it sits below `main-content-area`
