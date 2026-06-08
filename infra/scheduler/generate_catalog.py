import yaml
import os

DOMAINS_FILE = "/opt/open-reporting/products/ingestion/to_landing/domains.yaml"
SOURCES_FILE = "/opt/open-reporting/products/ingestion/to_landing/sources.yaml"
MAPPING_FILE = "/opt/open-reporting/products/ingestion/to_landing/mapping.yaml"
OUTPUT_HTML = "/opt/open-reporting/infra/nginx/html/data-catalog.html"

with open(DOMAINS_FILE, "r", encoding="utf-8") as f:
    domains_data = yaml.safe_load(f).get("domains", [])
with open(SOURCES_FILE, "r", encoding="utf-8") as f:
    sources_data = yaml.safe_load(f).get("sources", [])
with open(MAPPING_FILE, "r", encoding="utf-8") as f:
    mappings_data = yaml.safe_load(f).get("mappings", [])

domain_map = {d["id"]: d for d in domains_data}
source_map = {s["id"]: s for s in sources_data}

# Build many-to-many
for d in domains_data:
    d["sources"] = []
for s in sources_data:
    s["domains"] = []

for m in mappings_data:
    d_id = m["domain_id"]
    s_id = m["source_id"]
    if d_id in domain_map and s_id in source_map:
        domain_map[d_id]["sources"].append(source_map[s_id])
        source_map[s_id]["domains"].append(domain_map[d_id])

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Open Reporting — Data Catalog</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Inter, system-ui, sans-serif; background: #1e1e2e; color: #cdd6f4; min-height: 100vh; }
    header { background: #181825; border-bottom: 1px solid #313244; padding: 20px 32px; display: flex; justify-content: space-between; align-items: center;}
    header h1 { font-size: 20px; font-weight: 700; color: #a6e3a1; }
    main { max-width: 1200px; margin: 40px auto; padding: 0 24px; }
    
    .section-title { font-size: 24px; margin-bottom: 24px; color: #f38ba8; border-bottom: 1px solid #313244; padding-bottom: 8px;}
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 24px; margin-bottom: 40px; }
    
    .card { background: #181825; border: 1px solid #313244; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .card h3 { color: #89b4fa; font-size: 18px; margin-bottom: 8px; }
    .card p { font-size: 14px; color: #bac2de; margin-bottom: 16px; line-height: 1.4; }
    
    .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 6px; margin-bottom: 6px; background: #313244; color: #cdd6f4; }
    .status-active { color: #a6e3a1; border: 1px solid #a6e3a1; }
    .status-pending { color: #f9e2af; border: 1px solid #f9e2af; }
    
    .btn { background: #89b4fa; color: #11111b; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: 600; }
  </style>
</head>
<body>
<header>
  <div>
    <h1>Data Catalog & Source Registry</h1>
    <p style="color: #bac2de; font-size: 13px; margin-top: 4px;">Relational Metadata Graph</p>
  </div>
  <div style="display: flex; gap: 12px;">
    <a href="/ingestion-status.html" class="btn">View Ingestion Status</a>
    <a href="/admin.html" class="btn">⬅ Back to Admin</a>
  </div>
</header>
<main>

  <h2 class="section-title">📂 Business Domains</h2>
  <div class="grid">
"""

for d in domains_data:
    html_content += f"""
    <div class="card">
      <h3>{d['name']}</h3>
      <p>{d['description']}</p>
      <div style="margin-top: 12px; border-top: 1px solid #313244; padding-top: 12px;">
        <span style="font-size: 12px; color: #6c7086; text-transform: uppercase; font-weight: bold; display: block; margin-bottom: 8px;">Mapped Sources:</span>
"""
    for s in d["sources"]:
        html_content += f"""<span class="badge">{s['organization']} - {s['name']}</span>"""
    if not d["sources"]:
        html_content += f"""<span class="badge">No mapped sources</span>"""
    html_content += """
      </div>
    </div>
"""

html_content += """
  </div>

  <h2 class="section-title">📡 Discovered Data Sources</h2>
  <div class="grid">
"""

for s in sources_data:
    status_class = "status-active" if s["status"].lower() == "active" else "status-pending"
    html_content += f"""
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
        <h3>{s['organization']} - {s['name']}</h3>
        <span class="badge {status_class}">{s['status']}</span>
      </div>
      <p>{s['description']}</p>
      <p style="font-size: 13px; margin-bottom: 4px;"><strong>Method:</strong> {s['method']}</p>
      <p style="font-size: 13px; margin-bottom: 16px;"><strong>URL:</strong> <a href="{s['url']}" style="color: #89b4fa;">{s['url']}</a></p>
      
      <div style="margin-top: 12px; border-top: 1px solid #313244; padding-top: 12px;">
        <span style="font-size: 12px; color: #6c7086; text-transform: uppercase; font-weight: bold; display: block; margin-bottom: 8px;">Feeds into Domains:</span>
"""
    for d in s["domains"]:
        html_content += f"""<span class="badge">{d['name']}</span>"""
    if not s["domains"]:
        html_content += f"""<span class="badge">Unassigned</span>"""
    html_content += """
      </div>
    </div>
"""

html_content += """
  </div>
</main>
</body>
</html>
"""

os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated relational {OUTPUT_HTML}")

# --- Generate Ingestion Status Page ---
import duckdb
import pandas as pd

DUCKDB_PATH = "/opt/open-reporting/data/warehouse.duckdb"
STATUS_HTML = "/opt/open-reporting/infra/nginx/html/ingestion-status.html"

# Fetch status from duckdb if it exists
sync_statuses = {}
if os.path.exists(DUCKDB_PATH):
    try:
        conn = duckdb.connect(DUCKDB_PATH)
        # Create table if not exists so it doesn't fail
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ingestion_status (
                source_id VARCHAR PRIMARY KEY,
                last_sync TIMESTAMP,
                status VARCHAR,
                rows_fetched INTEGER,
                error_message VARCHAR
            )
        """)
        df = conn.execute("SELECT * FROM ingestion_status").fetchdf()
        for _, row in df.iterrows():
            sync_statuses[row['source_id']] = {
                "last_sync": str(row['last_sync']) if not pd.isna(row['last_sync']) else "Never",
                "status": row['status'],
                "rows_fetched": row['rows_fetched'],
                "error_message": row['error_message'] if not pd.isna(row['error_message']) else ""
            }
        conn.close()
    except Exception as e:
        print(f"Failed to read duckdb: {e}")

html_status = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Open Reporting — Ingestion Status</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Inter, system-ui, sans-serif; background: #1e1e2e; color: #cdd6f4; min-height: 100vh; }
    header { background: #181825; border-bottom: 1px solid #313244; padding: 20px 32px; display: flex; justify-content: space-between; align-items: center;}
    header h1 { font-size: 20px; font-weight: 700; color: #a6e3a1; }
    main { max-width: 1200px; margin: 40px auto; padding: 0 24px; }
    table { width: 100%; border-collapse: collapse; margin-top: 24px; background: #181825; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    th, td { padding: 16px; text-align: left; border-bottom: 1px solid #313244; }
    th { background: #313244; color: #89b4fa; font-weight: 600; font-size: 14px; text-transform: uppercase; }
    tr:last-child td { border-bottom: none; }
    .status-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .status-success { background: rgba(166, 227, 161, 0.2); color: #a6e3a1; }
    .status-failed { background: rgba(243, 139, 168, 0.2); color: #f38ba8; }
    .status-pending { background: rgba(249, 226, 175, 0.2); color: #f9e2af; }
    .btn { background: #89b4fa; color: #11111b; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: 600; }
  </style>
</head>
<body>
<header>
  <div>
    <h1>Live Ingestion Status</h1>
    <p style="color: #bac2de; font-size: 13px; margin-top: 4px;">Monitor all automated data pipelines</p>
  </div>
  <div style="display: flex; gap: 12px;">
    <a href="/data-catalog.html" class="btn">Data Catalog</a>
    <a href="/admin.html" class="btn">⬅ Back to Admin</a>
  </div>
</header>
<main>
  <table>
    <thead>
      <tr>
        <th>Source ID</th>
        <th>Organization & Name</th>
        <th>Status</th>
        <th>Last Sync</th>
        <th>Rows Fetched</th>
      </tr>
    </thead>
    <tbody>
"""

for s in sources_data:
    sid = s["id"]
    record = sync_statuses.get(sid, {"status": "Pending", "last_sync": "Never", "rows_fetched": 0, "error_message": ""})
    
    st_val = str(record["status"]).lower()
    if st_val == "success":
        badge = "status-success"
    elif st_val == "failed" or st_val == "error":
        badge = "status-failed"
    else:
        badge = "status-pending"
        
    err_msg = f"<br><span style='color: #f38ba8; font-size: 12px;'>{record['error_message']}</span>" if record['error_message'] else ""
        
    html_status += f"""
      <tr>
        <td style="font-family: monospace; color: #bac2de;">{sid}</td>
        <td><strong>{s['organization']}</strong> - {s['name']}{err_msg}</td>
        <td><span class="status-badge {badge}">{record['status']}</span></td>
        <td style="color: #a6adc8; font-size: 14px;">{record['last_sync']}</td>
        <td style="font-family: monospace;">{record['rows_fetched']:,}</td>
      </tr>
"""

html_status += """
    </tbody>
  </table>
</main>
</body>
</html>
"""

with open(STATUS_HTML, "w", encoding="utf-8") as f:
    f.write(html_status)

print(f"Generated status dashboard at {STATUS_HTML}")

