# Soil Monitoring System - Raspberry Pi Deployment

## Quick Start

### 1. Prerequisites
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv git
```

### 2. Install Python Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install pymodbus flask
```

### 3. Hardware Setup

#### RS-485 Converter Wiring (MAX485/SP3485)
```
Pi GPIO17 (DE/RE) ← RS-485 Module Pin 2 (DE)
Pi GPIO17 (DE/RE) ← RS-485 Module Pin 3 (RE)
Pi GPIO (TX)      ← RS-485 Module Pin 4 (DI)
Pi GPIO (RX)      ← RS-485 Module Pin 1 (RO)
Pi GND            ← RS-485 Module Pin 5 (GND)
+5V               ← RS-485 Module Pin 8 (VCC)

Pi /dev/serial0 (UART0 - GPIO14, GPIO15)
A-line (Blue)     ← All sensors connected (twisted pair)
B-line (White)    ← All sensors connected (twisted pair)
GND (Black/Brown) ← All sensors + common ground
```

#### Sensor Wiring
Each sensor has 7 pins (verify with your datasheet):
- Pin 1: +12V (external power supply)
- Pin 2: GND (common ground)
- Pin 3: A (RS-485, connect to converter A)
- Pin 4: B (RS-485, connect to converter B)
- Pin 5: GND (connect to common ground)
- Pins 6-7: Not typically used

### 4. Enable UART on Raspberry Pi
```bash
# Edit boot config
sudo nano /boot/config.txt

# Add or uncomment these lines:
# dtoverlay=disable-bt  # Disable Bluetooth to free UART0
# enable_uart=1

sudo reboot
```

Verify UART is available:
```bash
ls -l /dev/serial0
# Should show: /dev/serial0 -> ttyAMA0
```

### 5. Test Modbus Connection
```bash
python3 modbus_sensor.py
```

You should see output like:
```
Sensor 1:
  N: 185.5 mg/kg
  P: 142.3 mg/kg
  K: 210.7 mg/kg
  Moisture: 65.4%
```

### 6. Run Flask App
```bash
python3 app.py
```

Open browser: `http://<raspberry_pi_ip>:5000`

---

## Auto-Start with systemd

### Create Service File
```bash
sudo nano /etc/systemd/system/soil-monitor.service
```

Paste this content (adjust paths and user as needed):
```ini
[Unit]
Description=Soil Monitoring System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/soil-monitor
Environment="PATH=/home/pi/soil-monitor/venv/bin"
ExecStart=/home/pi/soil-monitor/venv/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable soil-monitor
sudo systemctl start soil-monitor
```

### Monitor Service
```bash
# Check status
sudo systemctl status soil-monitor

# View logs
sudo journalctl -u soil-monitor -f

# Stop service
sudo systemctl stop soil-monitor
```

---

## Sensor Configuration

### Register Addresses (Modbus Holding Registers)
Verify these with your sensor's datasheet. Common defaults shown:
- Address 0x0000: Nitrogen (N)
- Address 0x0001: Phosphorus (P)
- Address 0x0002: Potassium (K)
- Address 0x0003: Soil Moisture

Edit [modbus_sensor.py](modbus_sensor.py) if your sensors use different addresses:
```python
REGISTER_NITROGEN = 0x0000
REGISTER_PHOSPHORUS = 0x0001
REGISTER_POTASSIUM = 0x0002
REGISTER_MOISTURE = 0x0003
```

### Modbus IDs
Each sensor must have a unique Modbus ID (1-4):
- Sensor 1 → ID 1
- Sensor 2 → ID 2
- Sensor 3 → ID 3
- Sensor 4 → ID 4

Most sensors have DIP switches or settings to configure the Modbus ID. Refer to sensor documentation.

### Baud Rate & Serial Parameters
Standard settings (adjust in [app.py](app.py) if needed):
- Baud Rate: 9600
- Data Bits: 8
- Parity: None
- Stop Bits: 1

---

## API Endpoints

All endpoints return JSON.

### Get All Sensors
```
GET /api/sensors
```
Returns data from all 4 sensors:
```json
{
  "1": {
    "sensor_id": 1,
    "nitrogen": 185.5,
    "phosphorus": 142.3,
    "potassium": 210.7,
    "moisture": 65.4,
    "is_valid": true,
    "error": null,
    "timestamp": "2026-01-10T12:34:56.789123"
  },
  "2": { ... },
  "3": { ... },
  "4": { ... }
}
```

### Get Single Sensor
```
GET /api/sensor/<id>
```
Example: `GET /api/sensor/1`

### System Status
```
GET /api/status
```
Returns:
```json
{
  "timestamp": "2026-01-10T12:34:56.789123",
  "modbus_connected": true,
  "modbus_port": "/dev/serial0",
  "modbus_baudrate": 9600,
  "sensors": [1, 2, 3, 4]
}
```

### Health Check
```
GET /api/health
```
Returns `{"status": "healthy"}` or `{"status": "unhealthy"}`

---

## Troubleshooting

### No Response from Sensors
1. Check physical RS-485 wiring (A/B lines twisted pair)
2. Verify common ground between Pi, converter, and sensors
3. Check sensor Modbus IDs (should be 1-4)
4. Verify 12V power supply to sensors

### Connection Errors
```bash
# Check if UART is enabled
sudo cat /boot/config.txt | grep uart

# Test serial port
python3 -c "import serial; s = serial.Serial('/dev/serial0', 9600); print('OK')"
```

### Modbus Timeout
- Increase timeout in [modbus_sensor.py](modbus_sensor.py):
  ```python
  timeout=2.0  # increase from 1.0
  ```
- Check baud rate matches sensor configuration

### Service Won't Start
```bash
# Check logs
sudo journalctl -u soil-monitor -n 50
sudo journalctl -u soil-monitor -f

# Verify paths in service file
cat /etc/systemd/system/soil-monitor.service
```

---

## File Structure
```
soil-monitor/
├── app.py                 # Flask web server
├── modbus_sensor.py       # Modbus RTU reader
├── templates/
│   └── dashboard.html     # Web dashboard
├── venv/                  # Python virtual environment
└── README.md              # This file
```

---

## Production Notes

- **Stability**: Modbus RTU is very stable. Connection errors are rare with proper wiring.
- **Data Format**: All sensor values in standard units (mg/kg, %)
- **Error Handling**: Failed reads are logged; dashboard shows last valid value
- **Long-term**: No cloud dependency means unlimited operation as long as Pi has power
- **Monitoring**: Check logs monthly: `sudo journalctl -u soil-monitor | tail -20`

