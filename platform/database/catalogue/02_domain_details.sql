CREATE TABLE IF NOT EXISTS catalogue.domain_details (
    detail_id    VARCHAR(100) PRIMARY KEY,
    domain_id    VARCHAR(5)   NOT NULL REFERENCES catalogue.domains(domain_id),
    name         VARCHAR(200) NOT NULL,
    unit         VARCHAR(50),
    frequency    VARCHAR(20)  CHECK (frequency IN (
                     'real_time','daily','weekly','monthly',
                     'quarterly','biannual','annual','irregular')),
    detail_type  VARCHAR(20)  NOT NULL DEFAULT 'indicator' CHECK (detail_type IN (
                     'indicator',        -- aggregate numerical time series (national/regional level)
                     'micro_indicator',  -- entity-level numerical measure (company, individual)
                     'sentiment',        -- derived signal from text/events (score, count)
                     'reference'         -- pointer to document; not stored in warehouse
                 )),
    entity_level VARCHAR(20)  NOT NULL DEFAULT 'national' CHECK (entity_level IN (
                     'national',    -- Poland aggregate
                     'regional',    -- voivodeship / NUTS2
                     'local',       -- powiat / gmina / NUTS3
                     'sectoral',    -- industry sector (NACE/PKD)
                     'company',     -- legal entity (KRS/NIP)
                     'individual',  -- person
                     'other'
                 )),
    description  TEXT,
    notes        TEXT,
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Idempotent migrations for existing installations
ALTER TABLE catalogue.domain_details ADD COLUMN IF NOT EXISTS
    detail_type VARCHAR(20) NOT NULL DEFAULT 'indicator';
ALTER TABLE catalogue.domain_details ADD COLUMN IF NOT EXISTS
    entity_level VARCHAR(20) NOT NULL DEFAULT 'national';

COMMENT ON TABLE  catalogue.domain_details                IS 'Atomic statistical indicators and facts tracked by Open Reporting';
COMMENT ON COLUMN catalogue.domain_details.detail_id      IS 'Slug identifier, e.g. fin.exchange_rate_usd_pln, lab.unemployment_rate';
COMMENT ON COLUMN catalogue.domain_details.unit           IS 'Unit of measurement, e.g. %, PLN, index, persons';
COMMENT ON COLUMN catalogue.domain_details.detail_type    IS 'indicator=aggregate time series | micro_indicator=entity level | sentiment=text-derived signal | reference=document pointer';
COMMENT ON COLUMN catalogue.domain_details.entity_level   IS 'Primary granularity: national, regional, local, sectoral, company, individual';
