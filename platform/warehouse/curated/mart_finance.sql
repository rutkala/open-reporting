-- curated.mart_finance
-- Domain: Public Finance (PUB)
-- Layer: Gold mart — domain-specific star schema built from curated.all_indicators (silver)
--
-- Sources: eurostat (GFS multi-country), imf (WEO projections), dbw (Poland ESA 2010)
-- Grain: one row per (source_id, detail_id, geo, period_year)
-- Built by: platform/processing/dbt/models/mart/mart_finance.sql
--
-- Key columns:
--   fiscal_category   — policy-relevant hierarchy (Fiscal balance / Total revenue / COFOG: ...)
--   is_projection     — TRUE for IMF WEO forecast years (year >= 2026)
--   is_poland         — convenience flag for Poland vs EU benchmarking
--   is_v4             — Visegrad Four group flag (PL + CZ + SK + HU)
--   country_name      — human-readable EU country name
--   period_year       — INTEGER year (all public finance data is annual)
--
-- Note: mixed units across sources — filter by detail_unit for unit-homogeneous analysis
--   '%'      — Eurostat GFS, IMF WEO (% of GDP or % potential GDP)
--   'PLN mn' — DBW HVD Poland-only data in millions of PLN

-- This DDL is documentation only — the table is managed by dbt (mart_finance.sql model).
-- To rebuild: cd platform/processing/dbt && dbt run --select mart_finance

SELECT 'See platform/processing/dbt/models/mart/mart_finance.sql' AS note;
