"""
Semantic query engine.
Translates Measure / KPI definitions into ibis expressions and returns DataFrames.
"""
import logging
import os

import ibis
import ibis.expr.types as ir
import pandas as pd
from dotenv import load_dotenv

from .models import Domain, Measure, KPI

load_dotenv(override=True)
log = logging.getLogger(__name__)

# ── Connection (singleton) ─────────────────────────────────────────────────────

_conn: ibis.BaseBackend | None = None


def _get_conn() -> ibis.BaseBackend:
    global _conn
    if _conn is None:
        _conn = ibis.postgres.connect(
            host="localhost", port=5432,
            database="reporting", user="reporting",
            password=os.environ["POSTGRES_PASSWORD"],
        )
        log.debug("ibis postgres connection established")
    return _conn


# ── Aggregation helpers ────────────────────────────────────────────────────────

_AGG_FN = {
    "avg":   lambda col: col.mean(),
    "sum":   lambda col: col.sum(),
    "min":   lambda col: col.min(),
    "max":   lambda col: col.max(),
    "count": lambda col: col.count(),
}


def _apply_aggregation(table: ir.Table, measure: Measure, group_by: list[str]) -> ir.Table:
    """Apply measure aggregation grouped by the requested dimensions."""
    agg_fn = _AGG_FN.get(measure.aggregation)
    if agg_fn is None:
        raise ValueError(f"Unknown aggregation: {measure.aggregation}")

    col = table[measure.column].cast("float64")
    agg_expr = agg_fn(col).name(measure.id)

    group_cols = [table[c] for c in group_by]
    return table.group_by(group_cols).aggregate(agg_expr)


# ── KPI calculations (pandas post-processing) ─────────────────────────────────

def _calc_yoy_diff(df: pd.DataFrame, measure_col: str, kpi_id: str) -> pd.DataFrame:
    """Year-over-year absolute difference (pp for rates)."""
    df = df.sort_values(["region", "year"])
    df[kpi_id] = df.groupby("region")[measure_col].diff()
    return df.drop(columns=[measure_col])


def _calc_yoy_pct(df: pd.DataFrame, measure_col: str, kpi_id: str) -> pd.DataFrame:
    """Year-over-year percentage change."""
    df = df.sort_values(["region", "year"])
    df[kpi_id] = df.groupby("region")[measure_col].pct_change() * 100
    return df.drop(columns=[measure_col])


def _calc_rank_asc(df: pd.DataFrame, measure_col: str, kpi_id: str) -> pd.DataFrame:
    """Rank within year: 1 = lowest value (best for lower_is_better)."""
    df[kpi_id] = df.groupby("year")[measure_col].rank(method="min", ascending=True)
    return df.drop(columns=[measure_col])


def _calc_rank_desc(df: pd.DataFrame, measure_col: str, kpi_id: str) -> pd.DataFrame:
    """Rank within year: 1 = highest value (best for higher_is_better)."""
    df[kpi_id] = df.groupby("year")[measure_col].rank(method="min", ascending=False)
    return df.drop(columns=[measure_col])


_KPI_FN = {
    "yoy_diff":  _calc_yoy_diff,
    "yoy_pct":   _calc_yoy_pct,
    "rank_asc":  _calc_rank_asc,
    "rank_desc": _calc_rank_desc,
}


# ── Public query interface ─────────────────────────────────────────────────────

def query_measure(
    domain: Domain,
    measure_id: str,
    group_by: list[str] | None = None,
    regions: list[str] | None = None,
    year_range: tuple[int, int] | None = None,
    year: int | None = None,
) -> pd.DataFrame:
    """
    Query a measure from its source fact table.

    Returns a DataFrame with group_by columns + measure column.
    group_by defaults to all dimensions defined in the domain.
    """
    measure   = domain.get_measure(measure_id)
    fact      = domain.get_fact_for_measure(measure)
    conn      = _get_conn()
    table     = conn.table(fact.table, database=fact.schema)
    group_by  = group_by or list(domain.dimensions.keys())

    # ── Filters ───────────────────────────────────────────────────────────────
    if regions is not None:
        table = table.filter(table.region.isin(regions))

    if year is not None:
        table = table.filter(table.year == year)
    elif year_range is not None:
        y_from, y_to = year_range
        table = table.filter((table.year >= y_from) & (table.year <= y_to))

    # ── Aggregation ───────────────────────────────────────────────────────────
    result = _apply_aggregation(table, measure, group_by)
    df = result.execute()

    # Cast Decimal columns to float for Plotly compatibility
    for col in df.select_dtypes(include="object").columns:
        try:
            df[col] = df[col].astype(float)
        except (ValueError, TypeError):
            pass

    return df


def query_kpi(
    domain: Domain,
    kpi_id: str,
    regions: list[str] | None = None,
    year_range: tuple[int, int] | None = None,
    year: int | None = None,
) -> pd.DataFrame:
    """
    Query a KPI (derived from a base measure).

    KPIs that require temporal context (yoy_*) always include year.
    Returns a DataFrame with dimension columns + kpi column.
    """
    kpi       = domain.get_kpi(kpi_id)
    calc_fn   = _KPI_FN.get(kpi.calculation)
    if calc_fn is None:
        raise ValueError(f"Unknown KPI calculation: {kpi.calculation}")

    # KPIs always need both region and year
    df = query_measure(
        domain, kpi.base_measure,
        group_by=["region", "year"],
        regions=regions,
        year_range=year_range,
        year=year,
    )
    df = calc_fn(df, kpi.base_measure, kpi_id)
    return df
