"""Serialize a Dash component tree to a static HTML string.

The dbr dashboards are authored as Dash ``html``/``dcc`` component trees, but
they use **no server callbacks** (no slicers, cross-filter, tabs, or Interval —
verified across the live fleet). Every chart is a pre-computed Plotly figure;
the only runtime interactivity is Plotly's own client-side hover/zoom/legend,
which survives static export unchanged.

This module walks the compiled component tree and emits HTML:
  - ``html.*`` components       → the matching HTML tag (Div→div, H2→h2, …)
  - ``dcc.Graph(figure=…)``     → a ``plotly.io.to_html`` fragment (plotly.js
                                  vendored once per page, ``include_plotlyjs=False``)
  - ``dcc.Markdown(text)``      → rendered HTML (minimal: paragraphs + **bold**,
                                  *italic*, [text](url) — the subset prose uses)
  - ``dcc.Store`` / ``dcc.Location`` → dropped (no-ops without a backend)

Inline ``style`` dicts are serialized replicating React's rules (camelCase →
kebab-case; bare ``0``; ``px`` appended to non-unitless numbers) so the static
DOM is pixel-identical to the live Dash render under the same stylesheet.

Any *interactive* dcc component (Dropdown, Slider, RadioItems, Tabs, DatePicker)
raises ``UnsupportedComponentError`` — a loud signal that a dashboard relies on a
backend and must not be silently flattened to a broken static page.
"""
from __future__ import annotations

import html as _html
import re

# camelCase style properties that take a unitless number in CSS — a bare numeric
# value must NOT get a "px" suffix (matches React's CSSProperty unitless set,
# trimmed to what dbr actually emits).
_UNITLESS = {
    "flex", "flexGrow", "flexShrink", "order", "opacity", "zIndex",
    "fontWeight", "lineHeight", "zoom", "gridRow", "gridColumn", "columnCount",
}

# Dash component prop name → HTML attribute name. Anything not listed is emitted
# as-is when it contains a hyphen (data-*, aria-*), else lower-cased (colSpan →
# colspan, etc.). Dash-internal props are dropped (see _SKIP_PROPS).
_ATTR_RENAME = {"className": "class", "htmlFor": "for"}
_SKIP_PROPS = {
    "children", "style", "n_clicks", "n_clicks_timestamp", "key",
    "loading_state", "disable_n_clicks", "setProps", "config", "figure",
    "clickData", "hoverData", "selectedData", "relayoutData", "restyleData",
}

# Void HTML elements — no closing tag.
_VOID = {"img", "br", "hr", "input", "meta", "link", "source", "col"}

# Interactive dcc components that cannot render statically. Hitting one means a
# dashboard depends on a callback backend — fail loudly rather than ship a broken page.
_INTERACTIVE_DCC = {
    "Dropdown", "Slider", "RangeSlider", "RadioItems", "Checklist",
    "Tabs", "Tab", "DatePickerRange", "DatePickerSingle", "Input", "Textarea",
    "Upload", "Interval",
}


class UnsupportedComponentError(RuntimeError):
    """Raised when the tree contains a component that needs a runtime backend."""


def _camel_to_kebab(prop: str) -> str:
    return re.sub(r"([A-Z])", r"-\1", prop).lower()


def _css_value(prop: str, value) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        if value == 0:
            return "0"
        if prop in _UNITLESS:
            return _trim(value)
        return f"{_trim(value)}px"
    return str(value)


def _trim(value) -> str:
    """Render a number without a trailing ``.0`` (1.0 → "1", 1.5 → "1.5")."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _style_attr(style: dict) -> str:
    decls = "".join(
        f"{_camel_to_kebab(k)}:{_css_value(k, v)};"
        for k, v in style.items()
        if v is not None
    )
    return f' style="{_html.escape(decls, quote=True)}"' if decls else ""


def _attrs(props: dict) -> str:
    out = []
    if "style" in props and isinstance(props["style"], dict):
        out.append(_style_attr(props["style"]))
    for key, value in props.items():
        if key in _SKIP_PROPS or value is None:
            continue
        name = _ATTR_RENAME.get(key) or (key if "-" in key else key.lower())
        if value is True:
            out.append(f" {name}")
        elif value is False:
            continue
        else:
            out.append(f' {name}="{_html.escape(str(value), quote=True)}"')
    return "".join(out)


def render_markdown(text: str, style: dict | None) -> str:
    """Minimal Markdown → HTML for the prose subset dbr dashboards use:
    blank-line-separated paragraphs with **bold**, *italic*, and [text](url)."""
    paragraphs = re.split(r"\n\s*\n", (text or "").strip())
    blocks = []
    for para in paragraphs:
        if not para.strip():
            continue
        esc = _html.escape(para.strip()).replace("\n", " ")
        esc = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc)
        esc = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", esc)
        esc = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', esc)
        blocks.append(f'<p style="margin:0 0 8px 0">{esc}</p>')
    inner = "".join(blocks)
    return f"<div{_style_attr(style or {})}>{inner}</div>"


def render_graph(props: dict) -> str:
    """Render a dcc.Graph as a Plotly HTML fragment wrapped in the Graph's own
    div (carrying its id/className/style). plotly.js is referenced once in the
    page head, so each figure uses ``include_plotlyjs=False``."""
    import plotly.io as pio

    fig = props.get("figure") or {}
    config = props.get("config") or {}
    # Fill-mode charts have their fixed height cleared (None) → fill the flex cell
    # via default_height='100%'. Fixed-height charts (sparklines, companion-table
    # charts) keep their baked layout.height, which to_html honours over the default.
    fragment = pio.to_html(
        fig,
        include_plotlyjs=False,
        full_html=False,
        validate=False,
        config=config,
        default_width="100%",
        default_height="100%",
    )
    wrapper_props = {k: props[k] for k in ("id", "className", "style") if k in props}
    return f"<div{_attrs(wrapper_props)}>{fragment}</div>"


def render_node(node) -> str:
    """Recursively serialize a Dash component / list / scalar to an HTML string."""
    if node is None or node is False:
        return ""
    if isinstance(node, (str, int, float)):
        return _html.escape(str(node))
    if isinstance(node, (list, tuple)):
        return "".join(render_node(n) for n in node)

    # Dash component — use its canonical serialization (only set props appear).
    to_json = getattr(node, "to_plotly_json", None)
    if to_json is None:
        return _html.escape(str(node))
    spec = to_json()
    namespace = spec.get("namespace", "")
    ctype = spec.get("type", "")
    props = spec.get("props", {}) or {}

    if namespace == "dash_core_components":
        if ctype == "Graph":
            return render_graph(props)
        if ctype == "Markdown":
            return render_markdown(props.get("children", ""), props.get("style"))
        if ctype in ("Store", "Location"):
            return ""  # no-ops without a callback backend
        # Every other dcc component (interactive widgets AND anything unrecognised)
        # is treated as backend-dependent: fail loud rather than ship a page that is
        # silently missing a control. build sits in the deploy path, so a degrade here
        # would publish a broken dashboard.
        raise UnsupportedComponentError(
            f"dcc.{ctype} cannot be rendered statically — it requires a runtime "
            f"backend (or is not yet supported by the static exporter). This dashboard "
            f"cannot be exported to static HTML; interactivity is on hold (see OR-168)."
        )

    if namespace != "dash_html_components":
        # Unknown component library — refuse rather than guess a tag mapping.
        raise UnsupportedComponentError(
            f"Component {namespace}.{ctype} is from an unrecognised library and "
            f"cannot be serialized to static HTML."
        )

    # html component (dash_html_components) — map type to its lowercase tag.
    tag = ctype.lower()
    attrs = _attrs(props)
    if tag in _VOID:
        return f"<{tag}{attrs}>"
    children_html = render_node(props.get("children"))
    return f"<{tag}{attrs}>{children_html}</{tag}>"
