"""Example dashboard — synthetic data loaders.

Same loader interface as ``scaffolds/data_loaders.py.template`` —
``load_by_year``, ``load_by_region``, ``load_scalars`` — but backed
by hard-coded ``pd.DataFrame``s instead of DuckDB. This lets the
example run with no warehouse dependency while still exercising the
real interface contract documented in ``specs/data/data_loaders.md``.

Column-naming convention (matches ``measures.py``):

- ``dim_<dimension>`` — dimension columns (``dim_year``, ``dim_region``)
- ``val_<measure>``   — measure columns (``val_unemployment``, ``val_employment``)
"""
import pandas as pd


def load_by_year() -> pd.DataFrame:
    """Time series — one row per year, one column per measure."""
    return pd.DataFrame({
        "dim_year":         [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "val_unemployment": [5.8,  5.2,  6.3,  5.4,  4.9,  5.0,  5.1],
        "val_employment":   [16_400, 16_550, 16_320, 16_700, 17_050, 17_280, 17_410],
    })


def load_by_region() -> pd.DataFrame:
    """Regional breakdown — one row per voivodeship for the latest year."""
    return pd.DataFrame({
        "dim_region":       ["Mazowieckie", "Śląskie", "Małopolskie", "Wielkopolskie", "Pomorskie"],
        "val_employment":   [3_010, 1_840, 1_420, 1_490, 920],
    })


def load_scalars() -> dict:
    """Single-value KPIs. Keys must match ``MEASURES`` keys."""
    last = load_by_year().iloc[-1]
    return {
        "unemployment": float(last["val_unemployment"]),
        "employment":   float(last["val_employment"]),
    }
