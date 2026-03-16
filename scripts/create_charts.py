#!/usr/bin/env python3
"""Create 3 Metabase charts for national budget article."""

import jwt, time, requests, json

MB_URL = "http://172.18.0.4:3000"
KEY_ID = "69b715b8f257cc00016fc4c8"
KEY_SECRET = "2839026c1e8186efad8adf7b63aa934faa5ff0ba7f47875c7dbbb8d5b410403d"

def get_token():
    iat = int(time.time())
    payload = {"iat": iat, "exp": iat + 300, "aud": "/admin/"}
    header = {"alg": "HS256", "typ": "JWT", "kid": KEY_ID}
    return jwt.encode(payload, bytes.fromhex(KEY_SECRET), algorithm="HS256", headers=header)

def headers():
    return {"Authorization": f"Ghost {get_token()}", "Content-Type": "application/json"}

# Find the reporting database ID
r = requests.get(f"{MB_URL}/api/database", headers=headers())
databases = r.json()
db_id = None
for db in databases.get("data", databases if isinstance(databases, list) else []):
    if db.get("name") == "reporting" or db.get("dbname") == "reporting":
        db_id = db["id"]
        print(f"Found DB: {db['name']} (id={db_id})")
        break

if not db_id:
    print("Available databases:", [d.get('name') for d in (databases.get('data', databases) if isinstance(databases, dict) else databases)])
    # Try first non-metabase DB
    for db in (databases.get('data', databases) if isinstance(databases, dict) else databases):
        if 'metabase' not in db.get('name','').lower():
            db_id = db["id"]
            print(f"Using DB: {db['name']} (id={db_id})")
            break

assert db_id, "Could not find reporting database"

# Get collection to place charts in
r = requests.get(f"{MB_URL}/api/collection", headers=headers())
collections = r.json()
root_col = None
for c in (collections if isinstance(collections, list) else collections.get('data',[])):
    if c.get('personal_owner_id') is None and c.get('id') not in ('root',):
        root_col = c['id']
        break

print(f"Using collection: {root_col}")

def create_card(name, sql, display, visualization_settings, description=""):
    payload = {
        "name": name,
        "description": description,
        "display": display,
        "dataset_query": {
            "type": "native",
            "native": {"query": sql, "template-tags": {}},
            "database": db_id,
        },
        "visualization_settings": visualization_settings,
        "collection_id": root_col,
    }
    r = requests.post(f"{MB_URL}/api/card", headers=headers(), json=payload)
    if r.status_code == 200:
        card = r.json()
        # Make public
        r2 = requests.post(f"{MB_URL}/api/card/{card['id']}/public_link", headers=headers())
        uuid = r2.json().get("uuid", "")
        print(f"Created card '{name}' id={card['id']} uuid={uuid}")
        return card['id'], uuid
    else:
        print(f"ERROR creating '{name}': {r.status_code} {r.text[:200]}")
        return None, None

# -------------------------------------------------------
# Chart 1: Revenues & Expenditures Trend
# -------------------------------------------------------
sql1 = """
SELECT
    year AS "Rok",
    revenues_bn AS "Dochody (mld zł)",
    expenditures_bn AS "Wydatki (mld zł)"
FROM national_budget
ORDER BY year
"""

vis1 = {
    "graph.dimensions": ["Rok"],
    "graph.metrics": ["Dochody (mld zł)", "Wydatki (mld zł)"],
    "graph.x_axis.title_text": "Rok",
    "graph.y_axis.title_text": "mld zł",
    "graph.show_values": False,
    "series_settings": {
        "Dochody (mld zł)": {"color": "#509EE3", "display": "line"},
        "Wydatki (mld zł)": {"color": "#EF8C8C", "display": "line"},
    },
    "graph.label_value_frequency": "fit",
}

id1, uuid1 = create_card(
    "Budżet państwa: Dochody i wydatki 2008–2024",
    sql1, "line", vis1,
    "Dochody i wydatki budżetu państwa w miliardach PLN, 2008–2024"
)

# -------------------------------------------------------
# Chart 2: Budget Deficit
# -------------------------------------------------------
sql2 = """
SELECT
    year AS "Rok",
    -deficit_bn AS "Deficyt (mld zł)"
FROM national_budget
ORDER BY year
"""

vis2 = {
    "graph.dimensions": ["Rok"],
    "graph.metrics": ["Deficyt (mld zł)"],
    "graph.x_axis.title_text": "Rok",
    "graph.y_axis.title_text": "mld zł",
    "graph.show_values": True,
    "graph.label_value_frequency": "fit",
    "series_settings": {
        "Deficyt (mld zł)": {"color": "#EF8C8C", "display": "bar"},
    },
    "graph.colors": ["#EF8C8C"],
}

id2, uuid2 = create_card(
    "Budżet państwa: Deficyt 2008–2024",
    sql2, "bar", vis2,
    "Deficyt budżetu państwa w miliardach PLN (wartości ujemne = deficyt)"
)

# -------------------------------------------------------
# Chart 3: Deficit as % of revenues (fiscal pressure)
# -------------------------------------------------------
sql3 = """
SELECT
    year AS "Rok",
    ROUND(deficit_bn / revenues_bn * 100, 1) AS "Deficyt (% dochodów)",
    confidence AS "Pewność danych"
FROM national_budget
ORDER BY year
"""

vis3 = {
    "graph.dimensions": ["Rok"],
    "graph.metrics": ["Deficyt (% dochodów)"],
    "graph.x_axis.title_text": "Rok",
    "graph.y_axis.title_text": "% dochodów",
    "graph.show_values": True,
    "graph.label_value_frequency": "fit",
    "series_settings": {
        "Deficyt (% dochodów)": {"color": "#F9CF48", "display": "bar"},
    },
}

id3, uuid3 = create_card(
    "Budżet państwa: Deficyt jako % dochodów 2008–2024",
    sql3, "bar", vis3,
    "Deficyt budżetu państwa jako procent dochodów – wskaźnik presji fiskalnej"
)

print("\n=== CHART URLS ===")
base = "https://portal.open-reporting.dev/public/question/"
print(f"Chart 1 (Revenue/Expenditure): {base}{uuid1}")
print(f"Chart 2 (Deficit absolute):    {base}{uuid2}")
print(f"Chart 3 (Deficit % revenues):  {base}{uuid3}")
