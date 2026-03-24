CREATE TABLE IF NOT EXISTS catalogue.domain_details (
    detail_id       VARCHAR(100)    PRIMARY KEY,
    domain_id       VARCHAR(5)      NOT NULL REFERENCES catalogue.domains(domain_id),
    name            VARCHAR(200)    NOT NULL,
    unit            VARCHAR(50),
    frequency       VARCHAR(20)     CHECK (frequency IN ('real_time', 'daily', 'weekly', 'monthly', 'quarterly', 'biannual', 'annual', 'irregular')),
    description     TEXT,
    notes           TEXT,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  catalogue.domain_details           IS 'Atomic statistical indicators tracked by Open Reporting';
COMMENT ON COLUMN catalogue.domain_details.detail_id IS 'Slug identifier, e.g. exchange_rate_usd_pln, unemployment_rate';
COMMENT ON COLUMN catalogue.domain_details.unit      IS 'Unit of measurement, e.g. %, PLN, index, persons';
