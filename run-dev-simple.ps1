#!/usr/bin/env pwsh
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Crime Tracer Development Environment" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting Backend Server on port 8000..." -ForegroundColor Yellow
Start-Job -Name "CrimeTracerBackend" -ScriptBlock {
    Set-Location $using:PWD
    .\.venv\Scripts\Activate.ps1
    python main.py --host 0.0.0.0 --port 8000
}

Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "Starting Frontend Development Server on port 5173..." -ForegroundColor Yellow
Start-Job -Name "CrimeTracerFrontend" -ScriptBlock {
    Set-Location "$using:PWD\frontend"
    npm run dev
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "Services Started Successfully!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "Frontend App: http://localhost:5173" -ForegroundColor White
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor White

Write-Host ""
Write-Host "DEMO LOGIN CREDENTIALS:" -ForegroundColor Magenta
Write-Host "Admin Users:" -ForegroundColor Cyan
Write-Host "  Username: ADMIN001  |  Password: admin123" -ForegroundColor White
Write-Host "  Username: ADMIN002  |  Password: admin456" -ForegroundColor White
Write-Host ""
Write-Host "Police Officers:" -ForegroundColor Cyan
Write-Host "  Username: POL001    |  Password: police123" -ForegroundColor White
Write-Host "  Username: POL002    |  Password: police456" -ForegroundColor White
Write-Host "  Username: POL003    |  Password: police789" -ForegroundColor White
Write-Host "  Username: POL004    |  Password: police101" -ForegroundColor White
Write-Host "  Username: POL005    |  Password: police202" -ForegroundColor White

Write-Host ""
Write-Host "Press 'q' to stop all services..." -ForegroundColor Yellow

do {
    Start-Sleep -Seconds 1
    $key = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} while ($key.Character -ne 'q')

Write-Host ""
Write-Host "Stopping services..." -ForegroundColor Yellow
Get-Job -Name "CrimeTracerBackend" -ErrorAction SilentlyContinue | Stop-Job -PassThru | Remove-Job
Get-Job -Name "CrimeTracerFrontend" -ErrorAction SilentlyContinue | Stop-Job -PassThru | Remove-Job

Write-Host "Services stopped." -ForegroundColor Green