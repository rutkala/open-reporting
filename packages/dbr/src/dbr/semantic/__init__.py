"""`semantic` block — the formula-engine equivalent.

Wraps MetricFlow (`mf query` subprocess) so dashboards ask for a value
by metric name without knowing the source table, aggregation, or SQL.
Returns the value plus its semantic metadata (Polish label, unit,
format, thresholds) read from the metric's YAML definition.

Use:

    from dbr.semantic import semantic_query, semantic_query_data

    # Single latest value (for cards):
    r = semantic_query("fiscal_balance", filter={"geo": "PL"})
    r.value      # -6.5
    r.formatted  # "-6,5 % PKB"
    r.label      # "Saldo finansów publicznych"

    # Generic group-by query (for charts):
    df = semantic_query_data(
        "fiscal_balance",
        group_by=["metric_time__year"],
        filter={"geo": "PL"},
        order="metric_time__year",
    )
"""
from dbr.semantic.semantic import (
    SemanticResult,
    metric_label,
    semantic_query,
    semantic_query_data,
    semantic_query_history,
)

__all__ = [
    "metric_label",
    "semantic_query",
    "semantic_query_data",
    "semantic_query_history",
    "SemanticResult",
]
