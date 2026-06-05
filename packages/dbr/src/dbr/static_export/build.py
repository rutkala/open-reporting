"""Build a dashboard to a self-contained static HTML directory.

Produces, under ``<out_dir>/<domain>/``:
  - ``index.html``     — the full page (head + serialized layout + client JS)
  - ``plotly.min.js``  — plotly.js vendored once, referenced relatively

The page reuses the *exact* same stylesheet and client-side scripts as the live
Dash server (``dbr.make_app._CSS`` / ``_SCROLLSPY_JS`` / ``_SIDEBAR_TOGGLE_JS`` /
``_RESIZE_JS``)
and the same ``<meta name="dbr-build">`` stamp, so layout and behaviour are
identical — only Dash's React/renderer bundle and the always-on Python server
are gone. nginx serves the files directly; nothing runs at request time.
"""
from __future__ import annotations

import os
from pathlib import Path

from dbr.compiler.compiler import build_shell, load_dashboard
from dbr.make_app.make_app import (
    _CSS,
    _RESIZE_JS,
    _SCROLLSPY_JS,
    _SIDEBAR_TOGGLE_JS,
    build_sha,
)
from dbr.static_export.serialize import UnsupportedComponentError, render_node


def _document(*, title: str, body_html: str, build: str, plotly_src: str) -> str:
    return (
        "<!DOCTYPE html>\n<html>\n<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'  <meta name="dbr-build" content="{build}">\n'
        f"  <title>{title}</title>\n"
        f'  <script src="{plotly_src}" charset="utf-8"></script>\n'
        f"  <style>{_CSS}</style>\n"
        "</head>\n<body>\n"
        f"{body_html}\n"
        f"  <script>{_SCROLLSPY_JS}</script>\n"
        f"  <script>{_SIDEBAR_TOGGLE_JS}</script>\n"
        f"  <script>{_RESIZE_JS}</script>\n"
        "</body>\n</html>\n"
    )


def write_plotlyjs(dest_dir: str | Path) -> Path:
    """Write plotly.min.js to ``dest_dir`` (created if needed). Returns the path.
    Used to vendor ONE shared copy across all dashboards rather than per page."""
    from plotly.offline import get_plotlyjs

    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / "plotly.min.js"
    out.write_text(get_plotlyjs(), encoding="utf-8")
    return out


def build_static_dashboard(
    path: str | Path,
    out_dir: str | Path,
    *,
    plotly_src: str = "plotly.min.js",
    vendor_plotly: bool = True,
) -> Path:
    """Render the dashboard at ``path`` to ``<out_dir>/<domain>/``. Returns the
    written ``index.html`` path. Raises ``UnsupportedComponentError`` if the
    dashboard uses runtime interactivity (slicers, cross-filter, tabs).

    ``plotly_src`` is the ``<script src>`` value (default the per-page relative
    ``plotly.min.js``; pass an absolute URL like ``/assets/plotly.min.js`` to share
    one cached copy across dashboards). ``vendor_plotly`` writes plotly.min.js next
    to the page — set False when a shared copy is published separately.
    """
    _project_root, config, ctx, sections = load_dashboard(path)

    if ctx.has_bindings() or ctx.needs_location:
        raise UnsupportedComponentError(
            f"Dashboard {config.get('domain')!r} uses runtime interactivity "
            f"(slicers / cross-filter / drill-through) and cannot be exported to "
            f"static HTML. Interactivity is on hold to save VPS resources (OR-168)."
        )

    domain = config["domain"]
    shell = build_shell(config, sections)
    body_html = render_node(shell)
    html_doc = _document(
        title=config.get("title", "") or domain,
        body_html=body_html,
        build=build_sha(),
        plotly_src=plotly_src,
    )

    dest = Path(out_dir) / domain
    dest.mkdir(parents=True, exist_ok=True)
    if vendor_plotly:
        write_plotlyjs(dest)
    index = dest / "index.html"
    # Atomic write: render to a temp file in the same dir, then rename into place,
    # so nginx never serves a half-written index.html during a rebuild.
    tmp = dest / ".index.html.tmp"
    tmp.write_text(html_doc, encoding="utf-8")
    os.replace(tmp, index)
    return index
