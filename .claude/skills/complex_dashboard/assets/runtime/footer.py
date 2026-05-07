"""Shared footer builder.

`build_footer(name, *, source, updated)` returns the footer divider
plus the ``main-footer`` block. The footer is mandatory on every
dashboard — left slot carries the dashboard name in Polish plus the
source attribution line, right slot links to open-reporting.dev.

`source` and `updated` are required keyword-only arguments. Calling
without them raises ``TypeError`` at app import. The standard in
``team/standards/build/visualisation.md`` requires source attribution
on every published dashboard; the API enforces it.
"""
from dash import html

from complex_dashboard.assets.runtime.styles import S


def build_footer(
    name: str,
    *,
    source: str,
    updated: str,
    link_label: str = "open-reporting.dev",
    link_href: str = "https://open-reporting.dev",
) -> list:
    """Return ``[divider_hr, footer]`` ready to spread into ``html.Main``.

    Parameters
    ----------
    name
        Dashboard name in Polish — same text as the header H1.
    source
        Authoritative data source — Polish, e.g. ``"GUS BDL"``,
        ``"Ministerstwo Finansów"``, ``"Eurostat"``. Required.
    updated
        Last refresh date or coverage window — Polish, e.g.
        ``"luty 2026"``, ``"2018–2024"``. Required.
    link_label
        Right-slot link text. Default ``"open-reporting.dev"`` — only
        override for branded variants.
    link_href
        Right-slot link target.

    The left slot renders as ``"{name} · Dane: {source} — aktualizacja:
    {updated}"``.
    """
    attribution = f"Dane: {source} — aktualizacja: {updated}"
    return [
        html.Hr(style=S["footer-divider"]),
        html.Footer(style=S["main-footer"], children=[
            html.Span(f"{name} · {attribution}", style=S["footer-text"]),
            html.A(
                link_label, href=link_href,
                style={**S["footer-text"], "textDecoration": "none"},
            ),
        ]),
    ]
