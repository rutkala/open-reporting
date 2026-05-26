# Visualisation Standard

**Derived from:** `docs/visualization/principles.md` ✓ + `docs/visualization/ui-principles.md` ✓ + `docs/visualization/charts/*.md` ✓ + `docs/ux-perception/principles.md` ✓ (IBCS SUCCESS, Gestalt, pre-attentive attributes, Cowan 4±1 working memory, WCAG 2.2, eye-tracking patterns, chart-type selection)
**Used by builders:** `dashboard-dev` (building dashboards in `products/dashboards/` and components in `packages/dbr/src/dbr/visuals/`)
**Evaluated by:** `visual-screenshot-reviewer` (rendered output)
**Does NOT cover:** number formatting (see `measures.md`), KPI selection theory (see `business-analysis` KB), domain-specific framing (see `domains/{domain}.md` KB)

---

## Design Philosophy

Scandinavian / Nordic minimal style. Clean, functional, editorial. Colour is used to carry meaning, not for decoration. Typography and whitespace do the heavy lifting.

---

## Page Structure

Every dashboard page contains these blocks in this order:

```
┌─────────────────────────────────────────┐
│  HEADER  (logo, navigation)             │
├──────────┬──────────────────────────────┤
│  FILTER  │  MAIN CANVAS                 │
│  PANE    │  ┌── Topic Group A ────────┐ │
│          │  │  ┌────┐  ┌────┐        │ │
│          │  │  │card│  │card│        │ │
│          │  │  └────┘  └────┘        │ │
│          │  └────────────────────────┘ │
│          │  ┌── Topic Group B ────────┐ │
│          │  │  ┌─────────────────┐   │ │
│          │  │  │      card       │   │ │
│          │  │  └─────────────────┘   │ │
│          │  └────────────────────────┘ │
└──────────┴──────────────────────────────┤
│  FOOTER  (source, last updated)         │
└─────────────────────────────────────────┘
```

### Visual Layering

```
Page background      #F7F8FA  — the "table", light grey
└── Topic group      #F7F8FA  — same grey, separated by spacing + optional label
    └── Chart card   #FFFFFF  — white "paper" with subtle shadow
        └── Figure   transparent — Plotly figure, no own background
```

The "paper on table" effect is achieved through:
- White card background
- Subtle box shadow: `box-shadow: 0 1px 4px rgba(0,0,0,0.07), 0 0 1px rgba(0,0,0,0.04)`
- Rounded corners: `border-radius: 6px`
- No border needed — shadow provides the separation

### Blocks

- **Header** — logo, site navigation, dashboard title
- **Filter pane** — year, region, category selectors (left sidebar, 220px)
- **Topic group** — groups related charts under a section heading, grey background
- **Chart card** — individual chart, table, or KPI tile — always white with shadow
- **Footer** — data source attribution, last updated date, domain

---

## Colour Palette

```python
# backgrounds
BG_PAGE     = "#F7F8FA"   # page body, paper_bgcolor — light cool grey
BG_SURFACE  = "#FFFFFF"   # cards, header, footer
BG_PLOT     = "#F7F8FA"   # plot_bgcolor — same as page (flat look)

# borders and structure
BORDER      = "#DDE2E8"   # card borders, dividers
GRID        = "#E8ECF0"   # chart gridlines
ZERO_LINE   = "#C8CDD5"   # zero axis line

# text
TEXT        = "#2C3A4A"   # titles, labels — high contrast
SUBTEXT     = "#6B7A8D"   # axis ticks, units, secondary text
MUTED       = "#9BABB8"   # footnotes only

# data palette (azure/slate — use in order)
AZURE_1     = "#4A7FB5"   # primary series
AZURE_2     = "#7BAFD4"   # second series
AZURE_3     = "#A8C8E8"   # third series / area fill
SLATE_1     = "#6B8FA6"   # fourth series
SLATE_2     = "#9BB5C4"   # fifth series
SLATE_3     = "#C5D8E3"   # sixth / background fill
SAGE        = "#5A7A6E"   # accent / diverging complement
WARM_GREY   = "#B5C4C1"   # neutral

# semantic (annotations only — not main palette)
POSITIVE    = "#4A9B6F"   # growth, surplus
NEGATIVE    = "#C0503A"   # decline, deficit
WARNING     = "#D4874A"   # caution
```

**Rules:**
- Max 2-3 colours per chart
- Use palette in order (AZURE_1 first, then AZURE_2, etc.)
- Semantic colours (POSITIVE, NEGATIVE, WARNING) only for explicit meaning — never decoration
- Never use bright or saturated colours

---

## Typography

```python
FONT_FAMILY = "Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"
```

No external font loading required — system font stack. If Inter is available locally it will be used.

| Element | Size | Weight | Colour |
|---------|------|--------|--------|
| Dashboard title (HTML) | 28px | 700 | TEXT |
| Chart title | 16-18px | 600 | TEXT |
| Axis title | 12px | 400 | SUBTEXT |
| Axis tick labels | 11px | 400 | SUBTEXT |
| Legend | 12px | 400 | TEXT |
| Footer / source | 12px | 400 | SUBTEXT |
| Footnotes | 11px | 400 | MUTED |

---

## Plotly Template

Register once in `charts/lib/theme.py`, applied automatically to all figures:

```python
import plotly.graph_objects as go
import plotly.io as pio

pio.templates["nordic"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",   # transparent — white comes from HTML card
        plot_bgcolor="rgba(0,0,0,0)",    # transparent — white comes from HTML card
        colorway=["#4A7FB5","#7BAFD4","#A8C8E8","#6B8FA6","#9BB5C4","#C5D8E3","#5A7A6E","#B5C4C1"],
        font=dict(family="Inter, 'Segoe UI', system-ui, sans-serif", size=13, color="#2C3A4A"),
        title=dict(font=dict(size=18, color="#2C3A4A"), x=0.0, xanchor="left"),
        margin=dict(l=48, r=24, t=48, b=40),
        xaxis=dict(gridcolor="#E8ECF0", linecolor="#DDE2E8", tickfont=dict(color="#6B7A8D", size=11), zerolinecolor="#C8CDD5", showgrid=True),
        yaxis=dict(gridcolor="#E8ECF0", linecolor="#DDE2E8", tickfont=dict(color="#6B7A8D", size=11), zerolinecolor="#C8CDD5", showgrid=True),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=12), orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#DDE2E8", font=dict(size=12)),
    ),
    data=dict(
        scatter=[go.Scatter(line=dict(width=2), marker=dict(size=5))],
        bar=[go.Bar(marker=dict(line=dict(width=0)))],
    ),
)

pio.templates.default = "simple_white+nordic"
```

Import `charts.lib.theme` in any script to activate — no need to pass `template=` on each figure.

---

## Chart Types

**Preferred:**
- Bar (vertical or horizontal) — comparisons, rankings
- Line — time series, trends
- Area — cumulative, composition over time
- Scatter — correlations
- Table — precise values alongside charts

**Avoid:**
- Pie / donut — hard to read, use bar instead
- 3D charts — never
- Dual Y-axis — confusing, split into two charts instead
- Bubble charts — only with clear justification

---

## Required Elements on Every Dashboard

- [ ] Dashboard title and subtitle (what is shown, what period)
- [ ] Source attribution in footer: `Dane: {source} — aktualizacja: {date}`
- [ ] Last updated date
- [ ] Chart titles — every chart has a title
- [ ] Axis labels with units where relevant
- [ ] Polish language for all user-facing text

---

## HTML Page Generation

```python
# Generate figure as div fragment (no outer HTML, no inline JS)
from plotly.io import to_html

div = to_html(fig,
    include_plotlyjs=False,   # loaded once in page <head>
    full_html=False,
    config={"displayModeBar": False, "responsive": True}
)
```

Load Plotly.js once per page:
```html
<script src="https://cdn.plot.ly/plotly-3.0.0.min.js"></script>
```

Output path: `nginx/html/{domain}/{dashboard-name}.html`

---

## Layout Rules

- Charts grouped by topic — related charts in the same visual group
- Max 2 charts side by side in a grid
- Every chart in a card (`background: #FFFFFF, border-radius: 6px, box-shadow: 0 1px 4px rgba(0,0,0,0.07), 0 0 1px rgba(0,0,0,0.04)`) — no border, shadow provides separation
- Topic groups use grey background (`#F7F8FA`) with a section heading label above the cards
- Consistent padding: 24px gap between cards
- No chart without a title
- No orphaned charts — every chart belongs to a section
