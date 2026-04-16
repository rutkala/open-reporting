# Dashboard Assembly Standard

This standard defines the mandatory technical and visual requirements for a completed Dashboard application. It is the "Gold Standard" used by the Quality Engineer to sign off on the Assembly station.

## 1. Structural Integrity
- **Project Layout**: The dashboard must reside in its own directory `products/dashboards/{domain}/`.
- **Template Adherence**: The structure must strictly follow the `products/dashboards/template/` pattern:
    - `app.py`: Main layout and callbacks.
    - `data.py`: Data loading functions.
    - `measures.py`: Measure definitions and labels.
    - `static/`: Assets and CSS.

## 2. Data Implementation
- **No Sample Data**: `data.py` must not contain hardcoded sample DataFrames. All data must be fetched via `products.visuals.lib.db.query` from the warehouse.
- **Optimized Loading**: Data loaders must be pre-aggregated. The dashboard should not perform heavy aggregations in the `app.py` runtime.
- **Correct Measures**: All values must be passed through the `Measure` objects in `measures.py` to ensure correct formatting (currency, %, decimals).

## 3. Visual Execution
- **Library Usage**: All charts must be called from `products.visuals.components/`. Custom Plotly code is forbidden within `app.py`.
- **Theme Compliance**:
    - Backgrounds must use `BG_PAGE` and `BG_SURFACE`.
    - Cards must have the specified shadow and `border-radius: 6px`.
    - Fonts must match the `FONT_FAMILY` standard.
- **Layout Rules**: 
    - Max 2 charts per row.
    - Every chart must have a title.
    - All content must be wrapped in a "Topic Group" with a section heading.

## 4. Content & Language
- **Language**: All user-facing strings (titles, labels, tooltips, footers) must be in formal Polish.
- **Source Attribution**: The footer must contain a valid source and "last updated" date.
- **Clarity**: Every chart must have a clear subtitle explaining the time period or scope.

## 5. Performance & Security
- **Responsive Design**: The layout must be responsive (using `grid-auto` or `flex`).
- **No Secrets**: No API keys or database credentials may be committed to the repository; use `.env`.
