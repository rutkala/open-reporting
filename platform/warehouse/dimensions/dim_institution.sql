-- dim_institution: Public bodies — courts, schools, hospitals, ministries, regulators
-- Used in CRM (courts), EDU (schools), HLT (hospitals), PUB (ministries) domains
CREATE TABLE IF NOT EXISTS curated.dim_institution (
    institution_key INTEGER      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    institution_id  VARCHAR(50)  NOT NULL UNIQUE,   -- internal slug
    institution_type VARCHAR(30) NOT NULL CHECK (institution_type IN (
                        'ministry',
                        'regulator',
                        'court',
                        'school',
                        'university',
                        'hospital',
                        'municipality',
                        'other'
                    )),
    name_pl         VARCHAR(300) NOT NULL,
    name_en         VARCHAR(300),
    teryt_code      VARCHAR(10)  REFERENCES curated.dim_geography(teryt_code),
    voivodeship     VARCHAR(100),
    parent_id       VARCHAR(50)  REFERENCES curated.dim_institution(institution_id),
    rspo_number     VARCHAR(20),    -- school register number (EDU)
    regon           VARCHAR(14),    -- GUS business register
    nfz_code        VARCHAR(20),    -- NFZ provider code (HLT)
    valid_from      DATE,
    valid_to        DATE
);
