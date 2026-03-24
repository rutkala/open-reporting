CREATE SCHEMA IF NOT EXISTS catalogue;

CREATE TABLE IF NOT EXISTS catalogue.domains (
    domain_id       VARCHAR(50)     PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    domain_group    VARCHAR(50)     NOT NULL,
    description     TEXT,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  catalogue.domains              IS 'Broad thematic domains covered by Open Reporting';
COMMENT ON COLUMN catalogue.domains.domain_id    IS 'Slug identifier, e.g. finance_capital, labour_market';
COMMENT ON COLUMN catalogue.domains.domain_group IS 'Top-level group, e.g. Economy, Society, Environment';
