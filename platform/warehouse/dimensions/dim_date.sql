-- dim_date: Calendar dimension
-- Populated once via generate.py or dbt seed; never updated
CREATE TABLE IF NOT EXISTS curated.dim_date (
    date_key        INTEGER      PRIMARY KEY,  -- YYYYMMDD
    date            DATE         NOT NULL UNIQUE,
    year            SMALLINT     NOT NULL,
    half_year       SMALLINT     NOT NULL,     -- 1 or 2
    quarter         SMALLINT     NOT NULL,     -- 1–4
    month           SMALLINT     NOT NULL,     -- 1–12
    month_name      VARCHAR(10)  NOT NULL,     -- January … December
    month_name_pl   VARCHAR(15)  NOT NULL,     -- Styczeń … Grudzień
    week_iso        SMALLINT     NOT NULL,     -- ISO week number
    day_of_month    SMALLINT     NOT NULL,
    day_of_week     SMALLINT     NOT NULL,     -- 1=Mon … 7=Sun (ISO)
    day_name        VARCHAR(10)  NOT NULL,
    is_weekend      BOOLEAN      NOT NULL,
    is_polish_holiday BOOLEAN    NOT NULL DEFAULT FALSE,
    holiday_name_pl VARCHAR(100)
);
