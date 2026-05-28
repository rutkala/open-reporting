-- raw.bdl_observations
-- Source: GUS Bank Danych Lokalnych (BDL) REST API — bdl.stat.gov.pl/api/v1/
-- API endpoint: GET /data/by-variable/{variableId}?unitLevel=2&page=0&pageSize=100
-- Grain: one row per variable × administrative unit × year
-- Unit levels fetched: 5 (national) and 2 (voivodeship / NUTS2 equivalent)
--
-- nuts_code: populated where the BDL unit metadata includes a NUTS identifier;
--            NULL otherwise (common for powiat/gmina level units).
--
-- Update method: upsert on (variable_id, unit_id, year)

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.bdl_observations (
    variable_id    INTEGER         NOT NULL,   -- BDL variable ID e.g. 72305
    unit_id        VARCHAR         NOT NULL,   -- GUS unit code e.g. "011000000000"
    unit_name      VARCHAR,                    -- human-readable e.g. "DOLNOŚLĄSKIE"
    nuts_code      VARCHAR,                    -- NUTS2 code e.g. "PL21", NULL if unavailable
    year           INTEGER         NOT NULL,
    value          DOUBLE,                     -- NULL when data is suppressed or unavailable
    fetched_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT bdl_observations_pk
        PRIMARY KEY (variable_id, unit_id, year)
);

CREATE INDEX IF NOT EXISTS bdl_observations_variable_idx
    ON raw.bdl_observations (variable_id);

CREATE INDEX IF NOT EXISTS bdl_observations_year_idx
    ON raw.bdl_observations (year);

CREATE INDEX IF NOT EXISTS bdl_observations_unit_idx
    ON raw.bdl_observations (unit_id);
