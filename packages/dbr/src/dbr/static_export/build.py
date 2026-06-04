"""Build a dashboard to a self-contained static HTML directory.

Produces, under ``<out_dir>/<domain>/``:
  - ``index.html``     — the full page (head + serialized layout + client JS)
  - ``plotly.min.js``  — plotly.js vendored once, referenced relatively

The page reuses the *exact* same stylesheet and client-side scripts as the live
Dash server (``dbr.make_app._CSS`` / ``_SCROLLSPY_JS`` / ``_SIDEBAR_TOGGLE_JS``)
and the same ``<meta name="dbr-build">`` stamp, so layout and behaviour are
identical — only Dash's React/renderer bundle and the always-on Python server
are gone. nginx serves the files directly; nothing runs at request time.
"""
from __future__ import annotations

from pathlib import Path

from dbr.compiler.compiler import build_shell, load_dashboard
from dbr.make_app.make_app import (
    _CSS,
    _SCROLLSPY_JS,
    _SIDEBAR_TOGGLE_JS,
    build_sha,
)
from dbr.static_export.serialize import UnsupportedComponentError, render_node


def _document(*, title: str, body_html: str, build: str) -> str:
    return (
        "<!DOCTYPE html>\n<html>\n<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'  <meta name="dbr-build" content="{build}">\n'
        f"  <title>{title}</title>\n"
        '  <script src="plotly.min.js" charset="utf-8"></script>\n'
        f"  <style>{_CSS}</style>\n"
        "</head>\n<body>\n"
        f"{body_html}\n"
        f"  <script>{_SCROLLSPY_JS}</script>\n"
        f"  <script>{_SIDEBAR_TOGGLE_JS}</script>\n"
        "</body>\n</html>\n"
    )


def build_static_dashboard(path: str | Path, out_dir: str | Path) -> Path:
    """Render the dashboard at ``path`` to ``<out_dir>/<domain>/``. Returns the
    written ``index.html`` path. Raises ``UnsupportedComponentError`` if the
    dashboard uses runtime interactivity (slicers, cross-filter, tabs)."""
    from plotly.offline import get_plotlyjs

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
    )

    dest = Path(out_dir) / domain
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "plotly.min.js").write_text(get_plotlyjs(), encoding="utf-8")
    index = dest / "index.html"
    index.write_text(html_doc, encoding="utf-8")
    return index
