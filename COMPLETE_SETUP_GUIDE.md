# 🌱 Complete Setup Guide - Soil Monitoring System

**A comprehensive guide for setting up the Soil Monitoring System from scratch on your local machine and Raspberry Pi.**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Prerequisites](#prerequisites)
4. [Installation on Your PC](#installation-on-your-pc)
5. [Configuration Setup](#configuration-setup)
6. [Running Locally](#running-locally)
7. [Hardware Setup for Raspberry Pi](#hardware-setup-for-raspberry-pi)
8. [Deploying to Raspberry Pi](#deploying-to-raspberry-pi)
9. [Testing & Troubleshooting](#testing--troubleshooting)
10. [Updating the System](#updating-the-system)

---

## Project Overview

**Soil Monitoring System** is a production-ready Raspberry Pi application that:
- ✅ Monitors 4x NPK (Nitrogen, Phosphorus, Potassium) soil sensors
- ✅ Communicates via RS-485 Modbus RTU protocol
- ✅ Provides real-time web dashboard
- ✅ Offers REST API for data access
- ✅ Auto-starts on Pi boot via systemd service

**Key Technologies:**
- Python 3.7+
- Flask (web server)
- Pymodbus (RS-485 communication)
- RPi.GPIO (Raspberry Pi hardware control)
- JavaScript/HTML (dashboard frontend)

---

## System Architecture

### Single RS-485 Bus with 4 Sensors

```
┌─────────────────────────────────────────┐
│     Raspberry Pi (Master)               │
│  ┌───────────────────────────────────┐  │
│  │ app.py (Flask Server)             │  │
│  │ modbus_sensor.py (Modbus Driver)  │  │
│  │ /dev/serial0 (UART)               │  │
│  └───────────────────────────────────┘  │
│           ↓ RS-485 Converter Module     │
│           (MAX485/SP3485)               │
└─────────────────────────────────────────┘
         ↓ RS-485 Bus (A/B lines)
    ┌────────────────────────────┐
    │ Sensor 1 (Address: 1)      │
    │ Sensor 2 (Address: 2)      │
    │ Sensor 3 (Address: 3)      │
    │ Sensor 4 (Address: 4)      │
    └────────────────────────────┘
```

---

## Prerequisites

### For Your PC (Windows/Mac/Linux)

1. **Python 3.7 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Git**
   - Download from: https://git-scm.com/

3. **Text Editor or IDE** (optional but recommended)
   - VS Code: https://code.visualstudio.com/
   - PyCharm Community: https://www.jetbrains.com/pycharm/

### For Raspberry Pi (Production)

1. **Raspberry Pi 3B+ or newer**
2. **Micro SD Card (16GB+)**
3. **Raspberry Pi OS Lite or Desktop** (latest version)
4. **Stable Internet Connection** (WiFi or Ethernet)

### Hardware Components

- RS-485 Converter Module (MAX485 or SP3485)
- 4x NPK Soil Sensors (Model: SEN0189 or compatible)
- Jumper wires (F-F and M-F)
- 12V Power Supply (for sensors)
- 5V Power Supply (for Raspberry Pi)

---

## Installation on Your PC

### Step 1: Clone the Repository

```bash
# Clone the project
git clone https://github.com/DebugDroid-15/mushroom.git

# Navigate to project
cd mushroom

# Verify files (should see 40+ files)
ls -la
```

### Step 2: Create Python Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed flask-2.3.0 pymodbus-3.1.1 werkzeug-2.3.0 ...
```

### Step 4: Verify Installation

```bash
# Check installed packages
pip list

# Should show:
# Flask           2.3.0
# pymodbus        3.1.1
# Werkzeug        2.3.0
```

---

## Configuration Setup

### Step 1: Create Configuration File

```bash
# Copy example config
cp config.example.py calibration_config.py
```

### Step 2: Edit Configuration

Open `calibration_config.py` in your text editor:

```python
# ===== SERIAL PORT CONFIGURATION =====
SERIAL_PORT = "/dev/serial0"        # (Pi only) or "COM3" (Windows)
BAUD_RATE = 9600
TIMEOUT = 1
BYTE_SIZE = 8
STOP_BITS = 1
PARITY = 'N'

# ===== SENSOR CONFIGURATION =====
SENSORS = {
    1: {"name": "Sensor 1", "location": "Zone A"},
    2: {"name": "Sensor 2", "location": "Zone B"},
    3: {"name": "Sensor 3", "location": "Zone C"},
    4: {"name": "Sensor 4", "location": "Zone D"},
}

# ===== CALIBRATION VALUES =====
# These are sensor-specific and should be calibrated per your sensors
CALIBRATION = {
    1: {"N_min": 0, "N_max": 1000, "P_min": 0, "P_max": 1000, "K_min": 0, "K_max": 1000},
    2: {"N_min": 0, "N_max": 1000, "P_min": 0, "P_max": 1000, "K_min": 0, "K_max": 1000},
    3: {"N_min": 0, "N_max": 1000, "P_min": 0, "P_max": 1000, "K_min": 0, "K_max": 1000},
    4: {"N_min": 0, "N_max": 1000, "P_min": 0, "P_max": 1000, "K_min": 0, "K_max": 1000},
}

# ===== FLASK SERVER =====
FLASK_HOST = "0.0.0.0"              # Accessible from any IP
FLASK_PORT = 5000
DEBUG = False                        # Set True for development only

# ===== LOGGING =====
LOG_LEVEL = "INFO"
LOG_FILE = "soil_monitor.log"
```

---

## Running Locally

### Method 1: Development Mode (for testing)

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows

# Run Flask app in debug mode
python app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
 * WARNING: This is a development server. Do not use it in production.
```

### Method 2: Using Development Script

```bash
# Run dev helper script
chmod +x dev.sh          # Linux/Mac
./dev.sh                 # Run

# Windows
# Run dev.sh manually: edit it to extract Flask command
python app.py
```

### Accessing the Dashboard

Open your browser and go to:
- **Local machine:** http://localhost:5000
- **From another PC on the network:** http://<your-ip>:5000 (e.g., http://192.168.1.100:5000)

---

## Hardware Setup for Raspberry Pi

### RS-485 Converter Wiring

The RS-485 converter (MAX485/SP3485) acts as a bridge between the Pi's UART and the sensor bus.

#### Pinout Reference

**Raspberry Pi GPIO Pins:**
```
3V3  5V  5V  GND
17   27  22  10
 9   11   5  GND
```

**RS-485 Module Pins:**
```
Pin 1: RO  (Receiver Output)   → Pi RX (GPIO15)
Pin 2: DE  (Driver Enable)     → Pi GPIO17
Pin 3: RE  (Receiver Enable)   → Pi GPIO17
Pin 4: DI  (Driver Input)      → Pi TX (GPIO14)
Pin 5: GND (Ground)            → Pi GND
Pin 6: (VCC, optional)         → 3.3V or 5V
Pin 7: A   (RS-485 Line A)     → Sensors A (Blue wire)
Pin 8: B   (RS-485 Line B)     → Sensors B (White wire)
```

#### Complete Wiring Diagram

```
RASPBERRY PI                    RS-485 CONVERTER        SENSORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GPIO14 (TX) ────────────────→ Pin 4 (DI)
GPIO15 (RX) ←──────────────── Pin 1 (RO)
GPIO17 (Control) ─┐
                  ├────────→ Pin 2 (DE)
                  └────────→ Pin 3 (RE)
GND ──────────────────────→ Pin 5 (GND)
                              ↓
                            Pin 7 (A) ←─ Blue Wire ──→ All Sensors (A)
                            Pin 8 (B) ←─ White Wire ─→ All Sensors (B)
                            GND ←────── Black Wire ──→ All Sensors (GND)

SENSOR PINOUT (From top):
Pin 1: +12V (from external power supply)
Pin 2: GND  (to common ground)
Pin 3: A    (to RS-485 Line A)
Pin 4: B    (to RS-485 Line B)
Pin 5: GND  (to common ground)
Pins 6-7: Not used
```

### Step-by-Step Wiring Instructions

**1. Raspberry Pi to RS-485 Converter:**
- Pi GPIO14 → RS-485 Pin 4 (DI)
- Pi GPIO15 → RS-485 Pin 1 (RO)
- Pi GPIO17 → RS-485 Pins 2 & 3 (DE & RE)
- Pi GND → RS-485 Pin 5 (GND)

**2. RS-485 to Sensors (Parallel connection):**
- RS-485 Pin 7 (A) → ALL sensors Pin 3 (A)
- RS-485 Pin 8 (B) → ALL sensors Pin 4 (B)
- Common GND → ALL sensors Pins 2 & 5

**3. Power Supply:**
- Sensors: Use 12V external power supply
- Raspberry Pi: Use 5V micro-USB power supply

---

## Deploying to Raspberry Pi

### Step 1: Prepare the Raspberry Pi

```bash
# SSH into your Raspberry Pi
ssh pi@raspberrypi.local
# Default password: raspberry

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and Git
sudo apt-get install python3 python3-pip python3-venv git -y

# Install dev tools (for GPIO)
sudo apt-get install python3-dev libffi-dev libssl-dev -y
```

### Step 2: Enable UART on Raspberry Pi

```bash
# Edit boot config
sudo nano /boot/config.txt
```

Add or uncomment these lines:
```
# Disable Bluetooth to free UART0
dtoverlay=disable-bt

# Enable UART
enable_uart=1
```

Save (Ctrl+X, Y, Enter) and reboot:
```bash
sudo reboot
```

### Step 3: Clone Project to Pi

```bash
# Create projects directory
mkdir -p ~/projects
cd ~/projects

# Clone the repository
git clone https://github.com/DebugDroid-15/mushroom.git
cd mushroom
```

### Step 4: Set Up Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure for Raspberry Pi

```bash
# Copy config
cp config.example.py calibration_config.py

# Edit configuration for Pi
nano calibration_config.py
```

**Important changes for Raspberry Pi:**
```python
SERIAL_PORT = "/dev/serial0"    # Use UART0 on Raspberry Pi
FLASK_HOST = "0.0.0.0"          # Listen on all interfaces
FLASK_PORT = 5000
```

Save the file.

### Step 6: Test Connection

```bash
# Make sure you're still in the venv
source venv/bin/activate

# Test sensor connection
python -c "from modbus_sensor import ModbusSensor; s = ModbusSensor(port='/dev/serial0'); print('Connected!')"
```

If successful, you'll see: `Connected!`

### Step 7: Run Application Manually (Test)

```bash
# Start the Flask server
python app.py
```

Access it from another device:
```
http://<pi-ip-address>:5000
```

Find your Pi's IP: `hostname -I`

### Step 8: Set Up Auto-Start (Systemd Service)

```bash
# Stop the running app (Ctrl+C)

# Copy service file
sudo cp soil-monitor.service /etc/systemd/system/

# Edit it to set correct user and path
sudo nano /etc/systemd/system/soil-monitor.service
```

**Update these lines:**
```ini
[Service]
User=pi
WorkingDirectory=/home/pi/projects/mushroom
ExecStart=/home/pi/projects/mushroom/venv/bin/python app.py
```

Save and enable:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start
sudo systemctl enable soil-monitor

# Start the service
sudo systemctl start soil-monitor

# Check status
sudo systemctl status soil-monitor

# View logs (real-time)
sudo journalctl -u soil-monitor -f
```

---

## Testing & Troubleshooting

### Test 1: Verify UART is Enabled

```bash
# Check if serial port exists
ls -l /dev/serial0

# Should output: /dev/serial0 -> ttyAMA0
```

If it doesn't exist, you didn't enable UART properly. Go back to **Step 2: Enable UART**.

### Test 2: Verify Sensor Connection

```bash
# Activate venv
source venv/bin/activate

# Test Modbus connection
python quick_sensor_test.py
```

**Expected output:**
```
Testing Sensor 1...
NPK Values: N=150, P=80, K=200
Status: ✓ Success
```

If it fails, check:
- ✓ Wiring is correct
- ✓ Sensors have power (+12V)
- ✓ RS-485 converter is powered
- ✓ Baud rate matches sensor specs (usually 9600)

### Test 3: Flask Web Server

```bash
# Start app
python app.py

# Open browser
http://localhost:5000
```

**Should show:** Real-time dashboard with sensor readings

### Test 4: API Endpoint

```bash
# In another terminal, test API
curl http://localhost:5000/api/sensors

# Should return JSON with all sensor data
```

### Common Issues & Fixes

**Issue 1: "ModuleNotFoundError: No module named 'pymodbus'"**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue 2: "Permission denied: /dev/serial0"**
```bash
# Solution: Add user to dialout group
sudo usermod -a -G dialout pi
# Logout and login again
```

**Issue 3: "Connection timeout on sensor"**
- Check wiring (especially A/B lines)
- Verify +12V power to sensors
- Test with continuity meter if available
- Check GPIO17 is connected to both DE and RE pins

**Issue 4: "CORS error when accessing from another device"**
- This is expected; the dashboard works when accessed from Pi itself
- Use the REST API: `/api/sensors` for remote access

---

## Updating the System

### Update Code from GitHub

```bash
cd ~/projects/mushroom

# Pull latest changes
git pull origin main

# If you modified files, stash them first
git stash
git pull origin main
git stash pop
```

### Update Dependencies

```bash
# Activate venv
source venv/bin/activate

# Update packages
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl restart soil-monitor
```

### Rollback to Previous Version

```bash
# See commit history
git log --oneline

# Go back to specific commit
git checkout <commit-hash>

# Restart service
sudo systemctl restart soil-monitor
```

---

## Project File Structure

```
mushroom/
├── app.py                       (Main Flask application)
├── modbus_sensor.py             (Modbus RTU driver)
├── calibration_config.py        (Your local configuration)
├── config.example.py            (Configuration template)
├── requirements.txt             (Python dependencies)
├── soil-monitor.service         (Systemd autostart)
├── templates/
│   └── dashboard.html           (Web dashboard)
├── COMPLETE_SETUP_GUIDE.md      (This file)
├── README.md                    (Quick start)
├── WIRING.md                    (Detailed wiring)
├── QUICKREF.md                  (Command reference)
└── DOCUMENTATION.md             (Full documentation)
```

---

## Quick Command Reference

### Virtual Environment
```bash
# Activate
source venv/bin/activate              # macOS/Linux
.\venv\Scripts\Activate.ps1            # Windows

# Deactivate
deactivate
```

### Git Operations
```bash
git clone <url>                        # Clone repo
git pull origin main                   # Update from GitHub
git status                             # Check status
git add .                              # Stage all changes
git commit -m "message"                # Commit
git push origin main                   # Push to GitHub
```

### Running the App
```bash
python app.py                          # Run Flask server
python quick_sensor_test.py            # Test sensors
curl http://localhost:5000/api/sensors # Test API
```

### Raspberry Pi Services
```bash
sudo systemctl start soil-monitor      # Start
sudo systemctl stop soil-monitor       # Stop
sudo systemctl status soil-monitor     # Check status
sudo systemctl restart soil-monitor    # Restart
sudo journalctl -u soil-monitor -f     # View logs
```

---

## Support & Debugging

### Enable Debug Mode (Temporary)

```python
# In app.py, change:
app.run(debug=True)

# This will show detailed error messages
# ONLY for development, disable for production!
```

### View Logs

**On Raspberry Pi:**
```bash
# Live service logs
sudo journalctl -u soil-monitor -f

# Last 100 lines
sudo journalctl -u soil-monitor -n 100

# Since last boot
sudo journalctl -u soil-monitor -b
```

### Hardware Diagnostics

```bash
# Check Pi CPU temp
vcgencmd measure_temp

# Check GPIO pins
gpio readall  # If wiringPi installed

# Test serial port directly
cat /dev/serial0  # Press Ctrl+C to stop
```

---

## Next Steps

1. ✅ **Set up your PC environment** (Follow Installation section)
2. ✅ **Test locally** before deploying to Pi
3. ✅ **Wire hardware carefully** (Triple-check wiring!)
4. ✅ **Deploy to Raspberry Pi** (Follow Deployment section)
5. ✅ **Monitor logs** for any issues
6. ✅ **Set up backups** of your configuration

---

## Additional Resources

- **Raspberry Pi Documentation:** https://www.raspberrypi.org/documentation/
- **UART/Serial Guide:** https://www.raspberrypi.org/documentation/configuration/uart.md
- **Modbus RTU Spec:** http://www.modbus.org/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **Pymodbus Documentation:** https://pymodbus.readthedocs.io/

---

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Last Updated:** February 25, 2026  
**Version:** 1.0.0  
**For Questions:** Check DOCUMENTATION.md or create an issue on GitHub

---

**Ready to get started?** Begin with [Installation on Your PC](#installation-on-your-pc) and follow in order! 🚀
