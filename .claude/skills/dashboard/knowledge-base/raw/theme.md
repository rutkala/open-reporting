# Theme Reference

Nordic design system. All colour and layout values come from
`products/visuals/lib/theme.py`. Never hardcode hex values or pixel sizes.

---

## Import

```python
import products.visuals.lib.theme as _theme  # registers 'nordic' Plotly template
from products.visuals.lib.theme import (
    BG_PAGE, BG_SURFACE, BORDER,
    TEXT, SUBTEXT, MUTED,
    POSITIVE, NEGATIVE, WARNING,
    AZURE_1, AZURE_2, AZURE_3, AZURE_4,
    TEAL_1, TEAL_2, TEAL_3,
    SLATE_1, SLATE_2, SLATE_3, SLATE_4,
    COLORWAY, FONT_FAMILY,
)
```

Importing `_theme` registers the `nordic` Plotly template — do this once per app,
at the top of `app.py`. After that, all `go.Figure()` calls use nordic by default.

---

## Colour Tokens

### Backgrounds

| Token | Hex | Use |
|-------|-----|-----|
| `BG_PAGE` | `#F7F8FA` | Page body, `paper_bgcolor` on figures |
| `BG_SURFACE` | `#FFFFFF` | Cards, header, footer, modal backgrounds |
| `BG_PLOT` | `#F7F8FA` | `plot_bgcolor` — same as page (flat look) |

### Structure

| Token | Hex | Use |
|-------|-----|-----|
| `BORDER` | `#DDE2E8` | Card borders, dividers, table lines |
| `GRID` | `#E8ECF0` | Chart gridlines |
| `ZERO_LINE` | `#C8CDD5` | Zero axis line |

### Text

| Token | Hex | Use |
|-------|-----|-----|
| `TEXT` | `#2C3A4A` | Titles, labels — primary, high contrast |
| `SUBTEXT` | `#6B7A8D` | Axis ticks, units, secondary information |
| `MUTED` | `#9BABB8` | Footnotes, disabled states |

### Data Palette (use in order)

| Token | Hex | Position |
|-------|-----|----------|
| `AZURE_1` | `#4A7FB5` | First / primary series |
| `AZURE_2` | `#7BAFD4` | Second series |
| `AZURE_3` | `#A8C8E8` | Third series / area fill |
| `AZURE_4` | `#C5DCF0` | Fourth series |
| `TEAL_1` | `#3D7A6E` | Alternative first (teal-dominant dashboards) |
| `TEAL_2` | `#5A9A8C` | Alternative second |
| `TEAL_3` | `#82BDB3` | Alternative third |
| `SLATE_1` | `#6B8FA6` | Fifth series |
| `SLATE_2` | `#9BB5C4` | Sixth series |
| `SLATE_3` | `#C5D8E3` | Background fill / low emphasis |
| `SLATE_4` | `#E2EEF4` | Very light fill |
| `COLORWAY` | list | Full 8-colour sequence — used by Plotly template |

### Semantic (for explicit meaning only — never for decoration)

| Token | Hex | Use |
|-------|-----|-----|
| `POSITIVE` | `#4A9B6F` | Growth, surplus, above target |
| `NEGATIVE` | `#C0503A` | Decline, deficit, below target |
| `WARNING` | `#D4874A` | Caution, borderline |

**Rule:** never use POSITIVE/NEGATIVE for categorical distinction. They carry meaning —
using them decoratively breaks that meaning for the user.

---

## Page Layout

### Standard page structure

```
┌─────────────────────────────────────────┐
│  HEADER  (logo + navigation)            │
├──────────┬──────────────────────────────┤
│  FILTER  │  MAIN CANVAS                 │
│  PANE    │  ┌── Section A ────────────┐ │
│  220px   │  │  KPI cards + charts     │ │
│          │  └────────────────────────┘ │
│          │  ┌── Section B ────────────┐ │
│          │  │  More charts            │ │
│          │  └────────────────────────┘ │
├──────────┴──────────────────────────────┤
│  FOOTER  (source + last updated)        │
└─────────────────────────────────────────┘
```

### Visual layering

```
Page #F7F8FA
└── Section #F7F8FA (same colour, separated by spacing + label)
    └── Chart card #FFFFFF + shadow
        └── Plotly figure (transparent background)
```

Card style (apply via `style=` prop):
```python
CARD_STYLE = {
    "background": BG_SURFACE,
    "borderRadius": "6px",
    "boxShadow": "0 1px 4px rgba(0,0,0,0.07), 0 0 1px rgba(0,0,0,0.04)",
    "padding": "16px",
}
```

### Spacing constants

| Element | Value |
|---------|-------|
| Card gap | 24px |
| Filter pane width | 220px |
| Header height | 56px |
| Page padding | 24px |
| Card padding | 16px |

### Grid rules

- Max 2 charts side by side
- Every chart belongs to a named section
- No orphaned charts outside sections

---

## Typography

```python
FONT_FAMILY = "Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"
```

| Element | Size | Weight | Colour |
|---------|------|--------|--------|
| Dashboard title | 28px | 700 | `TEXT` |
| Section heading | 16px | 600 | `TEXT` |
| Chart title | 16–18px | 600 | `TEXT` |
| Axis title | 12px | 400 | `SUBTEXT` |
| Axis tick labels | 11px | 400 | `SUBTEXT` |
| KPI value | 28–36px | 700 | `TEXT` |
| KPI label | 13px | 400 | `SUBTEXT` |
| Footer | 12px | 400 | `SUBTEXT` |

---

## Required footer

Every dashboard page must have a visible footer:
```python
html.Footer(
    f"Dane: {source_name} — aktualizacja: {update_date}",
    style={"color": SUBTEXT, "fontSize": "12px", "padding": "16px 24px"}
)
```

Source attribution is not optional — it is a quality gate criterion.
