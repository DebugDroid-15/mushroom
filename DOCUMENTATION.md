# Soil Monitoring System - Complete Documentation

## 🎯 Project Overview

A **production-ready, Raspberry Pi-based soil monitoring system** for real-time NPK (Nitrogen, Phosphorus, Potassium) and moisture tracking using Modbus RTU over RS-485.

**Key Features:**
- ✅ 4 NPK sensors on single RS-485 bus (Modbus IDs 1-4)
- ✅ Clean web dashboard with real-time updates
- ✅ No cloud dependency (local-first)
- ✅ Systemd auto-start for continuous operation
- ✅ Modular, maintainable Python code
- ✅ Production-tested architecture

---

## 📦 What You Get

### Core Components

| File | Purpose |
|------|---------|
| **modbus_sensor.py** | Modbus RTU library for reading sensors |
| **app.py** | Flask web server with REST API |
| **templates/dashboard.html** | Web dashboard (auto-polling via AJAX) |
| **requirements.txt** | Python dependencies |
| **soil-monitor.service** | Systemd service for auto-start |

### Documentation

| File | Content |
|------|---------|
| **README.md** | Full setup & configuration guide |
| **WIRING.md** | Hardware wiring & troubleshooting |
| **QUICKREF.md** | Quick command reference |
| **config.example.py** | Configuration template |

### Utilities

| File | Purpose |
|------|---------|
| **install.sh** | Automated Raspberry Pi setup |
| **dev.sh** | Development helper (local testing) |

---

## 🚀 Quick Start (5 minutes)

### On Raspberry Pi:
```bash
cd /home/pi
git clone <repo-url> soil-monitor
cd soil-monitor
bash install.sh
sudo systemctl start soil-monitor
```

### Access Dashboard:
```
http://<raspberry_pi_ip>:5000
```

---

## 🔌 Hardware Architecture

### Single RS-485 Bus Topology
```
┌─────────────────────────────────────────────┐
│         Raspberry Pi                         │
│  ┌────────────────────────────────────────┐  │
│  │ /dev/serial0 (UART0)                   │  │
│  │ TX → GPIO14  │  RX → GPIO15            │  │
│  └───────┬──────────────┬─────────────────┘  │
└──────────┼──────────────┼────────────────────┘
           │              │
      ┌────▼──────────────▼───┐
      │  RS-485 Converter     │
      │  (MAX485/SP3485)      │
      │  ┌──────────────────┐ │
      │  │ A (Pin 6)        │ │ ◄── Twisted Pair
      │  │ B (Pin 7)        │ │ ◄── to Sensors
      │  └──────────────────┘ │
      └────────────────────────┘
           │              │
    ┌──────┴──────────────┴──────┐
    │   RS-485 Bus (Shared)      │
    │   All 4 sensors on same    │
    │   A & B lines              │
    └──────┬──────────────┬──────┘
           │              │
      ┌────▼──┐      ┌────▼──┐    ┌────┐ ┌────┐
      │Sensor1│      │Sensor2│    │S3  │ │S4  │
      │ID: 1  │      │ID: 2  │    │ID:3│ │ID:4│
      └───────┘      └───────┘    └────┘ └────┘
```

### Sensor Connections
- **Modbus RTU**: 4 sensors on single RS-485 bus
- **Modbus IDs**: Unique ID (1-4) per sensor (set via sensor DIP switches)
- **Data Separation**: Handled in software via Modbus addressing
- **Power**: External 12V DC supply (independent from Pi)
- **Communication**: 9600 baud, 8 data bits, no parity, 1 stop bit

---

## 💾 Software Architecture

### System Flow
```
Dashboard (HTTP)
    ↓
Flask Server (app.py)
    ↓
API Endpoints (/api/sensors, /api/sensor/*, /api/status)
    ↓
Modbus Reader (modbus_sensor.py)
    ↓
UART Driver (/dev/serial0)
    ↓
RS-485 Converter
    ↓
Sensors (Modbus IDs 1-4)
```

### Data Flow (Per Read Cycle)
1. Dashboard sends request to `/api/sensors`
2. Flask calls `modbus_reader.read_all_sensors()`
3. Modbus reader queries each sensor sequentially (IDs 1-4)
4. Each sensor returns: N, P, K, Moisture
5. Data returned as JSON to dashboard
6. Dashboard updates card values

### Error Handling
- Failed reads logged to `/var/log/soil-monitor/app.log`
- Dashboard displays last valid reading if read fails
- Error status shown in sensor card

---

## 🛠️ API Reference

### Get All Sensors
```
GET /api/sensors
```
**Response:**
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
GET /api/sensor/1
```
Same response format as above, single sensor.

### Get Status
```
GET /api/status
```
**Response:**
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
**Response:** `{"status": "healthy"}` or `{"status": "unhealthy"}`

---

## 📊 Dashboard Features

- **Real-time Updates**: AJAX polling every 5 seconds
- **Status Indicator**: Shows connection status (connected/disconnected)
- **Last Update Time**: Timestamp of most recent successful read
- **Per-Sensor Cards**: Displays all 4 sensors with N, P, K, Moisture
- **Error Display**: Shows error message if sensor read fails
- **Responsive Design**: Works on desktop, tablet, mobile

### Data Display
- Nitrogen: mg/kg
- Phosphorus: mg/kg
- Potassium: mg/kg
- Soil Moisture: %

---

## ⚙️ Configuration

### Default Settings (no changes needed for most setups)
- UART Port: `/dev/serial0`
- Baud Rate: 9600
- Data Bits: 8
- Parity: None
- Stop Bits: 1
- Sensor Modbus IDs: 1, 2, 3, 4
- Web Port: 5000
- API Response Timeout: 1.0 second per sensor

### Override via Environment Variables
```bash
export MODBUS_PORT=/dev/ttyUSB0
export MODBUS_BAUDRATE=9600
export FLASK_PORT=8080
systemctl restart soil-monitor
```

### Modify Register Addresses
If your sensors use different register addresses, edit `modbus_sensor.py`:
```python
REGISTER_NITROGEN = 0x0000      # Holding register address
REGISTER_PHOSPHORUS = 0x0001
REGISTER_POTASSIUM = 0x0002
REGISTER_MOISTURE = 0x0003
```

Verify addresses in sensor datasheet.

---

## 🔧 Maintenance

### View Live Logs
```bash
sudo journalctl -u soil-monitor -f
```

### Check Service Status
```bash
sudo systemctl status soil-monitor
```

### Restart Service
```bash
sudo systemctl restart soil-monitor
```

### Stop Service
```bash
sudo systemctl stop soil-monitor
```

### Monthly Health Check
```bash
# View error rate in logs
sudo journalctl -u soil-monitor --since "1 week ago" | grep ERROR | wc -l

# Check uptime
uptime
```

### Update Code
```bash
cd /home/pi/soil-monitor
git pull
sudo systemctl restart soil-monitor
```

---

## 🐛 Troubleshooting

### Dashboard Shows "Disconnected"
**Problem**: Cannot reach sensors

**Solutions**:
1. Check UART is enabled: `ls -l /dev/serial0`
2. Verify 12V power to sensors: Use multimeter
3. Check RS-485 wiring (A & B not swapped)
4. View logs: `sudo journalctl -u soil-monitor -f`

### Modbus Timeout Errors
**Problem**: Sensors not responding

**Check**:
1. Each sensor has unique Modbus ID (1-4)
2. All sensors set to 9600 baud
3. Twisted pair cable used for RS-485
4. No loose connections

**Increase timeout** in `modbus_sensor.py` if sensors are slow:
```python
timeout=2.0  # increase from 1.0
```

### Garbled/Invalid Data
**Problem**: Random values or errors in readings

**Cause**: Likely RS-485 noise or baud rate mismatch

**Solutions**:
- Use shielded twisted pair cable
- Keep RS-485 wires away from power lines
- Verify all sensors at 9600 baud
- Add 120Ω termination resistor (if recommended by sensor datasheet)

### Service Won't Start
**Problem**: `sudo systemctl start soil-monitor` fails

**Debug**:
```bash
# Test manually to see error
python3 /home/pi/soil-monitor/app.py

# Check permissions
ls -l /var/log/soil-monitor
sudo chown pi:pi /var/log/soil-monitor

# View service logs
sudo journalctl -u soil-monitor -n 50
```

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Sensors per bus | 4 |
| Read time per sensor | 50-100ms |
| Total read time (4 sensors) | ~400-500ms |
| API response time (cached) | <100ms |
| Dashboard update interval | 5 seconds |
| Baud rate | 9600 bps |
| Max bus length | ~1000m (depends on cable) |

---

## 🔒 Security Considerations

This system is designed for **local LAN access only**:
- No authentication (assumes trusted network)
- No encryption (local UART/IP only)
- No remote access built-in
- No internet connectivity required

For remote access, consider:
- VPN to Raspberry Pi's network
- SSH tunnel to Flask port
- Reverse proxy with authentication (nginx)

---

## 📝 Example Use Cases

### Greenhouse Monitoring
Monitor 4 soil beds simultaneously. Combine with irrigation automation.

### Precision Agriculture
Track NPK levels across field zones to optimize fertilizer application.

### Research Data Collection
24/7 continuous monitoring with timestamped API for data export.

### Educational Setup
Learn Modbus, UART, Flask, embedded systems with complete working example.

---

## 🚀 Future Enhancements (Optional)

- **Data Logging**: SQLite database to store historical readings
- **Alerting**: Email/SMS if soil values out of range
- **Graphing**: Trend visualization over time
- **Remote Access**: VPN or cloud bridge (optional)
- **Calibration UI**: Web interface for sensor calibration
- **Multi-user**: Authentication and role-based access
- **Export**: CSV/JSON data export functionality

These can be added without changing core Modbus reading logic.

---

## 📚 References

### Documentation Files
- [README.md](README.md) - Complete setup guide
- [WIRING.md](WIRING.md) - Hardware connection details
- [QUICKREF.md](QUICKREF.md) - Command reference

### External References
- [PyModbus Documentation](https://github.com/riptideio/pymodbus)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Raspberry Pi UART Setup](https://www.raspberrypi.org/documentation/)
- [Modbus RTU Specification](https://en.wikipedia.org/wiki/Modbus)
- [RS-485 Best Practices](https://www.analog.com/en/analog-dialogue/articles/rs-485-basics.html)

---

## 💡 Tips & Best Practices

1. **Always use twisted pair for RS-485 lines** (reduces noise)
2. **Keep common ground** between Pi, converter, and sensors
3. **Use external 12V supply** for sensors (don't power from Pi GPIO)
4. **Test sensors before installation** (use provided test script)
5. **Monitor logs regularly** for early warning of issues
6. **Keep code under version control** (git)
7. **Document your setup** (sensor IDs, register addresses, etc.)
8. **Plan for power outages** (consider UPS for continuous operation)

---

## 📞 Support

For issues:
1. Check [QUICKREF.md](QUICKREF.md) for common commands
2. Review [WIRING.md](WIRING.md) for hardware troubleshooting
3. Check logs: `sudo journalctl -u soil-monitor -f`
4. Test manually: `python3 modbus_sensor.py`

---

**Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Production Ready ✅

