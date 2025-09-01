#!/usr/bin/env python3
"""
Simple script to run Flask app using flask run command
"""

import os
import sys
import subprocess


def run_flask_app():
    """Run the Flask app using flask run"""
    print("🏈 Fantasy Drafting Web Dashboard")
    print("=" * 40)
    print("🚀 Starting dashboard with Flask CLI...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print()

    # Change to web_dashboard directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    web_dashboard_dir = os.path.join(script_dir, "web_dashboard")

    try:
        # Run flask command
        subprocess.run(["flask", "run"], cwd=web_dashboard_dir, check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Flask: {e}")
    except FileNotFoundError:
        print("❌ Flask not found. Make sure Flask is installed:")
        print("   pip install flask")


if __name__ == "__main__":
    run_flask_app()
