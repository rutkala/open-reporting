-- dim_company: Legal entities — GPW-listed companies, major enterprises
-- Source: REGON, KRS, GPW listing data
-- Slowly changing dimension (Type 2 for name/sector changes)
CREATE TABLE IF NOT EXISTS curated.dim_company (
    company_key     INTEGER      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    krs_number      VARCHAR(10),                    -- KRS court registry number
    nip             VARCHAR(10),                    -- tax identifier
    regon           VARCHAR(14),                    -- GUS business register
    ticker          VARCHAR(10),                    -- GPW stock ticker (if listed)
    isin            VARCHAR(12),                    -- ISIN security identifier
    name            VARCHAR(300) NOT NULL,
    short_name      VARCHAR(100),
    legal_form      VARCHAR(50),                    -- sp. z o.o., SA, etc.
    pkd_main        VARCHAR(10)  REFERENCES curated.dim_sector(pkd_code),
    is_gpw_listed   BOOLEAN      NOT NULL DEFAULT FALSE,
    gpw_market      VARCHAR(20),                    -- Main Market / NewConnect
    voivodeship     VARCHAR(100),
    founded_year    SMALLINT,
    -- SCD2 fields
    valid_from      DATE         NOT NULL,
    valid_to        DATE,                           -- NULL = current record
    is_current      BOOLEAN      NOT NULL DEFAULT TRUE
);
