# Bundled geographies

Static GeoJSON shapes used by the `choropleth` visual. Committed (not fetched at
runtime) because they are frozen reference geometries — a network dependency on
GISCO at render time would add a failure mode to every dashboard load.

All files are **Eurostat GISCO NUTS 2021**, EPSG:4326 (WGS84), keyed on the
`NUTS_ID` property, which matches our warehouse `geo` code 1:1.

| File | Source | NUTS level | Resolution | Features |
|------|--------|-----------|-----------|----------|
| `europe_countries.geojson` | GISCO `NUTS_RG_20M_2021_4326_LEVL_0` | 0 (country) | 1:20M | 32 EU/EFTA (incl. EL, UK) |
| `poland_nuts2.geojson` | GISCO `NUTS_RG_03M_2021_4326_LEVL_2` | 2 (region) | 1:3M | 17 PL voivodeships (PL21…PL92) |

Both were filtered to the relevant countries and slimmed to `NUTS_ID` + `NUTS_NAME`
properties only.

Source base URL:
`https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/`

**Refresh:** when Eurostat adopts a new NUTS vintage (next after 2021), re-fetch the
corresponding `LEVL_*` file, re-filter, and confirm the `NUTS_ID` set still matches
`curated.dim_geo` (`geo_level in ('country','nuts2')`).
