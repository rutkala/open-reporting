"""
Financial chart variants.

candlestick — OHLC price action over time

y_measure (optional Measure):
  When provided, sets y-axis title, tickformat and ticksuffix.
"""
import plotly.graph_objects as go

from products.visuals.lib.theme import (
    POSITIVE, NEGATIVE, BORDER, GRID, SUBTEXT, TEXT, ZERO_LINE, FONT_FAMILY,
)
from products.visuals.components import PLOT_H, MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B, _chart


def _rgba(hex_color: str, alpha: float = 0.6) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def candlestick(title, dates, open_, high, low, close, subtitle="", y_measure=None):
    """
    Candlestick chart — OHLC financial data.
    Green candle = close > open (price rose).
    Red candle   = close < open (price fell).

    Args:
        dates:     list of date strings or datetime objects
        open_:     list of opening prices
        high:      list of high prices
        low:       list of low prices
        close:     list of closing prices
        y_measure: when provided, sets y-axis title, tickformat and ticksuffix
    """
    fig = go.Figure(go.Candlestick(
        x=dates,
        open=open_, high=high, low=low, close=close,
        increasing=dict(line=dict(color=POSITIVE), fillcolor=_rgba(POSITIVE, 0.6)),
        decreasing=dict(line=dict(color=NEGATIVE), fillcolor=_rgba(NEGATIVE, 0.6)),
        hoverinfo="x+y",
    ))

    yaxis = dict(
        showgrid=True, gridcolor=GRID, zerolinecolor=ZERO_LINE,
        tickfont=dict(size=11, color=SUBTEXT),
    )
    if y_measure is not None:
        y_measure.apply_to_yaxis(yaxis)

    fig.update_layout({
        "template": "teal",
        "height": PLOT_H,
        "margin": dict(l=MARGIN_L, r=MARGIN_R, t=MARGIN_T, b=MARGIN_B),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "xaxis": dict(
            showgrid=False, showline=True, linecolor=BORDER,
            tickfont=dict(size=11, color=SUBTEXT),
            rangeslider=dict(visible=False),
        ),
        "yaxis": yaxis,
        "showlegend": False,
        "hovermode": "x",
    })

    return _chart(title=title, subtitle=subtitle, figure=fig)
