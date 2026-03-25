-- dim_sector: NACE Rev.2 / PKD 2007 industry classification
-- Source: Eurostat / GUS PKD classification
-- Hierarchy: section (A–U) → division (2-digit) → group (3-digit) → class (4-digit)
CREATE TABLE IF NOT EXISTS curated.dim_sector (
    sector_key      INTEGER      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    pkd_code        VARCHAR(10)  NOT NULL UNIQUE,  -- e.g. 'C', '26', '26.1', '26.11'
    nace_code       VARCHAR(10),                    -- Eurostat NACE (same as PKD for Rev.2)
    level           VARCHAR(10)  NOT NULL CHECK (level IN ('section','division','group','class')),
    name_pl         VARCHAR(300) NOT NULL,
    name_en         VARCHAR(300),
    parent_pkd      VARCHAR(10)  REFERENCES curated.dim_sector(pkd_code),
    section_code    CHAR(1)      NOT NULL,          -- top-level section (A–U), denormalised
    section_name_pl VARCHAR(200),
    is_market       BOOLEAN      NOT NULL DEFAULT TRUE  -- market vs non-market activity
);
