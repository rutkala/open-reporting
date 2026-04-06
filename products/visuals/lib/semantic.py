"""
Semantic layer — Dimension and Measure dataclasses.

These are display-config objects only. They carry labels, units, and format
strings for chart rendering. All aggregation and business logic lives in the
domain's semantic_service.py (or data.py for the template scaffold).

Usage pattern in app.py:
    import products.dashboards.template.data as _data
    import products.dashboards.template.measures as m

    _df_by_year = _data.load_by_year()
    _years = m.DIMS["year"].values(_df_by_year)

    clustered_column(
        "Tytuł wykresu",
        x=_years,
        series=[
            m.MEASURES["measure_a"].to_series(_df_by_year["val_a"].tolist()),
            m.MEASURES["measure_b"].to_series(_df_by_year["val_b"].tolist()),
        ],
    )
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd


# ── Dimension ─────────────────────────────────────────────────────────────────

@dataclass
class Dimension:
    """
    A categorical or temporal axis variable.

    Attributes:
        name:   machine key used in DIMS dict (e.g. "year")
        label:  user-facing label for axis / legend (e.g. "Rok")
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
    semantic_service.py (or data.py for the template). This class only carries
    what is needed to render charts and KPI cards correctly.

    Attributes:
        name:   machine key used in MEASURES dict (e.g. "fiscal_balance")
        label:  user-facing label for legend / KPI title (e.g. "Saldo fiskalne")
        column: DataFrame column that holds pre-aggregated values
        unit:   display unit appended to formatted values (e.g. "% PKB")
        format: Python format string for a single number (e.g. "{:.1f}")
    """
    name:   str
    label:  str
    column: str
    unit:   str = ""
    format: str = "{:.1f}"

    def to_series(self, y: list) -> dict:
        """Returns {"name": label, "y": y} — drop-in for chart series lists."""
        return {"name": self.label, "y": y}

    def format_value(self, v: float) -> str:
        """Format a pre-computed numeric value with this measure's format string."""
        try:
            if math.isnan(float(v)):
                return "—"
        except (TypeError, ValueError):
            return "—"
        return self.format.format(v)

    def kpi_value(self, v: float) -> str:
        """Formatted string ready for kpi_standard / kpi_compact."""
        return self.format_value(v)
