-- raw.nbp_exchange_rates
-- Source: NBP Web API — Table A (mid-rates for major currencies)
-- API: https://api.nbp.pl/api/exchangerates/rates/A/{code}
-- Grain: one row per currency per business day
-- Update method: upsert on (currency_code, rate_date)

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.nbp_exchange_rates (
    currency_code   VARCHAR(3)      NOT NULL,   -- ISO 4217 code: USD, EUR, CHF, GBP
    rate_date       DATE            NOT NULL,   -- effective date of the fixing
    mid_rate        NUMERIC(10, 4)  NOT NULL,   -- PLN mid-rate (e.g. 3.6803)
    table_no        VARCHAR(30),                -- NBP table identifier e.g. 058/A/NBP/2026
    fetched_at      TIMESTAMPTZ     DEFAULT NOW(),
    CONSTRAINT nbp_exchange_rates_pk PRIMARY KEY (currency_code, rate_date)
);

CREATE INDEX IF NOT EXISTS nbp_exchange_rates_date_idx
    ON raw.nbp_exchange_rates (rate_date);
