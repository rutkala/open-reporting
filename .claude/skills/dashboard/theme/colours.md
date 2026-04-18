# Colours

## Source
`products/visuals/lib/theme.py` — import this module to activate the Plotly `teal` template
and expose all tokens.

```python
import products.visuals.lib.theme as _theme  # noqa: F401 — activates template
from products.visuals.lib.theme import (
    BG_PAGE, BG_SURFACE, BORDER,
    COLORWAY, GRID, MUTED, NEGATIVE, POSITIVE,
    SUBTEXT, TEXT, WARNING, ZERO_LINE,
    FONT_FAMILY,
    TEAL_1, TEAL_2, TEAL_3, TEAL_4, TEAL_PALE,
    AZURE_1, AZURE_2, AZURE_3, AZURE_4, AZURE_PALE,
    SLATE_1, SLATE_2, SLATE_3, SLATE_4,
)
```

---

## Colour tokens

### Palette families
| Token | Hex | Use |
|-------|-----|-----|
| `TEAL_1` | `#4A9B8F` | Primary brand, active states, first chart series |
| `TEAL_2` | `#55A1AA` | Secondary teal |
| `TEAL_3` | `#6BB5A8` | Tertiary teal |
| `TEAL_4` | `#8BC4C7` | Light teal |
| `TEAL_PALE` | `#D7F3F0` | Teal background tint (KPI trend positive) |
| `AZURE_1` | `#4A7FB5` | Blue accent (first series in COLORWAY) |
| `AZURE_2` | `#6B9FD4` | Secondary azure |
| `AZURE_3` | `#8BB5E0` | Tertiary azure |
| `AZURE_4` | `#A8C8E8` | Light azure |
| `AZURE_PALE` | `#D6E4F4` | Azure background tint |
| `SLATE_1` | `#6B8090` | Neutral grey (second series in COLORWAY) |
| `SLATE_2` | `#8FA4B4` | Secondary slate |
| `SLATE_3` | `#B0C4D0` | Tertiary slate |
| `SLATE_4` | `#C8D8E2` | Light slate |

### Backgrounds & surfaces
| Token | Hex | Use |
|-------|-----|-----|
| `BG_PAGE` | `#F5F7F8` | Page background (`html.Div` body) |
| `BG_SURFACE` | `#FFFFFF` | Card and sidebar background |
| `BORDER` | `#D8E0E6` | Card borders, dividers, axis lines |
| `GRID` | `#E6ECF0` | Chart gridlines |
| `ZERO_LINE` | `#C5D0D8` | Chart zero reference line |

### Text
| Token | Hex | Use |
|-------|-----|-----|
| `TEXT` | `#2D3339` | Primary text (headings, labels) |
| `SUBTEXT` | `#6B7A85` | Secondary text (subtitles, axis ticks, footer) |
| `MUTED` | `#95A5B0` | Tertiary text (disabled, placeholder) |

### Semantic colours
| Token | Hex | Use |
|-------|-----|-----|
| `POSITIVE` | `#4A9B6F` | Growth, surplus, improvement |
| `NEGATIVE` | `#C0503A` | Decline, deficit, deterioration |
| `WARNING` | `#D4874A` | Caution, near-threshold |

### Chart colorway
```python
COLORWAY = [AZURE_1, SLATE_1, TEAL_1, AZURE_2, SLATE_2, TEAL_2, AZURE_3, SLATE_3]
```
8 colours cycling Azure → Slate → Teal. Applied automatically via the `teal` Plotly template.

---

## Rules
- Never hardcode hex values in `app.py` or chart calls — always use token names
- `POSITIVE` / `NEGATIVE` / `WARNING` are semantic — use only for directional meaning
- `TEAL_1` for active/selected states (tile slicer active tile, nav-item-active)
- Max 4 series in most charts (Cowan 4±1) — COLORWAY has 8 colours for edge cases only
