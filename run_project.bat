@echo off
title Crime Tracer - Full Stack Application
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                     🚨 CRIME TRACER 🚨                      ║
echo ║              Police Complaint Management System              ║
echo ║                                                              ║
echo ║           🌐 Full Stack Application Launcher                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Change to project directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Node.js not found - will run backend only
    echo Install Node.js to enable frontend
    set FRONTEND_AVAILABLE=false
) else (
    echo ✅ Node.js found
    node --version
    npm --version
    set FRONTEND_AVAILABLE=true
)

echo.
echo 🚀 Starting Crime Tracer Application...
echo.

REM Run the unified Python launcher
python run_project.py

echo.
echo 👋 Thank you for using Crime Tracer!
pause