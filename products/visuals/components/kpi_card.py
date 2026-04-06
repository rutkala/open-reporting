"""KPI card variants."""
from dash import html

from products.visuals.lib.theme import BG_SURFACE, BORDER, NEGATIVE, POSITIVE, SUBTEXT, TEXT


def kpi_row(cards: list, min_width: str = "180px", gap: str = "16px") -> html.Div:
    """
    Flex row container for multiple KPI cards.

    Wraps a list of kpi_standard() / kpi_compact() outputs so that cards
    share the row width evenly, stay the same height, and wrap gracefully
    on narrow screens.

    Args:
        cards:     list of html.Div outputs from kpi_standard() or kpi_compact()
        min_width: minimum width before a card wraps to the next row (default "180px")
        gap:       spacing between cards (default "16px")

    Usage:
        kpi_row([
            kpi_standard("Revenue",  measure_a.kpi_value(val_a), unit=measure_a.plotly_ticksuffix),
            kpi_standard("Expenses", measure_b.kpi_value(val_b), unit=measure_b.plotly_ticksuffix),
            kpi_standard("Balance",  measure_c.kpi_value(val_c), unit=measure_c.plotly_ticksuffix,
                         trend="▼ -0.4", trend_color=NEGATIVE),
        ])
    """
    wrapped = []
    for card in cards:
        # Each card gets flex:1 so they share width evenly; minWidth controls wrap breakpoint
        wrapped.append(html.Div(
            style={"flex": "1", "minWidth": min_width},
            children=[card],
        ))
    return html.Div(
        style={
            "display": "flex",
            "flexWrap": "wrap",
            "gap": gap,
            "alignItems": "stretch",
        },
        children=wrapped,
    )


def kpi_standard(
    label: str,
    value: str,
    unit: str = "",
    subtitle: str = "",
    reference_value: str = "",
    reference_label: str = "",
    trend: str = "",
    trend_color: str = "",
) -> html.Div:
    """
    Standard KPI card — label, large callout value, optional unit, subtitle,
    reference value and trend indicator.

    Args:
        label:           KPI title (e.g. "Fiscal balance")
        value:           formatted callout value string (e.g. "-3.2")
        unit:            unit string displayed next to value (e.g. "% GDP");
                         pass "%" to inline it directly into the value
        subtitle:        optional second line below title, above value
                         (e.g. "Average 2018–2024")
        reference_value: pre-formatted comparison number
                         (e.g. "80.0") — use Measure.format_value()
        reference_label: label for reference_value
                         (e.g. "Target", "Prior year", "EU avg")
        trend:           optional trend text (e.g. "▲ +0.8")
        trend_color:     colour for trend text; use POSITIVE/NEGATIVE from theme
    """
    if unit == "%":
        display_value = f"{value}%"
        unit = ""
    else:
        display_value = value

    children = [
        html.Div(label, style={
            "fontSize": "12px", "color": SUBTEXT, "marginBottom": "2px",
        }),
    ]

    if subtitle:
        children.append(html.Div(subtitle, style={
            "fontSize": "11px", "color": SUBTEXT, "marginBottom": "6px",
            "fontStyle": "italic",
        }))

    children.append(html.Div(
        style={"display": "flex", "alignItems": "baseline", "gap": "6px", "marginBottom": "4px"},
        children=[
            html.Span(display_value, style={
                "fontSize": "24px", "fontWeight": "700", "color": TEXT,
            }),
            html.Span(unit, style={"fontSize": "12px", "color": SUBTEXT}) if unit else None,
        ],
    ))

    if reference_value:
        children.append(html.Div(
            style={
                "display": "flex", "alignItems": "center", "gap": "6px",
                "marginBottom": "2px",
            },
            children=[
                html.Span(reference_label, style={"fontSize": "11px", "color": SUBTEXT})
                if reference_label else None,
                html.Span(reference_value, style={
                    "fontSize": "12px", "fontWeight": "600", "color": SUBTEXT,
                }),
            ],
        ))

    if trend:
        children.append(html.Div(trend, style={
            "fontSize": "12px",
            "color": trend_color or SUBTEXT,
            "marginTop": "2px",
        }))

    return html.Div(style={
        "background": BG_SURFACE,
        "border": f"1px solid {BORDER}",
        "borderRadius": "8px",
        "padding": "14px 18px",
    }, children=children)


def kpi_compact(
    label: str,
    value: str,
    unit: str = "",
    subtitle: str = "",
    reference_value: str = "",
    reference_label: str = "",
    trend: str = "",
    trend_color: str = "",
) -> html.Div:
    """
    Compact KPI card — smaller font, tighter padding, for dense rows.
    Same API as kpi_standard.
    """
    if unit == "%":
        display_value = f"{value}%"
        unit = ""
    else:
        display_value = value

    children = [
        html.Div(label, style={
            "fontSize": "11px", "color": SUBTEXT, "marginBottom": "2px",
        }),
    ]

    if subtitle:
        children.append(html.Div(subtitle, style={
            "fontSize": "10px", "color": SUBTEXT, "marginBottom": "4px",
            "fontStyle": "italic",
        }))

    children.append(html.Div(
        style={"display": "flex", "alignItems": "baseline", "gap": "4px", "marginBottom": "2px"},
        children=[
            html.Span(display_value, style={
                "fontSize": "18px", "fontWeight": "700", "color": TEXT,
            }),
            html.Span(unit, style={"fontSize": "11px", "color": SUBTEXT}) if unit else None,
        ],
    ))

    if reference_value:
        children.append(html.Div(
            style={"display": "flex", "alignItems": "center", "gap": "4px", "marginBottom": "1px"},
            children=[
                html.Span(reference_label, style={"fontSize": "10px", "color": SUBTEXT})
                if reference_label else None,
                html.Span(reference_value, style={
                    "fontSize": "11px", "fontWeight": "600", "color": SUBTEXT,
                }),
            ],
        ))

    if trend:
        children.append(html.Div(trend, style={
            "fontSize": "11px",
            "color": trend_color or SUBTEXT,
            "marginTop": "1px",
        }))

    return html.Div(style={
        "background": BG_SURFACE,
        "border": f"1px solid {BORDER}",
        "borderRadius": "6px",
        "padding": "10px 14px",
    }, children=children)
