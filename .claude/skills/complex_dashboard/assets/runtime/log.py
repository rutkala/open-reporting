"""Logging and environment helpers for domain dashboards.

Three helpers — call them at the top of ``app.py``:

- ``configure_logging(level=logging.INFO)`` — sets the root logger
  format and level once. Idempotent (will not duplicate handlers).
- ``get_logger(name)`` — thin wrapper around ``logging.getLogger`` so
  every dashboard imports its logger from the same place.
- ``require_env(name)`` — read an env var and raise ``RuntimeError`` if
  unset or empty. Use for ``DUCKDB_PATH`` and similar startup-critical
  values so misconfiguration fails at import, not on the first request.

Deliberately not included: JSON log formatter, log shipping, structured
context. Add when a dashboard genuinely needs them; for current scale
plain stdout is enough.
"""
import logging
import os
import sys

_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger for stdout output.

    Idempotent — repeated calls reset the level and replace any prior
    handler installed by this function. Other libraries' handlers are
    left untouched.
    """
    root = logging.getLogger()
    root.setLevel(level)
    for h in list(root.handlers):
        if getattr(h, "_open_reporting_dashboard_handler", False):
            root.removeHandler(h)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
    handler._open_reporting_dashboard_handler = True  # type: ignore[attr-defined]
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return ``logging.getLogger(name)``.

    A wrapper exists only so dashboards have a single place to import
    from (``from complex_dashboard.assets.runtime import get_logger``)
    rather than scattering ``import logging`` everywhere.
    """
    return logging.getLogger(name)


def require_env(name: str) -> str:
    """Return the value of env var ``name`` or raise ``RuntimeError``.

    Treats unset and empty-string as the same failure — both indicate
    misconfiguration. Call once at module load for every variable the
    app cannot start without (``DUCKDB_PATH`` is the canonical example).
    """
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Required environment variable {name!r} is unset or empty. "
            f"Set it before starting the dashboard."
        )
    return value
