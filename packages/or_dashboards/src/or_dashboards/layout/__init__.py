"""`layout` block — the visible chrome wrapped around every dashboard.

Currently exposes:

- ``page_shell(sections)`` — outer page wrapper that composes the sidebar
  and main canvas. Build the whole page tree with one call.
- ``build_sidebar(sections)`` — the sidebar component on its own (used by
  ``page_shell``, occasionally useful standalone).

To come: ``build_header``, ``build_footer``. Each layout function imports
theme tokens internally; dashboards never style the layout themselves.
"""
from or_dashboards.layout.page_shell import page_shell
from or_dashboards.layout.sidebar import build_sidebar

__all__ = ["page_shell", "build_sidebar"]
