@echo off
echo ===============================================
echo Crime Tracer Development Environment
echo ===============================================
echo.

echo Starting Backend Server on port 8000...
start "CrimeTracer Backend" cmd /c ".venv\Scripts\activate.bat && python main.py --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 5

echo Starting Frontend Development Server on port 5173...
start "CrimeTracer Frontend" cmd /c "cd frontend && npm run dev"

echo.
echo ===============================================
echo Services Started!
echo ===============================================
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:5173
echo API Documentation: http://localhost:8000/docs
echo.
echo Press any key to stop all services...
pause

echo.
echo Stopping services...
taskkill /fi "WindowTitle eq CrimeTracer Backend" /f /t
taskkill /fi "WindowTitle eq CrimeTracer Frontend" /f /t

echo Services stopped.
pause