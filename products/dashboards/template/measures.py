"""
Template dashboard — dimension and measure display config.

This file defines labels, units, and column bindings for the template
scaffold. When building a domain dashboard, update labels and column names
to match the domain's warehouse mart.

All aggregation logic lives in data.py (template) or semantic_service.py
(domain dashboards). Measures here carry display metadata only.

Domain example:
    DIMS = {
        "country": Dimension("country", "Kraj",  "geo"),
        "year":    Dimension("year",    "Rok",   "year"),
    }
    MEASURES = {
        "fiscal_balance": Measure(
            "fiscal_balance", "Saldo fiskalne", "fiscal_balance_pct_gdp",
            unit="% PKB", format="{:.1f}",
        ),
    }
"""
from products.visuals.lib.semantic import Dimension, Measure

# ── Dimensions ────────────────────────────────────────────────────────────────

DIMS = {
    # Main dataset (load_by_category / load_by_year / load_by_period)
    "category": Dimension("category", "Kategoria",  "dim_category"),
    "year":     Dimension("year",     "Okres (rok)", "dim_year"),
    "period":   Dimension("period",   "Okres",       "dim_period"),

    # Distribution dataset (load_distribution)
    "group":    Dimension("group",    "Grupa",       "dim_group"),

    # Geo dataset (load_geo)
    "iso3":     Dimension("iso3",     "ISO-3",       "dim_iso3"),
    "label":    Dimension("label",    "Region",      "dim_label"),

    # OHLC dataset (load_ohlc)
    "date":     Dimension("date",     "Okres",       "dim_date"),
}

# ── Measures ──────────────────────────────────────────────────────────────────

MEASURES = {
    # ── Main measures ─────────────────────────────────────────────────────────

    "measure_a": Measure("measure_a", "Miara A",            "val_a", unit="jedn.", format="{:.1f}"),
    "measure_b": Measure("measure_b", "Miara B",            "val_b", unit="jedn.", format="{:.1f}"),
    "measure_c": Measure("measure_c", "Miara C",            "val_c", unit="jedn.", format="{:.1f}"),
    "measure_d": Measure("measure_d", "Miara D",            "val_d", unit="jedn.", format="{:.1f}"),
    "measure_e": Measure("measure_e", "Miara E (dywerg.)",  "val_e", unit="jedn.", format="{:.1f}"),

    # ── Derived measures (pre-computed in data.py) ────────────────────────────

    "measure_a_pct": Measure("measure_a_pct", "Miara A (zmiana r/r)", "val_a_pct", unit="%",    format="{:.1f}"),
    "measure_a_cum": Measure("measure_a_cum", "Miara A (narastająco)", "val_a_cum", unit="jedn.", format="{:.0f}"),

    # ── Geo measures ──────────────────────────────────────────────────────────

    "geo_a":    Measure("geo_a",    "Miara A", "val_a",    unit="jedn.", format="{:.1f}"),
    "geo_b":    Measure("geo_b",    "Miara B", "val_b",    unit="jedn.", format="{:.1f}"),
    "geo_size": Measure("geo_size", "Rozmiar", "val_size",               format="{:.0f}"),
}
