# 🌱 Soil Monitoring System - Deployment Checklist

## ✅ Pre-Deployment Checklist

### Hardware Prerequisites
- [ ] Raspberry Pi (3, 4, 5, Zero 2W compatible)
- [ ] Raspberry Pi OS Lite (headless) installed
- [ ] Network access (LAN or Wi-Fi)
- [ ] 4× NPK soil sensors (7-pin RS-485 type)
- [ ] RS-485 to TTL converter (MAX485 or SP3485)
- [ ] Twisted pair cable for RS-485
- [ ] 12V DC power supply for sensors
- [ ] Jumper wires and connectors

### Project Files (All 17 Files)
- [ ] modbus_sensor.py
- [ ] app.py
- [ ] templates/dashboard.html
- [ ] requirements.txt
- [ ] config.example.py
- [ ] soil-monitor.service
- [ ] install.sh
- [ ] dev.sh
- [ ] README.md
- [ ] WIRING.md
- [ ] QUICKREF.md
- [ ] DOCUMENTATION.md
- [ ] FILES.md
- [ ] INDEX.py
- [ ] DELIVERY.md
- [ ] dashboard.html (old, replace)
- [ ] This file

---

## 🔧 Installation Steps (On Raspberry Pi)

### Step 1: Prepare Raspberry Pi
- [ ] SSH into Pi: `ssh pi@<ip_address>`
- [ ] Update system: `sudo apt-get update && sudo apt-get upgrade -y`
- [ ] Check UART is enabled: `ls -l /dev/serial0`
  - If not found, run `sudo raspi-config` and enable UART
  - Might need to reboot

### Step 2: Copy Project Files
```bash
cd /home/pi
git clone <repo_url> soil-monitor
# OR
scp -r soil-monitor pi@<ip>:/home/pi/
```

### Step 3: Run Setup Script
```bash
cd /home/pi/soil-monitor
bash install.sh
```
This will:
- Create Python virtual environment
- Install dependencies (pymodbus, flask)
- Create systemd service
- Create log directory

### Step 4: Verify UART Connection
```bash
python3 << 'EOF'
import serial
s = serial.Serial('/dev/serial0', 9600, timeout=1)
print("✓ UART OK")
s.close()
EOF
```

### Step 5: Test Modbus (Optional)
```bash
source venv/bin/activate
python3 modbus_sensor.py
# Should show sensor readings or timeout errors
```

### Step 6: Start Service
```bash
sudo systemctl start soil-monitor
sudo systemctl status soil-monitor  # should show "active (running)"
```

### Step 7: Enable Auto-Start
```bash
sudo systemctl enable soil-monitor
# Now service will auto-start after reboot
```

---

## 🔌 Hardware Setup Checklist

### RS-485 Converter Wiring
- [ ] RS-485 Pin 1 (RO) → Pi GPIO RX (GPIO15)
- [ ] RS-485 Pin 2 (DE) → Pi 5V (or GPIO17 for advanced control)
- [ ] RS-485 Pin 3 (RE) → Pi GND (or GPIO17 with DE)
- [ ] RS-485 Pin 4 (DI) → Pi GPIO TX (GPIO14)
- [ ] RS-485 Pin 5 (GND) → Pi GND
- [ ] RS-485 Pin 6 (A) → Twisted pair to sensors
- [ ] RS-485 Pin 7 (B) → Twisted pair to sensors
- [ ] RS-485 Pin 8 (VCC) → 5V power

### Sensor Wiring (Each Sensor)
- [ ] Pin 1 (+12V) → 12V DC supply
- [ ] Pin 2 (GND) → Common ground
- [ ] Pin 3 (A) → RS-485 A line (twisted pair)
- [ ] Pin 4 (B) → RS-485 B line (twisted pair)
- [ ] Pin 5 (GND) → Common ground
- [ ] Modbus ID set to: 1, 2, 3, or 4 (unique per sensor)

### Power & Ground
- [ ] 12V supply capable of powering all 4 sensors
- [ ] Common ground between: Pi, converter, sensors
- [ ] 5V power for converter from Pi or external
- [ ] All connections secure (no loose wires)

### Cable Quality
- [ ] RS-485 lines use twisted pair (CAT5 works)
- [ ] RS-485 cable shield grounded at converter only
- [ ] No sharp bends in twisted pair
- [ ] At least 30cm away from power lines

---

## 📊 Post-Deployment Verification

### API Endpoints Test
```bash
# Test all sensors
curl http://localhost:5000/api/sensors

# Test single sensor
curl http://localhost:5000/api/sensor/1

# Test system status
curl http://localhost:5000/api/status

# Test health check
curl http://localhost:5000/api/health
```

### Dashboard Access
- [ ] Open browser: `http://<pi_ip>:5000`
- [ ] Dashboard loads without errors
- [ ] 4 sensor cards visible
- [ ] Values updating every 5 seconds
- [ ] "Connected" status shown

### Sensor Data Validation
- [ ] Nitrogen values in range: 50-400 mg/kg
- [ ] Phosphorus values in range: 50-400 mg/kg
- [ ] Potassium values in range: 50-400 mg/kg
- [ ] Moisture values in range: 10-90 %
- [ ] No repeated identical values (indicates dead sensor)

### Log Verification
```bash
sudo journalctl -u soil-monitor -n 20  # Last 20 log entries
# Should show no ERROR messages
# Should show periodic sensor readings
```

---

## 🚀 Optimization Checklist

### Performance Tuning
- [ ] Dashboard refresh rate (5 seconds) - adjust if needed
- [ ] Modbus timeout - increase if sensors are slow
- [ ] Number of retry attempts - if network unstable

### Reliability
- [ ] Service auto-start enabled: `sudo systemctl is-enabled soil-monitor`
- [ ] Log rotation configured (optional, for 24/7 operation)
- [ ] UPS/backup power considered (for uninterrupted operation)
- [ ] Sensor calibration verified

### Monitoring
- [ ] Set up log monitoring: `sudo journalctl -u soil-monitor -f`
- [ ] Monitor disk space (for long-term logging if added)
- [ ] Plan for monthly health checks

---

## 🔄 Maintenance Tasks

### Daily (Automatic via Systemd)
- [ ] Service running: `sudo systemctl status soil-monitor`
- [ ] Dashboard accessible: `http://<pi_ip>:5000`

### Weekly
- [ ] Check logs for errors: `sudo journalctl -u soil-monitor --since "7 days ago" | grep ERROR`
- [ ] Verify sensor values are reasonable
- [ ] Check system uptime: `uptime`

### Monthly
- [ ] Review 30 days of logs: `sudo journalctl -u soil-monitor --since "1 month ago"`
- [ ] Clean dust from Raspberry Pi (if in field)
- [ ] Verify all connections are secure

### Yearly
- [ ] Update Raspberry Pi OS: `sudo apt-get update && sudo apt-get upgrade -y`
- [ ] Update Python packages: `pip install --upgrade -r requirements.txt`
- [ ] Recalibrate sensors (as per sensor manual)
- [ ] Review and update documentation

---

## 🐛 Troubleshooting Checklist

### Dashboard Shows "Disconnected"

**Check UART:**
```bash
ls -l /dev/serial0
# Should show: /dev/serial0 -> ttyAMA0
```

**Check Power:**
```bash
# Verify 12V to sensors with multimeter
# Should show 11.5V - 12.5V under load
```

**Check Wiring:**
- [ ] No loose connections
- [ ] A & B lines not swapped
- [ ] Common ground verified with multimeter
- [ ] Twisted pair cable intact

**Check Logs:**
```bash
sudo journalctl -u soil-monitor -f
# Should show connection errors, not syntax errors
```

### Modbus Timeout Errors

**Check Modbus IDs:**
- [ ] Sensor 1 set to ID 1
- [ ] Sensor 2 set to ID 2
- [ ] Sensor 3 set to ID 3
- [ ] Sensor 4 set to ID 4

**Check Baud Rate:**
```bash
stty -F /dev/serial0 -a
# Should show 9600 baud
```

**Check Cable:**
- [ ] Twisted pair used
- [ ] No exposed connections
- [ ] Shielding (if present) grounded at converter only

### Garbled/Invalid Data

**Check Noise:**
- [ ] RS-485 wires away from power lines
- [ ] No sharp bends in cable
- [ ] Proper shielding (if in noisy environment)

**Add Termination (if needed):**
- [ ] 120Ω resistor between A & B at converter end (if recommended by sensor)
- [ ] Check sensor datasheet for recommendations

### Service Won't Start

**Test Manually:**
```bash
source /home/pi/soil-monitor/venv/bin/activate
python3 /home/pi/soil-monitor/app.py
```

**Check Permissions:**
```bash
ls -l /var/log/soil-monitor
sudo chown pi:pi /var/log/soil-monitor
```

**View Errors:**
```bash
sudo journalctl -u soil-monitor -n 50 -e
```

---

## 📈 Monitoring Points

### Key Metrics to Monitor
- [ ] Service uptime (should be continuous)
- [ ] Sensor response time (400-500ms for all 4)
- [ ] API response time (<100ms)
- [ ] Data value ranges (see validation above)
- [ ] Error rate in logs (should be <1%)

### Alerts to Set Up (Optional)
- [ ] Sensor read fails >5 times consecutive
- [ ] Nitrogen/Phosphorus/Potassium out of range
- [ ] Moisture value unusual (too high/low)
- [ ] Service stopped unexpectedly
- [ ] High disk usage (if data logging added)

---

## 🎓 Knowledge Base

### Common Issues & Solutions
| Issue | Solution |
|-------|----------|
| UART not found | Enable via raspi-config, reboot |
| Modbus timeout | Check Modbus IDs 1-4, verify 9600 baud |
| Garbled data | Use twisted pair, shield properly, check for noise |
| Service won't start | Check UART enabled, verify permissions |
| Sensor reads fail | Verify 12V power, check RS-485 wiring |

### Reference Files
- **QUICKREF.md** - Common commands
- **WIRING.md** - Hardware troubleshooting
- **README.md** - Complete setup guide
- **DOCUMENTATION.md** - System architecture

---

## ✨ Final Checklist

### Before Going Live
- [ ] All files copied to Raspberry Pi
- [ ] install.sh run successfully
- [ ] UART verified working
- [ ] All sensors reading valid data
- [ ] Service enabled for auto-start
- [ ] Dashboard accessible and updating
- [ ] Logs show no ERROR messages
- [ ] Documentation reviewed

### Going Live
- [ ] Take system image for backup: `dd if=/dev/mmcblk0 of=backup.img`
- [ ] Document sensor locations
- [ ] Document Modbus IDs and register addresses
- [ ] Train users on dashboard access
- [ ] Set up monitoring procedures
- [ ] Plan maintenance schedule

### Production Readiness Sign-Off
- [ ] System tested 24+ hours without errors ✓
- [ ] All documentation reviewed ✓
- [ ] Backup plan in place ✓
- [ ] Maintenance team trained ✓
- [ ] Ready for deployment ✓

---

## 📞 Support Matrix

| Issue Type | Reference File | Solution Time |
|------------|---|---|
| Setup help | README.md | <10 min |
| Hardware wiring | WIRING.md | <30 min |
| API questions | DOCUMENTATION.md | <5 min |
| Quick commands | QUICKREF.md | <1 min |
| Troubleshooting | WIRING.md → README.md | <30 min |

---

## 🎉 Completion Status

- [ ] All files present (17 total)
- [ ] Installation script tested
- [ ] Documentation comprehensive
- [ ] Code production-ready
- [ ] Hardware verified
- [ ] APIs documented
- [ ] Troubleshooting guide complete
- [ ] Ready for deployment

---

**Deployment Checklist Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Ready for Production ✅

Print this checklist and keep it handy during installation and maintenance!

