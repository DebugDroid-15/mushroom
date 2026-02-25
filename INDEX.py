#!/usr/bin/env python3
"""
Soil Monitoring System - Project Index
Auto-generated file listing with descriptions
"""

PROJECT_FILES = {
    "Core Application": {
        "modbus_sensor.py": "Modbus RTU library - reads NPK sensors via RS-485",
        "app.py": "Flask web server - provides REST API and serves dashboard",
        "requirements.txt": "Python dependencies (pymodbus, flask)",
    },
    
    "Web Interface": {
        "templates/dashboard.html": "Responsive web dashboard with real-time updates",
        "dashboard.html": "[OLD] Original dashboard file - use templates/dashboard.html instead",
    },
    
    "Configuration": {
        "config.example.py": "Configuration template - copy to config.py and customize",
        "soil-monitor.service": "Systemd service file for auto-start on boot",
    },
    
    "Setup & Deployment": {
        "install.sh": "Raspberry Pi setup script - automated installation",
        "dev.sh": "Development helper - local testing only (not for Pi)",
    },
    
    "Documentation": {
        "README.md": "Complete setup guide - START HERE for new users",
        "QUICKREF.md": "Quick reference - commands and common tasks",
        "WIRING.md": "Hardware wiring guide - RS-485 connections and testing",
        "DOCUMENTATION.md": "Complete documentation - architecture and API reference",
        "FILES.md": "File descriptions - what each file does",
    }
}

def print_index():
    """Print formatted project index"""
    print("=" * 70)
    print("🌱 SOIL MONITORING SYSTEM - PROJECT INDEX".center(70))
    print("=" * 70)
    print()
    
    for category, files in PROJECT_FILES.items():
        print(f"📁 {category}")
        print("─" * 70)
        for filename, description in files.items():
            print(f"  • {filename:<30} {description}")
        print()
    
    print("=" * 70)
    print("QUICK START".center(70))
    print("=" * 70)
    print("""
1. Read: README.md (setup guide)
2. Read: WIRING.md (hardware connections)
3. Run: bash install.sh (on Raspberry Pi)
4. Access: http://<pi_ip>:5000

For quick answers: QUICKREF.md
For detailed info: DOCUMENTATION.md
For hardware help: WIRING.md
""")

if __name__ == "__main__":
    print_index()
