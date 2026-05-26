CREATE TABLE IF NOT EXISTS catalogue.domain_detail_sources (
    detail_id           VARCHAR(100)    NOT NULL REFERENCES catalogue.domain_details(detail_id),
    source_id           VARCHAR(50)     NOT NULL REFERENCES catalogue.sources(source_id),
    geo_levels          VARCHAR(200),
    year_from           SMALLINT,
    year_to             SMALLINT,
    coverage_notes      TEXT,
    series_id           VARCHAR(300),
    verified            BOOLEAN         NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT domain_detail_sources_pk PRIMARY KEY (detail_id, source_id)
);

-- Idempotent migrations for existing installations
ALTER TABLE catalogue.domain_detail_sources ADD COLUMN IF NOT EXISTS series_id  VARCHAR(300);
ALTER TABLE catalogue.domain_detail_sources ADD COLUMN IF NOT EXISTS verified   BOOLEAN NOT NULL DEFAULT FALSE;

COMMENT ON TABLE  catalogue.domain_detail_sources                IS 'Mapping of which sources provide which indicators';
COMMENT ON COLUMN catalogue.domain_detail_sources.geo_levels     IS 'Pipe-separated geo levels, e.g. country|voivodeship|county';
COMMENT ON COLUMN catalogue.domain_detail_sources.year_to        IS 'NULL means coverage continues to present';
COMMENT ON COLUMN catalogue.domain_detail_sources.coverage_notes IS 'Human-readable context: methodology caveats, lag notes, unit gotchas';
COMMENT ON COLUMN catalogue.domain_detail_sources.series_id      IS 'Exact identifier within the source system (Eurostat dataset+filter, NBP endpoint path, BDL variable ID, PSE data type, sheet!column for XLSX). NULL until verified.';
COMMENT ON COLUMN catalogue.domain_detail_sources.verified       IS 'TRUE only after series_id has been manually confirmed against the live source. Ingestion pipelines must only trust verified=TRUE rows.';
