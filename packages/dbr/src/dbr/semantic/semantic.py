"""Semantic-layer query helper for KPI cards and chart data.

Uses the MetricFlow Python API directly (via dbt-metricflow's
``CLIConfiguration``) so domain dashboards can ask for a metric by name
without knowing the source table, column, or filter SQL:

    from dbr.semantic import semantic_query, semantic_query_history

    r = semantic_query("fiscal_balance", filter={"geo": "PL"})
    r.value         # -6.5
    r.formatted     # "-6,5 % PKB"
    r.label         # "Saldo finansów publicznych"

    history = semantic_query_history("fiscal_balance", filter={"geo": "PL"}, n=2)
    # [latest, prior]  — for YoY computation

Performance: the previous implementation spawned a fresh ``mf query``
subprocess per call, which paid ~6s of dbt-project-load overhead each
time. A dashboard with 10 visuals therefore took ~75s to boot.

This module now holds a process-wide ``MetricFlowEngine`` initialised
once on first use (~2s), with subsequent queries running at ~100ms each.
Same dashboard boots in ~5s. The public API is unchanged.
"""
from __future__ import annotations

import logging
import os
import pathlib
import threading
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import yaml

log = logging.getLogger(__name__)

DBT_PROJECT_ROOT = Path("/opt/open-reporting/platform/processing/dbt")
SEMANTIC_MODELS_GLOB = "models/**/semantic_models/*.yml"


# ── Engine singleton ──────────────────────────────────────────────────────────

_engine_lock = threading.Lock()
_engine = None  # type: "MetricFlowEngine | None"


def _get_engine():
    """Return the process-wide MetricFlowEngine, initialising on first use.

    The engine loads the dbt project (manifest + adapter + semantic
    manifest) once, which is the expensive step. Thread-safe via a lock
    so a concurrent first call from two threads doesn't run setup twice.
    """
    global _engine
    if _engine is not None:
        return _engine
    with _engine_lock:
        if _engine is not None:
            return _engine
        from dbt_metricflow.cli.cli_configuration import CLIConfiguration

        # MetricFlow honours DBT_PROFILES_DIR / DBT_PROJECT_DIR if set, but
        # we default both to the warehouse repo's dbt root so dashboards
        # don't need to set anything.
        os.environ.setdefault("DBT_PROFILES_DIR", str(DBT_PROJECT_ROOT))
        os.environ.setdefault("DBT_PROJECT_DIR", str(DBT_PROJECT_ROOT))

        cfg = CLIConfiguration()
        cfg.setup(
            dbt_profiles_path=pathlib.Path(DBT_PROJECT_ROOT),
            dbt_project_path=pathlib.Path(DBT_PROJECT_ROOT),
            configure_file_logging=False,
        )
        _engine = cfg.mf
        log.info("MetricFlowEngine initialised (one-time dbt project load)")
        return _engine


# ── Public API ────────────────────────────────────────────────────────────────


@dataclass
class SemanticResult:
    """Single metric observation with display metadata.

    Attributes:
        value:      Raw numeric value after applying meta.format.scale.
                    None when the metric has no data for the requested filter.
        period:     Calendar year of the observation.
        label:      Human-readable Polish metric label.
        meta:       Free-form dict from the metric YAML's config.meta block.
        value_str:  Polish-formatted number (e.g. "-6,5"), no unit.
        unit_str:   Unit suffix (e.g. "% PKB").
        formatted:  Combined "value_str unit_str" — single display string.
    """
    value: float | None
    period: int | None
    label: str
    meta: dict = field(default_factory=dict)
    value_str: str = "—"
    unit_str: str = ""
    formatted: str = "—"


def semantic_query(metric: str, *, filter: dict[str, str] | None = None) -> SemanticResult:
    """Latest single-row value for a metric. Returns SemanticResult."""
    rows = _run_latest_query(metric, filter=filter, limit=1)
    return _build_result(metric, rows[0]) if rows else _build_result(metric, None)


def semantic_query_history(
    metric: str,
    *,
    filter: dict[str, str] | None = None,
    n: int = 2,
) -> list[SemanticResult]:
    """Last ``n`` rows ordered by metric_time descending. Newest first."""
    rows = _run_latest_query(metric, filter=filter, limit=n)
    return [_build_result(metric, row) for row in rows]


def semantic_query_data(
    metric: str | list[str],
    *,
    group_by: list[str] | None = None,
    filter: dict[str, object] | None = None,
    limit: int | None = None,
    order: str | None = None,
) -> "pd.DataFrame":
    """Generic semantic query — returns a DataFrame keyed by group-by dimensions.

    Used by encoding-based visuals. ``metric`` accepts a single metric name
    or a list (the engine returns one column per metric in the latter case).
    ``group_by`` is a list of MetricFlow dimension refs (e.g.
    ``["metric_time__year"]``, ``["geo"]``, or both). ``filter`` is a dict
    of entity/dimension → value (scalars or lists).

    Returns an empty DataFrame on query failure.
    """
    metrics_list = [metric] if isinstance(metric, str) else list(metric)
    where = _build_where(filter) if filter else None
    return _run_engine_query(
        metrics=metrics_list,
        group_by=list(group_by) if group_by else None,
        where=where,
        order=[order] if order else None,
        limit=limit,
    )


# ── Internals ─────────────────────────────────────────────────────────────────


def _run_engine_query(
    *,
    metrics: list[str],
    group_by: list[str] | None,
    where: str | None,
    order: list[str] | None,
    limit: int | None,
) -> "pd.DataFrame":
    """Run a MetricFlow query through the in-process engine.

    Returns an empty DataFrame on error so visual factories can render
    a "No data" placeholder instead of crashing the whole dashboard.
    """
    from metricflow.engine.metricflow_engine import MetricFlowQueryRequest

    try:
        engine = _get_engine()
        req = MetricFlowQueryRequest.create(
            metric_names=metrics,
            group_by_names=group_by,
            where_constraints=[where] if where else None,
            order_by_names=order,
            limit=limit,
        )
        result = engine.query(mf_request=req)
        table = result.result_df
        if table is None or table.row_count == 0:
            return pd.DataFrame(columns=list(table.column_names) if table else [])
        return pd.DataFrame(list(table.rows), columns=list(table.column_names))
    except Exception as e:
        log.error("MetricFlow query failed for %s: %s", metrics, e)
        return pd.DataFrame()


def _run_latest_query(
    metric: str,
    *,
    filter: dict[str, str] | None = None,
    limit: int | None = None,
) -> list[dict]:
    """Latest-N rows for a metric, ordered by metric_time__year descending."""
    where = _build_where(filter) if filter else None
    df = _run_engine_query(
        metrics=[metric],
        group_by=["metric_time__year"],
        where=where,
        order=["-metric_time__year"],
        limit=limit,
    )
    if df.empty or metric not in df.columns:
        return []
    return df.to_dict(orient="records")


def _build_where(filter: dict[str, object]) -> str:
    """Translate a {key: value-or-list} filter dict into a single Jinja where clause."""
    clauses = []
    for k, v in filter.items():
        ref = _filter_ref(k)
        if isinstance(v, (list, tuple)):
            quoted = ", ".join(f"'{x}'" for x in v)
            clauses.append(f"{ref} IN ({quoted})")
        else:
            clauses.append(f"{ref}='{v}'")
    return " AND ".join(clauses)


def _filter_ref(key: str) -> str:
    """Return the MetricFlow ref expression for a filter key.

    Entities and dimensions use different syntax. The simple rule for
    Open Reporting facts: ``geo`` is always the foreign-entity join to
    dim_geo; everything else is a dimension reference (potentially
    qualified by entity prefix, e.g. ``date_key__cal_year``).
    """
    _ENTITY_KEYS = {"geo"}
    if key in _ENTITY_KEYS:
        return f"{{{{ Entity('{key}') }}}}"
    return f"{{{{ Dimension('{key}') }}}}"


def _build_result(metric: str, row: dict | None) -> SemanticResult:
    cfg = _load_metric_config(metric)
    label = cfg.get("label", metric)
    meta = cfg.get("meta", {})
    fmt = meta.get("format", {})

    if row is None or pd.isna(row.get(metric)):
        return SemanticResult(value=None, period=None, label=label, meta=meta)

    raw = float(row[metric])
    value = raw * fmt.get("scale", 1.0)
    period = _extract_year(row.get("metric_time__year"))

    value_str = _format_pl(value, fmt.get("decimals", 1))
    unit_str = fmt.get("suffix", "")
    formatted = f"{value_str} {unit_str}".strip() if unit_str else value_str

    return SemanticResult(
        value=value,
        period=period,
        label=label,
        meta=meta,
        value_str=value_str,
        unit_str=unit_str,
        formatted=formatted,
    )


def _extract_year(ts: object) -> int | None:
    """metric_time__year arrives as a datetime or 'YYYY-01-01...' string."""
    if ts is None or (isinstance(ts, float) and pd.isna(ts)):
        return None
    # datetime objects (the engine returns these directly)
    if hasattr(ts, "year"):
        return int(ts.year)
    s = str(ts)
    return int(s[:4]) if len(s) >= 4 and s[:4].isdigit() else None


def _format_pl(value: float, decimals: int) -> str:
    """Polish number format: NBSP thousands separator, comma decimal."""
    raw = f"{value:,.{decimals}f}"
    # Two-step swap to avoid collisions: ',' →   thousands, '.' → ','
    return raw.replace(",", " ").replace(".", ",")


_metric_config_cache: dict[str, dict] = {}


def metric_label(metric: str) -> str:
    """Look up a metric's display label from its semantic_model YAML.

    Falls back to the metric name when no label is defined. Used by chart
    visuals to render legend entries for multi-metric series.
    """
    try:
        return _load_metric_config(metric).get("label", metric)
    except KeyError:
        return metric


def _load_metric_config(metric: str) -> dict:
    """Read the metric's `label` + `config.meta` block from semantic_models YAML."""
    if metric in _metric_config_cache:
        return _metric_config_cache[metric]
    for yml in DBT_PROJECT_ROOT.glob(SEMANTIC_MODELS_GLOB):
        try:
            doc = yaml.safe_load(yml.read_text())
        except yaml.YAMLError:
            continue
        for m in (doc or {}).get("metrics", []):
            if m.get("name") == metric:
                cfg = {
                    "label": m.get("label", metric),
                    "meta": m.get("config", {}).get("meta", {}),
                }
                _metric_config_cache[metric] = cfg
                return cfg
    raise KeyError(f"Metric {metric!r} not found in any semantic_models/*.yml")
