#!/usr/bin/env python3
"""
Run script for Fantasy Drafting Web Dashboard
"""

import os
import sys
import subprocess


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"]
        )
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True


def run_dashboard():
    """Run the Flask dashboard"""
    print("🚀 Starting Fantasy Drafting Web Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("❌ Press Ctrl+C to stop the server")

    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)

    # Run the Flask app
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running dashboard: {e}")


if __name__ == "__main__":
    print("🏈 Fantasy Drafting Web Dashboard")
    print("=" * 40)

    # Check if dependencies are installed
    try:
        import flask
        import flask_cors
        import pandas
        import numpy
        import openpyxl
    except ImportError:
        print("📦 Dependencies not found. Installing...")
        if not install_dependencies():
            sys.exit(1)

    # Run the dashboard
    run_dashboard()
