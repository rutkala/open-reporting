import os
import json
import time
import requests

from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.environ.get("LINEAR_API_KEY")
URL = "https://api.linear.app/graphql"
HEADERS = {"Authorization": API_KEY, "Content-Type": "application/json"}
HTML_PATH = "/opt/open-reporting/infra/nginx/html/po-dashboard.html"

def fetch_linear_data():
    query = """
    query {
      issues(first: 50, filter: { state: { type: { in: ["started", "unstarted", "completed"] } } }) {
        nodes {
          identifier
          title
          state { name type }
        }
      }
    }
    """
    res = requests.post(URL, headers=HEADERS, json={"query": query}).json()
    if "errors" in res:
        return []
    return res["data"]["issues"]["nodes"]

def generate_dashboard():
    issues = fetch_linear_data()
    
    in_progress = [i for i in issues if i["state"]["type"] == "started" or i["state"]["name"].lower() == "in progress"]
    blocked = [i for i in issues if "blocked" in i["state"]["name"].lower() or "po" in i["state"]["name"].lower()]
    completed = [i for i in issues if i["state"]["type"] == "completed"][:5] # latest 5
    
    html = f"""
    <html>
    <head>
        <title>PO Command Center</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #1e1e2e; color: #cdd6f4; margin: 0; padding: 20px; }}
            .container {{ max-width: 900px; margin: 0 auto; }}
            .header {{ text-align: center; border-bottom: 1px solid #45475a; padding-bottom: 15px; margin-bottom: 30px; }}
            h1 {{ color: #a6e3a1; margin: 0; font-size: 28px; }}
            h2 {{ font-size: 20px; margin-top: 0; border-bottom: 1px solid #45475a; padding-bottom: 10px; }}
            .card {{ background: #181825; border-radius: 8px; padding: 20px; margin-bottom: 20px; border: 1px solid #313244; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .blocked-card {{ border-color: #f38ba8; background: rgba(243, 139, 168, 0.05); }}
            .issue {{ background: #313244; padding: 12px; border-radius: 6px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }}
            .issue-id {{ color: #89b4fa; font-weight: bold; font-family: monospace; }}
            .issue-title {{ flex: 1; margin-left: 15px; color: #bac2de; }}
            .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
            .badge-blocked {{ background: #f38ba8; color: #11111b; }}
            .badge-active {{ background: #89b4fa; color: #11111b; }}
            .badge-done {{ background: #a6e3a1; color: #11111b; }}
            .empty {{ color: #6c7086; font-style: italic; text-align: center; padding: 10px; }}
        </style>
        <meta http-equiv="refresh" content="10">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>👑 PO Command Center</h1>
                <p style="color: #a6adc8;">Live tracking of AI execution and pending approvals.</p>
            </div>
            
            <div class="card blocked-card">
                <h2 style="color: #f38ba8;">🔴 Blocked on PO (Action Required)</h2>
                {"".join([f'<div class="issue"><span class="issue-id">{i["identifier"]}</span><span class="issue-title">{i["title"]}</span><span class="badge badge-blocked">BLOCKED</span></div>' for i in blocked]) if blocked else '<div class="empty">No blocking items. The AI team is unhindered.</div>'}
            </div>

            <div class="card">
                <h2 style="color: #89b4fa;">🟢 In Progress (AI Team Working)</h2>
                {"".join([f'<div class="issue"><span class="issue-id">{i["identifier"]}</span><span class="issue-title">{i["title"]}</span><span class="badge badge-active">CODING</span></div>' for i in in_progress]) if in_progress else '<div class="empty">Team is currently in standby.</div>'}
            </div>
            
            <div class="card">
                <h2 style="color: #a6e3a1;">✅ Recently Shipped</h2>
                {"".join([f'<div class="issue"><span class="issue-id">{i["identifier"]}</span><span class="issue-title">{i["title"]}</span><span class="badge badge-done">DONE</span></div>' for i in completed]) if completed else '<div class="empty">No recently completed tasks.</div>'}
            </div>
        </div>
    </body>
    </html>
    """
    
    os.makedirs(os.path.dirname(HTML_PATH), exist_ok=True)
    with open(HTML_PATH, "w") as f:
        f.write(html)

if __name__ == "__main__":
    while True:
        try:
            generate_dashboard()
        except Exception as e:
            pass
        time.sleep(10)
