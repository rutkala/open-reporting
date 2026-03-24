CREATE TABLE IF NOT EXISTS catalogue.source_domains (
    source_id           VARCHAR(50)     NOT NULL REFERENCES catalogue.sources(source_id),
    domain_id           VARCHAR(50)     NOT NULL REFERENCES catalogue.domains(domain_id),
    geo_levels          VARCHAR(200),
    year_from           SMALLINT,
    year_to             SMALLINT,
    coverage_notes      TEXT,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT source_domains_pk PRIMARY KEY (source_id, domain_id)
);

COMMENT ON TABLE  catalogue.source_domains                IS 'Mapping of which sources cover which domains';
COMMENT ON COLUMN catalogue.source_domains.geo_levels     IS 'Comma-separated geo levels, e.g. country, voivodeship, county';
COMMENT ON COLUMN catalogue.source_domains.year_to        IS 'NULL means coverage continues to present';
COMMENT ON COLUMN catalogue.source_domains.coverage_notes IS 'What specifically is available from this source for this domain';
