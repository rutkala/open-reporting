#!/bin/bash
cd /opt/open-reporting
pkill -f "template/app.py" 2>/dev/null
sleep 1
PYTHONPATH=/opt/open-reporting python3 products/dashboards/template/app.py > /tmp/template-dashboard.log 2>&1 &
disown
echo "Dashboard started, PID: $!"
