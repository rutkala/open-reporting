-- raw.imf_weo
-- Source: IMF World Economic Outlook (WEO) database
-- Package: weo (pip install weo)
-- API: downloads latest WEO release files from imf.org
-- Grain: one row per WEO subject × ISO country code × year
--
-- is_projection = TRUE for years beyond the last official actuals year
-- (IMF WEO typically marks actuals vs. projections per country per indicator)
--
-- Update method: upsert on (weo_subject, iso_code, year, weo_edition)
-- weo_edition: e.g. '2024-10' for October 2024 release

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.imf_weo (
    weo_subject     VARCHAR(30)     NOT NULL,   -- WEO indicator code e.g. GGXCNL_NGDP
    iso_code        VARCHAR(5)      NOT NULL,   -- ISO 3166-1 alpha-3 country code e.g. POL
    year            SMALLINT        NOT NULL,   -- Calendar year e.g. 2024
    value           DOUBLE,                     -- Indicator value (NULL if not available)
    is_projection   BOOLEAN         NOT NULL DEFAULT FALSE,  -- TRUE for forecast years
    weo_edition     VARCHAR(10)     NOT NULL,   -- Release edition e.g. 2024-10
    fetched_at      TIMESTAMPTZ     DEFAULT NOW(),
    CONSTRAINT imf_weo_pk
        PRIMARY KEY (weo_subject, iso_code, year, weo_edition)
);

CREATE INDEX IF NOT EXISTS imf_weo_subject_idx
    ON raw.imf_weo (weo_subject);

CREATE INDEX IF NOT EXISTS imf_weo_iso_idx
    ON raw.imf_weo (iso_code);

CREATE INDEX IF NOT EXISTS imf_weo_year_idx
    ON raw.imf_weo (year);
