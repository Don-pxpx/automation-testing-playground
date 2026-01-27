#!/usr/bin/env bash
# Start Flask API and React Dashboard (Mac / Linux)
# Run from repo root: ./ui/start_dashboard.sh   OR   bash ui/start_dashboard.sh

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo ""
echo "Starting Automation Testing Dashboard..."
echo ""

# Start Flask API in background
echo "Starting Flask API..."
(cd ui/flask_api && python3 app.py 2>/dev/null || python app.py) &
FLASK_PID=$!
sleep 2

# Start React in foreground so logs are visible and Ctrl+C stops it
echo "Starting React Dashboard..."
(cd ui/react_dashboard && npm run dev)

# If React exits, optional: kill Flask (uncomment to stop both on Ctrl+C)
# trap "kill $FLASK_PID 2>/dev/null" EXIT
