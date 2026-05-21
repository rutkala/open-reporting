{{ config(materialized='table', schema='curated') }}

/*
  dim_geo — shared geography dimension.

  Star-schema convention: any fact table with a `geo` column joins to this
  dim on the `geo` entity (Eurostat 2-letter country code) and exposes
  Polish/English country names, EU membership, and continent for slicing
  in dashboards.

  Grain: one row per country (Eurostat ISO 2-letter code).

  Columns:
    geo           TEXT      — 2-letter country code, primary key
    name_pl       TEXT      — Polish country name (e.g. "Polska")
    name_en       TEXT      — English country name (e.g. "Poland")
    eu_member     BOOLEAN   — current EU member (as of 2026-05)
    continent     TEXT      — broad region label (Europe / non-European peer)

  Coverage: EU-27 + UK + EFTA (NO, CH, IS, LI) + a few non-European peers
  commonly compared (US, JP). Extend as needed when ingesting new data.
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
        ('GR', 'Grecja',            'Greece',         true,  'Europe'),
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
)
select * from countries
