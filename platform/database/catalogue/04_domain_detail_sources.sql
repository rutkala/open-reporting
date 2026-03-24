CREATE TABLE IF NOT EXISTS catalogue.domain_detail_sources (
    detail_id           VARCHAR(100)    NOT NULL REFERENCES catalogue.domain_details(detail_id),
    source_id           VARCHAR(50)     NOT NULL REFERENCES catalogue.sources(source_id),
    geo_levels          VARCHAR(200),
    year_from           SMALLINT,
    year_to             SMALLINT,
    coverage_notes      TEXT,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT domain_detail_sources_pk PRIMARY KEY (detail_id, source_id)
);

COMMENT ON TABLE  catalogue.domain_detail_sources                IS 'Mapping of which sources provide which indicators';
COMMENT ON COLUMN catalogue.domain_detail_sources.geo_levels     IS 'Pipe-separated geo levels, e.g. country|voivodeship|county';
COMMENT ON COLUMN catalogue.domain_detail_sources.year_to        IS 'NULL means coverage continues to present';
COMMENT ON COLUMN catalogue.domain_detail_sources.coverage_notes IS 'What specifically is available from this source for this indicator';
