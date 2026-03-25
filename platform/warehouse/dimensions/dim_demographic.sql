-- dim_demographic: Population segments used across health, labour, social domains
-- Combination dimension — each row is a unique (age_group, gender, education) combination
CREATE TABLE IF NOT EXISTS curated.dim_demographic (
    demographic_key INTEGER      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    age_group       VARCHAR(20),                    -- e.g. '15-24', '25-34', '65+'
    age_from        SMALLINT,
    age_to          SMALLINT,                       -- NULL for open-ended (e.g. 65+)
    gender          CHAR(1)      CHECK (gender IN ('M','F','T')),  -- M/F/Total
    education_level VARCHAR(30)  CHECK (education_level IN (
                        'primary', 'lower_secondary', 'upper_secondary',
                        'post_secondary', 'tertiary', 'total', NULL
                    )),
    education_isced VARCHAR(5),                     -- ISCED 2011 code
    citizenship     VARCHAR(50)                     -- 'Polish', 'EU', 'non-EU', 'total'
);
