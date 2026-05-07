"""Shared layout styles for every Open Reporting dashboard.

The `S` dict and layout constants here are the single source of truth. All
dashboards import `S`, `SIDEBAR_W`, and `SIDEBAR_COLLAPSED` directly — they
are never redefined inline in `app.py`. Colour tokens come from
`products.visuals.lib.theme`.
"""
from products.visuals.lib.theme import (
    BG_PAGE,
    BG_SURFACE,
    BORDER,
    FONT_FAMILY,
    SUBTEXT,
    TEXT,
)

SIDEBAR_W = "240px"
SIDEBAR_COLLAPSED = "44px"
GAP = "4px"
RADIUS = "10px"

S = {
    # ── Page shell ────────────────────────────────────────────────────────────
    "body": {
        "fontFamily": FONT_FAMILY,
        "background": BG_PAGE, "color": TEXT,
        "height": "100vh", "display": "flex", "margin": 0,
        "padding": f"{GAP} 0 {GAP} {GAP}",
        "boxSizing": "border-box",
        "overflow": "hidden",
    },

    # ── Sidebar ───────────────────────────────────────────────────────────────
    "sidebar": {
        "width": SIDEBAR_W, "flexShrink": 0,
        "background": BG_SURFACE,
        "borderRadius": RADIUS,
        "boxShadow": "0 2px 8px rgba(0,0,0,0.06), 0 0 1px rgba(0,0,0,0.08)",
        "display": "flex", "flexDirection": "column",
        "height": f"calc(100vh - {GAP} * 2)",
        "overflow": "hidden",
        "transition": "width 0.25s ease",
        "position": "relative",
    },
    "sidebar-logo": {
        "padding": "20px 20px 16px",
        "whiteSpace": "nowrap", "overflow": "hidden",
        "height": "68px", "boxSizing": "border-box",
        "display": "flex", "alignItems": "center",
    },
    "sidebar-divider": {"margin": "0 16px", "border": "none", "borderTop": f"1px solid {BORDER}"},
    "logo": {"height": "32px", "width": "auto"},
    "sidebar-nav": {
        "flex": 1, "padding": "16px 0",
        "overflowY": "auto", "whiteSpace": "nowrap", "overflow": "hidden",
    },
    "nav-item": {
        "display": "block", "padding": "8px 20px",
        "fontSize": "13px", "color": SUBTEXT, "textDecoration": "none", "cursor": "pointer",
    },
    "nav-item-active": {
        "display": "block", "padding": "8px 20px",
        "fontSize": "13px", "color": TEXT, "textDecoration": "none",
        "borderLeft": f"3px solid {TEXT}", "backgroundColor": f"{BORDER}40", "cursor": "pointer",
    },
    "nav-item-section-label": {
        "display": "block", "padding": "8px 20px",
        "fontSize": "11px", "color": SUBTEXT, "textDecoration": "none",
        "marginTop": "8px", "pointerEvents": "none",
    },
    "toggle-btn": {
        "position": "absolute", "top": "28px", "right": "10px",
        "width": "24px", "height": "24px",
        "background": "none", "border": "none", "cursor": "pointer", "padding": 0,
        "display": "flex", "alignItems": "center", "justifyContent": "center", "zIndex": 100,
    },
    "toggle-icon": {"width": "20px", "height": "20px", "opacity": 0.5},

    # ── Main column ───────────────────────────────────────────────────────────
    "main": {
        "flex": 1, "minWidth": 0,
        "overflowY": "auto", "overflowX": "hidden",
        "height": f"calc(100vh - {GAP} * 2)",
        "boxSizing": "border-box",
        "display": "flex", "flexDirection": "column",
    },

    # ── Header ────────────────────────────────────────────────────────────────
    "main-header": {
        "padding": "0 32px", "flexShrink": 0,
        "display": "flex", "alignItems": "center", "justifyContent": "space-between",
        "height": "68px",
    },
    "header-actions": {"display": "flex", "alignItems": "center", "gap": "8px"},
    "header-btn": {
        "width": "32px", "height": "32px",
        "background": "none", "border": f"1px solid {BORDER}", "borderRadius": "6px",
        "cursor": "pointer", "display": "flex", "alignItems": "center", "justifyContent": "center",
        "color": SUBTEXT, "padding": 0,
    },
    "header-icon": {"width": "16px", "height": "16px"},
    "main-divider": {"margin": "0 32px", "border": "none", "borderTop": f"1px solid {BORDER}"},

    # ── Footer ────────────────────────────────────────────────────────────────
    "footer-divider": {"margin": "0 32px", "border": "none", "borderTop": f"1px solid {BORDER}"},
    "main-footer": {
        "padding": "0 32px", "flexShrink": 0,
        "display": "flex", "alignItems": "center", "justifyContent": "space-between",
        "height": "48px",
    },
    "footer-text": {"fontSize": "12px", "color": SUBTEXT},

    # ── Content area ──────────────────────────────────────────────────────────
    "main-content-area": {
        "flex": 1, "padding": "28px 32px 32px",
        "overflowY": "auto", "width": "100%", "boxSizing": "border-box",
    },

    # ── Section typography ────────────────────────────────────────────────────
    "section-heading": {
        "fontSize": "18px", "fontWeight": "700", "color": TEXT,
        "marginBottom": "6px", "marginTop": "48px",
    },
    "section-desc": {"fontSize": "13px", "color": SUBTEXT, "marginBottom": "24px"},

    # ── Content groups (optional sub-grouping within a section) ───────────────
    "group": {"marginBottom": "28px", "width": "100%"},
    "group-title": {"fontSize": "13px", "fontWeight": 600, "color": SUBTEXT, "marginBottom": "12px"},

    # ── Grid layouts ──────────────────────────────────────────────────────────
    "grid-2":    {"display": "grid", "gridTemplateColumns": "1fr 1fr",          "gap": "20px", "alignItems": "start"},
    "grid-3":    {"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr",      "gap": "20px", "alignItems": "start"},
    "grid-4":    {"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)",   "gap": "16px", "alignItems": "start"},
    "grid-auto": {
        "display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))",
        "gap": "16px", "maxWidth": "100%",
    },

    # ── Card container ────────────────────────────────────────────────────────
    "card": {
        "background": BG_SURFACE, "border": f"1px solid {BORDER}",
        "borderRadius": "8px", "padding": "16px", "overflow": "hidden", "minWidth": 0,
    },
}
