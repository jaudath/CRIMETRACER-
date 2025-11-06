# Crime Tracer Development Startup Script for Windows
Write-Host "Starting Crime Tracer Development Environment..." -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Blue
} catch {
    Write-Host "Python not found! Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>&1
    Write-Host "Node.js found: $nodeVersion" -ForegroundColor Blue
} catch {
    Write-Host "Node.js not found! Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python -c "import asyncio; from Backend.db import init_db; asyncio.run(init_db())"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Database initialized successfully!" -ForegroundColor Green
} else {
    Write-Host "Database initialization failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`nStarting Backend Server (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python main.py --host 0.0.0.0 --port 8000"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

Write-Host "Starting Frontend Development Server (Port 5173)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD/frontend'; npm run dev"

Write-Host "`n🚀 Crime Tracer Development Environment Started!" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend App: http://localhost:5173" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan

Write-Host "`nPress any key to stop all services..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Stop all Python and Node processes (be careful with this)
Write-Host "Stopping services..." -ForegroundColor Red
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "All services stopped." -ForegroundColor Green