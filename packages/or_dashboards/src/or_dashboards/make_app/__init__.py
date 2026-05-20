"""`make_app` block — builds and runs a Dash app for a domain.

Re-exports `make_app` and `run_app` so callers write:

    from or_dashboards.make_app import make_app, run_app

instead of the longer `from or_dashboards.make_app.make_app import ...`.
"""
from or_dashboards.make_app.make_app import make_app, run_app

__all__ = ["make_app", "run_app"]
