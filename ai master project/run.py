#!/usr/bin/env python
"""
Startup script for AI Master Project Dashboard
"""

import subprocess
import sys
import os

def main():
    """Start the dashboard"""
    print("=" * 60)
    print("🚀 AI Master Project - Admin Dashboard")
    print("=" * 60)
    print()
    
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit not installed!")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_path = os.path.join(script_dir, "dashboard.py")
    
    print(f"📂 Project directory: {script_dir}")
    print(f"🎯 Dashboard: {dashboard_path}")
    print()
    print("🌐 Starting dashboard...")
    print("📡 Dashboard will be available at: http://localhost:8501")
    print()
    print("Default credentials:")
    print("  Username: admin    | Password: admin  | Role: Admin")
    print("  Username: staff    | Password: admin  | Role: Staff")
    print("  Username: viewer   | Password: admin  | Role: Viewer")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            dashboard_path,
            "--logger.level=error"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
