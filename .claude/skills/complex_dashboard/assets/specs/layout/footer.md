# Footer

## What it is
The fixed bottom bar of the main content area. Left slot carries the dashboard
name plus the source attribution line (`Dane: {source} — aktualizacja: {updated}`).
Right slot links to open-reporting.dev. Separated from the content area by a
divider. Mandatory on every dashboard — omitting it breaks the branding contract,
and `source` / `updated` are required keyword-only arguments so a missing
attribution fails fast at app import.

## Usage in `app.py`

```python
from complex_dashboard.assets.runtime import build_footer

html.Main(style=S["main"], children=[
    *build_header(...),
    html.Div(style=S["main-content-area"], children=[ ... ]),
    *build_footer(
        name="Rynek pracy",
        source="GUS BDL",
        updated="luty 2026",
    ),
])
```

`build_footer(...)` returns `[divider_hr, footer]` — spread the list
into `html.Main` so the divider sits as a sibling of the footer.

## What `build_footer` does

| Argument | Type | Required | Purpose |
|---|---|---|---|
| `name` | `str` | yes (positional) | Polish dashboard name — same text as the header H1. |
| `source` | `str` | yes (kw-only) | Authoritative data source (Polish), e.g. `"GUS BDL"`, `"Ministerstwo Finansów"`, `"Eurostat"`. |
| `updated` | `str` | yes (kw-only) | Last refresh date or coverage window (Polish), e.g. `"luty 2026"`, `"2018–2024"`. |
| `link_label` | `str` | no | Right-slot link text. Default `"open-reporting.dev"`. |
| `link_href` | `str` | no | Right-slot link target. Default `"https://open-reporting.dev"`. |

Returns `html.Hr(style=S["footer-divider"])` plus the
`html.Footer(style=S["main-footer"], ...)`.

## Rendered output

Left slot text: `{name} · Dane: {source} — aktualizacja: {updated}`

Example: `Rynek pracy · Dane: GUS BDL — aktualizacja: luty 2026`

## Rules
- `source` and `updated` are required — calling `build_footer("Name")` without
  them raises `TypeError` at app import. This enforces the source-attribution
  rule from `team/standards/build/visualisation.md` at the API boundary.
- Left slot starts with the dashboard name in Polish — same text as the
  `html.H1` in the header.
- Right slot defaults: `open-reporting.dev` linking to
  `https://open-reporting.dev` — only override for branded variants.
- `footer-divider` and `main-footer` styles are in the `S` dict — do not
  override inline.
- Footer is outside the scrollable content area — it sits below
  `main-content-area`.
