#!/usr/bin/env python3
"""
Open Reporting — Reusable chart components.
Title/subtitle/legend as HTML, Plotly renders only the chart area.

Common settings (change here to affect all charts):
  PLOT_H      — standard chart height in px
  PLOT_H_TALL — tall chart height (combo subplots, tables)
  MARGIN_*    — chart margins

All chart functions are KB-grounded:
  bar_chart.py        — bar.md
  line_chart.py       — line.md
  combo_chart.py      — combo-subplots.md
  waterfall_chart.py  — waterfall.md
  scatter_chart.py    — scatter.md
  table_chart.py      — table.md
"""
from dash import dcc, html
import plotly.graph_objects as go

import products.visuals.lib.theme as _theme  # noqa: F401 — registers 'teal' template
from products.visuals.lib.theme import (
    BG_SURFACE, BORDER, COLORWAY, GRID,
    NEGATIVE, POSITIVE, SUBTEXT, TEXT, ZERO_LINE,
    FONT_FAMILY,
    TEAL_1, TEAL_2, TEAL_3, TEAL_4, TEAL_PALE,
    AZURE_1, AZURE_2, AZURE_3, AZURE_4, AZURE_PALE,
    SLATE_1, SLATE_2, SLATE_3, SLATE_4,
)

# ── Chart dimensions ──────────────────────────────────────────────────────────
PLOT_H      = 280    # standard chart height
PLOT_H_TALL = 400    # combo subplots, waterfall with many steps
MARGIN_L    = 40
MARGIN_R    = 16
MARGIN_T    = 4
MARGIN_B    = 40


def _plotly_layout(height=None, **kw):
    """Base Plotly layout — chart area only, no title/legend (those are HTML)."""
    h = height if height is not None else PLOT_H
    return {
        "template": "teal",
        "height": h,
        "margin": dict(l=MARGIN_L, r=MARGIN_R, t=MARGIN_T, b=MARGIN_B),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "xaxis": dict(
            gridcolor="rgba(0,0,0,0)", zerolinecolor=ZERO_LINE,
            tickfont=dict(size=11, color=SUBTEXT),
            showgrid=False, showline=True, linecolor=BORDER,
        ),
        "yaxis": dict(
            gridcolor=GRID, zerolinecolor=ZERO_LINE,
            tickfont=dict(size=11, color=SUBTEXT),
            showgrid=True, gridwidth=1,
            ticklabelstandoff=8,
            automargin=True,
        ),
        "showlegend": False,
        "hovermode": "x unified",
        **kw,
    }


def _chart(title, subtitle="", legend_items=None, figure=None, height=None):
    """Wrap a Plotly figure with an HTML title/subtitle/legend header."""
    h = height if height is not None else PLOT_H
    children = []

    children.append(html.Div(title, style={
        "fontSize": "14px", "fontWeight": "600", "color": TEXT,
        "marginBottom": "4px",
    }))

    if subtitle:
        children.append(html.Div(subtitle, style={
            "fontSize": "12px", "color": SUBTEXT,
            "marginBottom": "8px",
        }))

    if legend_items:
        leg = []
        for label, color in legend_items:
            leg.append(html.Div(style={
                "display": "flex", "alignItems": "center", "marginRight": "16px",
            }, children=[
                html.Div(style={
                    "width": "12px", "height": "12px", "borderRadius": "2px",
                    "backgroundColor": color, "marginRight": "6px", "flexShrink": 0,
                }),
                html.Span(label, style={"fontSize": "11px", "color": SUBTEXT}),
            ]))
        children.append(html.Div(style={
            "display": "flex", "alignItems": "center", "flexWrap": "wrap",
            "marginBottom": "12px",
        }, children=leg))

    # Explicit height keeps cards aligned in CSS grid
    children.append(dcc.Graph(
        figure=figure,
        config={"displayModeBar": False, "responsive": True},
        style={"width": "100%", "height": f"{h}px"},
    ))

    return html.Div(children=children)
