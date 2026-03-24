CREATE SCHEMA IF NOT EXISTS catalogue;

CREATE TABLE IF NOT EXISTS catalogue.domains (
    domain_id       VARCHAR(50)     PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    group_name      VARCHAR(50)     NOT NULL,
    description     TEXT,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  catalogue.domains              IS 'Smallest unique statistical domains tracked by Open Reporting';
COMMENT ON COLUMN catalogue.domains.domain_id    IS 'Slug identifier, e.g. labour_market, demographics';
COMMENT ON COLUMN catalogue.domains.group_name   IS 'Thematic group, e.g. Economy, Society, Environment';
