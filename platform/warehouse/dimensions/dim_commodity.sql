-- dim_commodity: Products and instruments across energy, agriculture, finance, trade domains
-- Covers: energy carriers, agricultural products, financial instruments, trade goods (HS)
CREATE TABLE IF NOT EXISTS curated.dim_commodity (
    commodity_key   INTEGER      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    commodity_id    VARCHAR(30)  NOT NULL UNIQUE,   -- internal slug, e.g. 'energy.electricity'
    domain_id       VARCHAR(5),                     -- primary domain (ENE, AGR, FIN, TRD)
    category        VARCHAR(30)  NOT NULL CHECK (category IN (
                        'energy',           -- electricity, gas, coal, oil, RES
                        'agricultural',     -- crops, livestock, forestry
                        'financial',        -- equities, bonds, FX, derivatives
                        'trade_good',       -- HS-coded traded goods
                        'other'
                    )),
    name_pl         VARCHAR(200) NOT NULL,
    name_en         VARCHAR(200),
    unit            VARCHAR(30),                    -- natural unit: MWh, tonne, PLN, USD
    hs_code         VARCHAR(10),                    -- Harmonised System code (TRD)
    cn_code         VARCHAR(10),                    -- Combined Nomenclature (EU trade)
    energy_carrier  VARCHAR(30),                    -- for energy: electricity/gas/coal/oil
    is_renewable    BOOLEAN                         -- for energy commodities
);
