"""
Template dashboard — dimension and measure definitions.

This file defines the semantic layer for the template showcase.
When building a domain dashboard, replace these with domain-specific
definitions referencing real indicator names and warehouse columns.

Finance domain example:
    DIMS = {
        "country": Dimension("country", "Kraj",  "geo"),
        "year":    Dimension("year",    "Rok",   "year"),
    }
    MEASURES = {
        "fiscal_balance": Measure(
            "fiscal_balance", "Saldo fiskalne", "fiscal_balance_pct_gdp",
            aggregation="last", unit="% PKB", format="{:.1f}",
        ),
        ...
    }
"""
from products.visuals.lib.semantic import Dimension, Measure

# ── Dimensions ────────────────────────────────────────────────────────────────

DIMS = {
    # Main dataset (load())
    "category": Dimension("category", "Kategoria",  "dim_category"),
    "year":     Dimension("year",     "Rok",         "dim_year"),
    "period":   Dimension("period",   "Okres",        "dim_period"),

    # Geo dataset (load_geo())
    "iso3":     Dimension("iso3",     "Kraj (ISO-3)", "dim_iso3"),
    "label":    Dimension("label",    "Region",       "dim_label"),

    # OHLC dataset (load_ohlc())
    "date":     Dimension("date",     "Data",         "dim_date"),
}

# ── Measures ──────────────────────────────────────────────────────────────────

MEASURES = {
    # ── Main measures (reference data from load()) ────────────────────────────

    "measure_a": Measure(
        name="measure_a", label="Miara A",
        column="val_a", aggregation="mean",
        unit="jedn.", format="{:.1f}",
    ),
    "measure_b": Measure(
        name="measure_b", label="Miara B",
        column="val_b", aggregation="mean",
        unit="jedn.", format="{:.1f}",
    ),
    "measure_c": Measure(
        name="measure_c", label="Miara C",
        column="val_c", aggregation="mean",
        unit="jedn.", format="{:.1f}",
    ),
    "measure_d": Measure(
        name="measure_d", label="Miara D",
        column="val_d", aggregation="mean",
        unit="jedn.", format="{:.1f}",
    ),
    "measure_e": Measure(
        name="measure_e", label="Miara E (dywerg.)",
        column="val_e", aggregation="mean",
        unit="jedn.", format="{:.1f}",
    ),

    # ── Derived measures ──────────────────────────────────────────────────────

    "measure_a_pct": Measure(
        name="measure_a_pct", label="Miara A (zmiana r/r)",
        column="val_a", aggregation="mean",
        unit="%", format="{:.1f}",
        calc="pct_change",
    ),
    "measure_a_cum": Measure(
        name="measure_a_cum", label="Miara A (narastająco)",
        column="val_a", aggregation="sum",
        unit="jedn.", format="{:.0f}",
        calc="cumsum",
    ),

    # ── Geo measures (reference data from load_geo()) ─────────────────────────

    "geo_a": Measure(
        name="geo_a", label="Miara A (geo)",
        column="val_a", aggregation="first",
        unit="jedn.", format="{:.1f}",
    ),
    "geo_b": Measure(
        name="geo_b", label="Miara B (geo)",
        column="val_b", aggregation="first",
        unit="jedn.", format="{:.1f}",
    ),
    "geo_size": Measure(
        name="geo_size", label="Rozmiar",
        column="val_size", aggregation="first",
        format="{:.0f}",
    ),
}
