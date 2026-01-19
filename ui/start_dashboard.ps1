# PowerShell script to start both Flask API and React Dashboard

Write-Host "`n🚀 Starting Automation Testing Dashboard...`n" -ForegroundColor Cyan

# Start Flask API in a new window
Write-Host "📡 Starting Flask API..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command `"cd ui\flask_api; python app.py`""

# Wait a moment for Flask to start
Start-Sleep -Seconds 2

# Start React Dashboard in a new window
Write-Host "⚛️  Starting React Dashboard..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command `"cd ui\react_dashboard; npm run dev`""

Write-Host "`n✨ Dashboard services are starting in new windows. ✨" -ForegroundColor Green
Write-Host "🚀 Open your browser to http://localhost:3001 to see the dashboard!" -ForegroundColor Cyan
Write-Host "`nPress any key to exit this script..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
