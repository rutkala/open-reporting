-- V001: Catalogue schema — domains, domain_details, sources, domain_detail_sources
-- Run once against PostgreSQL operational database
-- Idempotent: uses IF NOT EXISTS throughout

\i platform/database/catalogue/01_domains.sql
\i platform/database/catalogue/02_domain_details.sql
\i platform/database/catalogue/03_sources.sql
\i platform/database/catalogue/04_domain_detail_sources.sql
