"""
Waterfall chart variants.
KB reference: team/analytics/visualization/charts/waterfall.md

Rules applied:
- Uses Plotly native go.Waterfall (built-in connector lines)
- POSITIVE (green) for increases, NEGATIVE (red) for decreases, SLATE_1 for totals
- Value labels on every bar (KB requirement)
- Sorted by magnitude unless logical order is needed (caller's responsibility)

y_measure (optional Measure):
  When provided, sets y-axis title, tickformat and ticksuffix, and formats
  bar value labels via measure.format_value().
"""
import plotly.graph_objects as go

from products.visuals.lib.theme import (
    POSITIVE, NEGATIVE, SLATE_1, SUBTEXT, TEXT, BORDER, GRID, ZERO_LINE,
)
from products.visuals.components import PLOT_H, MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B, _chart
from products.visuals.lib.theme import FONT_FAMILY


def _wf_layout():
    return {
        "template": "teal",
        "height": PLOT_H,
        "margin": dict(l=MARGIN_L, r=MARGIN_R, t=MARGIN_T, b=MARGIN_B),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "xaxis": dict(showgrid=False, showline=True, linecolor=BORDER,
                      tickfont=dict(size=11, color=SUBTEXT)),
        "yaxis": dict(gridcolor=GRID, zerolinecolor=ZERO_LINE, showgrid=True,
                      tickfont=dict(size=11, color=SUBTEXT)),
        "showlegend": False,
        "hovermode": "x",
    }


def waterfall_contribution(title, categories, values, subtitle="", total_label="Total",
                           y_measure=None):
    """
    Contribution waterfall — how components sum to a total.
    Last bar is the total (anchored to zero, rendered in SLATE_1).

    Args:
        categories:  list of category labels (last is total)
        values:      list of component values; last value should equal sum of the rest
        total_label: label override for the total bar
        y_measure:   when provided, sets y-axis title/format and formats bar labels
    """
    n = len(categories)
    measures = ["relative"] * (n - 1) + ["total"]

    if y_measure is not None:
        text_labels = [y_measure.format_value(v) for v in values]
    else:
        text_labels = [str(round(v, 1)) for v in values]

    fig = go.Figure(go.Waterfall(
        x=categories,
        y=values,
        measure=measures,
        text=text_labels,
        textposition="outside",
        textfont=dict(size=11, color=SUBTEXT),
        connector=dict(line=dict(color=SLATE_1, width=1, dash="dot")),
        increasing=dict(marker=dict(color=POSITIVE)),
        decreasing=dict(marker=dict(color=NEGATIVE)),
        totals=dict(marker=dict(color=SLATE_1)),
    ))

    layout = _wf_layout()
    if y_measure is not None:
        y_measure.apply_to_yaxis(layout["yaxis"])
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, figure=fig)


def waterfall_variance(title, categories, values, subtitle="",
                       base_label="Base", final_label="Result", y_measure=None):
    """
    Variance waterfall — explains how a base value becomes the final value.
    First bar is the base (absolute), middle bars are contributions, last bar is total.

    Args:
        categories:  list including base and final labels
        values:      first value = base (absolute), rest = contributions
        base_label:  label shown for base bar (informational)
        final_label: label shown for final bar (informational)
        y_measure:   when provided, sets y-axis title/format and formats bar labels
    """
    n = len(categories)
    measures = ["absolute"] + ["relative"] * (n - 2) + ["total"]

    if y_measure is not None:
        text_labels = [y_measure.format_value(v) for v in values]
    else:
        text_labels = [str(round(v, 1)) for v in values]

    fig = go.Figure(go.Waterfall(
        x=categories,
        y=values,
        measure=measures,
        text=text_labels,
        textposition="outside",
        textfont=dict(size=11, color=SUBTEXT),
        connector=dict(line=dict(color=SLATE_1, width=1, dash="dot")),
        increasing=dict(marker=dict(color=POSITIVE)),
        decreasing=dict(marker=dict(color=NEGATIVE)),
        totals=dict(marker=dict(color=SLATE_1)),
    ))

    layout = _wf_layout()
    if y_measure is not None:
        y_measure.apply_to_yaxis(layout["yaxis"])
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, figure=fig)
