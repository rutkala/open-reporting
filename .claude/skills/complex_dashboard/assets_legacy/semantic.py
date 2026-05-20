"""
Semantic layer — Dimension and Measure dataclasses.

These are display-config objects only. They carry labels, units, and format
settings for chart rendering. All aggregation and business logic lives in the
domain's semantic_service.py (or data.py for the template scaffold).

Usage pattern in app.py:
    import products.dashboards.template.data as _data
    import products.dashboards.template.measures as m

    _df_by_year = _data.load_by_year()
    _years = m.DIMS["year"].values(_df_by_year)

    clustered_column(
        "Chart title",
        x=_years,
        series=[
            m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
            m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
        ],
        y_measure=m.MEASURES["measure_a"],
    )
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import pandas as pd

# Imported here to avoid repeating the import inside apply_to_* methods.
# theme.py has no dependency on semantic.py — no circular import risk.
from complex_dashboard.assets.theme import SUBTEXT as _SUBTEXT


# ── Dimension ─────────────────────────────────────────────────────────────────

@dataclass
class Dimension:
    """
    A categorical or temporal axis variable.

    Attributes:
        name:   machine key used in DIMS dict (e.g. "year")
        label:  user-facing label for axis / legend (e.g. "Year")
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

@dataclass
class Measure:
    """
    Display metadata for a numeric indicator.

    All aggregation and transformation logic lives upstream in the domain's
    semantic_service.py (or data.py for the template). This class carries
    what is needed to render charts and KPI cards consistently.

    Attributes:
        name:            machine key used in MEASURES dict
        label:           user-facing label for legend / KPI title / axis
        column:          DataFrame column that holds pre-aggregated values
        unit:            physical unit string (e.g. "pp", "% PKB", "units")
        format_type:     "number" | "currency" | "percent" | "text"
        scale:           magnitude divisor applied before formatting;
                         None = raw value, "K" = /1 000, "M" = /1 000 000, "B" = /1 000 000 000
        decimals:        decimal places in formatted output
        currency_symbol: symbol appended after value+scale (e.g. "zł", "€", "$")
        show_unit:       whether to include unit/symbol in display output
    """
    name:            str
    label:           str
    column:          str
    unit:            str                                         = ""
    format_type:     Literal["number", "currency", "percent", "text"] = "number"
    scale:           Literal[None, "K", "M", "B"]              = None
    decimals:        int                                         = 1
    currency_symbol: str                                         = ""
    show_unit:       bool                                        = True

    # ── Formatting ────────────────────────────────────────────────────────────

    def format_value(self, v: float) -> str:
        """
        Format a single value using this measure's display settings.
        Applies scale, decimals, format_type, currency_symbol, and unit.
        Returns "—" for NaN / non-numeric input.
        """
        if self.format_type == "text":
            return str(v)
        try:
            fv = float(v)
            if math.isnan(fv):
                return "—"
        except (TypeError, ValueError):
            return "—"

        divisor = {"K": 1e3, "M": 1e6, "B": 1e9}.get(self.scale, 1)
        scale_suffix = self.scale or ""
        scaled = fv / divisor

        if self.format_type == "percent":
            return f"{scaled:.{self.decimals}f}%"

        number_str = f"{scaled:,.{self.decimals}f}"

        if self.format_type == "currency":
            result = f"{number_str}{scale_suffix}"
            if self.currency_symbol and self.show_unit:
                result = f"{result} {self.currency_symbol}"
            return result

        # "number"
        result = number_str + scale_suffix
        if self.show_unit and self.unit:
            result = f"{result} {self.unit}"
        return result

    @property
    def axis_label(self) -> str:
        """Y-axis title string — label with unit annotation in parentheses."""
        if not self.show_unit:
            return self.label
        if self.format_type == "percent":
            u = "%"
        elif self.format_type == "currency":
            parts = [p for p in [self.scale, self.currency_symbol] if p]
            u = " ".join(parts)
        else:
            parts = [p for p in [self.scale, self.unit] if p]
            u = " ".join(parts)
        return f"{self.label} ({u})" if u else self.label

    @property
    def plotly_tickformat(self) -> str:
        """D3 format string for Plotly yaxis.tickformat / xaxis.tickformat."""
        if self.format_type == "percent":
            return f".{self.decimals}f"
        return f",.{self.decimals}f"

    @property
    def plotly_ticksuffix(self) -> str:
        """Suffix appended to each tick label — yaxis.ticksuffix."""
        if not self.show_unit:
            return ""
        if self.format_type == "percent":
            return "%"
        if self.format_type == "currency" and self.currency_symbol:
            return f" {self.currency_symbol}"
        if self.format_type == "number" and self.unit:
            return f" {self.unit}"
        return ""

    # ── Chart integration helpers ─────────────────────────────────────────────

    def apply_to_yaxis(self, axis_dict: dict) -> None:
        """
        Update a Plotly yaxis config dict in-place with this measure's
        title, tickformat, and ticksuffix.
        """
        axis_dict["title"] = dict(text=self.axis_label, font=dict(size=11, color=_SUBTEXT))
        axis_dict["tickformat"] = self.plotly_tickformat
        axis_dict["ticksuffix"] = self.plotly_ticksuffix

    def apply_to_xaxis(self, axis_dict: dict) -> None:
        """Same as apply_to_yaxis but for horizontal chart x-axes."""
        axis_dict["title"] = dict(text=self.axis_label, font=dict(size=11, color=_SUBTEXT))
        axis_dict["tickformat"] = self.plotly_tickformat
        axis_dict["ticksuffix"] = self.plotly_ticksuffix

    def fmt_labels(self, values: list) -> list:
        """Format a list of values for data labels (show_labels=True)."""
        return [self.format_value(v) for v in values]

    # ── KPI / series helpers ──────────────────────────────────────────────────

    def kpi_value(self, v: float) -> str:
        """
        Numeric-only formatted string for kpi_standard value param.
        Does NOT include unit or currency_symbol — pass those via plotly_ticksuffix.
        For percent: returns the number without "%" (kpi_standard handles "%" specially).
        """
        if self.format_type == "text":
            return str(v)
        try:
            fv = float(v)
            if math.isnan(fv):
                return "—"
        except (TypeError, ValueError):
            return "—"
        divisor = {"K": 1e3, "M": 1e6, "B": 1e9}.get(self.scale, 1)
        scale_suffix = self.scale or ""
        scaled = fv / divisor
        if self.format_type == "percent":
            return f"{scaled:.{self.decimals}f}"  # "%" comes from unit="%"
        return f"{scaled:,.{self.decimals}f}{scale_suffix}"

    def to_series(self, y: list) -> dict:
        """Returns {"name": label, "y": y} — drop-in for chart series lists."""
        return {"name": self.label, "y": y}
