#!/usr/bin/env python3
"""
Run script untuk ServerSide Squad
使用 Python 运行 Flask 应用
"""

import subprocess
import sys
import os

def install_requirements():
    """Install dependencies from requirements.txt"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def run_server():
    """Run the Flask development server"""
    print("\n🚀 Starting ServerSide Squad API...")
    print("="*50)
    print("🌐 Frontend: http://localhost:5000")
    print("📚 API: http://localhost:5000/api")
    print("="*50 + "\n")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped!")
    except Exception as e:
        print(f"❌ Error running server: {e}")

def main():
    """Main function"""
    print("\n" + "="*50)
    print("🎯 ServerSide Squad - Quick Start")
    print("="*50)
    
    # Check if dependencies are installed
    if not os.path.exists('venv') and not os.path.exists('__pycache__'):
        install_requirements()
    
    # Run the server
    run_server()

if __name__ == "__main__":
    main()
