#!/usr/bin/env python3
"""
Smoke test for the semantic-layer helper (`runtime.semantic`).

Verifies that:
  - `mf` CLI is reachable
  - dbt-metricflow returns a value for each Overview metric (Poland)
  - The Polish formatter produces sensible output

Run:
    PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
    python3 .claude/skills/complex_dashboard/assets/example/semantic_smoke.py

Exit codes:
    0 — all metrics returned a numeric value
    1 — at least one metric is missing or formatting is broken
"""
import sys

from complex_dashboard.assets.runtime import (
    semantic_query,
    semantic_query_history,
)

METRICS = ("fiscal_balance", "public_debt", "govt_revenue")


def main() -> int:
    failures: list[str] = []

    for metric in METRICS:
        result = semantic_query(metric, filter={"geo": "PL"})
        if result.value is None:
            failures.append(f"{metric}: no value returned for geo=PL")
            continue
        if not result.formatted or result.formatted == "—":
            failures.append(f"{metric}: empty formatted string")
            continue
        if result.period is None or result.period < 1995:
            failures.append(f"{metric}: implausible period {result.period}")
            continue
        print(f"  {metric:18s} {result.formatted:25s} ({result.period})  label={result.label!r}")

    history = semantic_query_history("fiscal_balance", filter={"geo": "PL"}, n=2)
    if len(history) != 2:
        failures.append(f"history: expected 2 rows, got {len(history)}")
    elif history[0].period <= history[1].period:
        failures.append(f"history: rows not ordered descending ({history[0].period}, {history[1].period})")
    else:
        print(f"  history (n=2)      {history[0].period}: {history[0].value}, {history[1].period}: {history[1].value}")

    if failures:
        print("\nFAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nPASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
