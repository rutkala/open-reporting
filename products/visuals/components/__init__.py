#!/usr/bin/env python3
"""
Open Reporting — Reusable chart components.
Title/subtitle/legend as HTML, Plotly renders only chart area.
"""
import plotly.graph_objects as go
from dash import dcc, html

import products.visuals.lib.theme as _theme  # noqa: F401 — registers 'teal' template
from products.visuals.lib.theme import (
    BG_SURFACE, BORDER, COLORWAY, GRID, MUTED,
    NEGATIVE, POSITIVE, SUBTEXT, TEXT, WARNING, ZERO_LINE,
    FONT_FAMILY, TEAL_1, TEAL_2, TEAL_3, TEAL_4, TEAL_PALE,
    AZURE_1, AZURE_2, AZURE_3, AZURE_4, AZURE_PALE,
    SLATE_1, SLATE_2, SLATE_3, SLATE_4,
)

# Fixed chart dimensions
PLOT_H   = 280
MARGIN_L = 30
MARGIN_R = 16
MARGIN_B = 40


def _plotly_layout(**kw):
    """Plotly layout — chart area only, no title/legend."""
    return {
        "template": "teal",
        "height": PLOT_H,
        "margin": dict(l=MARGIN_L, r=MARGIN_R, t=0, b=MARGIN_B),
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


def _chart(title, subtitle="", legend_items=None, figure=None):
    """HTML header + Plotly chart. Title/legend are HTML, Plotly renders only the chart area."""
    children = []

    # Title
    children.append(html.Div(title, style={
        "fontSize": "14px", "fontWeight": "600", "color": TEXT,
        "marginBottom": "4px",
    }))

    # Subtitle
    if subtitle:
        children.append(html.Div(subtitle, style={
            "fontSize": "12px", "color": SUBTEXT,
            "marginBottom": "8px",
        }))

    # Legend
    if legend_items:
        leg_items = []
        for label, color in legend_items:
            leg_items.append(html.Div(style={
                "display": "flex", "alignItems": "center", "marginRight": "16px",
            }, children=[
                html.Div(style={
                    "width": "12px", "height": "12px", "borderRadius": "2px",
                    "backgroundColor": color, "marginRight": "6px", "flexShrink": 0,
                }),
                html.Span(label, style={"fontSize": "11px", "color": SUBTEXT}),
            ]))
        children.append(html.Div(style={
            "display": "flex", "alignItems": "center", "marginBottom": "12px",
        }, children=leg_items))

    # Chart — explicit height so cards align uniformly in CSS grid
    children.append(dcc.Graph(
        figure=figure.update_layout(_plotly_layout()),
        config={"displayModeBar": False, "responsive": True},
        style={"width": "100%", "height": f"{PLOT_H}px"},
    ))

    return html.Div(children=children)
