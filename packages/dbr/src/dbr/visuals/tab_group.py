"""tab_group — Tab strip container for sub-page navigation within a section.

Renders a set of labelled tabs. Each tab shows a different set of visuals
without navigating to a new page. Useful when a page has multiple angles
on the same topic (e.g., Overview / By Country / Historical) that would
be too long to scroll through linearly.

YAML shape (in visuals.yml):

  rows:
    - items:
        - visual: topic_tabs
          width: "100%"

  # topic_tabs.yml
  type: tab_group
  options:
    tabs:
      - label: "Przegląd"
        rows:
          - items: [kpi_unemployment, kpi_employment, kpi_participation]
          - items: [trend_unemployment]
      - label: "Kraje UE"
        rows:
          - items: [bar_eu_comparison]
      - label: "Historia"
        rows:
          - items: [line_long_history]

  # visuals referenced inside tabs are defined as sibling .yml files
  # in the same visuals/ directory as tab_group.yml

Note: tab_group must be placed in a page's visuals/ directory. The visuals
referenced inside tabs are loaded from the same directory. This means they
share the same namespace — use distinct filenames.
"""
from __future__ import annotations

import uuid
from dash import dcc, html
import dash

from dbr.theme import (
    AZURE_1, BG_SURFACE, BORDER, CARD_RADIUS, FONT_FAMILY, SUBTEXT, TEXT,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "options"],
    "properties": {
        "type": {"const": "tab_group"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "required": ["tabs"],
            "properties": {
                "tabs": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "object",
                        "required": ["label", "rows"],
                        "additionalProperties": False,
                        "properties": {
                            "label": {"type": "string"},
                            "rows": {
                                "type": "array",
                                "description": "Row specs — same shape as visuals.yml rows block.",
                            },
                        },
                    },
                },
            },
        },
    },
}


def tab_group(*, options: dict | None = None, _visuals_dir=None, _build_context=None, _page_name="", **_kwargs) -> html.Div:
    """Render a Dash dcc.Tabs container with pre-built visual content per tab.

    This factory is called with pre-built rows (not raw YAML specs) when the
    compiler detects `type: tab_group` and pre-processes its content. For
    standalone use, pass `_rows_per_tab` via options.
    """
    opts  = options or {}
    tabs_spec = opts.get("tabs") or []
    pre_rows = opts.get("_pre_rows")   # injected by compiler when content is pre-built

    if pre_rows:
        # Compiler pre-built the rows for us
        tab_items = []
        for i, spec in enumerate(tabs_spec):
            rows = pre_rows[i] if i < len(pre_rows) else []
            tab_items.append(dcc.Tab(
                label=spec.get("label", f"Tab {i+1}"),
                value=f"tab_{i}",
                style={"fontSize": "13px", "padding": "8px 16px", "color": SUBTEXT, "borderBottom": f"2px solid transparent"},
                selected_style={"fontSize": "13px", "padding": "8px 16px", "color": AZURE_1, "fontWeight": 600, "borderBottom": f"2px solid {AZURE_1}"},
                children=[
                    _render_rows(rows),
                ],
            ))
    else:
        # Fallback: empty tabs (should be pre-built by compiler)
        tab_items = [
            dcc.Tab(label=spec.get("label", f"Tab {i+1}"), value=f"tab_{i}", children=[])
            for i, spec in enumerate(tabs_spec)
        ]

    return html.Div(
        dcc.Tabs(
            tab_items,
            value="tab_0",
            style={"fontFamily": FONT_FAMILY, "borderBottom": f"1px solid {BORDER}"},
        ),
        style={"background": BG_SURFACE, "borderRadius": CARD_RADIUS, "padding": "0 0 16px 0"},
    )


def _render_rows(rows) -> html.Div:
    """Render a list of rows (same shape as page_shell rows) inside a tab panel."""
    from dbr.theme import ROW_GAP
    _ROW_STYLE = {"display": "flex", "gap": ROW_GAP, "marginBottom": ROW_GAP, "alignItems": "stretch"}

    children = []
    for row_title, row_prose, row_items in (rows or []):
        if row_title:
            children.append(html.H3(row_title, style={"fontSize": "14px", "fontWeight": 600, "marginTop": "16px", "marginBottom": "8px", "color": TEXT}))
        if row_prose:
            children.append(html.P(row_prose, style={"fontSize": "13px", "color": TEXT, "marginBottom": "12px"}))
        flex_items = []
        for component, width in row_items:
            style = {"minWidth": 0, "flex": f"0 0 {width}" if width else "1"}
            flex_items.append(html.Div(component, style=style))
        children.append(html.Div(flex_items, style=_ROW_STYLE))
    return html.Div(children, style={"padding": "16px 0 0 0"})
