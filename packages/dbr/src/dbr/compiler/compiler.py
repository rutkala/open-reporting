"""compiler — reads a PBIP-shaped dashboard folder and builds a Dash app.

Folder shape (relative to the calling ``app.py``):

    products/dashboards/<domain>/
    ├── app.py                          ← one-line entry point, calls run_dashboard(__file__)
    ├── dashboard.yml                   ← root: domain, port, title (later: footer)
    └── pages/
        ├── pages.yml                   ← page order: [overview, trend, ...]
        └── <page>/
            ├── page.yml                ← page title, anchor (later: page filters)
            └── visuals/
                ├── visuals.yml         ← row layout (see below)
                └── <visual>.yml        ← one file per visual (type + metric + filter + options)

``visuals.yml`` supports two shapes:

  Short (one-column stack):
    order:
      - kpi_balance
      - trend_chart

  Explicit (multi-column rows, Rill canvas-style):
    rows:
      - items:                         # row 1 — three KPIs side by side
          - visual: kpi_balance
            width: "33%"
          - visual: kpi_debt
            width: "33%"
          - visual: kpi_revenue
            width: "33%"
      - items:                         # row 2 — one full-width chart
          - visual: trend_chart
            width: "100%"

  Items can also be bare strings (auto-equal-width, no override):
    rows:
      - items: [kpi_balance, kpi_debt, kpi_revenue]
      - items: [trend_chart]

Theme is fixed at the kit level and never appears in the dashboard tree.
Semantic model lives in ``products/warehouse/`` and is referenced by
metric name from visuals — never duplicated per dashboard.

The compiler walks this tree, instantiates each visual via the
``VISUAL_REGISTRY`` exposed by ``dbr.visuals``, hands the
resulting tree to ``page_shell``, and starts the server.
"""
from pathlib import Path

import yaml

from dbr.layout import page_shell
from dbr.make_app import make_app, run_app
from dbr.visuals import VISUAL_REGISTRY


def run_dashboard(path: str | Path) -> None:
    """Build and run the dashboard at ``path``.

    Accepts either:
      - a directory path (e.g. ``"products/dashboards/finance"``) — the
        project root containing ``dashboard.yml``, or
      - a file path (e.g. ``__file__`` from a calling ``app.py``) — the
        compiler uses its parent directory as the project root.
    """
    p = Path(path).resolve()
    project_root = p if p.is_dir() else p.parent
    config = _load_yaml(project_root / "dashboard.yml")

    sections = _load_pages(project_root / "pages")

    app = make_app(config["domain"])
    app.layout = page_shell(sections=sections)
    run_app(app, port=config["port"])


# A section is (title, anchor, rows). A row is (title-or-None, prose-or-None,
# list of (component, width-or-None)). Row title is optional H3 sub-heading;
# prose is optional Markdown paragraph rendered above the row items.
Row = tuple[str | None, str | None, list[tuple[object, str | None]]]
Section = tuple[str, str, list[Row]]


def _load_pages(pages_dir: Path) -> list[Section]:
    """Return ``[(title, anchor, rows), ...]`` in the declared page order."""
    if not pages_dir.exists():
        return []
    meta = _load_yaml(pages_dir / "pages.yml")
    sections: list[Section] = []
    for page_name in meta.get("order", []) or []:
        page_dir = pages_dir / page_name
        page_config = _load_yaml(page_dir / "page.yml")
        rows = _load_page_rows(page_dir / "visuals")
        sections.append((page_config["title"], page_config["anchor"], rows))
    return sections


def _load_page_rows(visuals_dir: Path) -> list[Row]:
    """Parse ``visuals.yml`` into a list of rows.

    Each row is ``(title-or-None, [(component, width-or-None), ...])``.
    The optional row title renders as an H3 sub-heading above the row
    items in ``page_shell``.
    """
    if not visuals_dir.exists():
        return []
    meta = _load_yaml(visuals_dir / "visuals.yml")

    # Normalize the two YAML shapes into a single internal form:
    #   rows_spec = [{"title"?: str, "items": [<string-or-dict>, ...]}, ...]
    if "rows" in meta:
        rows_spec = meta.get("rows") or []
    elif "order" in meta:
        # Short form: each entry becomes its own row of width 100% (no titles)
        rows_spec = [{"items": [name]} for name in (meta.get("order") or [])]
    else:
        return []

    rows: list[Row] = []
    for row_spec in rows_spec:
        is_dict = isinstance(row_spec, dict)
        row_title = row_spec.get("title") if is_dict else None
        row_prose = row_spec.get("prose") if is_dict else None
        row_items: list[tuple[object, str | None]] = []
        for item in row_spec.get("items", []) or []:
            if isinstance(item, str):
                visual_name, width = item, None
            else:
                visual_name = item["visual"]
                width = item.get("width")
            spec = _load_yaml(visuals_dir / f"{visual_name}.yml")
            row_items.append((_build_visual(spec), width))
        rows.append((row_title, row_prose, row_items))
    return rows


def _build_visual(spec: dict):
    vtype = spec.get("type")
    if vtype is None:
        raise ValueError(f"Visual spec missing required 'type': {spec}")
    if vtype not in VISUAL_REGISTRY:
        available = ", ".join(sorted(VISUAL_REGISTRY)) or "<none registered>"
        raise KeyError(
            f"Unknown visual type {vtype!r}. Available: {available}"
        )
    factory = VISUAL_REGISTRY[vtype]
    title    = spec.get("title")
    subtitle = spec.get("subtitle")
    kwargs = {k: v for k, v in spec.items() if k not in ("type", "title", "subtitle")}
    component = factory(**kwargs)
    if title or subtitle:
        _prepend_title(component, title, subtitle)
    return component


def _prepend_title(card, title: str | None, subtitle: str | None) -> None:
    """Mutate a rendered card Div to prepend a title/subtitle header."""
    from dash import html
    nodes: list = []
    if title:
        nodes.append(html.Div(title, style={
            "fontSize": "13px", "fontWeight": 600, "color": "#2D3339",
            "marginBottom": "2px" if subtitle else "8px",
            "lineHeight": "1.3",
        }))
    if subtitle:
        nodes.append(html.Div(subtitle, style={
            "fontSize": "11px", "color": "#6B7A85",
            "marginBottom": "8px", "lineHeight": "1.3",
        }))
    if isinstance(card.children, list):
        card.children = nodes + card.children
    elif card.children is not None:
        card.children = nodes + [card.children]
    else:
        card.children = nodes


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text()) or {}
