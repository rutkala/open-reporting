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


@dataclass
class Channel:
    """One encoding channel bound to either a dimension or a metric."""
    dimension:   str | None = None
    metric:      str | None = None
    granularity: str | None = None      # only for time dimensions

    @property
    def kind(self) -> str:
        if self.dimension is not None:
            return "dimension"
        if self.metric is not None:
            return "metric"
        return "empty"

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
