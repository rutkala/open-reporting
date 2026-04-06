"""
Template dashboard — sample data loaders.

This file is the ONLY thing that changes when building a domain dashboard.
Replace the return values with warehouse queries; measures.py and app.py
stay unchanged.

Domain example:
    from products.visuals.lib.db import query

    def load() -> pd.DataFrame:
        return query(\"\"\"
            SELECT geo AS dim_category, year AS dim_year,
                   revenue AS val_a, costs AS val_b, balance AS val_c, ...
            FROM curated.mart_finance
            ORDER BY dim_year, dim_category
        \"\"\")
"""
import numpy as np
import pandas as pd


def load() -> pd.DataFrame:
    """
    Main sample dataset: 5 categories × 7 years = 35 rows.

    Columns
    -------
    dim_category : str    — 5 generic categories (Kat. A–E)
    dim_year     : int    — years 2018–2024
    dim_period   : str    — Q1–Q4 cycling
    val_a        : float  — primary measure (positive, ~45–55 range)
    val_b        : float  — secondary measure (~5% higher than val_a)
    val_c        : float  — tertiary measure (~7% lower than val_a)
    val_d        : float  — small positive measure (~15% of val_a)
    val_e        : float  — diverging measure (positive and negative)
    """
    categories = ["Kat. A", "Kat. B", "Kat. C", "Kat. D", "Kat. E"]
    years = list(range(2018, 2025))
    quarters = ["Q1", "Q2", "Q3", "Q4"]

    rng = np.random.default_rng(42)
    base = {"Kat. A": 47.2, "Kat. B": 45.8, "Kat. C": 52.3, "Kat. D": 48.1, "Kat. E": 43.6}

    rows = []
    for cat in categories:
        v = base[cat]
        for i, year in enumerate(years):
            v = round(v + rng.normal(0, 0.4), 1)
            rows.append({
                "dim_category": cat,
                "dim_year":     year,
                "dim_period":   quarters[i % 4],
                "val_a":        round(v, 1),
                "val_b":        round(v * 1.065 + rng.normal(0, 0.2), 1),
                "val_c":        round(v * 0.935 + rng.normal(0, 0.2), 1),
                "val_d":        round(v * 0.15  + rng.normal(0, 0.1), 1),
                "val_e":        round((v - 48.0) * 0.6 + rng.normal(0, 0.1), 1),
            })

    return pd.DataFrame(rows)


def load_geo() -> pd.DataFrame:
    """
    Geographic sample dataset: 12 European countries.

    Columns
    -------
    dim_iso3    : str   — ISO 3166-1 alpha-3 codes (for choropleth locationmode="ISO-3")
    dim_label   : str   — generic region labels (Region A–L)
    dim_lat     : float — approximate capital latitude
    dim_lon     : float — approximate capital longitude
    val_a       : float — sequential measure (all positive, ~30–165)
    val_b       : float — diverging measure (positive and negative, ~−8 to +4)
    val_size    : int   — size measure for bubble map (proportional to area)
    """
    return pd.DataFrame({
        "dim_iso3":  ["POL", "DEU", "FRA", "ITA", "CZE", "GRC",
                      "ESP", "PRT", "AUT", "BEL", "SWE", "DNK"],
        "dim_label": [f"Region {chr(65 + i)}" for i in range(12)],
        "dim_lat":   [52.2, 51.2, 46.2, 41.9, 50.1, 37.9,
                      40.4, 38.7, 47.5, 50.8, 59.3, 55.7],
        "dim_lon":   [21.0, 10.4,  2.2, 12.5, 15.5, 23.7,
                      -3.7, -9.1, 14.6,  4.4, 18.1, 12.6],
        "val_a":     [54.1,  63.2, 109.1, 137.3,  44.1, 163.0,
                      103.0, 112.0,  82.0, 105.0,  32.0,  29.0],
        "val_b":     [-5.1,  -1.7,  -5.5,  -7.2,  -1.6,  -1.6,
                      -3.4,  -3.1,  -2.1,  -3.0,   0.6,   3.2],
        "val_size":  [680, 4200, 2800, 2100,  290,  180,
                      1500,  270,  470,  560,  580,  400],
    })


def load_ohlc() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Two OHLC sample time series (instrument A and instrument B).

    Each DataFrame has columns:
        dim_date : str   — "YYYY-MM" monthly periods
        open     : float
        high     : float
        low      : float
        close    : float

    Returns (df_instrument_a, df_instrument_b).
    """
    dates = [f"2024-{m:02d}" for m in range(1, 13)]
    rng = np.random.default_rng(7)

    def _ohlc_series(start_price: float, vol: float, small_vol: float) -> pd.DataFrame:
        rows = []
        p = start_price
        for d in dates:
            o = round(p + rng.normal(0, small_vol), 3)
            c = round(o + rng.normal(0, vol), 3)
            h = round(max(o, c) + abs(rng.normal(0, small_vol)), 3)
            lo = round(min(o, c) - abs(rng.normal(0, small_vol)), 3)
            rows.append({"dim_date": d, "open": o, "high": h, "low": lo, "close": c})
            p = c
        return pd.DataFrame(rows)

    return _ohlc_series(5.60, 0.08, 0.025), _ohlc_series(4.35, 0.035, 0.012)


def load_scatter() -> pd.DataFrame:
    """
    Scatter / bubble sample data: 10 observations.

    Columns
    -------
    dim_label : str   — observation label (Obs. 1–10)
    val_x     : float — x-axis variable
    val_y     : float — y-axis variable
    val_size  : float — bubble size variable (for scatter_bubble)
    """
    return pd.DataFrame({
        "dim_label": [f"Obs. {i}" for i in range(1, 11)],
        "val_x":     [32.0, 44.0, 54.0, 82.0, 103.0, 105.0, 109.0, 112.0, 137.0, 163.0],
        "val_y":     [-0.3, -3.2, -5.1, -2.1,  -3.4,  -4.8,  -5.5,  -3.1,  -7.2,  -1.6],
        "val_size":  [38.0, 10.0, 38.0,  9.0,  11.0,  68.0,  60.0,  15.0,  25.0,  18.0],
    })


def load_distribution() -> pd.DataFrame:
    """
    Distribution sample data: 3 groups × 12 observations each = 36 rows.
    Also includes a flat 'val_all' column for single-variable histograms.

    Columns
    -------
    dim_group : str   — group label (Seria A / B / C)
    val_obs   : float — observed value
    """
    rng = np.random.default_rng(11)
    rows = []
    params = [
        ("Seria A", 21.0, 2.5),
        ("Seria B", 29.5, 1.8),
        ("Seria C", 13.0, 1.4),
    ]
    for group, mu, sigma in params:
        for v in rng.normal(mu, sigma, 12):
            rows.append({"dim_group": group, "val_obs": round(float(v), 2)})
    return pd.DataFrame(rows)


def load_waterfall() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Waterfall sample data — two chart variants.

    Each DataFrame has columns:
        dim_stage      : str   — stage/category label
        val_amount     : float — contribution value (positive = increase, negative = decrease)
        is_total       : bool  — True for the final sum bar
        is_base        : bool  — True for the opening balance bar (variance chart only)

    Returns (df_contribution, df_variance).
    """
    df_contribution = pd.DataFrame({
        "dim_stage":  ["Składnik A", "Składnik B", "Składnik C", "Składnik D",
                       "Korekta A",  "Korekta B",  "Korekta C",  "Wynik"],
        "val_amount": [295.0, 135.0, 92.0, 93.0, -390.0, -180.0, -95.0, -50.0],
        "is_total":   [False, False, False, False, False, False, False, True],
        "is_base":    [False] * 8,
    })
    df_variance = pd.DataFrame({
        "dim_stage":  ["Start", "Wzrost A", "Wzrost B", "Spadek A", "Korekta", "Koniec"],
        "val_amount": [1240.0, 180.0, 35.0, -140.0, 15.0, 1330.0],
        "is_total":   [False, False, False, False, False, True],
        "is_base":    [True,  False, False, False, False, False],
    })
    return df_contribution, df_variance


def load_funnel() -> pd.DataFrame:
    """
    Funnel sample data.

    Columns
    -------
    dim_stage : str — stage label (Etap 1–5)
    val_count : int — volume at this stage
    """
    return pd.DataFrame({
        "dim_stage": ["Etap 1", "Etap 2", "Etap 3", "Etap 4", "Etap 5"],
        "val_count": [12400, 8900, 6200, 4800, 4100],
    })


def load_treemap() -> pd.DataFrame:
    """
    Treemap sample data (hierarchical).

    Columns
    -------
    dim_node   : str   — node label (unique)
    dim_parent : str   — parent node label ("" for root)
    val_size   : float — node value (0 for internal nodes)
    """
    return pd.DataFrame({
        "dim_node":   ["Razem", "Grupa A", "Grupa B", "A1", "A2", "B1", "B2", "B3"],
        "dim_parent": ["",      "Razem",   "Razem",   "Grupa A", "Grupa A",
                       "Grupa B", "Grupa B", "Grupa B"],
        "val_size":   [0.0,     615.0,     665.0,     295.0, 135.0, 390.0, 180.0, 68.0],
    })


def load_ribbon() -> pd.DataFrame:
    """
    Ribbon / bump chart sample data: 5 entities ranked over 5 time periods.

    Columns
    -------
    dim_entity : str — entity label (Podmiot A–E)
    dim_year   : int — year (2020–2024)
    val_rank   : int — rank (1 = best position)
    """
    rows = [
        ("Podmiot A", 2020, 1), ("Podmiot A", 2021, 1), ("Podmiot A", 2022, 1),
        ("Podmiot A", 2023, 1), ("Podmiot A", 2024, 1),
        ("Podmiot B", 2020, 2), ("Podmiot B", 2021, 2), ("Podmiot B", 2022, 2),
        ("Podmiot B", 2023, 2), ("Podmiot B", 2024, 2),
        ("Podmiot C", 2020, 3), ("Podmiot C", 2021, 3), ("Podmiot C", 2022, 3),
        ("Podmiot C", 2023, 3), ("Podmiot C", 2024, 3),
        ("Podmiot D", 2020, 4), ("Podmiot D", 2021, 4), ("Podmiot D", 2022, 4),
        ("Podmiot D", 2023, 4), ("Podmiot D", 2024, 4),
        ("Podmiot E", 2020, 8), ("Podmiot E", 2021, 7), ("Podmiot E", 2022, 6),
        ("Podmiot E", 2023, 6), ("Podmiot E", 2024, 5),
    ]
    return pd.DataFrame(rows, columns=["dim_entity", "dim_year", "val_rank"])


def load_heatmap() -> pd.DataFrame:
    """
    Heatmap matrix sample data: 4×4 correlation matrix.

    Columns
    -------
    dim_row : str   — row label (Zmienna A–D)
    dim_col : str   — column label (Zmienna A–D)
    val_z   : float — cell value
    """
    labels = ["Zmienna A", "Zmienna B", "Zmienna C", "Zmienna D"]
    matrix = [
        [1.00,  0.82, -0.41, -0.23],
        [0.82,  1.00, -0.78,  0.15],
        [-0.41, -0.78,  1.00, -0.56],
        [-0.23,  0.15, -0.56,  1.00],
    ]
    rows = []
    for i, row_label in enumerate(labels):
        for j, col_label in enumerate(labels):
            rows.append({"dim_row": row_label, "dim_col": col_label, "val_z": matrix[i][j]})
    return pd.DataFrame(rows)


def load_gauge() -> dict:
    """
    Gauge / bullet chart sample data (scalar values, no DataFrame needed).

    Returns dict with keys: value_a, target_a, value_b, target_b, max_b,
    value_c, target_c, min_c, max_c.
    """
    return {
        "gauge_value":  78.0,
        "gauge_target": 80.0,
        "gauge_max":    100.0,
        "bullet_a_value":  615.0,
        "bullet_a_target": 600.0,
        "bullet_a_max":    750.0,
        "bullet_b_value":  -3.2,
        "bullet_b_target": -3.0,
        "bullet_b_min":    -8.0,
        "bullet_b_max":     0.0,
    }


def load_table() -> pd.DataFrame:
    """
    Table sample data: 6 rows × 4 numeric measures + 1 attribute column.

    Columns
    -------
    dim_attribute : str   — row label (Wiersz A–F)
    val_a … val_d : float — numeric measures
    """
    return pd.DataFrame({
        "dim_attribute": ["Wiersz A", "Wiersz B", "Wiersz C",
                          "Wiersz D", "Wiersz E", "Wiersz F"],
        "val_a": [47.2, 45.8, 52.3, 48.1, 43.6, 44.2],
        "val_b": [50.4, 47.5, 55.8, 51.2, 45.1, 49.1],
        "val_c": [-3.2, -1.7, -5.5, -7.2, -1.6, -4.9],
        "val_d": [54.1, 63.2, 109.1, 137.3, 44.1, 73.4],
    })


def load_table_heatmap() -> pd.DataFrame:
    """
    Heatmap table sample data: 5 rows × 6 year columns.

    Columns
    -------
    dim_attribute : str   — row label (Wiersz A–E)
    yr_1 … yr_6   : float — yearly numeric values (positive and negative)
    """
    return pd.DataFrame({
        "dim_attribute": ["Wiersz A", "Wiersz B", "Wiersz C", "Wiersz D", "Wiersz E"],
        "yr_1": [ 4.5,  1.0,  1.8,  0.5,  3.0],
        "yr_2": [-2.5, -4.6, -7.9, -8.9, -5.5],
        "yr_3": [ 5.9,  3.1,  6.4,  7.2,  3.5],
        "yr_4": [ 5.3,  1.9,  2.6,  3.7,  2.4],
        "yr_5": [ 0.1, -0.3,  0.9,  0.9,  0.0],
        "yr_6": [ 3.1,  0.2,  1.1,  0.7,  1.5],
    })
