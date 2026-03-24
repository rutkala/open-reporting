-- V001: Catalogue schema — domains, sources, source_domains
-- Run once against PostgreSQL operational database
-- Idempotent: uses IF NOT EXISTS throughout

\i platform/database/catalogue/domains.sql
\i platform/database/catalogue/sources.sql
\i platform/database/catalogue/source_domains.sql
