"""Healthcheck endpoint registration.

`register_healthcheck(app, path="/health")` mounts a JSON liveness
probe on the underlying Flask server. systemd, nginx, and uptime
monitors call it to confirm the dashboard process is up — no auth,
no DB query, just "the WSGI app is responsive".

A more elaborate readiness probe (DuckDB ping, downstream API check)
can be added per-dashboard; this helper deliberately does the trivial
thing so it stays on every dashboard by default.
"""
from __future__ import annotations

from flask import jsonify


def register_healthcheck(app, path: str = "/health") -> None:
    """Register a JSON ``GET {path}`` route on the Dash app's Flask server.

    Returns ``{"status": "ok"}`` with HTTP 200. Idempotent — registering
    the same path twice raises ``AssertionError`` from Flask, so call
    once at app init.

    Parameters
    ----------
    app
        Dash app instance returned by ``make_app(...)``.
    path
        URL path under the dashboard's URL prefix. Default ``"/health"``;
        with ``url_base_pathname="/labour/"`` the full path becomes
        ``/labour/health``.
    """
    server = app.server
    endpoint = f"open_reporting_healthcheck_{path.strip('/').replace('/', '_') or 'root'}"

    @server.route(path, endpoint=endpoint)
    def _healthcheck():
        return jsonify({"status": "ok"})
