"""
Open Reporting visual theme — Teal/Azure/Slate palette derived from the project logo.

Import this module to activate the 'teal' Plotly template globally:
    import products.visuals.lib.theme as _theme  # noqa: F401
"""
import plotly.graph_objects as go
import plotly.io as pio

# ── Logo-derived core colors ──────────────────────────────────────────────────
TEAL_PRIMARY  = "#55A1AA"
AZURE_PRIMARY = "#4A7FB5"
CHARCOAL      = "#2D3339"

# ── Teal family (green-leaning) ───────────────────────────────────────────────
TEAL_1    = "#4A9B8F"
TEAL_2    = "#55A1AA"
TEAL_3    = "#6BB5A8"
TEAL_4    = "#8BC4C7"
TEAL_PALE = "#D7F3F0"

# ── Azure family (blue-leaning) ───────────────────────────────────────────────
AZURE_1    = "#4A7FB5"
AZURE_2    = "#6B9FD4"
AZURE_3    = "#8BB5E0"
AZURE_4    = "#A8C8E8"
AZURE_PALE = "#D6E4F4"

# ── Slate family (neutral greys) ──────────────────────────────────────────────
SLATE_1 = "#6B8090"
SLATE_2 = "#8FA4B4"
SLATE_3 = "#B0C4D0"
SLATE_4 = "#C8D8E2"

# ── Backgrounds / surfaces ────────────────────────────────────────────────────
BG_PAGE    = "#F5F7F8"
BG_SURFACE = "#FFFFFF"
BORDER     = "#D8E0E6"
GRID       = "#E6ECF0"
ZERO_LINE  = "#C5D0D8"
TEXT       = CHARCOAL
SUBTEXT    = "#6B7A85"
MUTED      = "#95A5B0"

# ── Semantic colors ───────────────────────────────────────────────────────────
POSITIVE = "#4A9B6F"
NEGATIVE = "#C0503A"
WARNING  = "#D4874A"

# ── Chart colorway (8 colors: azure, slate, teal alternating) ─────────────────
COLORWAY = [AZURE_1, SLATE_1, TEAL_1, AZURE_2, SLATE_2, TEAL_2, AZURE_3, SLATE_3]

FONT_FAMILY = "Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"

# ── Plotly template ───────────────────────────────────────────────────────────
_axis = dict(
    gridcolor=GRID,
    linecolor=BORDER,
    tickfont=dict(color=SUBTEXT, size=11),
    zerolinecolor=ZERO_LINE,
    showgrid=True,
)

pio.templates["teal"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=COLORWAY,
        font=dict(family=FONT_FAMILY, size=13, color=TEXT),
        title=dict(font=dict(size=17, color=TEXT), x=0.0, xanchor="left"),
        margin=dict(l=48, r=24, t=48, b=40),
        xaxis=_axis,
        yaxis=_axis,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=12),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hovermode="x unified",
        hoverlabel=dict(bgcolor=BG_SURFACE, bordercolor=BORDER, font=dict(size=12)),
    ),
    data=dict(
        scatter=[go.Scatter(line=dict(width=2), marker=dict(size=5))],
        bar=[go.Bar(marker=dict(line=dict(width=0)))],
    ),
)

pio.templates.default = "simple_white+teal"
