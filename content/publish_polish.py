import os
import jwt
import time
import requests
import json
import sqlite3

# Ghost Admin API key
KEY_ID = os.environ["GHOST_KEY_ID"]
KEY_SECRET = os.environ["GHOST_KEY_SECRET"]
POST_ID = "69b7166df257cc00016fc701"
GHOST_URL = "http://172.18.0.3:2368"

# Build JWT
iat = int(time.time())
header = {"alg": "HS256", "typ": "JWT", "kid": KEY_ID}
payload = {"iat": iat, "exp": iat + 300, "aud": "/admin/"}
token = jwt.encode(payload, bytes.fromhex(KEY_SECRET), algorithm="HS256", headers=header)

headers = {"Authorization": f"Ghost {token}", "Content-Type": "application/json"}

# Polish title
POLISH_TITLE = "Budżety polskich województw 1999–2024: Od chronicznego deficytu do strukturalnej nadwyżki"

# Polish lexical content
lexical = {
  "root": {
    "children": [
      {
        "children": [
          {"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "W latach 1999–2024 łączne budżety 16 polskich województw wzrosły niemal ", "type": "extended-text", "version": 1},
          {"detail": 0, "format": 1, "mode": "normal", "style": "", "text": "jedenastokrotnie", "type": "extended-text", "version": 1},
          {"detail": 0, "format": 0, "mode": "normal", "style": "", "text": " — z 3,3 mld zł do 35,7 mld zł. Za tą liczbą kryje się bardziej złożona historia: napływ środków po akcesji do UE, dekada chronicznego deficytu, reforma podatkowa motywowana politycznie oraz cicha, lecz istotna zmiana strukturalna w kierunku nadwyżki budżetowej. Artykuł przedstawia pełny obraz 25 lat na podstawie oficjalnych danych GUS BDL.", "type": "extended-text", "version": 1}
        ],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Kontekst: czym są budżety województw?", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Polska podzielona jest na 16 województw — najwyższy szczebel regionalnego samorządu terytorialnego, odpowiadający regionom NUTS-2 w klasyfikacji statystycznej UE. Każde województwo zarządza własnym budżetem finansowanym z udziałów w krajowych podatkach dochodowych, subwencji ogólnej z budżetu centralnego, współfinansowania unijnego oraz dochodów własnych.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Z budżetów tych finansowane są drogi regionalne, szpitale, instytucje kultury, a przede wszystkim programy inwestycyjne współfinansowane ze środków UE. Analiza finansów województw jest zatem dobrym wskaźnikiem tego, jak Polska inwestuje w siebie na poziomie regionalnym.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Trzy epoki polskich finansów regionalnych", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Dane z 25 lat układają się w trzy wyraźne okresy, każdy zdominowany przez inne siły makroekonomiczne lub polityczne.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Okres 1 (1999–2008): stabilny wzrost, zrównoważone budżety", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h3"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Pierwsza dekada po utworzeniu nowoczesnego systemu samorządu województw przyniosła stabilny, przewidywalny wzrost. Dochody wzrosły z 3,3 mld do 12,7 mld zł — napędzane silnym wzrostem PKB w Polsce przed kryzysem i pierwszym napływem unijnych funduszy strukturalnych po akcesji w 2004 r. Budżety były zasadniczo zrównoważone: ani duże nadwyżki, ani duże deficyty nie charakteryzowały tego okresu.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Okres 2 (2009–2015): dekada deficytu", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h3"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Dane z 2009 r. ujawniają uderzającą anomalię: dochody skoczyły do 19,5 mld zł w ciągu jednego roku — wzrost o ponad 50% — po czym runęły do 14,1 mld w 2010 r. To statystyczny ślad nierównomiernego napływu środków unijnych z perspektywy 2007–2013 na rachunki regionalne, spotęgowany przez globalny kryzys finansowy zaburzający poziom bazowy.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Wydatki jednak nie spadły równolegle. Województwa zobowiązały się do wieloletnich programów inwestycyjnych i nie mogły po prostu z dnia na dzień ciąć kosztów. Efektem był chroniczny deficyt: wydatki przewyższały dochody w każdym roku od 2009 do 2014, a w najgorszym roku (2011) łączny niedobór dla wszystkich regionów wyniósł 1,27 mld zł.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Okres 3 (2016–2024): strukturalna nadwyżka", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h3"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Po 2015 r. coś się zmieniło. Od 2016 r. dochody konsekwentnie rosły szybciej niż wydatki. Początkowo skromna nadwyżka stała się strukturalna około 2020–2021 r., a wynik za 2024 r. wynoszący +2,55 mld zł przy dochodach 35,7 mld zł to najlepszy rezultat w całym zbiorze danych. Skok dochodów w latach 2023–2024 odzwierciedla efekty redystrybucyjne Polskiego Ładu — reformy podatkowej, która istotnie zwiększyła udział podatku dochodowego od osób fizycznych trafiający do samorządów regionalnych.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Ogólnopolski trend budżetowy 1999–2024", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Łączne dochody i wydatki wszystkich 16 województw w miliardach PLN.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Geografia siły fiskalnej", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "W 2024 r. samo Mazowieckie zebrało 6,76 mld zł — niemal dwukrotnie więcej niż drugi region (Śląskie z 3,29 mld zł). Województwo warszawskie odpowiada za około 19% wszystkich dochodów województw w Polsce, choć zamieszkuje je ok. 14% ludności. Ta koncentracja odzwierciedla geografię ekonomiczną: Mazowieckie jest siedzibą stolicy, central większości dużych polskich korporacji i nieproporcjonalnie dużego udziału osób o wysokich dochodach.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Dochody według województw w 2024 r.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Łączne dochody według województwa w 2024 r., posortowane malejąco.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Kto osiąga nadwyżki, kto deficyty", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Jedną z najbardziej analitycznie interesujących cech zbioru danych jest to, że salda budżetów województw poruszają się w dużej mierze synchronicznie — ogólnopolskie cykle polityki dominują nad regionalnym zróżnicowaniem. W 2024 r. deficyt odnotowały tylko dwa regiony: Mazowieckie (−0,08 mld zł) i Lubuskie (−0,08 mld zł). Najsilniejsze nadwyżki w stosunku do wielkości budżetu osiągnęły Dolnośląskie, Małopolskie i Wielkopolskie — trzy najbardziej dynamiczne regionalne gospodarki poza Warszawą.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Saldo budżetowe według województw 1999–2024", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Roczne saldo budżetowe według województwa. Wartości ujemne oznaczają lata deficytu.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Na co zwrócić uwagę w kolejnych latach", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Warto śledzić kilka dynamik. Po pierwsze, wzrost dochodów z Polskiego Ładu to jednorazowa zmiana strukturalna — gdy zostanie wchłonięta, czy wzrost dochodów wróci do tempa sprzed 2022 r.? Po drugie, nowa perspektywa unijna 2021–2027 weszła w pełną fazę wypłat, co historycznie napędzało wydatki deficytowe, gdy regiony współfinansowały projekty inwestycyjne. Po trzecie, presja demograficzna — szczególnie w województwach wschodnich — będzie w coraz większym stopniu obciążać stronę wydatkową.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Metodologia", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"
      },
      {
        "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Wszystkie dane pochodzą z API Banku Danych Lokalnych GUS (BDL). Zmienne: 6454 (dochody ogółem) i 6476 (wydatki ogółem), poziom NUTS-2 według województw, lata 1999–2024. Saldo budżetowe obliczono jako dochody minus wydatki. Wszystkie kwoty w nominalnych złotych. Pełny interaktywny dashboard: portal.open-reporting.dev.", "type": "extended-text", "version": 1}],
        "direction": None, "format": "", "indent": 0, "type": "paragraph", "version": 1
      }
    ],
    "direction": None,
    "format": "",
    "indent": 0,
    "type": "root",
    "version": 1
  }
}

# Get current updated_at for optimistic locking
resp = requests.get(
    f"{GHOST_URL}/ghost/api/admin/posts/{POST_ID}/",
    headers=headers
)
current = resp.json()["posts"][0]
updated_at = current["updated_at"]

# Update the post
payload = {
    "posts": [{
        "title": POLISH_TITLE,
        "lexical": json.dumps(lexical),
        "updated_at": updated_at,
        "status": "published"
    }]
}

resp = requests.put(
    f"{GHOST_URL}/ghost/api/admin/posts/{POST_ID}/",
    headers=headers,
    json=payload
)

print("Status:", resp.status_code)
if resp.status_code == 200:
    print("SUCCESS — post updated in Polish")
else:
    print(resp.text[:500])
