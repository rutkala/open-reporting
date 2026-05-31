"""`layout` block — the visible chrome wrapped around every dashboard.

Exposes:

- ``page_shell(sections)`` — outer page wrapper that composes the full
  chrome: optional header + sidebar + main canvas + optional footer.
- ``build_header(title, subtitle)`` — full-width page header bar.
- ``build_footer(source, updated)`` — full-width page footer bar.
- ``build_sidebar(sections)`` — sticky left/right nav sidebar.

Each layout function imports theme tokens internally; dashboards never
style the layout themselves.
"""
from dbr.layout.footer import build_footer
from dbr.layout.header import build_header
from dbr.layout.page_shell import page_shell
from dbr.layout.sidebar import build_sidebar

__all__ = ["page_shell", "build_header", "build_footer", "build_sidebar"]
