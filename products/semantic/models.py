"""
Semantic layer data models.
Plain dataclasses with lightweight formatting helpers.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Literal


@dataclass
class Fact:
    id: str
    schema: str
    table: str
    grain: list[str]

    @property
    def full_table(self) -> str:
        return f"{self.schema}.{self.table}"


@dataclass
class Dimension:
    id: str
    column: str
    label: str
    type: Literal["categorical", "temporal"]


@dataclass
class Measure:
    id: str
    label: str
    column: str
    fact: str
    aggregation: Literal["avg", "sum", "min", "max", "count"]
    unit: str
    direction: Literal["higher_is_better", "lower_is_better", "neutral"]
    description: str = ""

    @property
    def higher_is_better(self) -> bool:
        return self.direction == "higher_is_better"

    @property
    def axis_label(self) -> str:
        """Short axis label including unit."""
        if self.unit == "%":
            return f"{self.label} (%)"
        if self.unit == "PLN":
            return f"{self.label} (zł)"
        if self.unit == "pp":
            return f"{self.label} (pp)"
        return self.label

    @property
    def fmt(self) -> Callable[[float], str]:
        """Value formatter function derived from unit."""
        if self.unit == "%":
            return lambda v: f"{v:.1f}%"
        if self.unit == "PLN":
            return lambda v: f"{v:,.0f} zł"
        if self.unit == "pp":
            return lambda v: f"{v:+.1f} pp"
        return lambda v: f"{v:,.2f}"

    @property
    def hover_fmt(self) -> str:
        """Plotly hovertemplate format string."""
        if self.unit == "%":
            return ".1f"
        if self.unit == "PLN":
            return ",.0f"
        return ".2f"


@dataclass
class KPI:
    id: str
    label: str
    base_measure: str
    calculation: Literal["yoy_diff", "yoy_pct", "rank_asc", "rank_desc"]
    unit: str
    description: str = ""


@dataclass
class Section:
    id: str
    label: str
    measures: list[str]          # Measure.id values


@dataclass
class Domain:
    id: str
    label: str
    description: str
    facts: dict[str, Fact]
    dimensions: dict[str, Dimension]
    measures: dict[str, Measure]
    kpis: dict[str, KPI]
    sections: list[Section] = field(default_factory=list)

    def get_measure(self, measure_id: str) -> Measure:
        if measure_id not in self.measures:
            raise KeyError(f"Measure '{measure_id}' not found in domain '{self.id}'")
        return self.measures[measure_id]

    def get_kpi(self, kpi_id: str) -> KPI:
        if kpi_id not in self.kpis:
            raise KeyError(f"KPI '{kpi_id}' not found in domain '{self.id}'")
        return self.kpis[kpi_id]

    def get_fact_for_measure(self, measure: Measure) -> Fact:
        return self.facts[measure.fact]
