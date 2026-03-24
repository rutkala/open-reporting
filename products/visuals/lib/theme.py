"""
Nordic/Scandinavian visual theme for Open Reporting dashboards.
Import this module to activate the 'nordic' Plotly template globally.
"""
import plotly.graph_objects as go
import plotly.io as pio

# ── Palette ───────────────────────────────────────────────────────────────────
BG_PAGE    = "#F7F8FA"
BG_SURFACE = "#FFFFFF"
BORDER     = "#DDE2E8"
GRID       = "#E8ECF0"
ZERO_LINE  = "#C8CDD5"
TEXT       = "#2C3A4A"
SUBTEXT    = "#6B7A8D"
MUTED      = "#9BABB8"

AZURE_1    = "#4A7FB5"
AZURE_2    = "#7BAFD4"
AZURE_3    = "#A8C8E8"
SLATE_1    = "#6B8FA6"
SLATE_2    = "#9BB5C4"
SLATE_3    = "#C5D8E3"
SAGE       = "#5A7A6E"
WARM_GREY  = "#B5C4C1"

POSITIVE   = "#4A9B6F"
NEGATIVE   = "#C0503A"
WARNING    = "#D4874A"

COLORWAY = [AZURE_1, AZURE_2, AZURE_3, SLATE_1, SLATE_2, SLATE_3, SAGE, WARM_GREY]

FONT_FAMILY = "Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"

# ── Plotly template ───────────────────────────────────────────────────────────
_axis = dict(
    gridcolor=GRID,
    linecolor=BORDER,
    tickfont=dict(color=SUBTEXT, size=11),
    zerolinecolor=ZERO_LINE,
    showgrid=True,
)

pio.templates["nordic"] = go.layout.Template(
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

pio.templates.default = "simple_white+nordic"
