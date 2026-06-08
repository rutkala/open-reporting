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
  <a href="/admin.html" class="btn">⬅ Back to Admin</a>
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
