"""
Slicer / filter UI components — Power BI naming convention.

Five slicer types matching Power BI's built-in slicer formats:
  dropdown_slicer  — single select from a collapsed dropdown
  list_slicer      — visible list with checkbox (multi) or radio (single)
  range_slicer     — dual-handle numeric range slider
  date_range_slicer — date picker with start/end
  tile_slicer      — button tiles, single or multi-select

All return html.Div wrappers with title/subtitle, consistent with _chart().
Slicers are UI controls — connect them to callbacks in the host app.
"""
from dash import dcc, html

from products.visuals.lib.theme import (
    BG_SURFACE, BORDER, SUBTEXT, TEXT, FONT_FAMILY,
    TEAL_1, AZURE_PALE,
)

_LABEL_STYLE = {"fontSize": "14px", "fontWeight": "600", "color": TEXT, "marginBottom": "4px"}
_SUB_STYLE   = {"fontSize": "12px", "color": SUBTEXT, "marginBottom": "8px"}
_WRAP_STYLE  = {"background": BG_SURFACE, "border": f"1px solid {BORDER}",
                "borderRadius": "8px", "padding": "14px 18px"}


def _slicer_card(title, subtitle, control):
    children = [html.Div(title, style=_LABEL_STYLE)]
    if subtitle:
        children.append(html.Div(subtitle, style=_SUB_STYLE))
    children.append(control)
    return html.Div(style=_WRAP_STYLE, children=children)


def dropdown_slicer(title, options, value=None, subtitle=""):
    """
    Dropdown slicer — single select from a collapsed list.

    Args:
        options: list of strings or {"label": str, "value": str} dicts
        value:   selected value (defaults to first option)
    """
    opts = [{"label": o, "value": o} if isinstance(o, str) else o for o in options]
    return _slicer_card(title, subtitle, dcc.Dropdown(
        options=opts,
        value=value if value is not None else (opts[0]["value"] if opts else None),
        clearable=False,
        style={"fontFamily": FONT_FAMILY, "fontSize": "13px"},
    ))


def list_slicer(title, options, value=None, multi=True, subtitle=""):
    """
    List slicer — visible checklist (multi=True) or radio (multi=False).

    Args:
        options: list of strings or {"label": str, "value": str} dicts
        value:   selected value(s)
        multi:   True = checklist, False = radio items
    """
    opts = [{"label": o, "value": o} if isinstance(o, str) else o for o in options]
    label_style = {
        "display": "flex", "alignItems": "center", "gap": "8px",
        "padding": "4px 0", "fontSize": "13px", "color": TEXT, "cursor": "pointer",
    }
    if multi:
        control = dcc.Checklist(
            options=opts,
            value=value if value is not None else [o["value"] for o in opts],
            labelStyle=label_style,
            inputStyle={"accentColor": TEAL_1},
        )
    else:
        control = dcc.RadioItems(
            options=opts,
            value=value if value is not None else (opts[0]["value"] if opts else None),
            labelStyle=label_style,
            inputStyle={"accentColor": TEAL_1},
        )
    return _slicer_card(title, subtitle, control)


def range_slicer(title, min_val, max_val, value=None, step=1, subtitle=""):
    """
    Range / between slicer — dual-handle numeric slider.

    Args:
        min_val, max_val: numeric range bounds
        value:            [low, high] selected range (defaults to full range)
        step:             slider step size
    """
    return _slicer_card(title, subtitle, dcc.RangeSlider(
        min=min_val, max=max_val, step=step,
        value=value if value is not None else [min_val, max_val],
        marks={min_val: str(min_val), max_val: str(max_val)},
        tooltip={"placement": "bottom", "always_visible": True},
    ))


def date_range_slicer(title, start_date, end_date, subtitle=""):
    """
    Date range slicer — date picker with start and end date.

    Args:
        start_date, end_date: ISO date strings ("YYYY-MM-DD")
    """
    return _slicer_card(title, subtitle, dcc.DatePickerRange(
        start_date=start_date,
        end_date=end_date,
        display_format="DD MMM YYYY",
        style={"fontFamily": FONT_FAMILY},
    ))


def tile_slicer(title, options, value=None, multi=False, subtitle=""):
    """
    Tile / button slicer — clickable button tiles, single or multi-select.
    Rendered as static buttons in the template (wire up n_clicks in the host app).

    Args:
        options: list of strings or {"label": str, "value": str} dicts
        value:   selected value or list of values
        multi:   allow multiple tiles selected simultaneously
    """
    opts = [{"label": o, "value": o} if isinstance(o, str) else o for o in options]
    selected = value if value is not None else ([] if multi else (opts[0]["value"] if opts else None))
    if not multi and not isinstance(selected, list):
        selected = [selected]

    tiles = []
    for o in opts:
        is_active = o["value"] in selected
        tiles.append(html.Button(
            o["label"],
            style={
                "padding": "6px 14px", "fontSize": "13px", "fontFamily": FONT_FAMILY,
                "border": f"1px solid {BORDER if not is_active else TEAL_1}",
                "borderRadius": "6px", "cursor": "pointer",
                "background": AZURE_PALE if is_active else BG_SURFACE,
                "color": TEXT, "fontWeight": "600" if is_active else "400",
            },
        ))

    return _slicer_card(title, subtitle, html.Div(
        style={"display": "flex", "flexWrap": "wrap", "gap": "8px", "marginTop": "4px"},
        children=tiles,
    ))
