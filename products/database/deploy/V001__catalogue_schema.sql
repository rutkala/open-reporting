-- V001: Catalogue schema — domains, domain_details, sources, domain_detail_sources
-- Run once against PostgreSQL operational database
-- Idempotent: uses IF NOT EXISTS throughout

\i products/database/catalogue/01_domains.sql
\i products/database/catalogue/02_domain_details.sql
\i products/database/catalogue/03_sources.sql
\i products/database/catalogue/04_domain_detail_sources.sql
