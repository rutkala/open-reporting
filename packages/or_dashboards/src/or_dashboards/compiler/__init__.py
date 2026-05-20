"""`compiler` block — the YAML→Dash translator.

A dashboard's ``app.py`` is one line: ``run_dashboard(__file__)``. The
compiler reads the PBIP-shaped folder next to ``app.py`` and builds the
running Dash app from the YAML tree.

Use:

    from or_dashboards.compiler import run_dashboard
    run_dashboard(__file__)
"""
from or_dashboards.compiler.compiler import run_dashboard

__all__ = ["run_dashboard"]
