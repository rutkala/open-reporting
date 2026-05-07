# Candlestick

## When to use
OHLC financial time series — open, high, low, close per period. Use only for financial
or quasi-financial data that has a genuine open/high/low/close structure.
E.g. bond yield ranges, commodity price ranges by month.
**Not:** general time series (use Line); data without genuine OHLC structure.

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| DATES | Yes | period labels ("YYYY-MM" or "YYYY-MM-DD") |
| OPEN | Yes | opening values per period |
| HIGH | Yes | high values per period |
| LOW | Yes | low values per period |
| CLOSE | Yes | closing values per period |
| Y MEASURE | Yes | primary measure |

## Import
```python
from complex_dashboard.assets.components.financial_chart import candlestick
```

## Template
```python
html.Div(style=S["card"], children=[
    candlestick(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: TODO — dane za 2024 r.",
        dates=m.DIMS["date"].values(_df_ohlc),
        open_=_df_ohlc["open"].tolist(),
        high=_df_ohlc["high"].tolist(),
        low=_df_ohlc["low"].tolist(),
        close=_df_ohlc["close"].tolist(),
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Data must have genuine OHLC semantics (high ≥ open/close ≥ low)
- `dates` column: use `dim_date` from the OHLC loader
- Green candle = close > open; red = close < open (enforced by Plotly)
