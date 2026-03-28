-- raw.dbw_observations + raw.dbw_positions
-- Source: GUS DBW HVD catalogue — dbw.stat.gov.pl/pl/katalog/bulk
-- Catalogue API: https://dbw.stat.gov.pl/api_app/getCatalogValues
-- File format: ZIP(CSV) — one file per variable × cross-section combo
-- Grain: one row per variable × cross-section × year × period × dimension combination
-- Update method: upsert on natural key
--
-- Dimensions are stored as integer position IDs (dimension_N_position_id in source CSV).
-- Resolve labels by joining to raw.dbw_positions on (section_id, dim_id, position_id).
-- Supports up to 6 dimension columns — covers all observed cross-section shapes in HVD.

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.dbw_observations (
    variable_id     INTEGER         NOT NULL,   -- id-zmienna
    section_id      INTEGER         NOT NULL,   -- id-przekroj (cross-section)
    year            INTEGER         NOT NULL,   -- id-daty
    period_id       INTEGER         NOT NULL,   -- id-okres
    dim1_id         BIGINT      NOT NULL DEFAULT 0,  -- dimension_1_position_id (0 = slot unused)
    dim2_id         BIGINT      NOT NULL DEFAULT 0,  -- dimension_2_position_id
    dim3_id         BIGINT      NOT NULL DEFAULT 0,  -- dimension_3_position_id
    dim4_id         BIGINT      NOT NULL DEFAULT 0,  -- dimension_4_position_id
    dim5_id         BIGINT      NOT NULL DEFAULT 0,  -- dimension_5_position_id
    dim6_id         BIGINT      NOT NULL DEFAULT 0,  -- dimension_6_position_id
    value           DOUBLE,                     -- wartosc (NULL if suppressed/missing)
    precision       INTEGER,                    -- precyzja — decimal places
    fetched_at      TIMESTAMPTZ     DEFAULT NOW(),
    CONSTRAINT dbw_observations_pk
        PRIMARY KEY (variable_id, section_id, year, period_id,
                     dim1_id, dim2_id, dim3_id, dim4_id, dim5_id, dim6_id)
);

CREATE INDEX IF NOT EXISTS dbw_observations_variable_idx
    ON raw.dbw_observations (variable_id);

CREATE INDEX IF NOT EXISTS dbw_observations_year_idx
    ON raw.dbw_observations (year);

-- Lookup table: resolves integer position IDs to human-readable labels.
-- Populated once per cross-section (section_id) during ingestion.
CREATE TABLE IF NOT EXISTS raw.dbw_positions (
    section_id      INTEGER         NOT NULL,   -- id-przekroj
    dim_id          INTEGER         NOT NULL,   -- id-wymiar (dimension number within cross-section)
    dim_name        VARCHAR(200),               -- nazwa-wymiar e.g. "Sex", "Type of locality"
    position_id     BIGINT          NOT NULL,   -- dimension_N_position_id (can exceed INT32)
    position_name   VARCHAR(500),               -- nazwa-pozycja e.g. "Males", "Total"
    symbol          VARCHAR(50),                -- short code e.g. "1", "MIA"
    fetched_at      TIMESTAMPTZ     DEFAULT NOW(),
    CONSTRAINT dbw_positions_pk
        PRIMARY KEY (section_id, dim_id, position_id)
);
