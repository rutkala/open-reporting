"""Semantic-layer query helper for KPI cards and chart data.

Wraps the `mf query` CLI (dbt-metricflow) so domain dashboards can ask for a
metric by name without knowing the source table, column, or filter SQL:

    from dbr.semantic import semantic_query, semantic_query_history

    r = semantic_query("fiscal_balance", filter={"geo": "PL"})
    r.value         # -6.5
    r.value_str     # "-6,5"
    r.unit_str      # "% PKB"
    r.formatted     # "-6,5 % PKB"
    r.period        # 2024
    r.label         # "Saldo finansów publicznych"
    r.meta          # {"thresholds": {...}, "source_label": "...", ...}

    history = semantic_query_history("fiscal_balance", filter={"geo": "PL"}, n=2)
    # [latest, prior]  — for YoY computation

Performance note: each call invokes `mf query` as a subprocess (~300ms).
For ≤6 metrics on a single page render this is acceptable. If it becomes
a bottleneck, swap the implementation for the MetricFlow Python API or add
an in-memory TTL cache here — the public API stays the same.
"""
from __future__ import annotations

import logging
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import yaml

log = logging.getLogger(__name__)

DBT_PROJECT_ROOT = Path("/opt/open-reporting/platform/processing/dbt")
SEMANTIC_MODELS_GLOB = "models/**/semantic_models/*.yml"


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
    rows = _run_mf_query(metric, filter=filter, limit=1)
    return _build_result(metric, rows[0]) if rows else _build_result(metric, None)


def semantic_query_history(
    metric: str,
    *,
    filter: dict[str, str] | None = None,
    n: int = 2,
) -> list[SemanticResult]:
    """Last `n` rows ordered by metric_time descending. Newest first."""
    rows = _run_mf_query(metric, filter=filter, limit=n)
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
    or a list (mf returns one column per metric in the latter case).
    ``group_by`` is a list of MetricFlow dimension refs (e.g.
    ``["metric_time__year"]``, ``["geo"]``, or both). ``filter`` is a dict
    of entity/dimension → value (scalars or lists).

    Returns an empty DataFrame on query failure.
    """
    metrics_list = [metric] if isinstance(metric, str) else list(metric)
    cmd = ["mf", "query", "--metrics", ",".join(metrics_list)]
    # mf CLI quirk: passing multiple --group-by flags drops earlier ones.
    # Use the comma-separated form which is processed as a single argument.
    if group_by:
        cmd += ["--group-by", ",".join(group_by)]
    if filter:
        clauses = []
        for k, v in filter.items():
            ref = _filter_ref(k)
            if isinstance(v, (list, tuple)):
                quoted = ", ".join(f"'{x}'" for x in v)
                clauses.append(f"{ref} IN ({quoted})")
            else:
                clauses.append(f"{ref}='{v}'")
        cmd += ["--where", " AND ".join(clauses)]
    if order:
        cmd += ["--order", order]
    if limit:
        cmd += ["--limit", str(limit)]

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as tmp:
        csv_path = tmp.name
    cmd += ["--csv", csv_path]

    try:
        subprocess.run(
            cmd, cwd=str(DBT_PROJECT_ROOT), check=True,
            capture_output=True, text=True, env=_mf_env(),
        )
        return pd.read_csv(csv_path)
    except subprocess.CalledProcessError as e:
        log.error("mf query failed for %s: %s", metric, e.stderr)
        return pd.DataFrame()
    finally:
        Path(csv_path).unlink(missing_ok=True)


def _filter_ref(key: str) -> str:
    """Return the MetricFlow ref expression for a filter key.

    Entities and dimensions use different syntax. Our `finance_overview`
    semantic model declares `geo` as a primary entity and `period` as a
    time dimension — for now we hard-code that distinction; later this
    can be resolved by inspecting the parsed semantic_model YAML.
    """
    _ENTITY_KEYS = {"geo"}
    if key in _ENTITY_KEYS:
        return f"{{{{ Entity('{key}') }}}}"
    return f"{{{{ Dimension('{key}') }}}}"


def _run_mf_query(
    metric: str,
    *,
    filter: dict[str, str] | None = None,
    limit: int | None = None,
) -> list[dict]:
    """Invoke `mf query` and return the result as a list of row dicts (newest first)."""
    cmd = [
        "mf", "query",
        "--metrics", metric,
        "--group-by", "metric_time__year",
        "--order", "-metric_time__year",
    ]
    if filter:
        clauses = " AND ".join(
            f"{{{{ Entity('{k}') }}}}='{v}'" for k, v in filter.items()
        )
        cmd += ["--where", clauses]
    if limit:
        cmd += ["--limit", str(limit)]

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as tmp:
        csv_path = tmp.name
    cmd += ["--csv", csv_path]

    try:
        subprocess.run(
            cmd,
            cwd=str(DBT_PROJECT_ROOT),
            check=True,
            capture_output=True,
            text=True,
            env=_mf_env(),
        )
        df = pd.read_csv(csv_path)
    except subprocess.CalledProcessError as e:
        log.error("mf query failed for %s: %s", metric, e.stderr)
        return []
    finally:
        Path(csv_path).unlink(missing_ok=True)

    if df.empty or metric not in df.columns:
        return []
    return df.to_dict(orient="records")


def _mf_env() -> dict[str, str]:
    """Environment for the `mf` subprocess — passes through DUCKDB_PATH and DBT_PROFILES_DIR."""
    import os
    env = os.environ.copy()
    env.setdefault("DBT_PROFILES_DIR", str(DBT_PROJECT_ROOT))
    return env


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
    """metric_time__year arrives as a 'YYYY-01-01T00:00:00' string."""
    if ts is None or (isinstance(ts, float) and pd.isna(ts)):
        return None
    s = str(ts)
    return int(s[:4]) if len(s) >= 4 and s[:4].isdigit() else None


def _format_pl(value: float, decimals: int) -> str:
    """Polish number format: NBSP thousands separator, comma decimal."""
    raw = f"{value:,.{decimals}f}"
    # Two-step swap to avoid collisions: ',' → \u00a0 thousands, '.' → ','
    return raw.replace(",", "\u00a0").replace(".", ",")


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
