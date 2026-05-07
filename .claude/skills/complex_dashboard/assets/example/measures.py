"""Example dashboard — dimension and measure display config.

Mirrors the shape of ``scaffolds/measures.py.template`` so a reader
can compare the live example to the copy-and-fill scaffold and see
exactly what gets replaced when adopting the skill.

Display metadata only — no aggregation, no warehouse access. The
companion ``data_loaders.py`` provides the actual frames.
"""
from products.visuals.lib.semantic import Dimension, Measure


DIMS = {
    "year":   Dimension("year",   "Rok",         "dim_year"),
    "region": Dimension("region", "Województwo", "dim_region"),
}


MEASURES = {
    "unemployment": Measure(
        "unemployment", "Stopa bezrobocia", "val_unemployment",
        unit="%", format_type="percent", decimals=1,
    ),
    "employment": Measure(
        "employment", "Zatrudnienie", "val_employment",
        unit="tys.", format_type="number", scale="K", decimals=0,
    ),
}
