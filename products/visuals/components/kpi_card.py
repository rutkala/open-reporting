"""KPI card component."""
from dash import html

from products.visuals.lib.theme import BG_SURFACE, BORDER, NEGATIVE, POSITIVE, SUBTEXT, TEXT


def kpi_card(
    label: str,
    value: str,
    unit: str = "",
    trend: str = "",
    trend_color: str = "",
) -> html.Div:
    """
    Args:
        label:       KPI label (e.g. "Saldo fiskalne")
        value:       formatted value string (e.g. "-3.2")
        unit:        unit string (e.g. "% PKB"); use "%" for inline suffix
        trend:       optional trend text (e.g. "▲ +0.5 pp")
        trend_color: optional colour for trend text
    """
    if unit == "%":
        display_value = f"{value}%"
        unit = ""
    else:
        display_value = value

    children = [
        html.Div(label, style={
            "fontSize": "12px", "color": SUBTEXT, "marginBottom": "4px",
        }),
        html.Div(style={"display": "flex", "alignItems": "baseline", "gap": "6px"}, children=[
            html.Span(display_value, style={
                "fontSize": "24px", "fontWeight": "700", "color": TEXT,
            }),
            html.Span(unit, style={
                "fontSize": "12px", "color": SUBTEXT,
            }) if unit else None,
        ]),
    ]
    if trend:
        children.append(html.Div(trend, style={
            "fontSize": "12px", "color": trend_color or SUBTEXT,
            "marginTop": "2px",
        }))
    return html.Div(style={
        "background": BG_SURFACE,
        "border": f"1px solid {BORDER}",
        "borderRadius": "8px",
        "padding": "14px 18px",
    }, children=children)
