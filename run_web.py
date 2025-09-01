#!/usr/bin/env python3
"""
Run script for Fantasy Drafting Web Dashboard
Updated for new project structure
"""

import os
import sys
import subprocess


def run_web_app():
    """Run the web dashboard"""
    print("🏈 Fantasy Drafting Web Dashboard")
    print("=" * 40)
    print("🚀 Starting dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print()

    # Change to web directory
    web_dir = os.path.join(os.path.dirname(__file__), "src", "web")

    try:
        # Run the Flask app
        os.chdir(web_dir)
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running app: {e}")
    except FileNotFoundError:
        print("❌ Flask app not found. Make sure all files are in place.")


if __name__ == "__main__":
    run_web_app()
