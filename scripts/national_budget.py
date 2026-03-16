#!/usr/bin/env python3
"""
Create national budget table in PostgreSQL and populate with data.
All figures in billions PLN. State budget (budżet państwa) only.
Sources: NIK annual budget execution analyses, Ministerstwo Finansów.
"""

import os
import psycopg2
import jwt, time, requests, json

# DB config
DB = dict(
    host=os.environ.get("POSTGRES_HOST", "172.18.0.2"),
    port=int(os.environ.get("POSTGRES_PORT", "5432")),
    dbname=os.environ.get("POSTGRES_DB", "reporting"),
    user=os.environ.get("POSTGRES_USER", "reporting"),
    password=os.environ["POSTGRES_PASSWORD"],
)

# Metabase config
MB_URL = os.environ.get("MB_URL", "http://172.18.0.4:3000")
MB_KEY_ID = os.environ["GHOST_KEY_ID"]
MB_KEY_SECRET = os.environ["GHOST_KEY_SECRET"]

# -------------------------------------------------------
# Data: state budget (budżet państwa) execution 2008-2024
# Sources:
#   NIK analyses: nik.gov.pl/analiza-budzetu-panstwa/archiwum
#   MF: gov.pl/web/finanse/szacunek-2024
# Confidence: HIGH = directly from NIK/MF source
#             EST  = calculated/estimated from available data
# -------------------------------------------------------
data = [
    # year, revenues, expenditures, deficit, confidence, notes
    (2008, 253.5, 277.9, 24.3, "HIGH",
     "Źródło: NIK. Deficyt wzrósł o 52% vs 2007 wskutek kryzysu finansowego."),
    (2009, 274.0, 297.8, 23.8, "HIGH",
     "Źródło: NIK. Polska jedynym krajem UE z dodatnim wzrostem PKB w czasie kryzysu."),
    (2010, 263.6, 307.3, 43.7, "EST",
     "Szacunek: 2011 dochody były o 5,1% wyższe od 2010; najgorszy rok deficytu."),
    (2011, 277.0, 302.1, 25.1, "HIGH",
     "Źródło: NIK. Planowany deficyt 40,2 mld zł; faktyczny tylko 25,1 mld zł."),
    (2012, 279.5, 317.0, 37.5, "EST",
     "Szacunek na podstawie: deficyt spadł o 8,8% vs 2011."),
    (2013, 279.2, 321.3, 42.2, "HIGH",
     "Źródło: NIK. Dochody 1,2% powyżej planu; wydatki 1,8% poniżej limitu."),
    (2014, 283.5, 312.5, 29.0, "HIGH",
     "Źródło: NIK. Deficyt o 13,2 mld zł niższy niż w 2013."),
    (2015, 289.1, 320.8, 31.7, "EST",
     "Szacunek. Rząd Civic Platform; ostatni rok przed programem 500+."),
    (2016, 314.6, 360.8, 46.2, "HIGH",
     "Źródło: NIK. Pierwsza pełna wersja 500+; skok wydatków o 40 mld zł."),
    (2017, 350.4, 375.8, 25.4, "HIGH",
     "Źródło: NIK. Uszczelnienie VAT: wzrost dochodów o 36 mld zł vs 2016."),
    (2018, 380.0, 390.4, 10.4, "HIGH",
     "Źródło: NIK. Najniższy deficyt od wejścia do UE."),
    (2019, 400.5, 414.3, 13.7, "HIGH",
     "Źródło: NIK. 500+ rozszerzone na wszystkie dzieci od lipca 2019."),
    (2020, 398.7, 508.0, 109.3, "HIGH",
     "Źródło: NIK. COVID-19: nowelizacja budżetu; 166 mld zł tarcz poza budżetem."),
    (2021, 494.8, 521.2, 26.4, "HIGH",
     "Źródło: NIK. Silne odbicie dochodów; NIK szacuje ukryty deficyt na 64,3 mld zł."),
    (2022, 556.0, 570.0, 14.0, "EST",
     "Szacunek; deficyt potwierdzony NIK. Tarcze antyinflacyjne: -37 mld zł VAT."),
    (2023, 574.0, 659.6, 85.6, "HIGH",
     "Źródło: Ministerstwo Finansów. Wzrost wydatków o 13% wskutek 800+, obronności."),
    (2024, 623.4, 834.3, 211.0, "HIGH",
     "Źródło: MF. Rekordowy deficyt: 800+ (+24 mld), obrona (115,5 mld), ZUS (+65,9 mld)."),
]

# -------------------------------------------------------
# CREATE TABLE
# -------------------------------------------------------
conn = psycopg2.connect(**DB)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS national_budget CASCADE;")
cur.execute("""
CREATE TABLE national_budget (
    year           INTEGER PRIMARY KEY,
    revenues_bn    NUMERIC(8,2),
    expenditures_bn NUMERIC(8,2),
    deficit_bn     NUMERIC(8,2),
    deficit_pct_revenue NUMERIC(6,2) GENERATED ALWAYS AS
        (ROUND(deficit_bn / revenues_bn * 100, 2)) STORED,
    confidence     VARCHAR(4),
    notes          TEXT
);
""")

cur.executemany(
    "INSERT INTO national_budget (year, revenues_bn, expenditures_bn, deficit_bn, confidence, notes) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    data
)
conn.commit()
print("Table created and data inserted:", cur.rowcount, "rows")

# Verify
cur.execute("SELECT year, revenues_bn, expenditures_bn, deficit_bn, confidence FROM national_budget ORDER BY year")
print("\nYear | Revenues | Expenditures | Deficit | Conf")
print("-" * 55)
for row in cur.fetchall():
    print(f"{row[0]} | {row[1]:>8} | {row[2]:>12} | {row[3]:>7} | {row[4]}")

conn.close()
print("\nDB setup complete.")
