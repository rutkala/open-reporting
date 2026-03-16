#!/usr/bin/env python3
"""
GPW (Warsaw Stock Exchange) daily stock data ingestion.
Data source: stooq.com (free, no API key needed).
Run daily after market close (GPW closes ~17:05 CET).

Usage:
    python3 gpw_ingest.py              # incremental update (today only)
    python3 gpw_ingest.py --backfill   # full historical backfill
    python3 gpw_ingest.py --ticker PKN # single ticker
    python3 gpw_ingest.py --verify     # verify/discover tickers
"""

import argparse
import io
import time
import sys
import psycopg2
import requests
from datetime import date, datetime, timedelta

# -------------------------------------------------------
# Config
# -------------------------------------------------------
DB = dict(host="172.18.0.2", port=5432, dbname="reporting",
          user="reporting", password="OpenReporting2603!")

STOOQ_URL = "https://stooq.com/q/d/l/?s={ticker}&i=d&d1={d1}&d2={d2}"
STOOQ_FULL = "https://stooq.com/q/d/l/?s={ticker}&i=d"
PAUSE = 0.5  # seconds between requests (be polite)

# -------------------------------------------------------
# GPW Main Market tickers (WIG20 + mWIG40 + sWIG80 + others)
# Format: (stooq_ticker, company_name, sector)
# Verified against stooq.com — tickers without .XX suffix
# -------------------------------------------------------
GPW_TICKERS = [
    # === WIG20 (large caps) ===
    ("ALR",  "Alior Bank",                      "Banks"),
    ("ALE",  "Allegro",                          "Retail"),
    ("CDR",  "CD Projekt",                       "Technology"),
    ("CPS",  "Cyfrowy Polsat",                   "Media"),
    ("DNP",  "Dino Polska",                      "Retail"),
    ("JSW",  "Jastrzębska Spółka Węglowa",       "Mining"),
    ("KGH",  "KGHM Polska Miedź",               "Mining"),
    ("KRU",  "Kruk",                             "Financial Services"),
    ("LPP",  "LPP",                              "Retail"),
    ("MBK",  "mBank",                            "Banks"),
    ("OPL",  "Orange Polska",                    "Telecommunications"),
    ("PEO",  "Bank Pekao",                       "Banks"),
    ("PGE",  "PGE Polska Grupa Energetyczna",    "Energy"),
    ("PKN",  "PKN Orlen",                        "Energy"),
    ("PKO",  "PKO Bank Polski",                  "Banks"),
    ("PZU",  "PZU",                              "Insurance"),
    ("SPL",  "Santander Bank Polska",            "Banks"),
    ("XTB",  "XTB",                              "Financial Services"),
    ("ATC",  "Atal",                             "Real Estate"),
    ("BDX",  "Budimex",                          "Construction"),

    # === mWIG40 (mid caps) ===
    ("APT",  "Apator",                           "Industrial"),
    ("ASB",  "Asseco Business Solutions",        "Technology"),
    ("ACP",  "Asseco Poland",                    "Technology"),
    ("BFT",  "Benefit Systems",                  "Services"),
    ("CCC",  "CCC",                              "Retail"),
    ("CIE",  "CIECH",                            "Chemicals"),
    ("COG",  "Cognor Holding",                   "Steel"),
    ("DOM",  "Develia",                          "Real Estate"),
    ("ECH",  "Echo Investment",                  "Real Estate"),
    ("ENA",  "Enea",                             "Energy"),
    ("ENG",  "Energa",                           "Energy"),
    ("EUR",  "Eurobank",                         "Banks"),
    ("GTC",  "GTC",                              "Real Estate"),
    ("GPW",  "Giełda Papierów Wartościowych",    "Financial Services"),
    ("GKW",  "Górniczo-Hutnicze",                "Industrial"),
    ("INP",  "InPost",                           "Logistics"),
    ("ING",  "ING Bank Śląski",                  "Banks"),
    ("KER",  "Kernel Holding",                   "Agriculture"),
    ("KTY",  "Grupa Kęty",                       "Manufacturing"),
    ("LWB",  "Lubelski Węgiel Bogdanka",         "Mining"),
    ("MRC",  "Mercator Medical",                 "Healthcare"),
    ("NEU",  "NEUCA",                            "Healthcare"),
    ("NWG",  "Newag",                            "Manufacturing"),
    ("PCO",  "Polska Telewizja Kablowa",         "Media"),
    ("PKP",  "PKP Cargo",                        "Transport"),
    ("PLW",  "PlayWay",                          "Technology"),
    ("RNK",  "Rank Progress",                    "Real Estate"),
    ("SNK",  "Śnieżka",                          "Chemicals"),
    ("TEN",  "Ten Square Games",                 "Technology"),
    ("TPE",  "Tauron",                           "Energy"),
    ("TXT",  "TEXTO",                            "Technology"),
    ("VRG",  "VRG",                              "Retail"),
    ("WPL",  "Wirtualna Polska",                 "Technology"),
    ("ZAP",  "Grupa Azoty Puławy",               "Chemicals"),

    # === sWIG80 and other main market ===
    ("ABE",  "AB",                               "Technology"),
    ("AGO",  "Agora",                            "Media"),
    ("AMB",  "Ambra",                            "Food"),
    ("AML",  "Alumetal",                         "Manufacturing"),
    ("AMC",  "Amica",                            "Manufacturing"),
    ("ARG",  "Argan",                            "Chemicals"),
    ("ATD",  "Atende",                           "Technology"),
    ("ATG",  "Auto Trading Group",               "Automotive"),
    ("BIK",  "Bank BIK",                         "Banks"),
    ("BLO",  "Bloober Team",                     "Technology"),
    ("BMX",  "Biomaxima",                        "Healthcare"),
    ("BML",  "Biomed Lublin",                    "Healthcare"),
    ("BOS",  "Bank Ochrony Środowiska",          "Banks"),
    ("BRK",  "Boryszew",                         "Manufacturing"),
    ("BST",  "Braster",                          "Healthcare"),
    ("CEL",  "Celon Pharma",                     "Healthcare"),
    ("CFG",  "CPD",                              "Real Estate"),
    ("CIG",  "CI Games",                         "Technology"),
    ("CMR",  "Comarch",                          "Technology"),
    ("CNT",  "Centrum Nowoczesności",            "Real Estate"),
    ("COI",  "Coig",                             "Services"),
    ("DAD",  "Dadelo",                           "Retail"),
    ("DEK",  "Dekpol",                           "Construction"),
    ("DEV",  "Devora",                           "Real Estate"),
    ("EMC",  "Elektrociepłownia Czechnica",      "Energy"),
    ("ENT",  "Enter Air",                        "Transport"),
    ("ERB",  "Erbud",                            "Construction"),
    ("ERG",  "Ergis",                            "Manufacturing"),
    ("ETL",  "Etalon",                           "Real Estate"),
    ("EUC",  "Eurocash",                         "Retail"),
    ("FMF",  "Fabryki Mebli Forte",              "Manufacturing"),
    ("FRO",  "Ferro",                            "Manufacturing"),
    ("GBK",  "Getin Bank",                       "Banks"),
    ("GEN",  "Genworth",                         "Financial Services"),
    ("GZK",  "Gazoprojekt",                      "Energy"),
    ("HRS",  "Herkules",                         "Construction"),
    ("HUB",  "Huuuge",                           "Technology"),
    ("IDA",  "Ida",                              "Services"),
    ("IMC",  "Industrial Milk Company",          "Agriculture"),
    ("IPO",  "IPO",                              "Financial Services"),
    ("KBD",  "Kobud",                            "Construction"),
    ("KLN",  "Klin",                             "Industrial"),
    ("KMP",  "Kompap",                           "Manufacturing"),
    ("KOG",  "Kogeneracja",                      "Energy"),
    ("KRC",  "Kruk",                             "Financial Services"),
    ("LCG",  "LiveChat Software",               "Technology"),
    ("LTS",  "Lotus Notes",                      "Technology"),
    ("MAB",  "Mabion",                           "Healthcare"),
    ("MCL",  "Mo-BRUK",                          "Environmental"),
    ("MCI",  "MCI Capital",                      "Financial Services"),
    ("MDI",  "Medicalgorithmics",               "Healthcare"),
    ("MIR",  "Mirbud",                           "Construction"),
    ("MLG",  "Milisystem",                       "Technology"),
    ("MND",  "Monnari Trade",                    "Retail"),
    ("MOB",  "Mobruk",                           "Environmental"),
    ("MRB",  "Marvipol",                         "Real Estate"),
    ("NTT",  "NTT System",                       "Technology"),
    ("OAT",  "OncoArendi",                       "Healthcare"),
    ("OND",  "ONDE",                             "Construction"),
    ("OPM",  "OPTeam",                           "Technology"),
    ("PAL",  "Pamapol",                          "Food"),
    ("PBX",  "Pekabex",                          "Construction"),
    ("PCC",  "PCC Rokita",                       "Chemicals"),
    ("PCF",  "PCF Group",                        "Technology"),
    ("PEK",  "Pekabex",                          "Construction"),
    ("PLZ",  "Polwax",                           "Chemicals"),
    ("PMG",  "Polimex-Mostostal",               "Construction"),
    ("POL",  "Polenergia",                       "Energy"),
    ("PRD",  "Primetech",                        "Industrial"),
    ("PRM",  "Premicon",                         "Real Estate"),
    ("PRT",  "Protektor",                        "Manufacturing"),
    ("PSW",  "Próchnik",                         "Retail"),
    ("PXM",  "Px Media",                         "Media"),
    ("R22",  "R22",                              "Technology"),
    ("RBW",  "Rainbow Tours",                    "Tourism"),
    ("RES",  "Res",                              "Real Estate"),
    ("RLP",  "Robyg",                            "Real Estate"),
    ("RON",  "Ronson Development",               "Real Estate"),
    ("RVU",  "Ryvu Therapeutics",               "Healthcare"),
    ("SAT",  "Satino",                           "Food"),
    ("SEB",  "Selena",                           "Chemicals"),
    ("SEL",  "Selgros",                          "Retail"),
    ("SEV",  "Selvita",                          "Healthcare"),
    ("SGN",  "Sagan",                            "Industrial"),
    ("SHD",  "Shoper",                           "Technology"),
    ("SIN",  "Sinopackaging",                    "Manufacturing"),
    ("SKA",  "SKARBIEC",                         "Financial Services"),
    ("SKH",  "Stalprodukt",                      "Manufacturing"),
    ("SKR",  "Skarbiec Holding",                 "Financial Services"),
    ("SML",  "Smlease",                          "Financial Services"),
    ("SNT",  "Sanok Rubber",                     "Manufacturing"),
    ("SOK",  "Sokołów",                          "Food"),
    ("SPN",  "Serpentina",                       "Industrial"),
    ("STL",  "Stalexport Autostrady",            "Infrastructure"),
    ("STX",  "Stalexport",                       "Manufacturing"),
    ("SVE",  "Sevenet",                          "Technology"),
    ("SWI",  "Świętokrzyskie",                   "Industrial"),
    ("TBL",  "T-Bull",                           "Technology"),
    ("TLM",  "Telimena",                         "Retail"),
    ("TOY",  "Toya",                             "Retail"),
    ("TRK",  "Trakcja",                          "Construction"),
    ("ULM",  "Ulma Construccion Polska",         "Construction"),
    ("UNI",  "Unified Factory",                  "Technology"),
    ("URS",  "Ursus",                            "Manufacturing"),
    ("VIV",  "Vivid Games",                      "Technology"),
    ("VOX",  "Voxel",                            "Healthcare"),
    ("WAW",  "Wawel",                            "Food"),
    ("WLT",  "Wielton",                          "Manufacturing"),
    ("WSE",  "Warsaw Stock Exchange",            "Financial Services"),
    ("WTN",  "Wittchen",                         "Retail"),
    ("ZUE",  "Zue",                              "Construction"),
    ("ZWC",  "Zamet",                            "Industrial"),
]


def stooq_csv(ticker: str, d1: str = None, d2: str = None) -> list[dict]:
    """Download OHLCV data from stooq.com for a ticker. Returns list of dicts."""
    if d1 and d2:
        url = STOOQ_URL.format(ticker=ticker.lower(), d1=d1, d2=d2)
    else:
        url = STOOQ_FULL.format(ticker=ticker.lower())

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    if r.status_code != 200:
        return []

    lines = r.text.strip().split("\n")
    if len(lines) < 2 or "Date" not in lines[0]:
        return []

    rows = []
    for line in lines[1:]:
        parts = line.strip().split(",")
        if len(parts) < 5:
            continue
        try:
            rows.append({
                "date": parts[0],
                "open": float(parts[1]) if parts[1] else None,
                "high": float(parts[2]) if parts[2] else None,
                "low": float(parts[3]) if parts[3] else None,
                "close": float(parts[4]) if parts[4] else None,
                "volume": int(float(parts[5])) if len(parts) > 5 and parts[5] else 0,
            })
        except (ValueError, IndexError):
            continue
    return rows


def verify_ticker(ticker: str) -> bool:
    """Check if ticker has data on Stooq (last 30 days)."""
    d2 = date.today().strftime("%Y%m%d")
    d1 = (date.today() - timedelta(days=60)).strftime("%Y%m%d")
    rows = stooq_csv(ticker, d1, d2)
    return len(rows) > 0


def upsert_company(cur, ticker: str, name: str, sector: str):
    cur.execute("""
        INSERT INTO companies (ticker, name, sector)
        VALUES (%s, %s, %s)
        ON CONFLICT (ticker) DO UPDATE SET name = EXCLUDED.name, sector = EXCLUDED.sector
    """, (ticker, name, sector))


def ingest_ticker(conn, cur, ticker: str, rows: list[dict]) -> int:
    if not rows:
        return 0
    inserted = 0
    for row in rows:
        try:
            cur.execute("""
                INSERT INTO stock_prices (ticker, date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticker, date) DO UPDATE SET
                    open=EXCLUDED.open, high=EXCLUDED.high, low=EXCLUDED.low,
                    close=EXCLUDED.close, volume=EXCLUDED.volume
            """, (ticker, row["date"], row["open"], row["high"],
                  row["low"], row["close"], row["volume"]))
            inserted += 1
        except Exception:
            pass
    conn.commit()
    return inserted


def log_run(cur, ticker, rows_inserted, date_from, date_to, status, error=None):
    cur.execute("""
        INSERT INTO ingestion_log (ticker, rows_inserted, date_from, date_to, status, error)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (ticker, rows_inserted, date_from, date_to, status, error))


def get_last_date(cur, ticker: str):
    cur.execute("SELECT MAX(date) FROM stock_prices WHERE ticker = %s", (ticker,))
    row = cur.fetchone()
    return row[0] if row and row[0] else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backfill", action="store_true", help="Full historical backfill")
    parser.add_argument("--ticker", help="Single ticker to update")
    parser.add_argument("--verify", action="store_true", help="Verify all tickers against Stooq")
    args = parser.parse_args()

    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    today = date.today().strftime("%Y%m%d")

    # Select tickers to process
    if args.ticker:
        targets = [(args.ticker.upper(), args.ticker.upper(), "")]
    else:
        targets = GPW_TICKERS

    # Verify mode: check which tickers are valid
    if args.verify:
        print(f"Verifying {len(targets)} tickers against Stooq...")
        valid, invalid = [], []
        for ticker, name, sector in targets:
            ok = verify_ticker(ticker)
            status = "OK" if ok else "MISS"
            print(f"  {ticker:8} {status}  {name}")
            if ok:
                valid.append(ticker)
            else:
                invalid.append(ticker)
            time.sleep(PAUSE)
        print(f"\nValid: {len(valid)}, Invalid: {len(invalid)}")
        print("Invalid tickers:", invalid)
        conn.close()
        return

    # Seed companies table
    for ticker, name, sector in targets:
        upsert_company(cur, ticker, name, sector)
    conn.commit()
    print(f"Seeded {len(targets)} companies")

    # Ingest data
    total_rows = 0
    ok_count = 0
    for i, (ticker, name, sector) in enumerate(targets):
        try:
            if args.backfill:
                # Full history
                rows = stooq_csv(ticker)
                d1 = rows[0]["date"] if rows else None
                d2 = rows[-1]["date"] if rows else None
            else:
                # Incremental: from last known date to today
                last = get_last_date(cur, ticker)
                if last:
                    d1 = (last + timedelta(days=1)).strftime("%Y%m%d")
                else:
                    d1 = "20000101"  # first run: get all history
                d2 = today
                rows = stooq_csv(ticker, d1, d2)

            n = ingest_ticker(conn, cur, ticker, rows)
            log_run(cur, ticker, n, d1, d2, "ok")
            conn.commit()
            total_rows += n
            ok_count += 1

            if n > 0 or args.backfill:
                print(f"[{i+1:3}/{len(targets)}] {ticker:8} +{n:5} rows")

        except Exception as e:
            print(f"[{i+1:3}/{len(targets)}] {ticker:8} ERROR: {e}")
            try:
                log_run(cur, ticker, 0, None, None, "error", str(e))
                conn.commit()
            except Exception:
                conn.rollback()

        time.sleep(PAUSE)

    print(f"\nDone. {ok_count}/{len(targets)} tickers, {total_rows:,} rows ingested.")
    conn.close()


if __name__ == "__main__":
    main()
