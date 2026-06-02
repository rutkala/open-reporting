{{ config(materialized='table', schema='curated') }}

/*
  dim_geo — shared geography dimension.

  Star-schema convention: any fact table with a `geo` column joins to this
  dim on the `geo` entity and exposes Polish/English names, EU membership,
  continent, and (for Polish regional data) the NUTS hierarchy for slicing
  in dashboards.

  Grain: one row per geography — country (Eurostat 2-letter code) OR Polish
  NUTS1 macroregion / NUTS2 voivodeship. `geo_level` discriminates the three.

  Columns:
    geo           TEXT      — geo code, primary key (e.g. "PL", "PL21")
    name_pl       TEXT      — Polish name (e.g. "Polska", "Małopolskie")
    name_en       TEXT      — English name; Polish proper noun for regions
    eu_member     BOOLEAN   — current EU member (regions inherit PL = true)
    continent     TEXT      — broad region label (Europe / non-European peer)
    geo_level     TEXT      — 'country' | 'nuts1' | 'nuts2'
    parent_geo    TEXT      — roll-up parent: nuts2→nuts1, nuts1→country;
                              NULL for countries. Enables choropleth + drill.

  Coverage: EU-27 + UK + EFTA (NO, CH, IS, LI) + non-European peers (US, JP)
  at country level, PLUS all 7 Polish NUTS1 macroregions and 17 NUTS2
  voivodeships (from the seed_geo_nuts authoritative seed). Extend the
  country VALUES block as needed when ingesting new data.
*/

with countries (geo, name_pl, name_en, eu_member, continent) as (
    values
        -- EU-27
        ('AT', 'Austria',           'Austria',        true,  'Europe'),
        ('BE', 'Belgia',            'Belgium',        true,  'Europe'),
        ('BG', 'Bułgaria',          'Bulgaria',       true,  'Europe'),
        ('HR', 'Chorwacja',         'Croatia',        true,  'Europe'),
        ('CY', 'Cypr',              'Cyprus',         true,  'Europe'),
        ('CZ', 'Czechy',            'Czech Republic', true,  'Europe'),
        ('DK', 'Dania',             'Denmark',        true,  'Europe'),
        ('EE', 'Estonia',           'Estonia',        true,  'Europe'),
        ('FI', 'Finlandia',         'Finland',        true,  'Europe'),
        ('FR', 'Francja',           'France',         true,  'Europe'),
        ('DE', 'Niemcy',            'Germany',        true,  'Europe'),
        ('EL', 'Grecja',            'Greece',         true,  'Europe'),  -- Eurostat code (ISO uses GR)
        ('HU', 'Węgry',             'Hungary',        true,  'Europe'),
        ('IE', 'Irlandia',          'Ireland',        true,  'Europe'),
        ('IT', 'Włochy',            'Italy',          true,  'Europe'),
        ('LV', 'Łotwa',             'Latvia',         true,  'Europe'),
        ('LT', 'Litwa',             'Lithuania',      true,  'Europe'),
        ('LU', 'Luksemburg',        'Luxembourg',     true,  'Europe'),
        ('MT', 'Malta',             'Malta',          true,  'Europe'),
        ('NL', 'Holandia',          'Netherlands',    true,  'Europe'),
        ('PL', 'Polska',            'Poland',         true,  'Europe'),
        ('PT', 'Portugalia',        'Portugal',       true,  'Europe'),
        ('RO', 'Rumunia',           'Romania',        true,  'Europe'),
        ('SK', 'Słowacja',          'Slovakia',       true,  'Europe'),
        ('SI', 'Słowenia',          'Slovenia',       true,  'Europe'),
        ('ES', 'Hiszpania',         'Spain',          true,  'Europe'),
        ('SE', 'Szwecja',           'Sweden',         true,  'Europe'),
        -- EFTA + UK
        ('UK', 'Wielka Brytania',   'United Kingdom', false, 'Europe'),
        ('NO', 'Norwegia',          'Norway',         false, 'Europe'),
        ('CH', 'Szwajcaria',        'Switzerland',    false, 'Europe'),
        ('IS', 'Islandia',          'Iceland',        false, 'Europe'),
        ('LI', 'Liechtenstein',     'Liechtenstein',  false, 'Europe'),
        -- non-European peers
        ('US', 'Stany Zjednoczone', 'United States',  false, 'Americas'),
        ('JP', 'Japonia',           'Japan',          false, 'Asia')
),

country_rows as (
    select
        geo, name_pl, name_en, eu_member, continent,
        'country'             as geo_level,
        cast(null as varchar) as parent_geo
    from countries
),

-- Polish NUTS1 macroregions + NUTS2 voivodeships from the authoritative seed.
-- Lets regional facts (geo = 'PL21' …) resolve to a Polish name and roll up
-- nuts2 → nuts1 → country for choropleths and regional explorers.
region_rows as (
    select
        geo,
        geo_name   as name_pl,
        geo_name   as name_en,   -- voivodeship names are Polish proper nouns
        true       as eu_member,
        'Europe'   as continent,
        geo_type   as geo_level,
        case
            when geo_type = 'nuts2' then nuts1_code     -- PL21 → PL2
            when geo_type = 'nuts1' then country_code   -- PL2  → PL
        end        as parent_geo
    from {{ ref('seed_geo_nuts') }}
    where geo_type in ('nuts1', 'nuts2')
)

select * from country_rows
union all
select * from region_rows
