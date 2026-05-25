"""Encoding parsing and channel utilities — shared across all encoding-based visuals.

Vega-Lite-style encoding: each visual declares which channels (x, y, color,
size, value, category, rows, columns) it accepts, and each channel binds
to either a dimension or a metric. This module turns YAML encoding specs
into Python objects and resolves them into MetricFlow ``--group-by`` args.

Channel shape in YAML:

    encoding:
      x:     { dimension: period, granularity: year }
      y:     { metric: fiscal_balance }
      color: { dimension: geo }

Channel kinds:
  - ``dimension`` — categorical or time attribute. Triggers a GROUP BY.
  - ``metric``    — aggregated value. Becomes the y-value (or x-value for `bar`).
  - ``granularity`` (only with time dimensions) — year/quarter/month/day.
"""
from __future__ import annotations

from dataclasses import dataclass

from dbr.theme import (
    AZURE_1, AZURE_2, AZURE_3, AZURE_4, AZURE_PALE,
    BORDER, NEGATIVE, POSITIVE, SLATE_1, SLATE_2, SLATE_3, SLATE_4,
    SUBTEXT, TEAL_1, TEAL_2, TEAL_3, TEAL_4, TEAL_PALE, WARNING,
)


@dataclass
class Channel:
    """One encoding channel bound to either a dimension or a metric.

    ``metric`` accepts either a single metric name or a list of names. The
    ``metrics`` property always returns a list, so callers don't need to
    branch on scalar/list shape. A multi-metric y-channel is how the line
    visual plots several series with shared x-axis (one trace per metric).
    """
    dimension:   str | None = None
    metric:      str | list[str] | None = None
    granularity: str | None = None      # only for time dimensions

    @property
    def kind(self) -> str:
        if self.dimension is not None:
            return "dimension"
        if self.metric is not None:
            return "metric"
        return "empty"

    @property
    def metrics(self) -> list[str]:
        """Always return metric(s) as a list (empty if none)."""
        if self.metric is None:
            return []
        if isinstance(self.metric, str):
            return [self.metric]
        return list(self.metric)

    def mf_group_by(self) -> str | None:
        """Return the `mf query --group-by` token for this channel, or None if it's a metric."""
        if not self.dimension:
            return None
        if self.granularity and self.dimension in ("period", "metric_time"):
            return f"metric_time__{self.granularity}"
        if self.granularity:
            return f"{self.dimension}__{self.granularity}"
        return self.dimension


def parse_channel(spec: dict | None) -> Channel | None:
    """Turn a YAML channel spec into a Channel object."""
    if not spec:
        return None
    if not isinstance(spec, dict):
        raise ValueError(f"Encoding channel must be an object, got {type(spec).__name__}")
    return Channel(
        dimension   = spec.get("dimension"),
        metric      = spec.get("metric"),
        granularity = spec.get("granularity"),
    )


@dataclass
class Encoding:
    """All channels for a single visual. Visuals read the channels they need."""
    x:        Channel | None = None
    y:        Channel | None = None
    color:    Channel | None = None
    size:     Channel | None = None
    value:    Channel | None = None       # KPI / card
    category: Channel | None = None       # pie / donut
    rows:     list[Channel] | None = None # table
    columns:  list[Channel] | None = None # table


def parse_encoding(spec: dict | None) -> Encoding:
    """Parse the full `encoding` block from a visual YAML."""
    spec = spec or {}
    enc = Encoding(
        x        = parse_channel(spec.get("x")),
        y        = parse_channel(spec.get("y")),
        color    = parse_channel(spec.get("color")),
        size     = parse_channel(spec.get("size")),
        value    = parse_channel(spec.get("value")),
        category = parse_channel(spec.get("category")),
    )
    if "rows" in spec:
        enc.rows = [parse_channel(c) for c in (spec["rows"] or [])]
    if "columns" in spec:
        enc.columns = [parse_channel(c) for c in (spec["columns"] or [])]
    return enc


def group_by_from_channels(*channels: Channel | None) -> list[str]:
    """Collect ``mf query --group-by`` tokens from one or more channels.

    Used by each visual to assemble the group_by list from whatever
    channels it has bound to dimensions.
    """
    out: list[str] = []
    for ch in channels:
        if ch is None:
            continue
        tok = ch.mf_group_by()
        if tok and tok not in out:
            out.append(tok)
    return out


def metric_from_channels(*channels: Channel | None) -> str:
    """Find the (single) metric referenced by a visual's encoding."""
    for ch in channels:
        if ch is not None and ch.metric:
            return ch.metric
    raise ValueError("No metric channel found in encoding")


def dimension_column_name(ch: Channel) -> str:
    """Return the column name to expect in the result DataFrame for a dimension channel."""
    return ch.mf_group_by()                                  # mf returns rows keyed by this name


def postprocess_time_columns(df, encoding: Encoding):
    """Convert MetricFlow time-dimension columns (full timestamps) to clean
    granularity-appropriate values.

    MetricFlow returns time-grouped columns as ``YYYY-MM-DD HH:MM:SS`` strings
    (the start of each bucket). For yearly data, that's 1995-01-01, 1996-01-01,
    ... — Plotly then renders the x-axis with month/day ticks between points.

    This helper converts those columns to:
      - year       → int (e.g. 1995)
      - quarter    → 'YYYY-Q1' / 'YYYY-Q2' / ...
      - month      → 'YYYY-MM'
      - day        → 'YYYY-MM-DD'

    Plotly then treats the axis as discrete and labels each bucket exactly.
    """
    import pandas as pd
    for ch in (encoding.x, encoding.y, encoding.color, encoding.value, encoding.category):
        if ch is None or not ch.dimension or not ch.granularity:
            continue
        col = ch.mf_group_by()
        if col not in df.columns:
            continue
        ts = pd.to_datetime(df[col])
        if ch.granularity == "year":
            df[col] = ts.dt.year
        elif ch.granularity == "quarter":
            df[col] = ts.dt.to_period("Q").astype(str)
        elif ch.granularity == "month":
            df[col] = ts.dt.strftime("%Y-%m")
        elif ch.granularity == "day":
            df[col] = ts.dt.strftime("%Y-%m-%d")
    # Same treatment for table.rows (list of channels)
    for ch_list in (encoding.rows, encoding.columns):
        if not ch_list:
            continue
        for ch in ch_list:
            if not ch.dimension or not ch.granularity:
                continue
            col = ch.mf_group_by()
            if col not in df.columns:
                continue
            ts = pd.to_datetime(df[col])
            if ch.granularity == "year":
                df[col] = ts.dt.year
            elif ch.granularity == "quarter":
                df[col] = ts.dt.to_period("Q").astype(str)
            elif ch.granularity == "month":
                df[col] = ts.dt.strftime("%Y-%m")
            elif ch.granularity == "day":
                df[col] = ts.dt.strftime("%Y-%m-%d")
    return df


# ── Reference lines ───────────────────────────────────────────────────────────
# YAML shape (per visual):
#
#   options:
#     reference_lines:
#       - { value: -3,  label: "Próg SGP",        color: negative }
#       - { value: 60,  label: "Próg Maastricht", color: warning }
#
# `value` is the position on the *value axis* of the visual:
#   - line, column, area → horizontal line at y = value
#   - bar                → vertical line at x = value
# Each visual passes the correct `axis` ("y" or "x") to apply_reference_lines.

_COLOR_ALIASES = {
    # Signal colors (semantic)
    "negative": NEGATIVE,
    "positive": POSITIVE,
    "warning":  WARNING,
    "subtext":  SUBTEXT,
    "border":   BORDER,
    # Brand palette (aliases for highlight / category colors)
    "azure_1":    AZURE_1, "azure_2": AZURE_2, "azure_3": AZURE_3,
    "azure_4":    AZURE_4, "azure_pale": AZURE_PALE,
    "teal_1":     TEAL_1,  "teal_2":  TEAL_2,  "teal_3":  TEAL_3,
    "teal_4":     TEAL_4,  "teal_pale": TEAL_PALE,
    "slate_1":    SLATE_1, "slate_2": SLATE_2, "slate_3": SLATE_3,
    "slate_4":    SLATE_4,
}


def _resolve_color(name: str | None, default: str = NEGATIVE) -> str:
    """Resolve a YAML color token (alias or hex) to a real color string."""
    if not name:
        return default
    if name.startswith("#"):
        return name
    return _COLOR_ALIASES.get(name, default)


def apply_annotations(fig, options: dict | None) -> None:
    """Add inline chart annotations from options.annotations to a Plotly figure.

    Each spec: {x, text, y?, direction?, color?}.
      x         — data x value of the point being annotated (year, category, etc.)
      text      — annotation label (Polish caption)
      y         — data y value; if absent, annotation floats at top of plot
                  area with no arrow (paper-coordinate placement)
      direction — above|below|left|right; controls arrow offset. Default: above.
      color     — palette alias or hex; default: subtext (muted grey).

    Used for marking structural breaks (COVID 2020 spike, ESA methodology
    changes, GFC inflection) per gap analysis dimension 21.
    """
    if not options:
        return
    anns = options.get("annotations") or []
    offsets = {
        "above": (0, -40),
        "below": (0, 40),
        "left":  (-40, 0),
        "right": (40, 0),
    }
    for spec in anns:
        if not isinstance(spec, dict) or "x" not in spec or "text" not in spec:
            continue
        ax, ay = offsets.get(spec.get("direction", "above"), (0, -40))
        color = _resolve_color(spec.get("color"), default=SUBTEXT)
        kwargs = dict(
            x=spec["x"], text=spec["text"],
            xref="x",
            showarrow=True,
            arrowhead=2, arrowsize=1, arrowwidth=1, arrowcolor=color,
            ax=ax, ay=ay,
            font=dict(color=color, size=11),
            align="center",
        )
        if "y" in spec:
            kwargs["y"] = spec["y"]
            kwargs["yref"] = "y"
        else:
            # No y given — float annotation at top of plot area, no arrow
            kwargs["y"] = 1.0
            kwargs["yref"] = "paper"
            kwargs["showarrow"] = False
        fig.add_annotation(**kwargs)


def apply_endpoint_labels(fig, options: dict | None, colorway: list[str] | None = None) -> None:
    """Replace the chart's legend with a label at the right edge of each trace.

    Used for multi-series line charts where reader has to match colour to
    legend label (rubric dimension 6). With label_endpoints: true the
    legend is hidden and each trace's name is rendered next to its last
    data point in the same colour as the line.

    Traces with showlegend=False are skipped — this keeps forecast
    continuation traces (dash_when) from getting duplicate labels.
    """
    import pandas as pd
    if not options or not options.get("label_endpoints"):
        return
    fig.update_layout(showlegend=False)
    palette = colorway or []
    palette_idx = 0
    for trace in fig.data:
        if getattr(trace, "showlegend", None) is False:
            continue
        x_vals = list(trace.x) if trace.x is not None else []
        y_vals = list(trace.y) if trace.y is not None else []
        if not x_vals or not y_vals:
            continue
        # Find last non-null y
        last_idx = None
        for i in range(len(y_vals) - 1, -1, -1):
            v = y_vals[i]
            if v is None or (isinstance(v, float) and pd.isna(v)):
                continue
            last_idx = i
            break
        if last_idx is None:
            continue
        # Resolve trace colour: explicit on line.color, else next palette slot, else SUBTEXT
        line_obj = getattr(trace, "line", None)
        color = getattr(line_obj, "color", None) if line_obj else None
        if not color and palette:
            color = palette[palette_idx % len(palette)]
            palette_idx += 1
        if not color:
            color = SUBTEXT
        fig.add_annotation(
            x=x_vals[last_idx], y=y_vals[last_idx],
            text=str(trace.name) if trace.name else "",
            xref="x", yref="y", showarrow=False,
            xanchor="left", xshift=8,
            font=dict(color=color, size=11),
        )


_ENDPOINT_LABELS_OPTION_SCHEMA = {
    "type": "boolean",
    "description": "Hide the legend and label each series at its right endpoint. Preferred over a top-of-chart legend box for multi-series line charts (rubric dim 6: direct labelling over legends).",
}


_ANNOTATIONS_OPTION_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["x", "text"],
        "properties": {
            "x":         {},
            "y":         {"type": "number"},
            "text":      {"type": "string"},
            "direction": {"enum": ["above", "below", "left", "right"]},
            "color":     {"type": "string"},
        },
    },
    "description": "Inline chart annotations. Each: {x, text, y?, direction?, color?}. Used to mark structural breaks (COVID 2020, ESA methodology changes, etc.).",
}


def apply_reference_lines(fig, options: dict | None, axis: str) -> None:
    """Add dashed reference lines from options.reference_lines to a Plotly figure.

    `axis` is "y" for line/column/area (horizontal lines) or "x" for bar
    (vertical lines). Each line is a dict with keys: value (required),
    label (optional), color (optional alias or hex; default = NEGATIVE).
    """
    if not options:
        return
    lines = options.get("reference_lines") or []
    for spec in lines:
        if not isinstance(spec, dict) or "value" not in spec:
            continue
        value = spec["value"]
        color = _resolve_color(spec.get("color"))
        label = spec.get("label", "")
        if axis == "y":
            fig.add_hline(
                y=value, line_dash="dash", line_color=color, line_width=1.5,
                annotation_text=label, annotation_position="top right",
                annotation_font=dict(color=color, size=11),
            )
        else:
            fig.add_vline(
                x=value, line_dash="dash", line_color=color, line_width=1.5,
                annotation_text=label, annotation_position="top right",
                annotation_font=dict(color=color, size=11),
            )
