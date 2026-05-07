"""Healthcheck endpoint registration.

`register_healthcheck(app, path="/health")` mounts a JSON liveness
probe on the underlying Flask server. systemd, nginx, and uptime
monitors call it to confirm the dashboard process is up — no auth,
no DB query, just "the WSGI app is responsive".

The route is registered under the dashboard's URL prefix (e.g.
``/labour/health``) so it lives at the same prefix as everything
else the reverse proxy serves for the domain, and so Dash's Pages
framework does not intercept it.
"""
from __future__ import annotations

from flask import jsonify


def register_healthcheck(app, path: str = "/health") -> None:
    """Register a JSON ``GET {prefix}{path}`` route on the Dash app.

    Returns ``{"status": "ok"}`` with HTTP 200. Idempotent — the same
    path can only be registered once on a given Flask server, so call
    once at app init.

    Parameters
    ----------
    app
        Dash app instance returned by ``make_app(...)``.
    path
        URL path appended to the dashboard's URL prefix. Default
        ``"/health"``; with ``url_base_pathname="/labour/"`` the full
        path becomes ``/labour/health``.
    """
    prefix = (app.config.get("routes_pathname_prefix") or "/").rstrip("/")
    full_path = f"{prefix}{path}"
    endpoint = (
        f"open_reporting_healthcheck_"
        f"{full_path.strip('/').replace('/', '_') or 'root'}"
    )

    @app.server.route(full_path, endpoint=endpoint)
    def _healthcheck():
        return jsonify({"status": "ok"})
