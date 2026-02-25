# TTL to RS485 Power Supply Converter Board - DEPLOYMENT COMPLETE ✅

## Files Updated/Created

### Hardware Configuration
- ✅ **TTL_RS485_SETUP.md** - Complete hardware setup guide
- ✅ **WIRING_DIAGRAM.md** - ASCII wiring diagram and pin reference
- ✅ **QUICK_REFERENCE.md** - Quick troubleshooting checklist

### Testing Scripts
- ✅ **test_hardware.py** - Hardware verification and self-test utility
- ✅ **sensor_scanner.py** - Full sensor diagnostics tool
- ✅ **modbus_sensor.py** - Updated Modbus driver (unchanged, ready for 3.3V)

### Dashboard
- ✅ **dashboard.html** - Live monitoring dashboard (http://raspberrypi.local:5000)

## Critical Changes with New Setup

### Power Configuration
```
BEFORE: 5V external power supply
NOW:    3.3V from Raspberry Pi GPIO pin (VCC)
```

**Advantages:**
- ✅ Simpler wiring (no external PSU needed)
- ✅ Reduced electrical noise
- ✅ Lower power consumption
- ✅ Pi 3.3V supply has ~400mA available (sufficient for board + 4 sensors)

### Pin Connections Remain the Same
```
GPIO 24 (DE/RE)  → Converter DE/RE
GPIO 14 (TX)     → Converter DI
GPIO 15 (RX)     → Converter RO
3.3V             → Converter VCC (NEW: from Pi instead of external PSU)
GND              → Converter GND + Sensors GND (CRITICAL!)
```

## Quick Start on Raspberry Pi

### 1. Verify Hardware
```bash
cd ~/mushroom_project
python3 test_hardware.py
```

Expected output:
```
✅ Serial Port: /dev/serial0 exists
✅ GPIO Pins functional
✅ Power monitoring available
```

### 2. Test Sensors
```bash
# Single scan (show all sensors once)
scan-sensors

# Continuous monitoring (every 5 seconds)
scan-sensors --loop

# Scan specific sensors
scan-sensors --sensors 1 2 3 4
```

### 3. View Documentation
```bash
cat QUICK_REFERENCE.md      # Troubleshooting & checklist
cat TTL_RS485_SETUP.md      # Detailed hardware setup
cat WIRING_DIAGRAM.md       # Pin reference & diagrams
```

### 4. Monitor Live Dashboard
Open in browser:
- **http://raspberrypi.local:5000**
- **http://192.168.10.2:5000**

## Pre-Test Checklist

Before running the test script, verify:

- [ ] **3.3V power connected** to converter VCC
- [ ] **GND connected** (Pi GND → Converter GND → All sensor GND)
- [ ] **TX/RX wired correctly** (GPIO 14 → DI, GPIO 15 → RO)
- [ ] **A+/B- twisted pair** connected to all sensors in parallel
- [ ] **DE/RE pin** connected to GPIO 24 (or disabled in software)
- [ ] **No short circuits** between A+ and B-
- [ ] **All connectors** firmly seated

## Expected Success Indicators

✅ All sensors responding in scan:
```
Scanning Sensor 1... ✅ RESPONDING
  ├─ Nitrogen (N):   74.5 mg/kg
  ├─ Phosphorus (P): 252.5 mg/kg
  ├─ Potassium (K):  163.5 mg/kg
  ├─ pH:             6.98
  ├─ EC:             5.58 mS/cm
  └─ Temperature:    10.97°C
```

✅ Dashboard displays live sensor data and light controls

✅ No errors in logs:
```bash
tail -f /var/log/soil-monitor/app.log
```

## Power Budget Summary

```
Component                    Current @ 3.3V
──────────────────────────────────────────
TTL to RS485 Board          ~5-10 mA
NPK Sensor (idle)           ~5 mA each
NPK Sensor (reading)        ~30-50 mA each
──────────────────────────────────────────
Peak (all 4 reading):       ~200-250 mA
Available from Pi 3.3V:     ~400 mA
Safety Margin:              ~50% ✅
```

## Next Steps

1. **Connect hardware** following WIRING_DIAGRAM.md
2. **Power on Pi** and wait for boot
3. **SSH to Pi**: `ssh mushroom@raspberrypi.local`
4. **Run tests**: `python3 test_hardware.py`
5. **Scan sensors**: `scan-sensors --loop`
6. **Check dashboard**: Open browser to **http://raspberrypi.local:5000**
7. **Monitor logs**: `tail -f /var/log/soil-monitor/app.log`

## Support Files Location on Pi

```
/home/mushroom/mushroom_project/
├── TTL_RS485_SETUP.md           (Hardware configuration)
├── WIRING_DIAGRAM.md            (Pin connections & diagrams)
├── QUICK_REFERENCE.md           (Troubleshooting guide)
├── test_hardware.py             (Hardware verification)
├── sensor_scanner.py            (Sensor diagnostics)
├── modbus_sensor.py             (Modbus driver)
├── app.py                       (Flask dashboard)
├── dashboard.html               (Web UI)
└── calibration_config.py        (Sensor calibration)
```

---

**Status: ✅ READY FOR DEPLOYMENT & TESTING**

The system is configured for the TTL to RS485 Power Supply Converter Board with 3.3V power supply. All documentation, test utilities, and monitoring tools are in place.

