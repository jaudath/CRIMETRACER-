#!/usr/bin/env python3
"""
🚨 CRIME TRACER - FINAL LAUNCHER 🚨
Complete Full Stack Application Startup Script
"""
import os
import sys
import time
import subprocess
import threading
from pathlib import Path

# Configure console for Windows
if os.name == 'nt':
    os.system('chcp 65001 > nul')  # Enable UTF-8 on Windows

def print_header():
    """Print application header"""
    header = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                      🚨 CRIME TRACER 🚨                       ║
    ║               Police Complaint Management System              ║
    ║                                                               ║
    ║                   🌟 FULL STACK LAUNCHER 🌟                  ║
    ║                                                               ║
    ║  🌐 Backend API  +  ⚛️ React Frontend  =  💪 Complete App    ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    📋 Features Available:
    ✅ Police Registration & Login
    ✅ Complaint Filing with Photo Capture
    ✅ Admin Portal & Analytics
    ✅ Case Management & Tracking
    ✅ Local Storage (No AWS needed)
    
    """
    print(header)

def check_system():
    """Check system dependencies"""
    print("🔍 Checking System Dependencies...")
    print("-" * 40)
    
    # Check Python
    try:
        python_version = sys.version.split()[0]
        print(f"✅ Python {python_version} - OK")
        python_ok = True
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        python_ok = False
    
    # Check Node.js and npm
    node_ok = False
    try:
        node_result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
        if node_result.returncode == 0:
            node_version = node_result.stdout.strip()
            print(f"✅ Node.js {node_version} - OK")
            
            # Check npm
            npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=10)
            if npm_result.returncode == 0:
                npm_version = npm_result.stdout.strip()
                print(f"✅ npm v{npm_version} - OK")
                node_ok = True
            else:
                print("⚠️  npm not available - Frontend will be limited")
        else:
            print("⚠️  Node.js not available - Backend only mode")
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        print("⚠️  Node.js/npm not found - Backend only mode")
    
    print()
    return python_ok, node_ok

def start_backend():
    """Start the backend server"""
    print("🚀 STARTING BACKEND SERVER...")
    print("-" * 40)
    
    backend_dir = Path("Backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Change to backend directory
    original_dir = os.getcwd()
    os.chdir(backend_dir)
    
    try:
        # Add to Python path
        sys.path.insert(0, str(backend_dir.absolute()))
        
        # Import and start server
        from simple_main import app
        import uvicorn
        
        print("✅ Backend modules imported successfully")
        print("🌐 Starting server on http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🎯 Test endpoint: http://localhost:8000/health")
        print()
        
        # Configure uvicorn
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        server.run()
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        # Try subprocess fallback
        try:
            print("🔄 Trying subprocess method...")
            subprocess.run([sys.executable, "simple_main.py"])
        except Exception as e2:
            print(f"❌ Subprocess failed: {e2}")
            return False
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False
    finally:
        os.chdir(original_dir)
    
    return True

def start_frontend():
    """Start the frontend development server"""
    print("⚛️  STARTING FRONTEND SERVER...")
    print("-" * 40)
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    # Install dependencies if needed
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True, timeout=120)
            print("✅ Dependencies installed")
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    # Start development server
    commands = ['npm run dev', 'npm start']
    
    for cmd in commands:
        try:
            print(f"🔄 Trying: {cmd}")
            process = subprocess.Popen(
                cmd.split(),
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor startup
            startup_timeout = 30
            start_time = time.time()
            
            while time.time() - start_time < startup_timeout:
                if process.poll() is not None:
                    print(f"❌ {cmd} exited early")
                    break
                
                try:
                    line = process.stdout.readline()
                    if line:
                        print(f"📱 {line.strip()}")
                        if 'local:' in line.lower() or 'localhost' in line.lower():
                            print("✅ Frontend server started successfully!")
                            # Continue reading output
                            for remaining_line in process.stdout:
                                if remaining_line.strip():
                                    print(f"📱 {remaining_line.strip()}")
                            process.wait()
                            return True
                except:
                    continue
                
                time.sleep(0.1)
            
            # If we get here, command didn't start properly
            process.terminate()
            
        except Exception as e:
            print(f"❌ Command failed: {e}")
            continue
    
    print("❌ All frontend start commands failed")
    return False

def run_full_stack():
    """Run both backend and frontend"""
    print("🎯 LAUNCHING FULL STACK APPLICATION...")
    print("=" * 50)
    
    # Start backend in separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to initialize
    print("⏳ Waiting for backend to start...")
    time.sleep(5)
    
    # Start frontend in main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\\n🛑 Application stopped by user")

def run_backend_only():
    """Run backend only"""
    print("🎯 LAUNCHING BACKEND APPLICATION...")
    print("=" * 50)
    
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\\n🛑 Backend stopped by user")

def show_instructions():
    """Show usage instructions"""
    instructions = """
    🎯 QUICK START INSTRUCTIONS:
    ═══════════════════════════════════════
    
    1️⃣  BACKEND ONLY (Minimum):
       • Python 3.8+ required
       • API available at http://localhost:8000
       • Test with: http://localhost:8000/docs
    
    2️⃣  FULL STACK (Complete):
       • Python 3.8+ and Node.js 16+ required
       • Backend: http://localhost:8000
       • Frontend: http://localhost:3000 or http://localhost:5173
    
    🎮 TEST CREDENTIALS:
       • Admin: ADMIN001 / AdminPass123
       • Create police accounts via registration
    
    🌟 FEATURES TO TRY:
       • File a complaint with photo capture
       • Register as police officer
       • Admin approval system
       • Case management dashboard
    
    """
    print(instructions)

def main():
    """Main launcher function"""
    print_header()
    show_instructions()
    
    # Get project root and change to it
    project_root = Path(__file__).parent
    os.chdir(project_root)
    print(f"📁 Project Directory: {project_root.absolute()}")
    print()
    
    # Check dependencies
    python_ok, node_ok = check_system()
    
    if not python_ok:
        print("❌ Python is required but not available!")
        input("Press Enter to exit...")
        return
    
    # Choose mode based on available tools
    if node_ok:
        print("🎉 Full Stack Mode Available!")
        print("   Both Backend API and Frontend UI will start")
        print()
        
        # Ask user preference
        choice = input("🤔 Start in Full Stack mode? (Y/n): ").strip().lower()
        if choice in ['', 'y', 'yes']:
            run_full_stack()
        else:
            run_backend_only()
    else:
        print("⚠️  Backend Only Mode (Node.js not available)")
        print("   Install Node.js for full frontend experience")
        print()
        run_backend_only()
    
    print()
    print("🎉 Thank you for using Crime Tracer!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n🛑 Application interrupted by user")
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")