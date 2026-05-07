"""Runtime helpers imported by domain dashboards at app startup.

Public surface — re-exported here so dashboards can write a single import:

    from complex_dashboard.assets.runtime import (
        make_app, S, SIDEBAR_W, SIDEBAR_COLLAPSED,
        build_header, build_footer,
        build_sidebar, register_toggle_callback,
    )

Helpers added in later phases (build_page_layout, configure_logging,
get_logger, require_env, register_healthcheck) are re-exported as they
land.
"""
from complex_dashboard.assets.runtime.app_init import make_app
from complex_dashboard.assets.runtime.footer import build_footer
from complex_dashboard.assets.runtime.header import build_header
from complex_dashboard.assets.runtime.sidebar_nav import (
    build_sidebar,
    register_toggle_callback,
)
from complex_dashboard.assets.runtime.styles import (
    GAP,
    RADIUS,
    S,
    SIDEBAR_COLLAPSED,
    SIDEBAR_W,
)

__all__ = [
    "make_app",
    "build_footer",
    "build_header",
    "build_sidebar",
    "register_toggle_callback",
    "S",
    "SIDEBAR_W",
    "SIDEBAR_COLLAPSED",
    "GAP",
    "RADIUS",
]
