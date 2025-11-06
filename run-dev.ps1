Write-Host "Starting Crime Tracer Development Environment..." -ForegroundColor Green

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python -c "import asyncio; from Backend.db import init_db; asyncio.run(init_db())"

# Start backend
Write-Host "Starting backend server..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python main.py --host 0.0.0.0 --port 8000"

# Wait for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host "Starting frontend server..." -ForegroundColor Yellow  
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd '$PWD/frontend'; npm run dev"

Write-Host ""
Write-Host "====================================================" -ForegroundColor Magenta
Write-Host "Crime Tracer Development Environment Started!" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Magenta
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend App: http://localhost:5173" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""