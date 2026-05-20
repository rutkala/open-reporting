"""`semantic` block — the formula-engine equivalent.

Wraps MetricFlow (`mf query` subprocess) so dashboards ask for a value
by metric name without knowing the source table, aggregation, or SQL.
Returns the value plus its semantic metadata (Polish label, unit,
format, thresholds) read from the metric's YAML definition.

Use:

    from or_dashboards.semantic import semantic_query, semantic_query_history

    r = semantic_query("fiscal_balance", filter={"geo": "PL"})
    r.value      # -6.5
    r.formatted  # "-6,5 % PKB"
    r.label      # "Saldo finansów publicznych"
"""
from or_dashboards.semantic.semantic import (
    SemanticResult,
    semantic_query,
    semantic_query_history,
)

__all__ = ["semantic_query", "semantic_query_history", "SemanticResult"]
