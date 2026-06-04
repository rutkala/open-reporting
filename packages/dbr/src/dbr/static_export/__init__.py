"""Static HTML export for dbr dashboards — renders a no-callback dashboard to a
self-contained directory served directly by nginx (no always-on Python server)."""
from dbr.static_export.build import build_static_dashboard, write_plotlyjs
from dbr.static_export.serialize import (
    UnsupportedComponentError,
    render_node,
)

__all__ = [
    "build_static_dashboard",
    "write_plotlyjs",
    "render_node",
    "UnsupportedComponentError",
]
