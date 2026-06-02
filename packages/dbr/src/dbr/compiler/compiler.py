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
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import yaml

from dbr.layout import page_shell
from dbr.make_app import make_app, run_app
from dbr.visuals import VISUAL_REGISTRY


@dataclass
class _SlicerBinding:
    """One chart ↔ slicer wiring collected during the build phase."""
    container_id: str
    filter_from: dict[str, str]   # {slicer_id: filter_key}
    factory: Callable
    base_kwargs: dict[str, Any]


@dataclass
class _CrossFilterSource:
    """A chart that emits click events as filter signals (cross_filter: true)."""
    graph_id: str          # Plotly dcc.Graph component ID
    slicer_id: str         # virtual slicer_id exposed to filter_from
    dimension: str         # which data column value to extract from clickData


@dataclass
class _DrillThrough:
    """A chart that navigates to a target page anchor on click."""
    graph_id: str            # Plotly dcc.Graph component ID
    target_anchor: str       # page anchor to scroll to (href)
    pass_filter: dict[str, str]  # {filter_key: dimension_col} to read from clickData
    slicer_id: str           # virtual slicer_id for the drilled value


@dataclass
class BuildContext:
    """Accumulates slicer + chart bindings during the compile phase."""
    slicers: dict[str, str] = field(default_factory=dict)          # slicer_id → Dash component id
    bindings: list[_SlicerBinding] = field(default_factory=list)
    cross_sources: list[_CrossFilterSource] = field(default_factory=list)
    drill_throughs: list[_DrillThrough] = field(default_factory=list)
    needs_location: bool = False   # True when any drill-through is registered

    def register_slicer(self, slicer_id: str, component_id: str) -> None:
        self.slicers[slicer_id] = component_id

    def register_cross_source(self, graph_id: str, slicer_id: str, dimension: str) -> None:
        self.cross_sources.append(_CrossFilterSource(graph_id, slicer_id, dimension))
        # Expose as a virtual slicer so filter_from can reference it
        self.slicers[slicer_id] = graph_id

    def register_drill_through(self, graph_id: str, target_anchor: str, pass_filter: dict, slicer_id: str) -> None:
        self.drill_throughs.append(_DrillThrough(graph_id, target_anchor, pass_filter, slicer_id))
        self.slicers[slicer_id] = graph_id  # expose as virtual slicer for filter_from
        self.needs_location = True

    def register_chart(
        self,
        container_id: str,
        filter_from: dict[str, str],
        factory: Callable,
        base_kwargs: dict[str, Any],
    ) -> None:
        self.bindings.append(_SlicerBinding(
            container_id=container_id,
            filter_from=filter_from,
            factory=factory,
            base_kwargs=base_kwargs,
        ))

    def has_bindings(self) -> bool:
        return bool(self.bindings) or bool(self.cross_sources) or bool(self.drill_throughs)

    def register_callbacks(self, app) -> None:
        """Wire slicer → chart callbacks and cross-filter click → store callbacks."""
        from dash import Input, Output, State
        import json as _json

        # Cross-filter sources: graph clickData → dcc.Store holding selected value
        for src in self.cross_sources:
            _gid = src.graph_id
            _dim = src.dimension
            _store_id = f"cf_store_{_gid}"

            @app.callback(Output(_store_id, "data"), Input(_gid, "clickData"), State(_store_id, "data"))
            def _on_click(click_data, current, _d=_dim, _gid=_gid):
                if click_data is None:
                    return None
                try:
                    point = click_data["points"][0]
                    # Try y (horizontal bar) then x (column/line)
                    val = point.get("y") or point.get("x") or point.get("label")
                    if val is not None:
                        val_str = str(val)
                        # Toggle: clicking same value again deselects
                        return None if val_str == current else val_str
                except (KeyError, IndexError):
                    return None
                return None

        # Chart bindings: slicer values / cross-filter store values → rebuild chart
        for b in self.bindings:
            inputs = []
            fkeys: list[str] = []
            for sid, fkey in b.filter_from.items():
                comp_id = self.slicers.get(sid)
                if not comp_id:
                    continue
                # Cross-filter sources use a dcc.Store, not the graph directly
                is_cross = any(src.slicer_id == sid for src in self.cross_sources)
                if is_cross:
                    inputs.append(Input(f"cf_store_{comp_id}", "data"))
                else:
                    inputs.append(Input(comp_id, "value"))
                fkeys.append(fkey)
            if not inputs:
                continue

            _cid         = b.container_id
            _factory     = b.factory
            _base_kwargs = dict(b.base_kwargs)
            _fkeys       = list(fkeys)

            @app.callback(Output(_cid, "children"), inputs)
            def _rebuild(*values, _f=_factory, _bk=_base_kwargs, _k=_fkeys):
                merged = dict(_bk.get("filter") or {})
                for fkey, val in zip(_k, values):
                    if val is not None and val != "__all__":
                        merged[fkey] = val
                    elif fkey in merged:
                        del merged[fkey]
                kwargs = {**_bk, "filter": merged or None}
                return [_f(**kwargs)]

        # Drill-through: click → store filter value + navigate to target anchor
        for dt in self.drill_throughs:
            _gid        = dt.graph_id
            _pass       = dt.pass_filter   # {filter_key: dim_col}
            _anchor     = dt.target_anchor
            _store_id   = f"cf_store_{_gid}"
            _loc_id     = "dbr_location"

            @app.callback(
                Output(_store_id, "data"),
                Output(_loc_id, "hash"),
                Input(_gid, "clickData"),
                State(_store_id, "data"),
            )
            def _on_drill(click_data, current_store, _p=_pass, _a=_anchor, _gid=_gid):
                if click_data is None:
                    from dash import no_update
                    return no_update, no_update
                try:
                    point = click_data["points"][0]
                    val   = point.get("y") or point.get("x") or point.get("label")
                    if val is None:
                        from dash import no_update
                        return no_update, no_update
                    val_str = str(val)
                    # Toggle deselect
                    if val_str == (current_store or {}).get("__drill"):
                        return {}, ""
                    store_data = {fk: val_str for fk in _p}
                    store_data["__drill"] = val_str
                    return store_data, f"#{_a}"
                except (KeyError, IndexError):
                    from dash import no_update
                    return no_update, no_update


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

    ctx = BuildContext()
    sections = _load_pages(project_root / "pages", ctx)

    dashboard_title    = config.get("title", "")
    dashboard_subtitle = config.get("subtitle", "")
    footer_source      = config.get("footer_source", "")
    footer_updated     = config.get("footer_updated", "")

    # Auto-derive the footer "Dane: YYYY" stamp from live warehouse data when
    # the author opts in (footer_updated omitted or "auto" + a footer_data_domain
    # listing the dashboard's domain_id code(s)). Keeps the footer honest after
    # every daily ingest without manual edits. Falls back to the literal on any
    # failure (warehouse unreachable, no rows). See OR-165.
    footer_data_domain = config.get("footer_data_domain")
    if footer_updated in ("", "auto") and footer_data_domain:
        from dbr.semantic import latest_actual_year
        domains = (
            [footer_data_domain]
            if isinstance(footer_data_domain, str)
            else list(footer_data_domain)
        )
        year = latest_actual_year(domains)
        footer_updated = f"Dane: {year}" if year is not None else ""

    app = make_app(config["domain"], title=dashboard_title)

    shell_kwargs = dict(
        sections=sections,
        dashboard_title=dashboard_title,
        dashboard_subtitle=dashboard_subtitle,
        footer_source=footer_source,
        footer_updated=footer_updated,
    )

    # Inject dcc.Location for drill-through URL hash navigation when needed
    if ctx.needs_location:
        from dash import dcc as _dcc, html as _html
        shell = page_shell(**shell_kwargs)
        app.layout = _html.Div([
            _dcc.Location(id="dbr_location", refresh=False),
            shell,
        ])
    else:
        app.layout = page_shell(**shell_kwargs)

    if ctx.has_bindings():
        ctx.register_callbacks(app)

    run_app(app, port=config["port"])


# A section is (title, anchor, rows). A row is (title-or-None, prose-or-None,
# list of (component, width-or-None), grow). Row title is optional H3 sub-heading;
# prose is optional Markdown paragraph rendered above the row items. ``grow`` is the
# vertical flex weight: 0 = natural height (KPI/slicer rows), 1 = stretch to fill the
# remaining page height (chart rows) — the fixed-page layout distributes leftover
# vertical space across all grow>0 rows so each page fills exactly one viewport.
Row = tuple[str | None, str | None, list[tuple[object, str | None]], int]
Section = tuple[str, str, list[Row]]

# Visual types that occupy only their natural (content) height — they must NOT be
# stretched to fill page height. Everything else (charts, tables, maps) grows.
_NON_GROWING_TYPES = {"card", "slicer"}


def _load_pages(pages_dir: Path, ctx: BuildContext) -> list[Section]:
    """Return ``[(title, anchor, rows), ...]`` in the declared page order."""
    if not pages_dir.exists():
        return []
    meta = _load_yaml(pages_dir / "pages.yml")
    sections: list[Section] = []
    for page_name in meta.get("order", []) or []:
        page_dir = pages_dir / page_name
        page_config = _load_yaml(page_dir / "page.yml")
        rows = _load_page_rows(page_dir / "visuals", page_name, ctx)
        sections.append((page_config["title"], page_config["anchor"], rows))
    return sections


def _load_page_rows(visuals_dir: Path, page_name: str, ctx: BuildContext) -> list[Row]:
    """Parse ``visuals.yml`` into a list of rows."""
    if not visuals_dir.exists():
        return []
    meta = _load_yaml(visuals_dir / "visuals.yml")

    if "rows" in meta:
        rows_spec = meta.get("rows") or []
    elif "order" in meta:
        rows_spec = [{"items": [name]} for name in (meta.get("order") or [])]
    else:
        return []

    rows: list[Row] = []
    for row_spec in rows_spec:
        is_dict = isinstance(row_spec, dict)
        row_title = row_spec.get("title") if is_dict else None
        row_prose = row_spec.get("prose") if is_dict else None
        row_items: list[tuple[object, str | None]] = []
        item_grows: list[bool] = []
        for item in row_spec.get("items", []) or []:
            if isinstance(item, str):
                visual_name, width = item, None
            else:
                visual_name = item["visual"]
                width = item.get("width")
            spec = _load_yaml(visuals_dir / f"{visual_name}.yml")
            vtype = spec.get("type", "")
            # A chart with an inline companion table renders at natural height (chart +
            # table stacked); it must NOT be stretched to fill the page, or the table
            # collapses the chart. So such a visual is treated as non-growing.
            has_table = bool((spec.get("options") or {}).get("table"))
            item_grows.append(vtype not in _NON_GROWING_TYPES and not has_table)
            row_items.append((_build_visual(spec, ctx, page_name, visual_name), width))
        # A row fills page height only when every visual in it is a fill-eligible chart
        # (a growing type, no companion table). KPI/slicer rows and chart+table rows keep
        # their natural height; empty rows don't grow.
        grow = 1 if (item_grows and all(item_grows)) else 0
        rows.append((row_title, row_prose, row_items, grow))
    return rows


def _build_visual(
    spec: dict,
    ctx: BuildContext | None = None,
    page_name: str = "",
    visual_name: str = "",
):
    from dash import html as _html

    vtype = spec.get("type")
    if vtype is None:
        raise ValueError(f"Visual spec missing required 'type': {spec}")
    if vtype not in VISUAL_REGISTRY:
        available = ", ".join(sorted(VISUAL_REGISTRY)) or "<none registered>"
        raise KeyError(
            f"Unknown visual type {vtype!r}. Available: {available}"
        )
    factory = VISUAL_REGISTRY[vtype]

    # ── Slicer ────────────────────────────────────────────────────────────────
    if vtype == "slicer":
        slicer_id = spec.get("slicer_id", visual_name)
        comp_id   = f"slicer_{slicer_id}"
        if ctx:
            ctx.register_slicer(slicer_id, comp_id)
        kwargs = {k: v for k, v in spec.items()
                  if k not in ("type", "title", "subtitle", "slicer_id")}
        component = factory(component_id=comp_id, slicer_id=slicer_id, **kwargs)
        title, subtitle = spec.get("title"), spec.get("subtitle")
        if title or subtitle:
            _prepend_title(component, title, subtitle)
        return component

    # ── Regular chart / table ─────────────────────────────────────────────────
    title         = spec.get("title")
    subtitle      = spec.get("subtitle")
    filter_from   = spec.get("filter_from")    # dict[slicer_id, filter_key] | None
    cross_filter  = spec.get("cross_filter", False)
    cross_dim     = spec.get("cross_filter_dimension")
    drill_through = spec.get("drill_through")  # {target_page, pass_filter: {dim: col}}

    # Strip compiler-only keys before calling factory
    _compiler_keys = (
        "type", "title", "subtitle", "filter_from",
        "cross_filter", "cross_filter_dimension", "drill_through",
    )
    kwargs = {k: v for k, v in spec.items() if k not in _compiler_keys}

    # If cross_filter: inject graph_id into kwargs so _render.py can tag dcc.Graph
    graph_id: str | None = None
    if cross_filter and ctx and cross_dim:
        graph_id = f"graph__{page_name}__{visual_name}"
        slicer_id = f"__cf_{page_name}_{visual_name}"
        ctx.register_cross_source(graph_id, slicer_id, cross_dim)
        # Pass the graph_id and store id via options so the factory can use chart_with_graph_id
        # We achieve this by injecting _graph_id into options (factory ignores unknown options
        # only if schema is lenient; for cross_filter we pass via a special key the factory
        # reads from the build context rather than from options)
        kwargs["_cross_filter_graph_id"] = graph_id

    component = factory(**{k: v for k, v in kwargs.items() if not k.startswith("_")})

    if title or subtitle:
        _prepend_title(component, title, subtitle)

    # ── cross_filter: inject a dcc.Store sibling for click state ─────────────
    if cross_filter and ctx and graph_id:
        from dash import dcc as _dcc
        store = _dcc.Store(id=f"cf_store_{graph_id}", data=None)
        if isinstance(component.children, list):
            component.children = [store] + component.children
        elif component.children is not None:
            component.children = [store, component.children]
        else:
            component.children = [store]

    # ── drill_through: click → navigate to target anchor + pass filter ────────
    if drill_through and ctx:
        from dash import dcc as _dcc
        dt_graph_id  = f"graph__{page_name}__{visual_name}__dt"
        dt_slicer_id = f"__dt_{page_name}_{visual_name}"
        target_anchor = drill_through.get("target_page", "")
        pass_filter   = drill_through.get("pass_filter", {})  # {filter_key: dim_col}
        ctx.register_drill_through(dt_graph_id, target_anchor, pass_filter, dt_slicer_id)
        # Inject dcc.Store for the drill filter value
        dt_store = _dcc.Store(id=f"cf_store_{dt_graph_id}", data={})
        # Tag the graph inside the component with the dt_graph_id
        # We wrap the component children with the store and assign the graph id
        _inject_graph_id(component, dt_graph_id)
        if isinstance(component.children, list):
            component.children = [dt_store] + component.children
        elif component.children is not None:
            component.children = [dt_store, component.children]
        else:
            component.children = [dt_store]

    # ── filter_from: wrap in a named container for the callback ───────────────
    if filter_from and ctx:
        container_id = f"chart__{page_name}__{visual_name}"
        ctx.register_chart(container_id, filter_from, factory, kwargs)
        return _html.Div([component], id=container_id)

    return component


def _inject_graph_id(component, graph_id: str) -> None:
    """Walk a component tree and assign graph_id to the first dcc.Graph found."""
    from dash import dcc as _dcc
    children = getattr(component, "children", None)
    if children is None:
        return
    if not isinstance(children, list):
        children = [children]
    for child in children:
        if isinstance(child, _dcc.Graph) and not child.id:
            child.id = graph_id
            return
        _inject_graph_id(child, graph_id)


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
