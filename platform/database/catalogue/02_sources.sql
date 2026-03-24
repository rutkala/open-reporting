CREATE TABLE IF NOT EXISTS catalogue.sources (
    source_id           VARCHAR(50)     PRIMARY KEY,
    name                VARCHAR(200)    NOT NULL,
    provider            VARCHAR(100)    NOT NULL,
    tier                SMALLINT        NOT NULL CHECK (tier IN (1, 2, 3)),
    url                 VARCHAR(500),
    api_url             VARCHAR(500),
    auth_type           VARCHAR(20)     CHECK (auth_type IN ('none', 'api_key', 'oauth', 'basic')),
    auth_env_var        VARCHAR(100),
    format              VARCHAR(20)     CHECK (format IN ('json', 'xml', 'csv', 'xlsx', 'html')),
    update_frequency    VARCHAR(20)     CHECK (update_frequency IN ('daily', 'weekly', 'monthly', 'quarterly', 'biannual', 'annual', 'irregular')),
    notes               TEXT,
    active              BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  catalogue.sources                  IS 'Data source systems available for ingestion';
COMMENT ON COLUMN catalogue.sources.tier             IS '1=GUS API, 2=International API, 3=File-based/scrape';
COMMENT ON COLUMN catalogue.sources.auth_env_var     IS 'Name of env var holding the API key or secret';
COMMENT ON COLUMN catalogue.sources.active           IS 'FALSE = source decommissioned or temporarily disabled';
