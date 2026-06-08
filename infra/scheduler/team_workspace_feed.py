import os
import json
import glob
import time

def get_agent_name(t_file, agent_id):
    name = f"Subagent-{agent_id}"
    try:
        with open(t_file, "r") as f:
            head = f.read(4000).lower()
            if "orchestrat" in head or "teamwork" in head:
                name = "Project Orchestrator 🧠"
            if "dashboard" in head and ("css" in head or "frontend" in head or "dev" in head):
                name = "Frontend Developer 🎨"
            if "visual" in head and "screenshot" in head:
                name = "Visual QA Auditor 👁️"
            if "data engineer" in head or "duckdb" in head:
                name = "Data Engineer ⚙️"
            if "auditor" in head or "victory" in head:
                name = "Victory Auditor 🛡️"
    except:
        pass
    return name

def generate_chat_html():
    brain_dir = "/home/radek/.gemini/antigravity-cli/brain"
    html_path = "/opt/open-reporting/infra/nginx/html/team.html"
    
    # Read Status
    status_content = "Loading status..."
    try:
        with open("/opt/open-reporting/.agents/sentinel/handoff.md", "r") as f:
            status_content = f.read()
    except:
        status_content = "No active handoff reports."
        
    transcript_files = glob.glob(f"{brain_dir}/*/.system_generated/logs/transcript.jsonl")
    
    messages = []
    name_cache = {}
    
    for t_file in transcript_files:
        try:
            agent_id = t_file.split("/")[-4][:8]
            if agent_id not in name_cache:
                name_cache[agent_id] = get_agent_name(t_file, agent_id)
            
            with open(t_file, "r") as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        if data.get("type") == "PLANNER_RESPONSE":
                            content = data.get("content", "")
                            if content and not content.startswith("Created At:"):
                                messages.append({
                                    "time": os.path.getmtime(t_file), 
                                    "agent": name_cache[agent_id],
                                    "text": content
                                })
                    except:
                        pass
        except:
            pass
            
    # Sort messages chronologically
    messages.sort(key=lambda x: x["time"])
    messages = messages[-50:]
    
    # JSON dump for frontend rendering
    msg_json = json.dumps([{"agent": m["agent"], "text": m["text"]} for m in messages])
    status_json = json.dumps(status_content)
    
    html = f"""
    <html>
    <head>
        <title>AI Team Workspace</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #1e1e2e; color: #cdd6f4; margin: 0; padding: 20px; }}
            .layout {{ display: flex; flex-direction: column; gap: 20px; max-width: 1200px; margin: 0 auto; }}
            @media(min-width: 768px) {{ .layout {{ flex-direction: row; }} }}
            
            .sidebar {{ flex: 1; background: #181825; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #313244; height: fit-content; }}
            .chat {{ flex: 2; }}
            
            .message {{ background: #313244; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .agent-name {{ color: #89b4fa; font-weight: bold; margin-bottom: 5px; font-size: 16px; border-bottom: 1px solid #45475a; padding-bottom: 5px; }}
            .message-text {{ font-size: 14px; line-height: 1.6; color: #bac2de; overflow-x: auto; }}
            .message-text pre {{ background: #11111b; padding: 10px; border-radius: 4px; }}
            .message-text code {{ font-family: monospace; color: #f38ba8; }}
            
            .header {{ text-align: center; border-bottom: 1px solid #45475a; padding-bottom: 15px; margin-bottom: 20px; }}
            h2 {{ margin: 0; color: #a6e3a1; font-size: 24px; }}
            h3 {{ color: #f9e2af; margin-top: 0; }}
            p {{ color: #a6adc8; }}
        </style>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <div class="layout">
            <div class="sidebar">
                <h3>📊 Live Status & Progress</h3>
                <div id="status-content"></div>
            </div>
            <div class="chat">
                <div class="header">
                    <h2>🟢 Open Reporting Team Chat</h2>
                    <p>Watching autonomous agents collaborate in real-time. (Auto-refreshes every 5s)</p>
                </div>
                <div id="chat-content"></div>
            </div>
        </div>
        
        <script>
            // Render markdown content
            document.getElementById('status-content').innerHTML = marked.parse({status_json});
            
            const messages = {msg_json};
            let chatHtml = "";
            messages.forEach(msg => {{
                chatHtml += `<div class="message">
                    <div class="agent-name">🤖 ${{msg.agent}}</div>
                    <div class="message-text">${{marked.parse(msg.text)}}</div>
                </div>`;
            }});
            document.getElementById('chat-content').innerHTML = chatHtml;
        </script>
    </body>
    </html>
    """
    
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, "w") as f:
        f.write(html)

if __name__ == "__main__":
    while True:
        generate_chat_html()
        time.sleep(5)
