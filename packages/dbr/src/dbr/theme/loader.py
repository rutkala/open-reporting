"""Theme loader — reads theme.yaml and exposes design tokens to Python.

On import:
  1. Loads the package's default ``theme.yaml`` (immutable, ships with the kit).
  2. If env var ``DBR_PROJECT_ROOT`` is set and the project has its
     own ``theme.yaml``, deep-merges it on top of the defaults. The override
     YAML can contain only the keys you want to change; everything else
     inherits the kit defaults.
  3. Exposes every resolved colour / typography / spacing / effects token
     as a module-level constant.
  4. Builds the Plotly template named in the YAML and sets it as default.

Other blocks import from ``dbr.theme`` (the package);
the package's ``__init__.py`` re-exports the constants defined here.

The env var must be set BEFORE any ``dbr`` import — the CLI does
this in ``cmd_run``; ``app.py`` shims should set it as their first action.
"""
import os
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio
import yaml


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursive dict merge — override wins on leaf-key collisions."""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


_PACKAGE_DEFAULTS = yaml.safe_load((Path(__file__).parent / "theme.yaml").read_text())
_DATA = _PACKAGE_DEFAULTS

_project_root = os.environ.get("DBR_PROJECT_ROOT")
if _project_root:
    _override_path = Path(_project_root) / "theme.yaml"
    if _override_path.exists():
        _override = yaml.safe_load(_override_path.read_text()) or {}
        _DATA = _deep_merge(_PACKAGE_DEFAULTS, _override)

_COLORS    = _DATA["colors"]
_TYPO      = _DATA["typography"]
_SPACING   = _DATA["spacing"]
_EFFECTS   = _DATA["effects"]
_CHART     = _DATA["chart"]
_VISUALS   = _DATA["visuals"]

# ── Colours — logo core ────────────────────────────────────────────────
TEAL_PRIMARY  = _COLORS["teal_primary"]
AZURE_PRIMARY = _COLORS["azure_primary"]
CHARCOAL      = _COLORS["charcoal"]

# ── Colours — Teal family ──────────────────────────────────────────────
TEAL_1    = _COLORS["teal_1"]
TEAL_2    = _COLORS["teal_2"]
TEAL_3    = _COLORS["teal_3"]
TEAL_4    = _COLORS["teal_4"]
TEAL_PALE = _COLORS["teal_pale"]

# ── Colours — Azure family ─────────────────────────────────────────────
AZURE_1    = _COLORS["azure_1"]
AZURE_2    = _COLORS["azure_2"]
AZURE_3    = _COLORS["azure_3"]
AZURE_4    = _COLORS["azure_4"]
AZURE_PALE = _COLORS["azure_pale"]

# ── Colours — Slate family ─────────────────────────────────────────────
SLATE_1 = _COLORS["slate_1"]
SLATE_2 = _COLORS["slate_2"]
SLATE_3 = _COLORS["slate_3"]
SLATE_4 = _COLORS["slate_4"]

# ── Colours — Backgrounds / surfaces / text ────────────────────────────
BG_PAGE    = _COLORS["bg_page"]
BG_SURFACE = _COLORS["bg_surface"]
BORDER     = _COLORS["border"]
GRID       = _COLORS["grid"]
ZERO_LINE  = _COLORS["zero_line"]
TEXT       = _COLORS["text"]
SUBTEXT    = _COLORS["subtext"]
MUTED      = _COLORS["muted"]

# ── Colours — Semantic ─────────────────────────────────────────────────
POSITIVE = _COLORS["positive"]
NEGATIVE = _COLORS["negative"]
WARNING  = _COLORS["warning"]

# ── Chart colourway — resolved from colour-name references ─────────────
COLORWAY = [_COLORS[name] for name in _CHART["colorway"]]

# ── Typography ─────────────────────────────────────────────────────────
FONT_FAMILY            = _TYPO["font_family"]
SIZE_BODY              = _TYPO["size_body"]
SIZE_SECTION_HEADING   = _TYPO["size_section_heading"]
WEIGHT_SECTION_HEADING = _TYPO["weight_section_heading"]

# ── Spacing ────────────────────────────────────────────────────────────
PAGE_GAP           = _SPACING["page_gap"]
PAGE_PADDING       = _SPACING["page_padding"]
MAIN_PADDING       = _SPACING["main_padding"]
MAIN_MAX_WIDTH     = _SPACING.get("main_max_width", "1440px")
SIDEBAR_WIDTH      = _SPACING["sidebar_width"]
SIDEBAR_PADDING    = _SPACING["sidebar_padding"]
NAV_LINK_PADDING   = _SPACING["nav_link_padding"]
SECTION_TOP_GAP    = _SPACING["section_top_gap"]
SECTION_BOTTOM_GAP = _SPACING["section_bottom_gap"]
ROW_GAP            = _SPACING["row_gap"]

# ── Effects ────────────────────────────────────────────────────────────
CARD_RADIUS = _EFFECTS["card_radius"]
CARD_SHADOW = _EFFECTS["card_shadow"]

# ── Per-visual default tokens ──────────────────────────────────────────
KPI_PADDING          = _VISUALS["kpi"]["padding"]
KPI_LABEL_SIZE       = _VISUALS["kpi"]["label_size"]
KPI_VALUE_SIZE       = _VISUALS["kpi"]["value_size"]
KPI_VALUE_WEIGHT     = _VISUALS["kpi"]["value_weight"]
KPI_PERIOD_SIZE      = _VISUALS["kpi"]["period_size"]
KPI_LABEL_BOTTOM_GAP = _VISUALS["kpi"]["label_bottom_gap"]
KPI_PERIOD_TOP_GAP   = _VISUALS["kpi"]["period_top_gap"]

KPI_COMPACT_PADDING         = _VISUALS["kpi_compact"]["padding"]
KPI_COMPACT_LABEL_SIZE      = _VISUALS["kpi_compact"]["label_size"]
KPI_COMPACT_VALUE_SIZE      = _VISUALS["kpi_compact"]["value_size"]
KPI_COMPACT_VALUE_WEIGHT    = _VISUALS["kpi_compact"]["value_weight"]
KPI_COMPACT_LABEL_VALUE_GAP = _VISUALS["kpi_compact"]["label_value_gap"]

LINE_CHART_HEIGHT        = _VISUALS["line_chart"]["height"]
LINE_CHART_LINE_WIDTH    = _VISUALS["line_chart"]["line_width"]
LINE_CHART_MARKER_SIZE   = _VISUALS["line_chart"]["marker_size"]
LINE_CHART_HISTORY_YEARS = _VISUALS["line_chart"]["history_years"]

AREA_CHART_HEIGHT        = _VISUALS["area_chart"]["height"]
AREA_CHART_LINE_WIDTH    = _VISUALS["area_chart"]["line_width"]
AREA_CHART_OPACITY       = _VISUALS["area_chart"]["opacity"]
AREA_CHART_HISTORY_YEARS = _VISUALS["area_chart"]["history_years"]

BAR_CHART_HEIGHT        = _VISUALS["bar_chart"]["height"]
BAR_CHART_BARGAP        = _VISUALS["bar_chart"]["bargap"]
BAR_CHART_HISTORY_YEARS = _VISUALS["bar_chart"]["history_years"]

TABLE_ROW_HEIGHT = _VISUALS["table"]["row_height"]
TABLE_FONT_SIZE  = _VISUALS["table"]["font_size"]
TABLE_ROW_LIMIT  = _VISUALS["table"]["row_limit"]

# ── Plotly template (side effect: registers globally on import) ────────
_axis = dict(
    gridcolor=GRID,
    linecolor=BORDER,
    tickfont=dict(color=SUBTEXT, size=11),
    zerolinecolor=ZERO_LINE,
    showgrid=True,
)

pio.templates[_CHART["template_name"]] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=COLORWAY,
        font=dict(family=FONT_FAMILY, size=13, color=TEXT),
        title=dict(font=dict(size=17, color=TEXT), x=0.0, xanchor="left"),
        margin=dict(l=48, r=24, t=48, b=40),
        xaxis=_axis,
        yaxis=_axis,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=12),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hovermode="x unified",
        hoverlabel=dict(bgcolor=BG_SURFACE, bordercolor=BORDER, font=dict(size=12)),
    ),
    data=dict(
        scatter=[go.Scatter(line=dict(width=2), marker=dict(size=5))],
        bar=[go.Bar(marker=dict(line=dict(width=0)))],
    ),
)

pio.templates.default = _CHART["template_default"]
