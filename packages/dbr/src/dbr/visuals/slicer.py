"""slicer — Interactive filter control (dropdown, radio, multi-select).

Slicers are the dbr equivalent of Power BI's Slicer visual. A slicer on a
page updates all charts that declare ``filter_from: {slicer_id: dimension}``
in their YAML. No Python callback code is required — the wiring is fully
declarative.

YAML shape:

  # The slicer visual:
  type: slicer
  slicer_id: country_filter      # unique ID referenced by charts
  encoding:
    value:
      dimension: geo             # which dimension this slicer filters
  options:
    metric: fiscal_balance       # any metric that has the dimension (used to fetch options)
    kind: dropdown               # dropdown | radio | multi (default: dropdown)
    label: "Kraj"                # label shown above the control
    placeholder: "(wszystkie)"  # dropdown placeholder / first radio option
    default: PL                  # pre-selected value (null = all / placeholder)
    clearable: true              # dropdown: allow clearing selection (default: true)

  # A chart that is filtered by the slicer (add filter_from to any chart YAML):
  type: line
  filter_from:
    country_filter: geo          # slicer_id → dimension key in the filter dict
  encoding:
    x: { dimension: metric_time, granularity: year }
    y: { metric: fiscal_balance }

When the slicer value changes the chart re-queries the semantic layer with
``filter[geo] = <selected_value>``. Selecting the placeholder (None) removes
the filter key so all dimension values are returned.
"""
from __future__ import annotations

from dash import dcc, html

from dbr.semantic import semantic_query_data
from dbr.theme import (
    BG_SURFACE, BORDER, CARD_RADIUS, CARD_SHADOW,
    FONT_FAMILY, SUBTEXT, TEXT,
)
from dbr.visuals._encoding import (
    postprocess_time_columns, dimension_column_name, group_by_from_channels, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "slicer_id", "encoding"],
    "properties": {
        "type":      {"const": "slicer"},
        "slicer_id": {
            "type": "string",
            "description": "Unique identifier referenced by charts via filter_from.",
        },
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["value"],
            "additionalProperties": False,
            "properties": {
                "value": {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "metric":      {"type": "string", "description": "Any metric that has the filtered dimension — used to query option values."},
                "kind":        {"enum": ["dropdown", "radio", "multi"]},
                "label":       {"type": "string"},
                "placeholder": {"type": "string"},
                "default":     {},
                "clearable":   {"type": "boolean"},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "12px 16px", "height": "100%", "boxSizing": "border-box",
    "fontFamily": FONT_FAMILY,
}


def slicer(
    *,
    encoding: dict,
    filter: dict | None = None,
    options: dict | None = None,
    component_id: str | None = None,
    slicer_id: str | None = None,
) -> html.Div:
    enc  = parse_encoding(encoding)
    opts = options or {}

    if not (enc.value and enc.value.dimension):
        raise ValueError("slicer: encoding.value must bind a dimension")

    dim_col = dimension_column_name(enc.value)
    metric  = opts.get("metric")
    kind    = opts.get("kind", "dropdown")
    label   = opts.get("label", "")
    placeholder = opts.get("placeholder", "(wszystkie)")
    default = opts.get("default")
    clearable = opts.get("clearable", True)

    # Fetch distinct dimension values using the provided metric
    if metric:
        group_by = group_by_from_channels(enc.value)
        df = semantic_query_data(metric, group_by=group_by, filter=filter)
        if not df.empty:
            df = postprocess_time_columns(df, enc)
            values = sorted(df[dim_col].dropna().unique().tolist(), key=str)
        else:
            values = []
    else:
        values = []

    comp_id = component_id or f"slicer_{slicer_id or 'unnamed'}"
    options_list = [{"label": str(v), "value": str(v)} for v in values]

    children: list = []
    if label:
        children.append(html.Div(label, style={
            "fontSize": "11px", "color": SUBTEXT, "fontWeight": 500,
            "marginBottom": "6px", "textTransform": "uppercase",
            "letterSpacing": "0.04em",
        }))

    if kind == "dropdown":
        children.append(dcc.Dropdown(
            id=comp_id,
            options=options_list,
            value=str(default) if default is not None else None,
            placeholder=placeholder,
            clearable=clearable,
            style={"fontSize": "13px"},
        ))
    elif kind == "radio":
        radio_opts = [{"label": placeholder, "value": "__all__"}] + options_list
        children.append(dcc.RadioItems(
            id=comp_id,
            options=radio_opts,
            value=str(default) if default is not None else "__all__",
            inputStyle={"marginRight": "6px"},
            labelStyle={"display": "block", "fontSize": "13px", "marginBottom": "4px", "color": TEXT},
        ))
    elif kind == "multi":
        children.append(dcc.Dropdown(
            id=comp_id,
            options=options_list,
            value=[str(default)] if default is not None else None,
            placeholder=placeholder,
            multi=True,
            style={"fontSize": "13px"},
        ))

    return html.Div(children=children, style=_CARD_STYLE)
