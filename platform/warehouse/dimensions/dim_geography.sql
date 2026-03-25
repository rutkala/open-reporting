-- dim_geography: TERYT administrative hierarchy
-- Source: GUS TERYT register (catalogue source: teryt)
-- Levels: national (PL) → voivodeship (NUTS2) → powiat (NUTS3) → gmina
CREATE TABLE IF NOT EXISTS curated.dim_geography (
    geo_key         INTEGER      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    teryt_code      VARCHAR(10)  NOT NULL UNIQUE,  -- GUS TERYT identifier
    nuts_code       VARCHAR(10),                    -- Eurostat NUTS code
    name            VARCHAR(200) NOT NULL,
    name_en         VARCHAR(200),
    level           VARCHAR(20)  NOT NULL CHECK (level IN (
                        'national',     -- PL
                        'voivodeship',  -- NUTS2 (16 units)
                        'powiat',       -- NUTS3 (~380 units)
                        'gmina'         -- LAU (~2500 units)
                    )),
    parent_teryt    VARCHAR(10)  REFERENCES curated.dim_geography(teryt_code),
    voivodeship     VARCHAR(100),   -- denormalised for convenience
    is_urban        BOOLEAN,        -- gmina type: urban/rural/mixed
    area_km2        NUMERIC(10,2),
    valid_from      DATE,
    valid_to        DATE            -- NULL = currently active
);
