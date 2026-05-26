{{ config(materialized='table', schema='curated') }}

/*
  dim_cofog — Classification of the Functions of Government (COFOG).

  Star-schema convention: fact_finance_cofog joins to this dim on the
  cofog_function entity (integer 1..10). Visuals slice by the Polish
  label for human-readable axes.

  Grain: one row per top-level COFOG function (10 rows).

  Columns:
    cofog_function   INT   — 1..10, primary key
    cofog_code       TEXT  — 'pub.cofog_01_gdp' etc., source detail_id
    cofog_label_pl   TEXT  — Polish function name
    cofog_label_en   TEXT  — English function name

  Source: Eurostat / IMF GFS — COFOG 10-class system.
*/

with funcs (cofog_function, cofog_code, cofog_label_pl, cofog_label_en) as (
    values
        (1,  'pub.cofog_01_gdp', 'Usługi publiczne',       'General public services'),
        (2,  'pub.cofog_02_gdp', 'Obrona',                 'Defence'),
        (3,  'pub.cofog_03_gdp', 'Porządek publiczny',     'Public order and safety'),
        (4,  'pub.cofog_04_gdp', 'Gospodarka',             'Economic affairs'),
        (5,  'pub.cofog_05_gdp', 'Środowisko',             'Environmental protection'),
        (6,  'pub.cofog_06_gdp', 'Mieszkalnictwo',         'Housing and community amenities'),
        (7,  'pub.cofog_07_gdp', 'Zdrowie',                'Health'),
        (8,  'pub.cofog_08_gdp', 'Kultura i rekreacja',    'Recreation, culture, religion'),
        (9,  'pub.cofog_09_gdp', 'Edukacja',               'Education'),
        (10, 'pub.cofog_10_gdp', 'Ochrona socjalna',       'Social protection')
)
select * from funcs
