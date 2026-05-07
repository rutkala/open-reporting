# Typography

## Font family
```python
FONT_FAMILY = "Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"
```
Loaded via Google Fonts in `index_string` (see `settings/app.md`). Fallback stack covers
Windows (Segoe UI), macOS (system-ui), and all other platforms.

## Element sizes

| Element | Size | Weight | Color | Token |
|---------|------|--------|-------|-------|
| Dashboard title (H1) | 20px | 700 | `#2D3339` | `TEXT` |
| Dashboard subtitle | 13px | 400 | `#6B7A85` | `SUBTEXT` |
| Section heading (H2) | 18px | 700 | `#2D3339` | `TEXT` |
| Section description | 13px | 400 | `#6B7A85` | `SUBTEXT` |
| Chart title | 17px | 400 | `#2D3339` | set by `teal` Plotly template |
| Chart axis ticks | 11px | 400 | `#6B7A85` | `SUBTEXT` — set in template |
| Chart body / hover | 13px | 400 | `#2D3339` | set by `teal` Plotly template |
| KPI value | 28px | 700 | `#2D3339` | `TEXT` — set in `kpi_card.py` |
| KPI label | 12px | 500 | `#6B7A85` | `SUBTEXT` — set in `kpi_card.py` |
| Nav item | 13px | 400/600 | `#2D3339` | set in `S["nav-item"]` |
| Footer text | 12px | 400 | `#6B7A85` | `SUBTEXT` |

## S dict typography entries (copy into app.py)
```python
S = {
    # Header
    # H1: {"fontSize": "20px", "fontWeight": 700, "color": TEXT, "margin": 0}
    # subtitle P: {"fontSize": "13px", "color": SUBTEXT, "margin": "4px 0 0"}

    # Section
    "section-heading": {"fontSize": "18px", "fontWeight": "700", "color": TEXT,
                        "marginBottom": "6px", "marginTop": "48px"},
    "section-desc":    {"fontSize": "13px", "color": SUBTEXT, "marginBottom": "24px"},

    # Footer
    "footer-text": {"fontSize": "12px", "color": SUBTEXT},
}
```

## Rules
- Never use `font-weight` above 700 — no 800 or 900 weights in Inter
- Section description: always `13px SUBTEXT` — do not make it larger to compensate for low-info content; write better copy instead
- Inline styles only — no CSS files. All typography via the `S` dict or inline `style={}` dicts
- Plotly chart titles and axis labels are controlled by the `teal` Plotly template — do not override in chart calls unless required by a specific exception
