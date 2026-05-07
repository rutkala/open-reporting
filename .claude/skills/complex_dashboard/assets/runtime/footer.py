"""Shared footer builder.

`build_footer(name)` returns the footer divider plus the ``main-footer``
block. The footer is mandatory on every dashboard — left slot carries
the dashboard name in Polish, right slot links to open-reporting.dev.
"""
from dash import html

from complex_dashboard.assets.runtime.styles import S


def build_footer(
    name: str,
    *,
    link_label: str = "open-reporting.dev",
    link_href: str = "https://open-reporting.dev",
) -> list:
    """Return ``[divider_hr, footer]`` ready to spread into ``html.Main``.

    Parameters
    ----------
    name
        Dashboard name in Polish — same text as the header H1.
    link_label
        Right-slot link text. Default ``"open-reporting.dev"`` — only
        override for branded variants.
    link_href
        Right-slot link target.
    """
    return [
        html.Hr(style=S["footer-divider"]),
        html.Footer(style=S["main-footer"], children=[
            html.Span(name, style=S["footer-text"]),
            html.A(
                link_label, href=link_href,
                style={**S["footer-text"], "textDecoration": "none"},
            ),
        ]),
    ]
