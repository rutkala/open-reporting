"""
Semantic layer — Dimension and Measure dataclasses.

Charts are pure renderers; they never know where data comes from.
Data binding lives here: each dashboard defines DIMS and MEASURES
that reference columns in its DataFrame, and uses these objects to
produce the x/series/values arguments that chart functions accept.

Usage pattern in app.py:
    from . import data, measures as m
    df = data.load()

    clustered_column(
        m.MEASURES["revenue"].label,
        x=m.DIMS["year"].values(df),
        series=[
            m.MEASURES["revenue"].series(df, by=m.DIMS["year"]),
            m.MEASURES["costs"].series(df, by=m.DIMS["year"]),
        ],
    )
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd


# ── Dimension ─────────────────────────────────────────────────────────────────

@dataclass
class Dimension:
    """
    A categorical or temporal axis variable.

    Attributes:
        name:   machine key used in DIMS dict (e.g. "country")
        label:  user-facing label for axis / legend (e.g. "Kraj")
        column: DataFrame column that holds dimension values
    """
    name:   str
    label:  str
    column: str

    def values(self, df: pd.DataFrame) -> list:
        """
        Ordered unique values from this dimension column.
        Preserves first-occurrence order (matches typical query ORDER BY).
        """
        return list(dict.fromkeys(df[self.column].tolist()))


# ── Measure ───────────────────────────────────────────────────────────────────

_VALID_AGG = {"sum", "mean", "median", "last", "first", "count", "min", "max"}
_VALID_CALC = {None, "pct_change", "cumsum", "pct_of_total"}


@dataclass
class Measure:
    """
    A numeric indicator with aggregation and display metadata.

    Attributes:
        name:        machine key used in MEASURES dict (e.g. "fiscal_balance")
        label:       user-facing label for legend / KPI title (e.g. "Saldo fiskalne")
        column:      DataFrame column that holds raw values
        aggregation: pandas aggregation method applied when grouping by a Dimension
        unit:        display unit appended to formatted values (e.g. "% PKB")
        format:      Python format string for a single number (e.g. "{:.1f}")
        calc:        optional post-aggregation transformation:
                       "pct_change"   — period-over-period % change
                       "cumsum"       — running total
                       "pct_of_total" — each value as % of group sum
    """
    name:        str
    label:       str
    column:      str
    aggregation: str
    unit:        str            = ""
    format:      str            = "{:.1f}"
    calc:        Optional[str]  = None

    def __post_init__(self):
        if self.aggregation not in _VALID_AGG:
            raise ValueError(f"Measure '{self.name}': aggregation must be one of {_VALID_AGG}")
        if self.calc not in _VALID_CALC:
            raise ValueError(f"Measure '{self.name}': calc must be one of {_VALID_CALC}")

    # ── core methods ──────────────────────────────────────────────────────────

    def values(self, df: pd.DataFrame, by: Dimension) -> list:
        """
        Aggregated values aligned to the dimension's ordered unique values.
        Missing combinations return NaN.
        """
        grouped = df.groupby(by.column)[self.column].agg(self.aggregation)
        dim_vals = by.values(df)
        result = [_safe_float(grouped.get(v)) for v in dim_vals]
        return _apply_calc(result, self.calc)

    def series(self, df: pd.DataFrame, by: Dimension) -> dict:
        """
        Returns {"name": label, "y": [...]} — drop-in for chart series lists.
        """
        return {"name": self.label, "y": self.values(df, by)}

    def scalar(self, df: pd.DataFrame) -> float:
        """
        Single aggregated value across the whole DataFrame — for KPI cards.
        """
        return _safe_float(df[self.column].agg(self.aggregation))

    def format_value(self, v: float) -> str:
        """Format a numeric value with this measure's format string."""
        if math.isnan(v):
            return "—"
        return self.format.format(v)

    def kpi_value(self, df: pd.DataFrame) -> str:
        """Formatted scalar string ready for kpi_standard / kpi_compact."""
        return self.format_value(self.scalar(df))


# ── Internal helpers ──────────────────────────────────────────────────────────

def _safe_float(v) -> float:
    try:
        f = float(v)
        return f if not math.isnan(f) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


def _apply_calc(vals: list, calc: Optional[str]) -> list:
    if calc is None:
        return vals
    if calc == "pct_change":
        result = [float("nan")]
        for i in range(1, len(vals)):
            prev, cur = vals[i - 1], vals[i]
            if not math.isnan(prev) and not math.isnan(cur) and prev != 0:
                result.append((cur - prev) / abs(prev) * 100)
            else:
                result.append(float("nan"))
        return result
    if calc == "cumsum":
        total = 0.0
        result = []
        for v in vals:
            if not math.isnan(v):
                total += v
            result.append(total)
        return result
    if calc == "pct_of_total":
        total = sum(v for v in vals if not math.isnan(v))
        if total == 0:
            return [float("nan")] * len(vals)
        return [v / total * 100 if not math.isnan(v) else float("nan") for v in vals]
    return vals
