"""`theme` block — colour palette + typography + spacing + Plotly template.

Source of truth is ``theme.yaml``. ``loader.py`` reads it on import and
exposes every token as a Python constant; this ``__init__.py`` re-exports
them so callers write a clean one-line import.

Edit ``theme.yaml`` to change the brand. Every dashboard picks up the new
values on next start — no code changes required.

Use:

    from dbr.theme import BG_PAGE, TEXT, FONT_FAMILY, SIDEBAR_WIDTH
"""
from dbr.theme.loader import (
    # Logo-derived core colours
    TEAL_PRIMARY, AZURE_PRIMARY, CHARCOAL,
    # Teal family
    TEAL_1, TEAL_2, TEAL_3, TEAL_4, TEAL_PALE,
    # Azure family
    AZURE_1, AZURE_2, AZURE_3, AZURE_4, AZURE_PALE,
    # Slate family
    SLATE_1, SLATE_2, SLATE_3, SLATE_4,
    # Backgrounds / surfaces / text
    BG_PAGE, BG_SURFACE, BORDER, GRID, ZERO_LINE, TEXT, SUBTEXT, MUTED,
    # Semantic colours
    POSITIVE, NEGATIVE, WARNING,
    # Chart colourway
    COLORWAY,
    # Typography
    FONT_FAMILY, SIZE_BODY, SIZE_SECTION_HEADING, WEIGHT_SECTION_HEADING,
    # Spacing
    PAGE_GAP, PAGE_PADDING, MAIN_PADDING, MAIN_MAX_WIDTH,
    SIDEBAR_WIDTH, SIDEBAR_PADDING, NAV_LINK_PADDING,
    SECTION_TOP_GAP, SECTION_BOTTOM_GAP, ROW_GAP,
    # Effects
    CARD_RADIUS, CARD_SHADOW,
    # Visual-specific defaults — kpi_standard
    KPI_PADDING, KPI_LABEL_SIZE, KPI_VALUE_SIZE, KPI_VALUE_WEIGHT,
    KPI_PERIOD_SIZE, KPI_LABEL_BOTTOM_GAP, KPI_PERIOD_TOP_GAP,
    # Visual-specific defaults — kpi_compact
    KPI_COMPACT_PADDING, KPI_COMPACT_LABEL_SIZE, KPI_COMPACT_VALUE_SIZE,
    KPI_COMPACT_VALUE_WEIGHT, KPI_COMPACT_LABEL_VALUE_GAP,
    # Visual-specific defaults — line_chart
    LINE_CHART_HEIGHT, LINE_CHART_LINE_WIDTH, LINE_CHART_MARKER_SIZE,
    LINE_CHART_HISTORY_YEARS,
    # Visual-specific defaults — area_chart
    AREA_CHART_HEIGHT, AREA_CHART_LINE_WIDTH, AREA_CHART_OPACITY,
    AREA_CHART_HISTORY_YEARS,
    # Visual-specific defaults — bar_chart
    BAR_CHART_HEIGHT, BAR_CHART_BARGAP, BAR_CHART_HISTORY_YEARS,
    # Visual-specific defaults — table
    TABLE_ROW_HEIGHT, TABLE_FONT_SIZE, TABLE_ROW_LIMIT,
    # Named number-format templates
    FORMATS,
)

__all__ = [
    # Colours
    "TEAL_PRIMARY", "AZURE_PRIMARY", "CHARCOAL",
    "TEAL_1", "TEAL_2", "TEAL_3", "TEAL_4", "TEAL_PALE",
    "AZURE_1", "AZURE_2", "AZURE_3", "AZURE_4", "AZURE_PALE",
    "SLATE_1", "SLATE_2", "SLATE_3", "SLATE_4",
    "BG_PAGE", "BG_SURFACE", "BORDER", "GRID", "ZERO_LINE", "TEXT", "SUBTEXT", "MUTED",
    "POSITIVE", "NEGATIVE", "WARNING",
    "COLORWAY",
    # Typography
    "FONT_FAMILY", "SIZE_BODY", "SIZE_SECTION_HEADING", "WEIGHT_SECTION_HEADING",
    # Spacing
    "PAGE_GAP", "PAGE_PADDING", "MAIN_PADDING", "MAIN_MAX_WIDTH",
    "SIDEBAR_WIDTH", "SIDEBAR_PADDING", "NAV_LINK_PADDING",
    "SECTION_TOP_GAP", "SECTION_BOTTOM_GAP", "ROW_GAP",
    # Effects
    "CARD_RADIUS", "CARD_SHADOW",
    # Visual-specific defaults — kpi_standard
    "KPI_PADDING", "KPI_LABEL_SIZE", "KPI_VALUE_SIZE", "KPI_VALUE_WEIGHT",
    "KPI_PERIOD_SIZE", "KPI_LABEL_BOTTOM_GAP", "KPI_PERIOD_TOP_GAP",
    # Visual-specific defaults — kpi_compact
    "KPI_COMPACT_PADDING", "KPI_COMPACT_LABEL_SIZE", "KPI_COMPACT_VALUE_SIZE",
    "KPI_COMPACT_VALUE_WEIGHT", "KPI_COMPACT_LABEL_VALUE_GAP",
    # Visual-specific defaults — line_chart
    "LINE_CHART_HEIGHT", "LINE_CHART_LINE_WIDTH", "LINE_CHART_MARKER_SIZE",
    "LINE_CHART_HISTORY_YEARS",
    # Visual-specific defaults — area_chart
    "AREA_CHART_HEIGHT", "AREA_CHART_LINE_WIDTH", "AREA_CHART_OPACITY",
    "AREA_CHART_HISTORY_YEARS",
    # Visual-specific defaults — bar_chart
    "BAR_CHART_HEIGHT", "BAR_CHART_BARGAP", "BAR_CHART_HISTORY_YEARS",
    # Visual-specific defaults — table
    "TABLE_ROW_HEIGHT", "TABLE_FONT_SIZE", "TABLE_ROW_LIMIT",
    # Named number-format templates
    "FORMATS",
]
