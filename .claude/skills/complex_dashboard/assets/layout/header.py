"""Shared header builder.

`build_header(title, subtitle, domain, extra_actions=None)` returns the
``main-header`` block plus its trailing divider. The header tree is
identical across dashboards: H1 title + subtitle on the left, two
action buttons (settings + user) on the right. Dashboards supply only
the title text, the subtitle text, and the URL prefix used to build
asset paths.
"""
from dash import html

from complex_dashboard.assets.layout.styles import S
from products.visuals.lib.theme import SUBTEXT, TEXT


def build_header(
    title: str,
    subtitle: str,
    domain: str,
    *,
    extra_actions: list | None = None,
) -> list:
    """Return ``[header_div, divider_hr]`` ready to spread into ``html.Main``.

    Parameters
    ----------
    title
        Polish dashboard title — concise, no "Dashboard" suffix.
    subtitle
        Domain + date range, e.g. "Rynek pracy — GUS 2018–2024".
    domain
        URL prefix segment, must match ``make_app(domain=...)``.
    extra_actions
        Optional list of additional ``html.Button`` (or any) elements
        appended **after** the standard settings + user buttons.
    """
    actions: list = [
        html.Button(
            html.Img(src=f"/{domain}/assets/images/settings.svg", style=S["header-icon"]),
            id="btn-settings", style=S["header-btn"],
        ),
        html.Button(
            html.Img(src=f"/{domain}/assets/images/user.svg", style=S["header-icon"]),
            id="btn-user", style=S["header-btn"],
        ),
    ]
    if extra_actions:
        actions.extend(extra_actions)

    header = html.Div(id="main-header", style=S["main-header"], children=[
        html.Div(children=[
            html.H1(
                title,
                style={"fontSize": "20px", "fontWeight": 700, "color": TEXT, "margin": 0},
            ),
            html.P(
                subtitle,
                style={"fontSize": "13px", "color": SUBTEXT, "margin": "4px 0 0"},
            ),
        ]),
        html.Div(style=S["header-actions"], children=actions),
    ])

    return [header, html.Hr(style=S["main-divider"])]
