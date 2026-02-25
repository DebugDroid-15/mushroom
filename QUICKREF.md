# Quick Reference

## File Structure
```
soil-monitor/
├── app.py                    # Flask web server (main entry point)
├── modbus_sensor.py          # Modbus RTU reader library
├── templates/
│   └── dashboard.html        # Web dashboard (served by Flask)
├── requirements.txt          # Python dependencies
├── config.example.py         # Configuration template
├── soil-monitor.service      # Systemd service file
├── install.sh                # Automated setup script
├── README.md                 # Full documentation
├── WIRING.md                 # Hardware wiring guide
└── QUICKREF.md              # This file
```

## Installation (30 seconds)
```bash
cd /home/pi
git clone <your-repo-url> soil-monitor
cd soil-monitor
bash install.sh
# Follow prompts
```

## Start System
```bash
# Automatic (recommended)
sudo systemctl start soil-monitor

# Manual (for testing)
cd /home/pi/soil-monitor
source venv/bin/activate
python3 app.py
```

## Check Status
```bash
sudo systemctl status soil-monitor
sudo journalctl -u soil-monitor -f
```

## Dashboard Access
```
http://<raspberry_pi_ip>:5000
```

## API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `GET /` | Dashboard |
| `GET /api/sensors` | All 4 sensors |
| `GET /api/sensor/1` | Specific sensor |
| `GET /api/status` | System info |
| `GET /api/health` | Health check |

## Common Commands

### View Live Logs
```bash
sudo journalctl -u soil-monitor -f
```

### Restart Service
```bash
sudo systemctl restart soil-monitor
```

### Disable Auto-Start
```bash
sudo systemctl disable soil-monitor
```

### Test Modbus Manually
```bash
cd /home/pi/soil-monitor
source venv/bin/activate
python3 modbus_sensor.py
```

### Update Code
```bash
cd /home/pi/soil-monitor
git pull
sudo systemctl restart soil-monitor
```

## Hardware Checklist
- [ ] Raspberry Pi with UART enabled
- [ ] RS-485 converter (MAX485/SP3485)
- [ ] 4× NPK sensors with unique Modbus IDs (1-4)
- [ ] 12V DC power supply for sensors
- [ ] Twisted pair cable for RS-485 (Category 5 works)
- [ ] Common ground between all devices

## Common Issues

### Dashboard shows "Disconnected"
1. Check UART is enabled: `ls -l /dev/serial0`
2. Verify sensors are powered (12V)
3. Check RS-485 wiring (A & B swapped?)
4. View logs: `sudo journalctl -u soil-monitor -f`

### Modbus timeout
1. Verify sensor Modbus IDs (1-4)
2. Check baud rate: 9600
3. Confirm twisted pair cable
4. Increase timeout in `modbus_sensor.py` if needed

### Service won't start
```bash
# Manual test to see error
python3 /home/pi/soil-monitor/app.py

# Check permissions
ls -l /var/log/soil-monitor
```

## Sensor Values (Typical)

| Parameter | Range | Unit |
|-----------|-------|------|
| Nitrogen | 50-400 | mg/kg |
| Phosphorus | 50-400 | mg/kg |
| Potassium | 50-400 | mg/kg |
| Soil Moisture | 10-90 | % |

## Customization

### Change UART Port
```bash
export MODBUS_PORT=/dev/ttyUSB0  # if using USB adapter
systemctl restart soil-monitor
```

### Change Poll Interval
Edit dashboard.html:
```javascript
const POLL_INTERVAL = 5000;  // milliseconds (change to 10000 for 10 sec)
```

### Change Web Port
```bash
export FLASK_PORT=8080  # instead of 5000
systemctl restart soil-monitor
```

## Performance Notes
- Reading all 4 sensors takes ~400-500ms
- Dashboard updates every 5 seconds (configurable)
- No cloud dependency - runs locally
- Designed for 24/7 operation

## Support

Refer to:
- `README.md` - Full setup & configuration
- `WIRING.md` - Hardware wiring & testing guide
- `config.example.py` - All available settings

