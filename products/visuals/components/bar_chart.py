"""
Bar and column chart variants.
KB reference: team/analytics/visualization/charts/bar.md

Rules applied:
- All variants enforce rangemode="tozero" (never truncate axis)
- bar_horizontal: sorted descending by default (largest at top)
- bar_diverging: uses POSITIVE/NEGATIVE semantic colours from theme
- Value labels available via show_labels=True
"""
import plotly.graph_objects as go

from products.visuals.lib.theme import COLORWAY, POSITIVE, NEGATIVE, SLATE_1, SUBTEXT, TEXT
from products.visuals.components import PLOT_H, _plotly_layout, _chart


def bar_grouped(title, x, series, subtitle="", show_labels=False, reference=None):
    """
    Grouped (clustered) bar chart — multiple series side by side.

    Args:
        x:          category labels
        series:     list of {"name": str, "y": list, "color": str (optional)}
        show_labels: display value labels above bars
        reference:  {"value": float, "label": str} — horizontal reference line
    """
    fig = go.Figure()
    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Bar(
            x=x, y=s["y"], name=s["name"],
            marker_color=color,
            text=[str(v) for v in s["y"]] if show_labels else None,
            textposition="outside" if show_labels else "none",
            textfont=dict(size=11, color=SUBTEXT),
        ))

    layout = _plotly_layout(barmode="group", yaxis={"rangemode": "tozero"})
    if reference:
        layout["shapes"] = [dict(
            type="line", x0=-0.5, x1=len(x) - 0.5,
            y0=reference["value"], y1=reference["value"],
            line=dict(color=SLATE_1, width=1.5, dash="dash"),
        )]
        layout["annotations"] = [dict(
            x=len(x) - 0.5, y=reference["value"],
            text=reference.get("label", ""), showarrow=False,
            font=dict(size=11, color=SLATE_1), xanchor="right", yanchor="bottom",
        )]
    fig.update_layout(layout)

    legend = [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)] if len(series) > 1 else None
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)


def bar_stacked(title, x, series, subtitle="", pct=False, show_labels=False):
    """
    Stacked bar chart — shows total AND composition.

    Args:
        pct:        if True, normalise to 100% (composition-only view)
        show_labels: display value labels inside bars
    """
    fig = go.Figure()
    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Bar(
            x=x, y=s["y"], name=s["name"],
            marker_color=color,
            text=[f"{v}%" if pct else str(v) for v in s["y"]] if show_labels else None,
            textposition="inside" if show_labels else "none",
            textfont=dict(size=11, color="white"),
        ))

    barmode = "stack" if not pct else "relative"
    layout = _plotly_layout(barmode=barmode, yaxis={"rangemode": "tozero"})
    fig.update_layout(layout)

    legend = [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)]
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)


def bar_horizontal(title, categories, values, subtitle="", color=None, show_labels=True):
    """
    Horizontal bar chart — for rankings and long category labels.
    Sorted descending by default (largest at top, per KB).

    Args:
        categories: list of category labels
        values:     list of numeric values
        color:      single colour for all bars (default: AZURE_1)
        show_labels: display value labels outside bars
    """
    from products.visuals.lib.theme import AZURE_1
    bar_color = color or AZURE_1

    # Sort descending (largest at top)
    pairs = sorted(zip(values, categories), reverse=True)
    sorted_values = [p[0] for p in pairs]
    sorted_cats = [p[1] for p in pairs]

    fig = go.Figure(go.Bar(
        x=sorted_values, y=sorted_cats,
        orientation="h",
        marker_color=bar_color,
        text=[str(v) for v in sorted_values] if show_labels else None,
        textposition="outside" if show_labels else "none",
        textfont=dict(size=11, color=SUBTEXT),
    ))

    layout = _plotly_layout(
        xaxis={"rangemode": "tozero", "showgrid": True, "gridcolor": "#E6ECF0"},
        yaxis={"showgrid": False, "automargin": True, "tickfont": dict(size=11)},
    )
    layout["hovermode"] = "y unified"
    fig.update_layout(layout)

    return _chart(title=title, subtitle=subtitle, figure=fig)


def bar_diverging(title, x, values, subtitle="", show_labels=False):
    """
    Diverging bar chart — positive/negative from zero.
    Uses POSITIVE (green) for increases, NEGATIVE (red) for decreases.

    Args:
        values: list of numeric values (positive and/or negative)
    """
    colors = [POSITIVE if v >= 0 else NEGATIVE for v in values]

    fig = go.Figure(go.Bar(
        x=x, y=values,
        marker_color=colors,
        text=[str(v) for v in values] if show_labels else None,
        textposition="outside" if show_labels else "none",
        textfont=dict(size=11, color=SUBTEXT),
    ))

    fig.update_layout(_plotly_layout(
        yaxis={"zeroline": True, "zerolinewidth": 1.5, "zerolinecolor": "#C5D0D8"},
    ))

    return _chart(title=title, subtitle=subtitle, figure=fig)
