# Hardware Wiring & Testing Guide

## RS-485 Converter to Raspberry Pi

### MAX485 / SP3485 Pinout
```
Pin 1: RO   (Receiver Output)      → Pi GPIO RX (GPIO15)
Pin 2: DE   (Driver Enable)        → Pi GPIO17 (or pull HIGH if always transmitting)
Pin 3: RE   (Receiver Enable)      → Pi GPIO17 (or pull LOW if always receiving)
Pin 4: DI   (Driver Input)         → Pi GPIO TX (GPIO14)
Pin 5: GND  (Ground)               → Pi GND
Pin 6: A    (Non-inverting output) → Sensors A (blue wire, twisted pair)
Pin 7: B    (Inverting output)     → Sensors B (white wire, twisted pair)
Pin 8: VCC  (Power 5V)             → Pi 5V
```

### Raspberry Pi UART Pins
- GPIO14 (Pin 8, BCM): UART TX
- GPIO15 (Pin 10, BCM): UART RX
- GPIO17 (Pin 11, BCM): GPIO for DE/RE control (optional)

### DE/RE Control Strategy
**Option A: Always Enabled (Simpler)**
```
DE pin → tie to +5V (always transmitting)
RE pin → tie to GND (always receiving)
```
This works for single-master, multiple-slave setup (Pi is master).

**Option B: GPIO Controlled (Advanced)**
```
DE pin → GPIO17
RE pin → GPIO17
```
Set LOW before reading (receive mode), HIGH before writing (transmit mode).

---

## NPK Sensor Wiring

### 7-Pin Sensor Connector
```
Pin 1: +12V  (external DC power supply)
Pin 2: GND   (common ground)
Pin 3: A     (RS-485 non-inverting) → Converter Pin 6 (twisted pair)
Pin 4: B     (RS-485 inverting)     → Converter Pin 7 (twisted pair)
Pin 5: GND   (another ground)       → Common ground
Pins 6-7: Usually not used
```

### Multiple Sensors (Parallel Connection)
All sensors share the same RS-485 bus:
```
Converter Pin 6 (A) ──┬──→ Sensor1 A
                      ├──→ Sensor2 A
                      ├──→ Sensor3 A
                      └──→ Sensor4 A

Converter Pin 7 (B) ──┬──→ Sensor1 B
                      ├──→ Sensor2 B
                      ├──→ Sensor3 B
                      └──→ Sensor4 B

+12V Supply ─────────┬──→ Sensor1 Pin1
                      ├──→ Sensor2 Pin1
                      ├──→ Sensor3 Pin1
                      └──→ Sensor4 Pin1

GND ──────────────────┬──→ Sensor1 GND (Pins 2, 5)
                      ├──→ Sensor2 GND (Pins 2, 5)
                      ├──→ Sensor3 GND (Pins 2, 5)
                      ├──→ Sensor4 GND (Pins 2, 5)
                      ├──→ Converter Pin 5 (GND)
                      └──→ Pi GND
```

### Twisted Pair Cable (RS-485 Best Practice)
- Use twisted pair for A & B lines (reduces interference)
- Category 5 Ethernet cable works well
- Use shielded cable in electrically noisy environments
- Shield connects to GND at converter end only (not at sensor end)

---

## Configuration Checklist

### Pre-Testing
- [ ] UART enabled in Pi boot config
- [ ] RS-485 converter wired correctly
- [ ] Sensors powered with 12V DC (check with multimeter)
- [ ] Common ground between Pi, converter, and sensors
- [ ] Twisted pair cable used for A & B lines
- [ ] No loose connections

### Sensor Setup
- [ ] Each sensor has unique Modbus ID (1-4)
- [ ] Baud rate set to 9600
- [ ] 8N1 (8 data bits, no parity, 1 stop bit)
- [ ] Note the register addresses from sensor datasheet

---

## Testing Procedure

### Step 1: Verify UART
```bash
# Check UART is available
ls -l /dev/serial0

# Should output: /dev/serial0 -> ttyAMA0
# If error, UART not enabled. Run: sudo raspi-config
```

### Step 2: Check Wiring
```bash
# Install tools
sudo apt-get install i2c-tools

# Test serial port connection
python3 << 'EOF'
import serial
try:
    s = serial.Serial('/dev/serial0', 9600, timeout=1)
    print("✓ Serial port opened successfully")
    s.close()
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

### Step 3: Test Modbus Communication
```bash
# Run individual sensor tests
python3 << 'EOF'
from modbus_sensor import ModbusNPKReader

reader = ModbusNPKReader(port='/dev/serial0', baudrate=9600)
if reader.connect():
    print("✓ Connected to Modbus RTU")
    
    # Test each sensor
    for sensor_id in range(1, 5):
        print(f"\nTesting Sensor {sensor_id}...")
        data = reader.read_sensor(sensor_id)
        if data.is_valid:
            print(f"  ✓ N: {data.nitrogen}, P: {data.phosphorus}, K: {data.potassium}, M: {data.moisture}")
        else:
            print(f"  ✗ Error: {data.error}")
    
    reader.disconnect()
else:
    print("✗ Failed to connect")
EOF
```

### Step 4: Test Flask API
```bash
# Start Flask server
python3 app.py

# In another terminal, test endpoints
curl http://localhost:5000/api/status
curl http://localhost:5000/api/sensors
curl http://localhost:5000/api/sensor/1
```

### Step 5: Access Dashboard
Open browser: `http://<raspberry_pi_ip>:5000`

---

## Troubleshooting

### No UART Found
```bash
# Check boot config
sudo cat /boot/config.txt | grep -E "uart|disable-bt"

# Should show:
# enable_uart=1
# (optionally) dtoverlay=disable-bt

# If missing, add these lines:
sudo nano /boot/config.txt
# Add: enable_uart=1
sudo reboot
```

### Modbus Timeout Errors
**Cause**: No response from sensors

**Check**:
1. Verify 12V power to sensors (multimeter)
2. Verify Modbus IDs (check sensor documentation/DIP switches)
3. Check RS-485 wiring (A & B swapped? Loose connections?)
4. Verify baud rate: `stty -F /dev/serial0 -a` should show 9600

**Solution**:
```python
# In modbus_sensor.py, increase timeout:
timeout=2.0  # was 1.0
```

### Garbled Data
**Cause**: Baud rate mismatch or noise on RS-485 bus

**Solutions**:
- Verify all sensors are at 9600 baud
- Use shielded twisted pair cable
- Keep RS-485 wires away from power lines
- Add 120Ω termination resistor between A & B at converter (if recommended by datasheet)

### Intermittent Errors
**Cause**: Loose connection or power supply fluctuation

**Check**:
- Reseat all connectors
- Check power supply voltage under load (should be stable 12V)
- Add capacitor across 12V supply (0.1µF ceramic + 10µF electrolytic)

### Service Won't Start
```bash
# Check for errors
sudo systemctl status soil-monitor
sudo journalctl -u soil-monitor -n 20

# Verify permissions
ls -l /var/log/soil-monitor
sudo chown pi:pi /var/log/soil-monitor

# Test manually first
cd /home/pi/soil-monitor
source venv/bin/activate
python3 app.py
```

---

## Performance Metrics

With 4 sensors on a single RS-485 bus:
- **Read time per sensor**: ~50-100ms
- **Total read time (4 sensors)**: ~400-500ms
- **API response time**: <100ms (cached)
- **Dashboard update interval**: 5 seconds (default)

---

## Advanced: Oscilloscope Verification

If troubleshooting with oscilloscope (optional):

### Modbus RTU Signal
- RS-485 lines (A, B) should show differential Manchester encoding
- Logic levels: 0-5V
- Baud rate: 9600
- Check for proper rise/fall times (not too slow)

### Idle State
- Both A and B should idle near 3V (differential ≈ 0V)
- Watch for noise or reflections (indicates termination issue)

---

## Next Steps

Once testing is complete:
1. Run installation script: `bash install.sh`
2. Enable systemd service: `sudo systemctl start soil-monitor`
3. Configure auto-start: `sudo systemctl enable soil-monitor`
4. Monitor logs: `sudo journalctl -u soil-monitor -f`

