@echo off
title Crime Tracer - Development Environment

echo ===============================================
echo Crime Tracer Development Environment
echo ===============================================
echo.

echo Killing any existing processes on ports 8000 and 5173...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5173" ^| find "LISTENING"') do taskkill /f /pid %%a 2>nul

echo.
echo Starting Backend Server (Port 8000)...
start "CrimeTracer Backend" cmd /c "cd /d "%~dp0" && .venv\Scripts\activate.bat && python main.py --host 0.0.0.0 --port 8000 && pause"

echo Waiting for backend to initialize...
timeout /t 10 /nobreak >nul

echo.
echo Starting Frontend Server (Port 5173)...
start "CrimeTracer Frontend" cmd /c "cd /d "%~dp0frontend" && npm run dev && pause"

echo.
echo ===============================================
echo Services Started Successfully!
echo ===============================================
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:5173  
echo API Documentation: http://localhost:8000/docs
echo.
echo ===============================================
echo DEMO LOGIN CREDENTIALS:
echo ===============================================
echo.
echo ADMIN USERS:
echo   Username: ADMIN001  ^|  Password: admin123
echo   Username: ADMIN002  ^|  Password: admin456
echo.
echo POLICE OFFICERS:
echo   Username: POL001    ^|  Password: police123
echo   Username: POL002    ^|  Password: police456
echo   Username: POL003    ^|  Password: police789
echo   Username: POL004    ^|  Password: police101
echo   Username: POL005    ^|  Password: police202
echo.
echo ===============================================
echo.
echo Both services are now running in separate windows.
echo Close this window or press Ctrl+C to exit this launcher.
echo To stop the services, close their respective terminal windows.
echo.
pause