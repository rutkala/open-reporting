#!/usr/bin/env python3
"""Insert national budget article into Ghost SQLite DB."""

import sqlite3, json, time, uuid

CHART1_URL = "https://portal.open-reporting.dev/public/question/3fdcad31-bf71-4540-999d-d83353f88a50"
CHART2_URL = "https://portal.open-reporting.dev/public/question/6a5d6a55-4e6d-4543-9664-b2c67dcfb4e8"
CHART3_URL = "https://portal.open-reporting.dev/public/question/96a6936e-2c1e-4d8f-a90b-167a83afe09f"

TITLE = "Budżet państwa 2008–2024: Od kryzysu przez konsolidację do rekordowego deficytu"
SLUG = "budzet-panstwa-2008-2024"

def txt(text, fmt=0):
    return {"detail": 0, "format": fmt, "mode": "normal", "style": "", "text": text, "type": "extended-text", "version": 1}

def para(*nodes):
    return {"children": list(nodes), "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1}

def heading(text, tag="h2"):
    return {"children": [txt(text)], "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": tag}

def embed(url, caption=""):
    iframe = f'<iframe src="{url}" frameborder="0" width="800" height="600" allowtransparency></iframe>'
    return {
        "type": "embed",
        "version": 1,
        "url": url,
        "embedType": "html",
        "html": iframe,
        "metadata": {},
        "caption": caption
    }

lexical_data = {
    "root": {
        "children": [
            para(
                txt("W latach 2008–2024 budżet centralny Polski przeszedł trzy wyraźne etapy: chroniczny deficyt w cieniu kryzysu finansowego i polityki socjalnej, krótki epizod konsolidacji fiskalnej napędzanej uszczelnieniem VAT, a wreszcie bezprecedensową ekspansję wydatkową. Rekordowy deficyt "),
                txt("211 mld zł", 1),
                txt(" odnotowany w 2024 r. — równy 33,9% rocznych dochodów — to najwyższa wartość w całej analizowanej historii. Artykuł przedstawia pełny obraz na podstawie danych Najwyższej Izby Kontroli (NIK) i Ministerstwa Finansów.")
            ),
            heading("Czym jest budżet państwa?"),
            para(txt("Budżet państwa to plan finansowy obejmujący dochody i wydatki organów centralnych — rządu, ministerstw i agencji rządowych. Nie należy go mylić z sektorem finansów publicznych, który obejmuje dodatkowo samorządy, ZUS, NFZ i fundusze celowe. Budżet państwa to węższe, lecz kluczowe pojęcie: odzwierciedla bezpośrednie decyzje rządu o priorytetach wydatkowych i metodach finansowania.")),
            para(txt("Dochody budżetu pochodzą głównie z podatku VAT, podatku dochodowego od osób fizycznych (PIT) i prawnych (CIT) oraz akcyzy. Wydatki obejmują obsługę długu, transfery do ZUS i KRUS, subwencje dla samorządów, obronę narodową, wydatki na administrację i programy społeczne.")),
            heading("Trzy epoki budżetu centralnego"),
            para(txt("Dane z 17 lat układają się w trzy wyraźne okresy, każdy zdominowany przez inne siły makroekonomiczne lub polityczne decyzje.")),
            heading("Epoka 1 (2008–2015): Kryzys i chroniczny deficyt", "h3"),
            para(txt("Globalny kryzys finansowy 2008–2009 uderzył w polskie dochody podatkowe, choć Polska jako jedyna w UE uniknęła recesji. Deficyt w 2008 r. wyniósł 24,3 mld zł i zaledwie nieznacznie zmalał rok później. Najgorszym rokiem był 2010: szacowany deficyt sięgnął 43,7 mld zł (16,6% dochodów), gdy wydatki na infrastrukturę współfinansowaną ze środków UE rosły, a dochody podatkowe pozostawały słabe.")),
            para(txt("W latach 2011–2015 rząd PO–PSL próbował konsolidacji — deficyt wahał się między 25 a 42 mld zł, lecz nigdy nie udało się go trwale ograniczyć. Wydatki socjalne, rosnące koszty obsługi długu i słaby wzrost dochodów podatkowych blokowały powrót do równowagi. W tym czasie Polska wielokrotnie przekraczała unijną procedurę nadmiernego deficytu (>3% PKB).")),
            heading("Epoka 2 (2016–2019): Konsolidacja fiskalna i program 500+", "h3"),
            para(
                txt("Rok 2016 przyniósł paradoks: rząd PiS uruchomił program "),
                txt("500+", 1),
                txt(" (świadczenie wychowawcze 500 zł miesięcznie na dziecko), a wydatki wzrosły o ponad 40 mld zł. Mimo to deficyt wyniósł 46,2 mld zł — wysoko, lecz poniżej obawianych katastroficznych poziomów.")
            ),
            para(
                txt("Kluczowym czynnikiem okazało się "),
                txt("uszczelnienie systemu VAT", 1),
                txt(": wdrożenie JPK (Jednolity Plik Kontrolny), split payment i mechanizmy odwrotnego obciążenia przyniosły w 2017 r. dodatkowe 36 mld zł wpływów podatkowych. Rok 2017 zamknął się deficytem zaledwie 25,4 mld zł, a 2018 — "),
                txt("10,4 mld zł", 1),
                txt(", najniższym wynikiem od wejścia Polski do UE. W 2019 r. rozszerzono 500+ na pierwsze dziecko, co podniosło deficyt do 13,7 mld zł — wciąż historycznie niski poziom.")
            ),
            heading("Epoka 3 (2020–2024): Ekspansja i rekordowe deficyty", "h3"),
            para(
                txt("Pandemia COVID-19 wywróciła całą logikę fiskalną: deficyt 2020 r. wyniósł "),
                txt("109,3 mld zł", 1),
                txt(" (27,4% dochodów). Nie oddaje to pełnej skali interwencji — rząd przeniósł część wydatków pandemicznych do Funduszu Przeciwdziałania COVID-19, poza budżetem, co NIK skrytykowała jako omijanie reguły wydatkowej.")
            ),
            para(txt("Lata 2021–2022 przyniosły silne odbicie dochodów podatkowych (inflacja i wzrost PKB pchały wpływy w górę), co obniżyło deficyt do odpowiednio 26,4 i 14 mld zł. Jednak od 2023 r. wydatki znów zaczęły rosnąć wykładniczo: program 800+, bezprecedensowy wzrost wydatków obronnych oraz dopłaty do ZUS. Deficyt 2023 r. osiągnął 85,6 mld zł, a 2024 — rekordowe 211 mld zł.")),
            heading("Dochody i wydatki budżetu państwa 2008–2024"),
            para(txt("Łączne dochody i wydatki budżetu centralnego w miliardach PLN.")),
            embed(CHART1_URL, "Dochody i wydatki budżetu państwa 2008–2024"),
            heading("Szok pandemiczny 2020 roku"),
            para(txt("Rok 2020 wyróżnia się jako osobna kategoria. Dochody budżetu nieznacznie spadły — z 400,5 do 398,7 mld zł — lecz wydatki skoczyły o 93,7 mld zł, do poziomu 508 mld zł. Rząd nowelizował budżet trzykrotnie w ciągu roku. Poza samym budżetem uruchomiono Fundusz Przeciwdziałania COVID-19 zasilany pożyczkami z Banku Gospodarstwa Krajowego — NIK oceniła, że realne potrzeby pożyczkowe sektora były o 64–66 mld zł wyższe niż wykazywał sam budżet.")),
            para(txt("Pandemia obnażyła słabość konstrukcyjną: Polska nie dysponowała buforem fiskalnym pozwalającym na antycykliczne wydatki bez gwałtownego wzrostu długu publicznego. Dług Skarbu Państwa wzrósł w 2020 r. o ok. 200 mld zł.")),
            heading("Uszczelnienie VAT i efekty Polskiego Ładu"),
            para(
                txt("Dwa kluczowe reformy podatkowe ukształtowały trajektorię dochodów. Po pierwsze, "),
                txt("uszczelnienie VAT w latach 2016–2018", 1),
                txt(" zwiększyło efektywność poboru podatku — tzw. luka VAT spadła z ok. 24% w 2015 r. do poniżej 10% w 2020 r. Po drugie, "),
                txt("Polski Ład (2022)", 1),
                txt(" podniósł kwotę wolną od podatku do 30 tys. zł i drugi próg podatkowy do 120 tys. zł, co początkowo obniżyło wpływy z PIT, ale jednocześnie zwiększyło udział PIT trafiający do samorządów kosztem budżetu centralnego.")
            ),
            para(txt("Efekt netto Polskiego Ładu dla budżetu centralnego był kontrowersyjny — rząd szacował neutralność fiskalną, jednak NIK w analizach wykonania budżetu za 2022 r. wskazywała na niedobory metodologiczne prognoz podatkowych.")),
            heading("Deficyt budżetu państwa 2008–2024 (mld zł)"),
            para(txt("Roczny deficyt budżetu centralnego w miliardach PLN. Wartości wyższe = większy deficyt.")),
            embed(CHART2_URL, "Deficyt budżetu państwa 2008–2024"),
            heading("Rekordowy deficyt 2024: przyczyny strukturalne"),
            para(
                txt("Deficyt "),
                txt("211 mld zł", 1),
                txt(" w 2024 r. to wynik kumulacji trzech kategorii wydatków, każda z nich strukturalna — nie jednorazowa:")
            ),
            para(
                txt("• "),
                txt("Program 800+", 1),
                txt(": podwyżka świadczenia wychowawczego z 500 do 800 zł od marca 2024 r. oznacza wzrost rocznych kosztów o ok. 24 mld zł. Świadczenie obejmuje ponad 6,7 mln dzieci.")
            ),
            para(
                txt("• "),
                txt("Wydatki obronne", 1),
                txt(": budżet MON w 2024 r. wyniósł 115,5 mld zł — 4% PKB, najwyższy wskaźnik w NATO. Skokowy wzrost wynika z ustawy o obronie ojczyzny (2022) i zamówień na uzbrojenie po inwazji Rosji na Ukrainę.")
            ),
            para(
                txt("• "),
                txt("Dopłaty do ZUS", 1),
                txt(": dotacja uzupełniająca do Funduszu Ubezpieczeń Społecznych wzrosła o 65,9 mld zł rok do roku — efekt połączenia wyższych świadczeń (waloryzacja rent i emerytur 12,12% w 2024 r.) z deficytem strukturalnym ZUS wynikającym ze zmian demograficznych.")
            ),
            para(txt("Dochody budżetu wzrosły o 49,4 mld zł (8,6% r/r) — wzrost realny, ale niewystarczający do pokrycia ekspansji wydatkowej. Ministerstwo Finansów szacowało deficyt pierwotnie na 184 mld zł — rzeczywisty wynik był o 27 mld zł wyższy.")),
            heading("Deficyt jako % dochodów 2008–2024"),
            para(txt("Deficyt budżetu jako procent dochodów — wskaźnik fiskalnej presji strukturalnej.")),
            embed(CHART3_URL, "Deficyt jako % dochodów budżetu państwa 2008–2024"),
            heading("Na co zwrócić uwagę w kolejnych latach"),
            para(txt("Kilka dynamik będzie kluczowe dla trajektorii budżetowej w perspektywie 2025–2027.")),
            para(
                txt("Po pierwsze, "),
                txt("reguła wydatkowa", 1),
                txt(": Polska stosuje stabilizującą regułę wydatkową (SRW), lecz wielokrotnie zawieszała jej działanie. Powrót do SRW od 2025 r. oznaczałby konieczność hamowania wzrostu wydatków — rząd złożył już wniosek do Komisji Europejskiej o objęcie procedurą nadmiernego deficytu.")
            ),
            para(
                txt("Po drugie, "),
                txt("koszty obsługi długu", 1),
                txt(": przy długu sektora finansów publicznych zbliżającym się do 60% PKB i stopach procentowych NBP powyżej 5%, koszty odsetkowe w budżecie 2024 r. przekroczyły 65 mld zł — i będą rosnąć.")
            ),
            para(
                txt("Po trzecie, "),
                txt("demografia i ZUS", 1),
                txt(": strukturalny deficyt FUS będzie rósł wraz ze starzeniem się społeczeństwa. Każda waloryzacja emerytur zwiększa dotację z budżetu centralnego, tworząc automatyczny stabilizator o negatywnym znaku fiskalnym.")
            ),
            heading("Metodologia i źródła"),
            para(txt("Dane o wykonaniu budżetu państwa (dochody, wydatki, deficyt) pochodzą z corocznych analiz Najwyższej Izby Kontroli (NIK) opublikowanych na nik.gov.pl/analiza-budzetu-panstwa oraz z komunikatów Ministerstwa Finansów (gov.pl/web/finanse). Dane za 2022 r. zostały oznaczone jako szacunek (EST) z uwagi na niepotwierdzone jeszcze w NIK wartości. Dane za pozostałe lata oznaczono jako HIGH confidence. Wszystkie kwoty w nominalnych miliardach złotych. Interaktywne wykresy: portal.open-reporting.dev.")),
        ],
        "direction": None,
        "format": "",
        "indent": 0,
        "type": "root",
        "version": 1
    }
}

def build_html(lexical_data):
    parts = []
    for node in lexical_data["root"]["children"]:
        ntype = node.get("type")
        if ntype == "paragraph":
            inner = ""
            for c in node.get("children", []):
                t = c.get("text", "")
                fmt = c.get("format", 0)
                if fmt == 1:
                    t = f"<strong>{t}</strong>"
                elif fmt == 2:
                    t = f"<em>{t}</em>"
                inner += t
            parts.append(f"<p>{inner}</p>")
        elif ntype == "extended-heading":
            tag = node.get("tag", "h2")
            inner = "".join(c.get("text","") for c in node.get("children",[]))
            parts.append(f"<{tag}>{inner}</{tag}>")
        elif ntype == "embed":
            url = node.get("url", "")
            cap = node.get("caption", "")
            iframe = f'<iframe src="{url}" frameborder="0" width="800" height="600" allowtransparency></iframe>'
            cap_html = f"<figcaption>{cap}</figcaption>" if cap else ""
            parts.append(f'<figure class="kg-card kg-embed-card">{iframe}{cap_html}</figure>')
    return "\n".join(parts)

html_content = build_html(lexical_data)
lexical_str = json.dumps(lexical_data)

# Generate post ID (Ghost uses hex IDs)
import secrets
post_id = secrets.token_hex(12)
now_ms = int(time.time() * 1000)

# Get author ID from DB
conn = sqlite3.connect('/tmp/ghost_nb.db')
cur = conn.cursor()

cur.execute("SELECT id FROM users LIMIT 1")
row = cur.fetchone()
author_id = row[0] if row else "1"
print(f"Author ID: {author_id}")

# Check if slug already exists
cur.execute("SELECT id FROM posts WHERE slug = ?", (SLUG,))
existing = cur.fetchone()

if existing:
    post_id = existing[0]
    print(f"Updating existing post: {post_id}")
    cur.execute("""
        UPDATE posts SET
            title = ?,
            lexical = ?,
            html = ?,
            plaintext = ?,
            status = 'published',
            updated_at = ?
        WHERE id = ?
    """, (TITLE, lexical_str, html_content, TITLE, now_ms, post_id))
else:
    print(f"Inserting new post: {post_id}")
    # Get column list
    cur.execute("PRAGMA table_info(posts)")
    cols = {r[1] for r in cur.fetchall()}
    print("Available columns:", sorted(cols))

    post_uuid = str(__import__('uuid').uuid4())
    cur.execute("""
        INSERT INTO posts (
            id, uuid, title, slug, lexical, html, plaintext,
            status, visibility, type,
            email_recipient_filter, comment_id, show_title_and_feature_image,
            created_at, updated_at, published_at,
            created_by, updated_by, published_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'published', 'public', 'post', 'all', ?, 1, ?, ?, ?, ?, ?, ?)
    """, (
        post_id, post_uuid, TITLE, SLUG, lexical_str, html_content, TITLE,
        post_id,
        now_ms, now_ms, now_ms,
        author_id, author_id, author_id
    ))
    # Insert into posts_authors
    pa_id = __import__('secrets').token_hex(12)
    cur.execute("""
        INSERT INTO posts_authors (id, post_id, author_id, sort_order)
        VALUES (?, ?, ?, 0)
    """, (pa_id, post_id, author_id))

conn.commit()
print("Committed successfully")

# Verify
cur.execute("SELECT id, title, slug, status FROM posts WHERE slug = ?", (SLUG,))
row = cur.fetchone()
print(f"Post in DB: {row}")
conn.close()
