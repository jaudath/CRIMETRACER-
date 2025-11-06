# Crime Tracer Development Environment - PowerShell Script
param(
    [switch]$StopAll,
    [switch]$BackendOnly,
    [switch]$FrontendOnly
)

$ErrorActionPreference = "Stop"

# Configuration
$BACKEND_PORT = 8000
$FRONTEND_PORT = 5173
$PROJECT_ROOT = $PWD

# Colors for output
$Colors = @{
    Success = "Green"
    Warning = "Yellow" 
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColoredMessage {
    param($Message, $Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Header {
    param($Message)
    Write-Host "`n" -NoNewline
    Write-Host "="*60 -ForegroundColor $Colors.Header
    Write-Host " $Message " -ForegroundColor $Colors.Header
    Write-Host "="*60 -ForegroundColor $Colors.Header
    Write-Host ""
}

function Test-Prerequisites {
    Write-ColoredMessage "Checking prerequisites..." $Colors.Info
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColoredMessage "✓ Python found: $pythonVersion" $Colors.Success
        } else {
            throw "Python check failed"
        }
    } catch {
        Write-ColoredMessage "✗ Python not found! Please install Python 3.10+" $Colors.Error
        return $false
    }
    
    # Check Node.js
    try {
        $nodeVersion = node --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColoredMessage "✓ Node.js found: $nodeVersion" $Colors.Success
        } else {
            throw "Node.js check failed"
        }
    } catch {
        Write-ColoredMessage "✗ Node.js not found! Please install Node.js 16+" $Colors.Error
        return $false
    }
    
    return $true
}

function Stop-AllServices {
    Write-Header "Stopping All Services"
    
    Write-ColoredMessage "Stopping Python processes on port $BACKEND_PORT..." $Colors.Warning
    Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
        $_.ProcessName -eq "python"
    } | ForEach-Object {
        Write-ColoredMessage "Stopping Python process: $($_.Id)" $Colors.Warning
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    
    Write-ColoredMessage "Stopping Node processes on port $FRONTEND_PORT..." $Colors.Warning
    Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object {
        $_.ProcessName -eq "node"
    } | ForEach-Object {
        Write-ColoredMessage "Stopping Node process: $($_.Id)" $Colors.Warning
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    
    # Kill processes using specific ports
    netstat -ano | Select-String ":$BACKEND_PORT " | ForEach-Object {
        $processId = ($_ -split "\s+")[-1]
        if ($processId -and $processId -ne "0") {
            Write-ColoredMessage "Killing process $processId using port $BACKEND_PORT" $Colors.Warning
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }
    
    netstat -ano | Select-String ":$FRONTEND_PORT " | ForEach-Object {
        $processId = ($_ -split "\s+")[-1]
        if ($processId -and $processId -ne "0") {
            Write-ColoredMessage "Killing process $processId using port $FRONTEND_PORT" $Colors.Warning
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }
    
    Write-ColoredMessage "All services stopped." $Colors.Success
}

function Initialize-Database {
    Write-ColoredMessage "Initializing database..." $Colors.Info
    try {
        python -c "import asyncio; from Backend.db import init_db; asyncio.run(init_db())" 2>&1 | Out-Host
        if ($LASTEXITCODE -eq 0) {
            Write-ColoredMessage "✓ Database initialized successfully!" $Colors.Success
        } else {
            throw "Database initialization failed"
        }
    } catch {
        Write-ColoredMessage "✗ Database initialization failed!" $Colors.Error
        throw
    }
}

function Start-Backend {
    Write-ColoredMessage "Starting Backend Server on port $BACKEND_PORT..." $Colors.Info
    
    $backendCmd = "python main.py --host 0.0.0.0 --port $BACKEND_PORT"
    $backendJob = Start-Job -ScriptBlock {
        param($cmd, $workingDir)
        Set-Location $workingDir
        Invoke-Expression $cmd
    } -ArgumentList $backendCmd, $PROJECT_ROOT
    
    Start-Sleep -Seconds 3
    
    # Check if backend is running
    $backendRunning = $false
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$BACKEND_PORT/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $backendRunning = $true
            Write-ColoredMessage "✓ Backend server is running!" $Colors.Success
        }
    } catch {
        Write-ColoredMessage "Backend server starting (may take a moment)..." $Colors.Warning
    }
    
    return $backendJob
}

function Start-Frontend {
    Write-ColoredMessage "Starting Frontend Development Server on port $FRONTEND_PORT..." $Colors.Info
    
    $frontendCmd = "npm run dev"
    $frontendJob = Start-Job -ScriptBlock {
        param($cmd, $workingDir)
        Set-Location "$workingDir/frontend"
        Invoke-Expression $cmd
    } -ArgumentList $frontendCmd, $PROJECT_ROOT
    
    Start-Sleep -Seconds 3
    Write-ColoredMessage "✓ Frontend server started!" $Colors.Success
    
    return $frontendJob
}

function Show-ServiceStatus {
    Write-Header "Service Status"
    
    # Check Backend
    try {
        $backendResponse = Invoke-WebRequest -Uri "http://localhost:$BACKEND_PORT/health" -TimeoutSec 2 -ErrorAction Stop
        Write-ColoredMessage "✓ Backend API: http://localhost:$BACKEND_PORT (Status: $($backendResponse.StatusCode))" $Colors.Success
        Write-ColoredMessage "✓ API Documentation: http://localhost:$BACKEND_PORT/docs" $Colors.Info
    } catch {
        Write-ColoredMessage "✗ Backend API: http://localhost:$BACKEND_PORT (Not responding)" $Colors.Error
    }
    
    # Check Frontend
    try {
        $frontendResponse = Invoke-WebRequest -Uri "http://localhost:$FRONTEND_PORT" -TimeoutSec 2 -ErrorAction Stop
        Write-ColoredMessage "✓ Frontend App: http://localhost:$FRONTEND_PORT (Status: $($frontendResponse.StatusCode))" $Colors.Success
    } catch {
        Write-ColoredMessage "✗ Frontend App: http://localhost:$FRONTEND_PORT (Not responding)" $Colors.Error
    }
}

# Main Script Logic
try {
    Write-Header "Crime Tracer Development Environment"
    
    if ($StopAll) {
        Stop-AllServices
        return
    }
    
    if (-not (Test-Prerequisites)) {
        exit 1
    }
    
    # Stop any existing services
    Stop-AllServices
    Start-Sleep -Seconds 2
    
    # Initialize database
    Initialize-Database
    
    $jobs = @()
    
    if (-not $FrontendOnly) {
        Write-Header "Starting Backend Service"
        $backendJob = Start-Backend
        $jobs += $backendJob
    }
    
    if (-not $BackendOnly) {
        Write-Header "Starting Frontend Service"  
        $frontendJob = Start-Frontend
        $jobs += $frontendJob
    }
    
    Start-Sleep -Seconds 5
    Show-ServiceStatus
    
    Write-Header "Services Started Successfully!"
    Write-ColoredMessage "🚀 Crime Tracer Development Environment is running!" $Colors.Success
    Write-ColoredMessage "`nBackend API: http://localhost:$BACKEND_PORT" $Colors.Info
    Write-ColoredMessage "Frontend App: http://localhost:$FRONTEND_PORT" $Colors.Info
    Write-ColoredMessage "API Docs: http://localhost:$BACKEND_PORT/docs" $Colors.Info
    
    Write-ColoredMessage "`nPress 'q' to stop all services and exit..." $Colors.Warning
    
    # Wait for user input to stop
    do {
        $key = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    } while ($key.Character -ne 'q')
    
    Write-Header "Shutting Down Services"
    $jobs | ForEach-Object {
        if ($_ -and $_.State -eq 'Running') {
            Stop-Job $_ -ErrorAction SilentlyContinue
            Remove-Job $_ -Force -ErrorAction SilentlyContinue
        }
    }
    
    Stop-AllServices
    Write-ColoredMessage "`nCrime Tracer Development Environment stopped." $Colors.Success
    
} catch {
    Write-ColoredMessage "`nError: $($_.Exception.Message)" $Colors.Error
    Write-ColoredMessage "Cleaning up..." $Colors.Warning
    
    if ($jobs) {
        $jobs | ForEach-Object {
            if ($_ -and $_.State -eq 'Running') {
                Stop-Job $_ -ErrorAction SilentlyContinue
                Remove-Job $_ -Force -ErrorAction SilentlyContinue
            }
        }
    }
    
    Stop-AllServices
    exit 1
}