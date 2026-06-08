import yaml
import os

SOURCES_FILE = "/opt/open-reporting/products/ingestion/to_landing/sources.yaml"
OUTPUT_HTML = "/opt/open-reporting/infra/nginx/html/data-catalog.html"

with open(SOURCES_FILE, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

sources = data.get("sources", [])

html_content = """<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Open Reporting — Data Catalog</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Inter, system-ui, sans-serif; background: #1e1e2e; color: #cdd6f4; min-height: 100vh; }
    header { background: #181825; border-bottom: 1px solid #313244; padding: 20px 32px; display: flex; justify-content: space-between; align-items: center;}
    header h1 { font-size: 20px; font-weight: 700; color: #a6e3a1; }
    main { max-width: 1000px; margin: 40px auto; padding: 0 24px; }
    .table-wrapper { background: #181825; border: 1px solid #313244; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #313244; font-size: 14px; }
    th { background: #11111b; color: #bac2de; font-weight: 600; text-transform: uppercase; font-size: 12px; }
    .status-active { color: #a6e3a1; font-weight: bold; }
    .status-planned { color: #f9e2af; font-weight: bold; }
    .btn { background: #89b4fa; color: #11111b; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: 600; }
  </style>
</head>
<body>
<header>
  <div>
    <h1>Data Catalog & Source Registry</h1>
    <p style="color: #bac2de; font-size: 13px; margin-top: 4px;">Zarządzanie źródłami danych i rurociągami</p>
  </div>
  <a href="/admin.html" class="btn">⬅ Back to Admin</a>
</header>
<main>
  <h2 style="margin-bottom: 20px; font-size: 18px;">Registry of Data Sources</h2>
  <div class="table-wrapper">
    <table>
      <thead>
        <tr>
          <th>Domain</th>
          <th>Organization</th>
          <th>Description</th>
          <th>Method</th>
          <th>Scope</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
"""

for s in sources:
    status_class = "status-active" if s["status"].lower() == "active" else "status-planned"
    html_content += f"""
        <tr>
          <td>{s['domain']}</td>
          <td><strong>{s['organization']}</strong></td>
          <td>{s['description']}</td>
          <td>{s['method']}</td>
          <td>{s['granularity']}</td>
          <td class="{status_class}">● {s['status']}</td>
        </tr>
"""

html_content += """
      </tbody>
    </table>
  </div>
</main>
</body>
</html>
"""

os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated {OUTPUT_HTML}")
