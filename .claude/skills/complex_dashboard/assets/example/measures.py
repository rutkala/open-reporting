"""
Showroom — dimension and measure display config.

Defines labels, units, and format settings for the visual-component
showroom in ``showroom.py``. When building a domain dashboard, copy
the shape and update labels and column names to match the domain's
warehouse mart.

All aggregation logic lives in ``data_loaders.py`` (showroom) or in your
domain's ``semantic_service.py``. Measures here carry display metadata
only.

Domain example:
    DIMS = {
        "country": Dimension("country", "Country", "geo"),
        "year":    Dimension("year",    "Year",    "year"),
    }
    MEASURES = {
        "fiscal_balance": Measure(
            "fiscal_balance", "Fiscal balance", "fiscal_balance_pct_gdp",
            unit="% GDP", format_type="number", decimals=1,
        ),
        "expenditure": Measure(
            "expenditure", "Expenditure", "expenditure_bn",
            format_type="currency", scale="M", currency_symbol="zł", decimals=1,
        ),
    }
"""
from complex_dashboard.assets.semantic import Dimension, Measure

# ── Dimensions ────────────────────────────────────────────────────────────────

DIMS = {
    # Main dataset (load_by_category / load_by_year / load_by_period)
    "category": Dimension("category", "Category",  "dim_category"),
    "year":     Dimension("year",     "Year",       "dim_year"),
    "period":   Dimension("period",   "Period",     "dim_period"),

    # Distribution dataset (load_distribution)
    "group":    Dimension("group",    "Group",      "dim_group"),

    # Geo dataset (load_geo)
    "iso3":     Dimension("iso3",     "ISO-3",      "dim_iso3"),
    "label":    Dimension("label",    "Region",     "dim_label"),

    # OHLC dataset (load_ohlc)
    "date":     Dimension("date",     "Period",     "dim_date"),
}

# ── Measures ──────────────────────────────────────────────────────────────────

MEASURES = {
    # ── Main measures ─────────────────────────────────────────────────────────

    "measure_a": Measure("measure_a", "Measure A",          "val_a",
                         unit="units", format_type="number", decimals=1),
    "measure_b": Measure("measure_b", "Measure B",          "val_b",
                         unit="units", format_type="number", decimals=1),
    "measure_c": Measure("measure_c", "Measure C",          "val_c",
                         unit="units", format_type="number", decimals=1),
    "measure_d": Measure("measure_d", "Measure D",          "val_d",
                         unit="units", format_type="number", decimals=1),
    "measure_e": Measure("measure_e", "Measure E (diverg)", "val_e",
                         unit="units", format_type="number", decimals=1),

    # ── Derived measures (pre-computed in data.py) ────────────────────────────

    "measure_a_pct": Measure("measure_a_pct", "Measure A (YoY change)", "val_a_pct",
                             format_type="percent", decimals=1),
    "measure_a_cum": Measure("measure_a_cum", "Measure A (cumulative)", "val_a_cum",
                             unit="units", format_type="number", decimals=0),

    # ── Geo measures ──────────────────────────────────────────────────────────

    "geo_a":    Measure("geo_a",    "Measure A", "val_a",
                        unit="units", format_type="number", decimals=1),
    "geo_b":    Measure("geo_b",    "Measure B", "val_b",
                        unit="units", format_type="number", decimals=1),
    "geo_size": Measure("geo_size", "Size",      "val_size",
                        format_type="number", decimals=0, show_unit=False),
}
