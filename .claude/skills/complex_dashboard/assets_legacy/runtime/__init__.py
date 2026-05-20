"""Runtime helpers imported by domain dashboards at app startup.

Public surface — re-exported here so dashboards can write a single import:

    from complex_dashboard.assets.runtime import (
        make_app, S, SIDEBAR_W, SIDEBAR_COLLAPSED,
        build_header, build_footer,
        build_sidebar, register_toggle_callback,
        build_page_layout,
        configure_logging, get_logger, require_env,
        register_healthcheck,
    )

Helpers added in later phases (multi-page nav from page_registry,
extra observability hooks) are re-exported here as they land.
"""
from complex_dashboard.assets.runtime.app_init import make_app
from complex_dashboard.assets.runtime.footer import build_footer
from complex_dashboard.assets.runtime.header import build_header
from complex_dashboard.assets.runtime.healthcheck import register_healthcheck
from complex_dashboard.assets.runtime.log import (
    configure_logging,
    get_logger,
    require_env,
)
from complex_dashboard.assets.runtime.page_shell import build_page_layout
from complex_dashboard.assets.runtime.semantic import (
    SemanticResult,
    semantic_query,
    semantic_query_history,
)
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
    "build_page_layout",
    "configure_logging",
    "get_logger",
    "require_env",
    "register_healthcheck",
    "semantic_query",
    "semantic_query_history",
    "SemanticResult",
    "S",
    "SIDEBAR_W",
    "SIDEBAR_COLLAPSED",
    "GAP",
    "RADIUS",
]
