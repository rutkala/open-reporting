-- raw.eurostat_observations
-- Source: Eurostat SDMX REST API
-- API: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}
-- Grain: one row per dataset × geo × period × dimension combination
--
-- Dimensions vary by dataset (e.g. demo_gind has indic_de; lfsq_ergan has sex/age/unit).
-- They are stored as a sorted key=value string so the combination can serve as a PK component.
-- Example dimension_key: "age=TOTAL&sex=T&unit=PC_ACT"
--
-- Update method: upsert on (dataset_code, geo, period, dimension_key)

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.eurostat_observations (
    dataset_code    VARCHAR(60)     NOT NULL,   -- Eurostat dataset identifier e.g. demo_gind
    geo             VARCHAR(10)     NOT NULL,   -- NUTS/ISO geo code e.g. PL
    period          VARCHAR(10)     NOT NULL,   -- Time period e.g. 2024, 2024-Q1, 2024-01
    dimension_key   VARCHAR(500)    NOT NULL,   -- Sorted dim=val pairs e.g. "indic_de=GBIRTHRT"
    value           DOUBLE,                     -- Observed value (NULL if status only)
    obs_status      VARCHAR(5),                 -- Eurostat status flag: e=estimated, p=provisional
    fetched_at      TIMESTAMPTZ     DEFAULT NOW(),
    CONSTRAINT eurostat_observations_pk
        PRIMARY KEY (dataset_code, geo, period, dimension_key)
);

CREATE INDEX IF NOT EXISTS eurostat_observations_dataset_idx
    ON raw.eurostat_observations (dataset_code);

CREATE INDEX IF NOT EXISTS eurostat_observations_period_idx
    ON raw.eurostat_observations (period);
