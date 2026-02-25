# 🌱 Complete Setup Guide - Soil Monitoring System

**A comprehensive guide for setting up the Soil Monitoring System from scratch on your local machine and Raspberry Pi.**

**Version:** 1.0.0 | **Last Updated:** February 25, 2026 | **Difficulty:** Intermediate

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Prerequisites](#prerequisites)
4. [Understanding the Technology Stack](#understanding-the-technology-stack)
5. [Installation on Your PC](#installation-on-your-pc)
6. [Understanding the Codebase](#understanding-the-codebase)
7. [Configuration Setup](#configuration-setup)
8. [Running Locally](#running-locally)
9. [API Reference](#api-reference)
10. [Hardware Setup for Raspberry Pi](#hardware-setup-for-raspberry-pi)
11. [RS-485 Protocol Deep Dive](#rs-485-protocol-deep-dive)
12. [Deploying to Raspberry Pi](#deploying-to-raspberry-pi)
13. [Testing & Troubleshooting](#testing--troubleshooting)
14. [Advanced Configuration](#advanced-configuration)
15. [Performance Optimization](#performance-optimization)
16. [Updating the System](#updating-the-system)
17. [Maintenance & Monitoring](#maintenance--monitoring)

---

## Project Overview

**Soil Monitoring System** is a production-ready Raspberry Pi application that:
- ✅ Monitors 4x NPK (Nitrogen, Phosphorus, Potassium) soil sensors
- ✅ Communicates via RS-485 Modbus RTU protocol
- ✅ Provides real-time web dashboard with live updates
- ✅ Offers REST API for programmatic data access
- ✅ Auto-starts on Pi boot via systemd service
- ✅ Handles disconnections and sensor failures gracefully
- ✅ Logs all sensor readings to persistent storage
- ✅ Supports multiple simultaneous connections

**Key Technologies:**
- **Python 3.7+** - Core language
- **Flask** - Lightweight web server and microframework
- **Pymodbus** - Modbus RTU protocol implementation
- **RPi.GPIO** - Raspberry Pi hardware control
- **JavaScript/HTML/CSS** - Dashboard frontend

**Typical Use Cases:**
- Agricultural greenhouse monitoring
- Research facility soil analysis
- Smart irrigation systems
- Environmental monitoring
- IoT data collection platforms

### What Makes This System Unique?

1. **Single Bus Architecture** - All 4 sensors share one RS-485 bus (more efficient than parallel connections)
2. **No Cloud Dependency** - Runs entirely on local network (privacy & reliability)
3. **Production Ready** - Includes systemd service, error handling, and logging
4. **Documented** - Complete hardware wiring diagrams and troubleshooting guides
5. **Extensible** - Easy to add more sensors (up to 247 on RS-485 bus)

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

## Understanding the Technology Stack

Before diving into installation, let's understand each component:

### Python (3.7+)

**What it is:** High-level programming language, perfect for IoT applications.

**Why Python?**
- Easy to read and maintain
- Excellent library ecosystem (Flask, Pymodbus, GPIO bindings)
- Rapid prototyping capability
- Great for Raspberry Pi applications

**Version Requirements:**
```bash
# Check your Python version
python --version  # Windows/macOS
python3 --version # Linux

# Should output: Python 3.7.0 or higher
```

### Flask Web Framework

**What it is:** Lightweight web server framework for building web applications.

**In this project:**
- Serves the web dashboard (HTML/CSS/JS)
- Provides REST API endpoints (`/api/sensors`, etc.)
- Handles HTTP requests and responses
- Serves static files (dashboard.html, stylesheets)

**Key Routes:**
```
GET  /              → Serves dashboard.html
GET  /api/sensors   → Returns JSON with all sensor data
GET  /api/sensor/<id> → Returns data for specific sensor
```

**Why Flask?**
- Minimal dependencies
- Fast to develop with
- Perfect for embedded systems (low memory footprint)
- Easy to understand and modify

### Pymodbus Library

**What it is:** Python library implementing the Modbus RTU protocol.

**What's Modbus?**
- Industrial communication protocol (de-facto standard since 1979)
- Designed for robust master-slave communication over serial lines
- Perfect for sensor networks
- Used in factories, power plants, water systems worldwide

**Modbus RTU Format:**
```
[Slave ID] [Function Code] [Data] [CRC Check]
   1 byte      1 byte      N bytes  2 bytes
```

**In this project:**
- Communicates with sensors using Modbus RTU
- Handles requests/responses automatically
- Includes CRC error checking for reliable transmission
- Library handles the complexity; you focus on data

### RS-485 Serial Communication

**What it is:** Serial communication standard optimized for noisy industrial environments.

**Advantages over standard UART:**
```
Characteristic      UART (TTL)          RS-485
─────────────────────────────────────────────────
Maximum distance    10 meters           1200+ meters
Noise immunity      Low                 Very High
Voltage tolerance   ±5V                 ±30V
Connections         Point-to-point      Multi-drop (bus)
Wiring              2 wires             2 wires (twisted pair)
Cost                Lower               Higher (better reliability)
```

**In this project:**
- Connects 4 sensors on a single bus (more efficient than 4 separate connections)
- Uses twisted pair cables (A/B lines) for noise immunity
- MAX485/SP3485 converter chip bridges Raspberry Pi's UART to RS-485
- Can be extended to 247 devices on same bus

### GPIO (General Purpose Input/Output)

**What it is:** Digital input/output pins on Raspberry Pi.

**In this project:**
- GPIO17 controls RS-485 converter's DE and RE (Driver Enable / Receiver Enable) pins
- Tells converter whether to transmit or receive
- Critical for half-duplex RS-485 communication

### Systemd (Service Management)

**What it is:** System and service manager for Linux/Raspberry Pi OS.

**Why systemd?**
- Automatically starts service on boot
- Restarts service if it crashes (ensures 24/7 operation)
- Manages logs automatically (centralized to system journal)
- Standard on all modern Linux distributions
- provides restart policies, dependency management, and more

**In this project:**
- Keeps your application running 24/7 without manual intervention
- Auto-recovery on failures (configurable restart behavior)
- Easy to start/stop/check status with simple commands
- Integrated logging via journalctl

---

## Prerequisites

### For Your PC (Windows/Mac/Linux)

1. **Python 3.7 or higher**
   - Download from: https://www.python.org/downloads/
   - **Windows users:** Check "Add Python to PATH" during installation
   - Verify: `python --version`
   - Recommended: Python 3.8, 3.9, or 3.10+ for best compatibility

2. **Git (Version Control)**
   - Download from: https://git-scm.com/
   - Used to clone the project repository from GitHub
   - Verify: `git --version`
   - Recommended: Git 2.25+

3. **Text Editor or IDE** (optional but recommended)
   - **VS Code** (Recommended): https://code.visualstudio.com/
     - Install Python extension (by Microsoft)
     - Install Pylance for advanced features
   - **PyCharm Community**: https://www.jetbrains.com/pycharm/
     - Full-featured IDE for Python
   - **Sublime Text**: https://www.sublimetext.com/
     - Lightweight, paid license recommended

4. **Terminal/Command Line Access**
   - **Windows:** PowerShell (comes built-in) or Windows Terminal
   - **macOS:** Terminal app
   - **Linux:** Any terminal emulator

5. **Internet Connection**
   - Required for downloading dependencies
   - Required for cloning GitHub repository
   - Required for Raspberry Pi deployment

### For Raspberry Pi (Production Deployment)

1. **Raspberry Pi Hardware**
   - **Minimum:** Raspberry Pi 3B+ (1GB RAM)
   - **Recommended:** Raspberry Pi 4B (2GB RAM) or newer
   - **Storage:** MicroSD Card 16GB+ (Class 10 recommended)

2. **Raspberry Pi Operating System**
   - Download from: https://www.raspberrypi.org/software/
   - **Option 1:** Raspberry Pi OS Lite (headless, ~1GB) - Recommended for production
   - **Option 2:** Raspberry Pi OS Desktop (with GUI, ~3GB) - Easier for learning
   - Both 32-bit and 64-bit versions work; 64-bit recommended for Pi 4

3. **Network Setup**
   - **WiFi:** Built-in on Pi 3B+ and newer
   - **Ethernet:** Recommended for stability and speed
   - IP address to identify Pi on network
   - SSH access for remote management

4. **Power Supply**
   - **Raspberry Pi:** 5V 2.5A minimum (3A recommended)
   - **Sensors:** 12V power supply (external from Pi)
   - **RS-485 Converter:** 3.3V-5V (from Pi) or separate supply

### Hardware Components for Sensor Network

1. **RS-485 Converter Module**
   - **Common Models:** MAX485, SP3485, SN65HVD11
   - **Voltage:** 3.3V or 5V compatible
   - **Function:** Bridges Raspberry Pi's UART to RS-485 bus
   - **Cost:** $2-5 USD

2. **NPK Soil Sensors**
   - **Recommended Model:** DFRobot SEN0189 (Capacitive)
   - **Specifications:**
     - Modbus RTU protocol compatible
     - 12V operating voltage
     - IP68 waterproof (suitable for soil)
     - Measure: Nitrogen (N), Phosphorus (P), Potassium (K)
   - **Quantity:** 4 sensors (expandable to 247)
   - **Cost:** $25-40 USD per sensor

3. **Cabling & Connectors**
   - **RS-485 Bus:** Twisted pair shielded cable (A/B lines)
   - **Sensor Connections:** Screw terminals or connectors
   - **Jumper Wires:** Mix of M-M and F-F connectors
   - **Recommended:** AWG 20-22 for 12V power, AWG 24-26 for RS-485

4. **Power Supplies**
   - **Raspberry Pi:** 5V micro-USB or USB-C (2.5-3A)
   - **Sensors:** 12V DC power supply (2A+ depending on sensor count)
   - Consider using regulated supplies to avoid noise issues

5. **Tools (Optional but helpful)**
   - Multimeter (for troubleshooting electrical issues)
   - Continuity tester (check cable connections)
   - Oscilloscope (advanced: see RS-485 signal quality)
   - Cable tester (for twisted pair integrity)

### Software Requirements Summary

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.7+ | Core programming language |
| Flask | 2.0+ | Web server framework |
| Pymodbus | 3.1+ | Modbus RTU protocol |
| RPi.GPIO | 0.7.0 | GPIO control (Pi only) |
| pip | Latest | Python package manager |
| Git | 2.25+ | Version control |

### Learning Prerequisites (Helpful to Know)

Before starting, it helps to understand:

1. **Basic Python** - Variables, functions, loops, dictionaries
2. **Command Line Basics** - Working with terminal/PowerShell
3. **Networking Concepts** - IP addresses, ports, HTTP
4. **Serial Communication** - UART, baud rates, data frames
5. **Version Control** - Git basics (clone, pull, push)

**Don't know these?** That's okay! We'll explain as we go, but consider:
- Python tutorial: https://www.python.org/about/gettingstarted/
- Git basics: https://git-scm.com/book/en/v2
- Networking: https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13769-5.html

---

---

## Understanding the Codebase

Before installing, let's understand the project structure and main components:

### File Structure & Purpose

```
mushroom/
├── app.py                          (Main Flask Application)
├── modbus_sensor.py                (Modbus RTU Communication Driver)
├── ambient_sensor.py               (Environmental Sensor Module) 
├── sensor_scanner.py               (Scan & Detect Sensors on Bus)
├── quick_sensor_test.py            (Simple Testing Script)
├── test_hardware.py                (Hardware Diagnostics)
│
├── templates/
│   └── dashboard.html              (Web Dashboard UI)
│   └── dashboard_minimal.html      (Minimal version)
│
├── config.example.py               (Configuration Template)
├── calibration_config.py           (Your Local Configuration)
│   └── [COPY THIS AND CUSTOMIZE]
│
├── requirements.txt                (Python Dependencies)
├── soil-monitor.service            (Systemd Auto-Start Service)
│
├── install.sh                      (Automated Pi Setup Script)
├── dev.sh                          (Development Helper)
├── deploy.sh                       (Deployment Script)
│
├── COMPLETE_SETUP_GUIDE.md         (This File!)
├── README.md                       (Quick Start)
├── DOCUMENTATION.md                (Full Technical Docs)
├── WIRING.md                       (Hardware Wiring Guide)
└── QUICKREF.md                     (Command Reference)
```

### Core Files Explained

#### 1. **app.py** (Main Application)

This is the heart of the system. It:

```python
# Starts Flask web server
# Initializes Modbus communication
# Defines API endpoints
# Serves the dashboard
# Handles requests from browsers
```

**Key Functions:**
- `@app.route('/')` - Serves dashboard.html
- `@app.route('/api/sensors')` - Returns all sensor data as JSON
- `read_sensors()` - Periodically polls sensors
- The server listens on port 5000 by default

**How it works:**
1. Flask starts listening on 0.0.0.0:5000
2. When you visit http://localhost:5000, it serves dashboard.html
3. Dashboard JS fetches data from /api/sensors every 5 seconds
4. Data is displayed in real-time charts

#### 2. **modbus_sensor.py** (Sensor Communication Driver)

This module handles all RS-485/Modbus communication. It:

```python
# Establishes serial connection to RS-485 converter
# Sends Modbus RTU requests to sensors
# Reads and parses sensor responses
# Handles errors and timeouts
# Implements CRC checking
```

**Key Classes:**
- `ModbusSensor` - Main class for sensor communication
- Methods: `connect()`, `read_registers()`, `get_npk_values()`
- Handles multiple sensors with different slave IDs

**How it works:**
1. Opens serial port at configured speed (9600 baud)
2. Sends Modbus request: `[Slave ID][Function Code][Data][CRC]`
3. Waits for response from sensor
4. Parses response and returns NPK values
5. Handles timeouts and CRC errors

**Example Code Flow:**
```python
sensor = ModbusSensor(port='/dev/serial0', baud_rate=9600)
sensor.connect()
nitrogen, phosphorus, potassium = sensor.get_npk_values(slave_id=1)
sensor.close()
```

#### 3. **config_example.py & calibration_config.py**

Configuration file that defines:
- Serial port and baud rate
- Sensor addresses (slave IDs 1-4)
- Calibration values (min/max ranges)
- Flask server settings
- Logging configuration

**Important:** 
- `config.example.py` is the template
- `calibration_config.py` is where YOU put your specific settings
- Never commit `calibration_config.py` to Git (contains local config)

#### 4. **templates/dashboard.html** (Web Interface)

The user-facing dashboard that:
- Displays real-time sensor readings
- Shows graphs and charts
- Updates every 5 seconds via AJAX
- Works in any web browser
- Responsive design (mobile-friendly)

**Technologies Used:**
- HTML5 for structure
- CSS3 for styling
- Chart.js for graphs
- JavaScript for real-time updates

#### 5. **soil-monitor.service** (Auto-Start Service)

Systemd service file that:
- Starts application automatically on Pi boot
- Restarts if application crashes
- Manages logging
- Provides start/stop/restart commands

**Key Sections:**
```ini
[Unit]          - Service metadata
[Service]       - How to run the service
[Install]       - Auto-start configuration
```

### How Components Work Together

```
┌─────────────────────────────────────────────────┐
│  Your Browser                                   │
│  ┌──────────────────────────────┐              │
│  │ dashboard.html               │              │
│  │ (HTML/CSS/JavaScript)        │              │
│  └──────────────┬───────────────┘              │
└────────────────┼──────────────────────────────┘
                 │ HTTP Requests
                 │ GET /api/sensors
                 ↓
      ┌─────────────────────────────┐
      │  Flask Web Server (app.py)  │
      │  - Listen on port 5000      │
      │  - Handle HTTP requests     │
      │  - Return JSON responses    │
      └────────────┬────────────────┘
                   │ Poll (every 5 sec)
                   ↓
      ┌─────────────────────────────┐
      │  modbus_sensor.py (Driver)  │
      │  - Modbus RTU protocol      │
      │  - CRC checking             │
      │  - Timeout handling         │
      └────────────┬────────────────┘
                   │ RS-485 Communication
                   │ (Modbus RTU)
                   ↓
      ┌─────────────────────────────┐
      │  RS-485 Converter (GPIO17)  │
      │  Raspberry Pi TTL → RS-485  │
      └────────────┬────────────────┘
                   │ Twisted Pair Cables
                   │ (A/B lines)
                   ↓
      ┌─────────────────────────────┐
      │  NPK Soil Sensors (1-4)     │
      │  Modbus Slave IDs: 1,2,3,4  │
      │  Measure: N, P, K values    │
      └─────────────────────────────┘
```

### Data Flow Example

```
1. Browser requests: GET /api/sensors
2. Flask route handler calls: read_sensors()
3. modbus_sensor.py connects to /dev/serial0
4. Sends Modbus request to Sensor 1 (Slave ID=1):
   [0x01][0x03][0x00...][CRC]
5. Sensor responds with NPK values
6. Parse response and store values
7. Repeat for Sensors 2, 3, 4
8. Return JSON: {"sensor_1": {N:150, P:80, K:200}, ...}
9. JavaScript receives JSON and updates charts
10. Browser displays new data
```

### Important Concepts

**Slave ID (Modbus Address)**
- Each sensor has a unique ID (1-4 by default, configurable to 247)
- Used to identify which sensor to communicate with
- Set in sensor's DIP switches or software

**Modbus Function Code**
- 0x03 = Read Holding Registers (standard for sensor values)
- 0x10 = Write Multiple Registers (for configuration)

**Baud Rate**
- Speed of serial communication (bits per second)
- Standard for sensors: 9600 baud
- Both converter and sensor must match!

**GPIO17 (Control Pin)**
- Controls RS-485 converter's DE and RE pins
- High = Transmit mode
- Low = Receive mode
- Critical for half-duplex operation

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

## API Reference

The system provides a REST API for programmatic access to sensor data. Use these endpoints to integrate with other systems.

### Base URL

```
http://localhost:5000  (development)
http://<pi-ip>:5000    (production on Pi)
```

### Endpoints

#### 1. Get All Sensors Data

**Endpoint:**
```
GET /api/sensors
```

**Description:** Returns current NPK values for all sensors.

**Response (200 OK):**
```json
{
  "success": true,
  "timestamp": "2026-02-25T10:30:45.123Z",
  "sensors": {
    "1": {
      "name": "Sensor 1",
      "location": "Zone A",
      "nitrogen": 150,
      "phosphorus": 80,
      "potassium": 200,
      "last_update": "2026-02-25T10:30:40.000Z",
      "status": "OK"
    },
    "2": {
      "name": "Sensor 2",
      "location": "Zone B",
      "nitrogen": 175,
      "phosphorus": 92,
      "potassium": 210,
      "last_update": "2026-02-25T10:30:40.000Z",
      "status": "OK"
    }
  }
}
```

**Example Usage:**
```bash
curl http://localhost:5000/api/sensors

# With Python
import requests
response = requests.get('http://localhost:5000/api/sensors')
data = response.json()
print(data['sensors']['1']['nitrogen'])
```

#### 2. Get Single Sensor Data

**Endpoint:**
```
GET /api/sensor/<sensor_id>
```

**Parameters:**
- `sensor_id` (integer): 1, 2, 3, or 4

**Response (200 OK):**
```json
{
  "success": true,
  "sensor_id": 1,
  "name": "Sensor 1",
  "location": "Zone A",
  "nitrogen": 150,
  "phosphorus": 80,
  "potassium": 200,
  "last_update": "2026-02-25T10:30:40.000Z",
  "status": "OK"
}
```

**Example Usage:**
```bash
curl http://localhost:5000/api/sensor/1

# Get sensor 2
curl http://localhost:5000/api/sensor/2
```

#### 3. Get Sensor History (if implemented)

**Endpoint:**
```
GET /api/sensor/<sensor_id>/history?hours=24
```

**Parameters:**
- `sensor_id`: Sensor ID (1-4)
- `hours`: Number of hours of history (optional, default: 24)

**Response (200 OK):**
```json
{
  "success": true,
  "sensor_id": 1,
  "timeframe_hours": 24,
  "data_points": 288,
  "measurements": [
    {"timestamp": "2026-02-24T10:30:00Z", "nitrogen": 145, "phosphorus": 78, "potassium": 195},
    {"timestamp": "2026-02-24T10:35:00Z", "nitrogen": 148, "phosphorus": 79, "potassium": 197}
  ]
}
```

### Error Responses

**Sensor Not Responding (504 Gateway Timeout):**
```json
{
  "success": false,
  "error": "Sensor 1 did not respond",
  "sensor_id": 1,
  "status": "OFFLINE"
}
```

**Invalid Sensor ID (400 Bad Request):**
```json
{
  "success": false,
  "error": "Invalid sensor ID. Must be 1-4",
  "received": 5
}
```

**Server Error (500 Internal Server Error):**
```json
{
  "success": false,
  "error": "Serial port error: Permission denied"
}
```

### Rate Limiting

- No rate limiting implemented (modify `app.py` if needed for security)
- Sensor polling interval: 5 seconds
- API calls can be made more frequently without issues

### Data Formats

#### NPK Values

Values are typically in the range 0-1000 (mg/kg or similar):
- **0-100:** Very low
- **100-300:** Low
- **300-600:** Medium
- **600-900:** High
- **900+:** Very high

Values depend on sensor calibration and soil type.

#### Timestamps

All timestamps are in ISO 8601 format with UTC timezone:
```
2026-02-25T10:30:45.123Z
```

#### Status Values

- `OK`: Sensor responding normally
- `OFFLINE`: No response from sensor
- `ERROR`: Modbus error
- `TIMEOUT`: Communication timeout

### Integration Examples

#### Python Integration

```python
import requests
import json
from datetime import datetime

def get_all_sensors():
    """Fetch all sensor data"""
    response = requests.get('http://localhost:5000/api/sensors')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def check_nitrogen_levels(threshold=300):
    """Alert if any sensor's nitrogen is below threshold"""
    data = get_all_sensors()
    if not data['success']:
        return
    
    for sensor_id, sensor_data in data['sensors'].items():
        if sensor_data['nitrogen'] < threshold:
            print(f"ALERT: {sensor_data['name']} nitrogen is low!")

# Example usage
if __name__ == "__main__":
    data = get_all_sensors()
    print(json.dumps(data, indent=2))
```

#### JavaScript Integration

```javascript
// Fetch sensor data and update every 5 seconds
async function updateSensorData() {
    try {
        const response = await fetch('/api/sensors');
        const data = await response.json();
        
        if (data.success) {
            Object.entries(data.sensors).forEach(([id, sensor]) => {
                console.log(`${sensor.name}: N=${sensor.nitrogen}  P=${sensor.phosphorus}  K=${sensor.potassium}`);
            });
        }
    } catch (error) {
        console.error('Failed to fetch sensor data:', error);
    }
}

// Poll every 5 seconds
setInterval(updateSensorData, 5000);
updateSensorData(); // Initial call
```

#### MQTT Integration (Advanced)

```python
import paho.mqtt.client as mqtt
import requests
import json

def publish_to_mqtt():
    client = mqtt.Client()
    client.connect("mqtt-broker.local", 1883, 60)
    
    response = requests.get('http://localhost:5000/api/sensors')
    data = response.json()
    
    for sensor_id, sensor_data in data['sensors'].items():
        topic = f"soil_monitor/sensor/{sensor_id}"
        payload = json.dumps(sensor_data)
        client.publish(topic, payload)
    
    client.disconnect()

# Publish every minute
import schedule
schedule.every(1).minute.do(publish_to_mqtt)
```

---

## RS-485 Protocol Deep Dive

Understanding RS-485 and Modbus will help you troubleshoot issues and optimize performance.

### RS-485 Physical Layer

#### Signal Characteristics

RS-485 uses **differential signaling:**
```
Voltage = V_A - V_B

Normal state (Idle):    V_A ≈ V_B
Logic 1 (Mark):         V_A - V_B ≈ +1.5V to +6V  (or more)
Logic 0 (Space):        V_A - V_B ≈ -6V to -1.5V
```

#### Cable Requirements

**Twisted Pair Shielded Cable:**
- Twist pairs together to cancel electromagnetic noise
- Use shielded cable for long runs (>10m) or noisy environments
- Shield connected to ground at ONE end only (prevents ground loops)

**Impedance Matching:**
- RS-485 cable impedance: typically 120 ohms
- Terminal resistors (120Ω) at both bus ends reduce reflections
- Without terminators: signal reflections cause communication errors

**Maximum Cable Length:**
- Standard: 1200 meters at 9600 baud
- Shorter distances at faster baud rates
- Shielded cable allows longer runs

#### Half-Duplex Operation

RS-485 is **half-duplex**: either transmit OR receive, not both simultaneously.

```
Time ──────────────────────────────────────→

Master TX: [Request to Sensor 1]
Sensors:   [Listening...]
           ↓
Master RX: [Waiting for response]
Sensor 1 TX: [Response with NPK values]

This is why GPIO17 (DE/RE control) is critical!
```

### Modbus RTU Protocol

#### Frame Structure

Every Modbus RTU message follows this format:

```
┌─────────┬──────────┬──────────┬──────┬──────┐
│ Slave ID│ Function │  Data    │ CRC  │ Gap  │
│ 1 byte  │ 1 byte   │ N bytes  │ 2 by │ >= 3 │
└─────────┴──────────┴──────────┴──────┴──────┘

Example (Read Sensor 1 NPK):
01 03 00 00 00 03 44 09
```

**Breakdown:**
- `01` = Slave ID (Sensor 1)
- `03` = Function code (Read Holding Registers)
- `00 00` = Starting register address (0x0000)
- `00 03` = Number of registers to read (3 registers)
- `44 09` = CRC checksum (calculated automatically)

#### Function Codes

Common function codes:

| Code | Function | Use Case |
|------|----------|----------|
| 0x03 | Read Holding Registers | Read NPK values |
| 0x04 | Read Input Registers | Read sensor status |
| 0x10 | Write Multiple Registers | Configure sensor |
| 0x06 | Write Single Register | Set single value |

Sensor documentation specifies which function codes and registers correspond to NPK values.

#### CRC Calculation

CRC (Cyclic Redundancy Check) detects transmission errors:

```python
def calculate_crc(data):
    """Calculate CRC-16-CCITT checksum"""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, 'little')

# Pymodbus handles this automatically!
```

#### Message Timeout

If sensor doesn't respond within timeout:
```python
TIMEOUT = 1  # seconds
# After 1 second with no response, consider sensor offline
```

### Debugging RS-485 Issues

#### Using pyserial to Monitor Traffic

```python
import serial
import time

# Open serial port and monitor raw data
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            print(f"RX: {data.hex()}")
        time.sleep(0.1)
finally:
    ser.close()
```

#### Oscilloscope Analysis (Advanced)

If you have access to an oscilloscope, probe the RS-485 A/B lines:

```
Expected RS-485 signal:
┌─────────────┬─────────────┐
│   Idle      │   Data      │
│  (±0V)      │ (±3-5V)     │
└─────────────┴─────────────┘

Signs of problems:
- Ringing (oscillation after transitions)  → Cable too long or no terminator
- Weak signal (<2V differential)  → Drive issue or too much capacitive load
- Noise spikes  → EMI interference, poor shielding
```

#### Common Issues & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Frequent timeouts | No terminator | Add 120Ω resistors at both bus ends |
| Intermittent errors | Loose connections | Check all connectors and solder joints |
| High error rate | Baud rate mismatch | Verify sensor and Pi both use 9600 |
| Weak signal | Cable too long | Use shielded cable, reduce distance |
| CRC errors | Noise/interference | Use twisted pair, improve shielding |

---

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

## Advanced Configuration

### Extending to More Sensors

The current setup supports 4 sensors, but Modbus RTU allows up to 247 devices on a single bus!

#### Adding Sensor 5 and Beyond

**Step 1: Set Sensor IDs (on each sensor)**
```
Sensor 1: Slave ID = 1
Sensor 2: Slave ID = 2
Sensor 3: Slave ID = 3
Sensor 4: Slave ID = 4
Sensor 5: Slave ID = 5  (new)
Sensor 6: Slave ID = 6  (new)
...
```

Most sensors use DIP switches on the device to set the ID. Check your sensor's manual.

**Step 2: Update calibration_config.py**
```python
SENSORS = {
    1: {"name": "Sensor 1", "location": "Zone A"},
    2: {"name": "Sensor 2", "location": "Zone B"},
    3: {"name": "Sensor 3", "location": "Zone C"},
    4: {"name": "Sensor 4", "location": "Zone D"},
    5: {"name": "Sensor 5", "location": "Zone E"},  # Add new sensors
    6: {"name": "Sensor 6", "location": "Zone F"},
}
```

**Step 3: Update app.py (if needed)**
The app automatically loops through all sensors in the config, so no code changes needed!

**Step 4: Wire sensors in parallel**
```
All sensors A pins → RS-485 Pin 7 (A)
All sensors B pins → RS-485 Pin 8 (B)
All sensors GND → Common ground
```

#### RS-485 Bus Length Limits

| Baud Rate | Max Cable Length | Notes |
|-----------|-----------------|-------|
| 9600      | 1200m           | Standard |
| 19200     | 600m            | Faster but shorter |
| 38400     | 300m            | Fast, short only |

**For runs > 300m:**
- Use repeaters (RS-485 signal regenerators)
- Use higher gauge wire (lower resistance)
- Consider fiber optic converters (very long distances)

### Custom Sensor Registers

Different sensor models may store NPK values in different Modbus registers. To find them:

```python
# In modbus_sensor.py, modify read_npk_values():
def read_npk_values(self, slave_id):
    # Default assumes: registers 0x00=N, 0x01=P, 0x02=K
    # For custom sensor, check datasheet for register map
    
    # Example: if your sensor uses 0x0100 for N
    n_register = 0x0100
    p_register = 0x0101
    k_register = 0x0102
    
    # Use sensor's actual register addresses
    # Ask sensor manufacturer or check datasheet
```

### Changing Baud Rate

To use a faster baud rate (if your sensor supports it):

```python
# In calibration_config.py
BAUD_RATE = 19200  # Change from 9600

# Then:
# 1. Update sensor's baud rate (usually via DIP switch or software)
# 2. Restart application
# 3. Test with quick_sensor_test.py
```

**Warning:** If baud rates don't match, you'll get timeout errors!

### Custom Flask Endpoints

Add your own endpoints to `app.py`:

```python
@app.route('/api/export/<format>')
def export_data(format):
    """Export sensor data in various formats"""
    sensors_data = read_sensors()
    
    if format == 'csv':
        # Return CSV format
        return '...'
    elif format == 'json':
        return sensors_data
    else:
        return {'error': 'Unknown format'}, 400
```

### SSL/HTTPS Support

For secure remote access:

```python
# Generate self-signed certificate
# openssl req -x509 -newkey rsa:2048 -nodes -out cert.pem -keyout key.pem -days 365

# In app.py:
app.run(
    host='0.0.0.0',
    port=443,
    ssl_context=('cert.pem', 'key.pem'),
    debug=False
)
```

---

## Performance Optimization

### Reducing Sensor Poll Interval

By default, sensors are polled every 5 seconds. To make it faster or slower:

```python
# In app.py, find:
POLL_INTERVAL = 5  # seconds

# Change to:
POLL_INTERVAL = 2  # faster (more responsive, more traffic)
# OR
POLL_INTERVAL = 10  # slower (less frequent updates, less traffic)
```

**Trade-offs:**
- Faster polling: More responsive but more strain on serial port
- Slower polling: Less responsive but uses less power/network

### Optimizing Memory Usage

On Raspberry Pi with limited RAM, optimize memory:

```python
# In app.py, limit stored history
MAX_HISTORY_POINTS = 100  # Store only last 100 readings per sensor
# Older readings automatically deleted

# Reduce dashboard update frequency
DASHBOARD_UPDATE_INTERVAL = 10  # seconds (instead of 5)
```

### Increasing Buffer Sizes

For noisy environments, increase serial buffer:

```python
# In modbus_sensor.py
import serial

self.port = serial.Serial(
    port=self.port_name,
    baudrate=self.baud_rate,
    timeout=self.timeout,
    write_timeout=1,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False,
    inter_byte_timeout=1000  # Increase this value
)
```

### Caching Responses

Avoid repeated sensor reads for the same data:

```python
# In app.py
from functools import lru_cache
from time import time

CACHE_TIME = 2  # seconds

class SensorCache:
    def __init__(self):
        self.data = None
        self.last_update = 0
    
    def get(self):
        now = time()
        if now - self.last_update > CACHE_TIME:
            self.data = read_sensors()
            self.last_update = now
        return self.data
```

### Database Logging (Advanced)

Store readings in SQLite for historical analysis:

```python
import sqlite3
import json

class SensorLog:
    def __init__(self, db_file='sensors.db'):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                sensor_id INT,
                nitrogen INT,
                phosphorus INT,
                potassium INT
            )
        ''')
        self.db.commit()
    
    def log_reading(self, sensor_id, n, p, k):
        self.db.execute(
            'INSERT INTO readings (sensor_id, nitrogen, phosphorus, potassium) VALUES (?, ?, ?, ?)',
            (sensor_id, n, p, k)
        )
        self.db.commit()

# Use in app.py
logger = SensorLog()
for sensor_id, values in sensors_data.items():
    logger.log_reading(sensor_id, values['N'], values['P'], values['K'])
```

---

## Maintenance & Monitoring

### Regular Maintenance Schedule

| Task | Frequency | Importance |
|------|-----------|-----------|
| Check sensor readings | Daily | Critical |
| Verify all sensors responding | Weekly | Critical |
| Clean sensor probes | Monthly | High |
| Backup configuration | Monthly | High |
| Update software | Quarterly | Medium |
| Check power supplies | Quarterly | High |
| Test failover/recovery | Quarterly | Medium |
| Review logs for errors | Weekly | Medium |

### Sensor Maintenance

**Cleaning Sensor Probes:**
```
1. Stop the application
2. Carefully remove sensor from soil
3. Rinse with distilled water (NOT tap water - minerals interfere!)
4. Gently dry with soft cloth
5. Reinstall and restart app
```

**Storage:**
- Store in cool, dry place
- Keep probes moist if storing long-term
- Avoid direct sunlight

### Backup & Restore Configuration

**Creating Backup:**
```bash
# On Raspberry Pi
cp ~/projects/mushroom/calibration_config.py ~/backups/calibration_config.backup.py
tar -czf ~/backups/soil-monitor-$(date +%Y%m%d).tar.gz ~/projects/mushroom/
```

**Restoring from Backup:**
```bash
# If something goes wrong
cd ~/projects
tar -xzf ~/backups/soil-monitor-YYYYMMDD.tar.gz
sudo systemctl restart soil-monitor
```

### Reading Systemd Logs

Monitor service health:

```bash
# Real-time log following
sudo journalctl -u soil-monitor -f

# Last 50 lines
sudo journalctl -u soil-monitor -n 50

# Since last boot
sudo journalctl -u soil-monitor -b

# Errors only
sudo journalctl -u soil-monitor -p err

# Date range
sudo journalctl -u soil-monitor --since "2026-02-20" --until "2026-02-25"

# Export to file
sudo journalctl -u soil-monitor > sensor_logs.txt
```

### Monitoring System Resources

```bash
# CPU and memory usage
top

# Disk usage
df -h

# Temperature
vcgencmd measure_temp

# Check systemd service status
sudo systemctl status soil-monitor

# Auto-restart logs
sudo systemctl status soil-monitor | grep Restart
```

### Alerting on Problems

Setup email alerts with Python (advanced):

```python
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, message):
    """Send email alert for critical issues"""
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'pi@raspberrypi.local'
    msg['To'] = 'admin@example.com'
    
    # Send via SMTP (configure with your email provider)
    # s = smtplib.SMTP('smtp.gmail.com', 587)
    # s.starttls()
    # s.login('your_email', 'your_password')
    # s.send_message(msg)
    # s.quit()

# In app.py, call when sensor offline:
if sensor_status == 'OFFLINE':
    send_alert('Soil Monitor Alert', f'Sensor {id} is offline!')
```

### Performance Metrics to Monitor

Track these metrics for system health:

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Sensor response time | <100ms | 100-500ms | >500ms |
| API response time | <500ms | 500-2000ms | >2000ms |
| CPU usage | <20% | 20-50% | >50% |
| RAM usage | <50% | 50-70% | >70% |
| Disk usage | <50% | 50-80% | >80% |
| Serial error rate | 0% | <5% | >5% |
| Uptime | 99%+ | 95-99% | <95% |

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
