"""Runtime helpers imported by domain dashboards at app startup.

Public surface (re-exported here so dashboards can write a single import):

    from complex_dashboard.assets.runtime import (
        make_app, S, SIDEBAR_W, SIDEBAR_COLLAPSED,
        build_header, build_footer, build_sidebar,
        register_toggle_callback, build_page_layout,
        configure_logging, get_logger, require_env,
        register_healthcheck,
    )
"""
