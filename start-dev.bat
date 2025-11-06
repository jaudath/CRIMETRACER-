@echo off
echo Starting Crime Tracer Development Environment...
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.10+
    pause
    exit /b 1
)
echo Python found: 
python --version

:: Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found! Please install Node.js 16+
    pause
    exit /b 1
)
echo Node.js found: 
node --version
echo.

:: Initialize database
echo Initializing database...
python -c "import asyncio; from Backend.db import init_db; asyncio.run(init_db())"
if errorlevel 1 (
    echo ERROR: Database initialization failed!
    pause
    exit /b 1
)
echo Database initialized successfully!
echo.

:: Start backend in new window
echo Starting Backend Server (Port 8000)...
start "Crime Tracer Backend" cmd /k "python main.py --host 0.0.0.0 --port 8000"

:: Wait for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend in new window
echo Starting Frontend Development Server (Port 5173)...
start "Crime Tracer Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo =================================================
echo ^| 🚀 Crime Tracer Development Environment Started! ^|
echo =================================================
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Close the backend and frontend windows to stop the services.
echo Press any key to exit this script...
pause >nul