#!/usr/bin/env python3
"""
Crime Tracer Project Launcher
Unified script to run both frontend and backend simultaneously
"""
import os
import sys
import time
import subprocess
import threading
from pathlib import Path

class Colors:
    """Console colors for better output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(message, color=Colors.OKGREEN):
    """Print colored message"""
    print(f"{color}{message}{Colors.ENDC}")

def print_banner():
    """Print project banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                     🚨 CRIME TRACER 🚨                      ║
    ║              Police Complaint Management System              ║
    ║                                                              ║
    ║           🌐 Full Stack Application Launcher                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print_colored(banner, Colors.HEADER)

def check_dependencies():
    """Check if required dependencies are available"""
    print_colored("\n🔍 Checking dependencies...", Colors.OKCYAN)
    
    # Check Python
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print_colored(f"✅ Python: {result.stdout.strip()}", Colors.OKGREEN)
    except Exception as e:
        print_colored(f"❌ Python check failed: {e}", Colors.FAIL)
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        print_colored(f"✅ Node.js: {result.stdout.strip()}", Colors.OKGREEN)
        node_available = True
    except Exception:
        print_colored("⚠️  Node.js not found - will skip frontend", Colors.WARNING)
        node_available = False
    
    # Check npm
    if node_available:
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print_colored(f"✅ npm: v{result.stdout.strip()}", Colors.OKGREEN)
            else:
                print_colored("⚠️  npm not working properly - will skip frontend", Colors.WARNING)
                node_available = False
        except Exception:
            print_colored("⚠️  npm not found - will skip frontend", Colors.WARNING)
            node_available = False
    
    return True, node_available

def install_backend_deps():
    """Install backend dependencies"""
    print_colored("\n📦 Installing backend dependencies...", Colors.OKCYAN)
    
    try:
        # Check if uvicorn is available
        subprocess.run([sys.executable, "-c", "import uvicorn"], 
                      check=True, capture_output=True)
        print_colored("✅ Backend dependencies already installed", Colors.OKGREEN)
        return True
    except subprocess.CalledProcessError:
        print_colored("📦 Installing backend dependencies...", Colors.WARNING)
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "Backend/requirements.txt"], 
                          check=True)
            print_colored("✅ Backend dependencies installed", Colors.OKGREEN)
            return True
        except subprocess.CalledProcessError as e:
            print_colored(f"❌ Failed to install backend dependencies: {e}", Colors.FAIL)
            return False

def install_frontend_deps():
    """Install frontend dependencies"""
    print_colored("\n📦 Checking frontend dependencies...", Colors.OKCYAN)
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print_colored("⚠️  Frontend directory not found", Colors.WARNING)
        return False
    
    node_modules = frontend_path / "node_modules"
    if node_modules.exists():
        print_colored("✅ Frontend dependencies already installed", Colors.OKGREEN)
        return True
    
    print_colored("📦 Installing frontend dependencies...", Colors.WARNING)
    try:
        subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
        print_colored("✅ Frontend dependencies installed", Colors.OKGREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Failed to install frontend dependencies: {e}", Colors.FAIL)
        return False

def run_backend():
    """Run the backend server"""
    print_colored("\n🚀 Starting Backend Server...", Colors.OKCYAN)
    
    backend_path = Path("Backend")
    if not backend_path.exists():
        print_colored("❌ Backend directory not found", Colors.FAIL)
        return
    
    # Store original directory
    original_dir = Path.cwd()
    
    try:
        # Change to backend directory
        os.chdir(backend_path)
        
        # Add backend path to Python path
        sys.path.insert(0, str(backend_path.absolute()))
        
        # Try to import and run directly
        try:
            from simple_main import app
            import uvicorn
            
            print_colored("🌐 Backend API starting on http://localhost:8000", Colors.OKGREEN)
            print_colored("📚 API Documentation: http://localhost:8000/docs", Colors.OKBLUE)
            
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=8000,
                log_level="info"
            )
            
        except ImportError as e:
            print_colored(f"❌ Backend import failed: {e}", Colors.FAIL)
            # Fallback to subprocess
            try:
                print_colored("🔄 Trying subprocess method...", Colors.OKCYAN)
                subprocess.run([sys.executable, "simple_main.py"])
            except Exception as e2:
                print_colored(f"❌ Backend subprocess failed: {e2}", Colors.FAIL)
                # Try run_server.py as last resort
                try:
                    print_colored("🔄 Trying run_server.py...", Colors.OKCYAN)
                    subprocess.run([sys.executable, "run_server.py"])
                except Exception as e3:
                    print_colored(f"❌ All backend start methods failed: {e3}", Colors.FAIL)
                    
    except KeyboardInterrupt:
        print_colored("\n🛑 Backend server stopped", Colors.WARNING)
    except Exception as e:
        print_colored(f"❌ Backend error: {e}", Colors.FAIL)
    finally:
        # Restore original directory
        os.chdir(original_dir)

def run_frontend():
    """Run the frontend development server"""
    print_colored("\n⚛️  Starting Frontend Development Server...", Colors.OKCYAN)
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print_colored("❌ Frontend directory not found", Colors.FAIL)
        return
    
    try:
        # Try different npm start commands
        commands = ["npm run dev", "npm start", "npm run serve"]
        
        for cmd in commands:
            try:
                print_colored(f"🔄 Trying: {cmd}", Colors.OKBLUE)
                process = subprocess.Popen(
                    cmd.split(),
                    cwd=frontend_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                
                # Wait a bit to see if it starts successfully
                time.sleep(3)
                if process.poll() is None:  # Process is still running
                    print_colored("🌐 Frontend starting on http://localhost:5173 or http://localhost:3000", Colors.OKGREEN)
                    
                    # Continue reading output
                    for line in process.stdout:
                        if "local:" in line.lower() or "localhost" in line.lower():
                            print_colored(f"📱 Frontend: {line.strip()}", Colors.OKGREEN)
                        elif "error" in line.lower():
                            print_colored(f"❌ {line.strip()}", Colors.FAIL)
                        else:
                            print(f"📱 {line.strip()}")
                    
                    process.wait()
                    break
                else:
                    print_colored(f"❌ {cmd} failed", Colors.WARNING)
                    
            except Exception as e:
                print_colored(f"❌ Command '{cmd}' failed: {e}", Colors.WARNING)
                continue
        else:
            print_colored("❌ All frontend start commands failed", Colors.FAIL)
            
    except KeyboardInterrupt:
        print_colored("\n🛑 Frontend server stopped", Colors.WARNING)
    except Exception as e:
        print_colored(f"❌ Frontend error: {e}", Colors.FAIL)

def main():
    """Main function to run the entire project"""
    print_banner()
    
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print_colored(f"📁 Project Directory: {project_root.absolute()}", Colors.OKBLUE)
    
    # Check dependencies
    python_ok, node_ok = check_dependencies()
    if not python_ok:
        print_colored("❌ Python dependencies check failed", Colors.FAIL)
        return
    
    # Install backend dependencies
    if not install_backend_deps():
        print_colored("❌ Backend setup failed", Colors.FAIL)
        return
    
    # Install frontend dependencies if Node.js is available
    frontend_available = False
    if node_ok:
        frontend_available = install_frontend_deps()
    
    print_colored("\n🎯 Starting Crime Tracer Application...", Colors.HEADER)
    
    if frontend_available:
        print_colored("🔄 Running in Full Stack Mode (Frontend + Backend)", Colors.OKGREEN)
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend in main thread
        try:
            run_frontend()
        except KeyboardInterrupt:
            print_colored("\n🛑 Application stopped by user", Colors.WARNING)
    else:
        print_colored("🔄 Running in Backend Only Mode", Colors.WARNING)
        print_colored("📱 Frontend will not be available - install Node.js to enable it", Colors.WARNING)
        
        try:
            run_backend()
        except KeyboardInterrupt:
            print_colored("\n🛑 Application stopped by user", Colors.WARNING)
    
    print_colored("\n👋 Thank you for using Crime Tracer!", Colors.HEADER)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n🛑 Application interrupted", Colors.WARNING)
    except Exception as e:
        print_colored(f"\n❌ Unexpected error: {e}", Colors.FAIL)
        raise