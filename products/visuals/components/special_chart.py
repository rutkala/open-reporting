"""
Special chart variants: funnel, treemap, gauge, bullet, ribbon (bump), heatmap_matrix.

funnel       — conversion / pipeline stages
treemap      — hierarchical composition (area = value)
gauge        — single KPI vs range (use sparingly — bullet is usually better)
bullet       — KPI vs target with performance bands (better than gauge)
ribbon       — rank changes over time (bump chart)
heatmap_matrix — correlation or cross-tab colour matrix
"""
import plotly.graph_objects as go

from products.visuals.lib.theme import (
    COLORWAY, AZURE_1, AZURE_PALE, POSITIVE, NEGATIVE, WARNING,
    BORDER, GRID, SLATE_1, SLATE_4, SUBTEXT, TEXT, ZERO_LINE, FONT_FAMILY,
    TEAL_1, TEAL_PALE, BG_SURFACE,
)
from products.visuals.components import PLOT_H, PLOT_H_TALL, MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B, _chart


def _base(height=None, **kw):
    h = height or PLOT_H
    return {
        "template": "teal",
        "height": h,
        "margin": dict(l=MARGIN_L, r=MARGIN_R, t=MARGIN_T, b=MARGIN_B),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "showlegend": False,
        **kw,
    }


def funnel(title, stages, values, subtitle=""):
    """
    Funnel chart — conversion or pipeline stages.
    Stages ordered top-to-bottom; values decrease down the funnel.

    Args:
        stages: list of stage labels (top to bottom)
        values: list of numeric values (same length as stages)
    """
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textposition="inside",
        textinfo="value+percent initial",
        textfont=dict(size=12, color="white"),
        marker=dict(
            color=[COLORWAY[i % len(COLORWAY)] for i in range(len(stages))],
            line=dict(width=1, color="white"),
        ),
        connector=dict(line=dict(color=BORDER, dash="dot", width=1)),
    ))
    fig.update_layout(_base(hovermode="closest"))
    return _chart(title=title, subtitle=subtitle, figure=fig)


def treemap(title, labels, parents, values, subtitle=""):
    """
    Treemap — hierarchical composition, area proportional to value.

    Args:
        labels:  list of node labels (root has parent "")
        parents: list of parent labels for each node (root = "")
        values:  list of numeric values

    Example:
        treemap("Budżet", ["Razem","Dochody","Wydatki","VAT","PIT","Świadczenia"],
                          ["","Razem","Razem","Dochody","Dochody","Wydatki"],
                          [0, 615, 665, 295, 135, 390])
    """
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        textinfo="label+value+percent parent",
        textfont=dict(size=12),
        marker=dict(
            colorscale=[[0, TEAL_PALE], [1, TEAL_1]],
            line=dict(width=1, color="white"),
        ),
        hovertemplate="<b>%{label}</b><br>Wartość: %{value}<br>Udział: %{percentParent:.1%}<extra></extra>",
    ))
    fig.update_layout(_base(margin=dict(l=0, r=0, t=4, b=0)))
    return _chart(title=title, subtitle=subtitle, figure=fig)


def gauge(title, value, min_val=0, max_val=100, subtitle="", reference=None, suffix=""):
    """
    Gauge chart — single KPI vs range.
    Note: prefer bullet() for KPI vs target — gauge is best for speed/progress metaphors.

    Args:
        value:     current value
        min_val:   minimum of gauge range
        max_val:   maximum of gauge range
        reference: target value (shown as threshold line)
        suffix:    unit suffix (e.g. "%", " mld")
    """
    steps = [
        dict(range=[min_val, max_val * 0.5], color=SLATE_4),
        dict(range=[max_val * 0.5, max_val * 0.75], color=AZURE_PALE),
        dict(range=[max_val * 0.75, max_val], color=TEAL_PALE),
    ]
    threshold = dict(line=dict(color=POSITIVE, width=3), thickness=0.75, value=reference) if reference else None

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(suffix=suffix, font=dict(size=28, color=TEXT)),
        gauge=dict(
            axis=dict(range=[min_val, max_val], tickfont=dict(size=10, color=SUBTEXT)),
            bar=dict(color=AZURE_1, thickness=0.3),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=steps,
            threshold=threshold,
        ),
    ))
    fig.update_layout(_base(height=220, margin=dict(l=30, r=30, t=20, b=10)))
    return _chart(title=title, subtitle=subtitle, figure=fig, height=220)


def bullet(title, value, target, min_val=0, max_val=None, subtitle="", suffix=""):
    """
    Bullet chart — KPI value vs target with performance bands.
    Superior to gauge: clearer, more compact, works in grids.

    Args:
        value:   actual value
        target:  target / benchmark value
        min_val: range minimum (default 0)
        max_val: range maximum (default: 120% of max(value, target))
        suffix:  unit suffix
    """
    if max_val is None:
        max_val = max(value, target) * 1.25

    # Performance bands: poor / acceptable / good
    band = max_val - min_val
    bands = [min_val + band * 0.5, min_val + band * 0.75, max_val]

    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta",
        value=value,
        delta=dict(
            reference=target,
            increasing=dict(color=POSITIVE),
            decreasing=dict(color=NEGATIVE),
            font=dict(size=14),
        ),
        number=dict(suffix=suffix, font=dict(size=24, color=TEXT)),
        gauge=dict(
            shape="bullet",
            axis=dict(range=[min_val, max_val], tickfont=dict(size=10, color=SUBTEXT)),
            bar=dict(color=AZURE_1, thickness=0.35),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[
                dict(range=[min_val, bands[0]], color=SLATE_4),
                dict(range=[bands[0], bands[1]], color=AZURE_PALE),
                dict(range=[bands[1], bands[2]], color=TEAL_PALE),
            ],
            threshold=dict(
                line=dict(color=TEXT, width=2),
                thickness=0.75,
                value=target,
            ),
        ),
    ))
    fig.update_layout(_base(height=160, margin=dict(l=60, r=40, t=30, b=20)))
    return _chart(title=title, subtitle=subtitle, figure=fig, height=160)


def ribbon(title, x, series, subtitle=""):
    """
    Ribbon / bump chart — rank changes over time.
    Shows how positions change across time periods.
    Lower rank number = better position (rank 1 = top).

    Args:
        x:      list of time periods
        series: list of {"name": str, "ranks": list of int (1 = best)}
    """
    fig = go.Figure()
    n_ranks = len(series)

    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        ranks = s["ranks"]
        # Invert ranks for display (rank 1 at top)
        y_vals = [n_ranks + 1 - r for r in ranks]

        fig.add_trace(go.Scatter(
            x=x, y=y_vals, name=s["name"],
            mode="lines+markers+text",
            line=dict(color=color, width=3, shape="spline"),
            marker=dict(size=10, color=color, line=dict(color="white", width=2)),
            text=[s["name"] if xi == len(x) - 1 else "" for xi in range(len(x))],
            textposition="middle right",
            textfont=dict(size=11, color=color),
            hovertemplate=f"<b>{s['name']}</b><br>%{{x}}: Miejsce %{{customdata}}<extra></extra>",
            customdata=ranks,
        ))

    tick_vals = list(range(1, n_ranks + 1))
    tick_text = [str(n_ranks + 1 - v) for v in tick_vals]

    fig.update_layout({
        "template": "teal",
        "height": PLOT_H,
        "margin": dict(l=MARGIN_L, r=80, t=MARGIN_T, b=MARGIN_B),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "xaxis": dict(showgrid=False, showline=True, linecolor=BORDER,
                      tickfont=dict(size=11, color=SUBTEXT)),
        "yaxis": dict(
            showgrid=True, gridcolor=GRID,
            tickvals=tick_vals, ticktext=tick_text,
            tickfont=dict(size=11, color=SUBTEXT),
            title=dict(text="Miejsce", font=dict(size=11, color=SUBTEXT)),
            range=[0.5, n_ranks + 0.5],
        ),
        "showlegend": False,
        "hovermode": "closest",
    })

    return _chart(title=title, subtitle=subtitle, figure=fig)


def heatmap_matrix(title, x_labels, y_labels, z_values, subtitle="",
                   color_scale="teal", show_values=True):
    """
    Heatmap matrix — colour-encoded grid (e.g. correlation matrix, cross-tab).

    Args:
        x_labels:    column labels
        y_labels:    row labels
        z_values:    2D list [rows][cols] of numeric values
        color_scale: "teal" (sequential) | "diverging" (neg/pos)
        show_values: overlay numeric values on cells
    """
    if color_scale == "diverging":
        cscale = [[0, NEGATIVE], [0.5, "#FFFFFF"], [1, POSITIVE]]
    else:
        cscale = [[0, TEAL_PALE], [1, TEAL_1]]

    text_vals = [[f"{v:.2f}" if isinstance(v, float) else str(v) for v in row]
                 for row in z_values] if show_values else None

    h = max(PLOT_H, len(y_labels) * 36 + 80)

    fig = go.Figure(go.Heatmap(
        x=x_labels,
        y=y_labels,
        z=z_values,
        colorscale=cscale,
        text=text_vals,
        texttemplate="%{text}" if show_values else "",
        textfont=dict(size=11),
        hovertemplate="%{y} × %{x}<br>Wartość: %{z}<extra></extra>",
        showscale=True,
        colorbar=dict(
            thickness=12, len=0.8,
            tickfont=dict(size=10, color=SUBTEXT),
            outlinewidth=0,
        ),
        xgap=2, ygap=2,
    ))

    fig.update_layout({
        "template": "teal",
        "height": h,
        "margin": dict(l=MARGIN_L + 20, r=60, t=MARGIN_T, b=MARGIN_B + 20),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "xaxis": dict(side="bottom", tickfont=dict(size=11, color=SUBTEXT), tickangle=-30),
        "yaxis": dict(tickfont=dict(size=11, color=SUBTEXT), autorange="reversed"),
        "showlegend": False,
    })

    return _chart(title=title, subtitle=subtitle, figure=fig, height=h)
