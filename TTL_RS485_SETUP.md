# TTL to RS485 Power Supply Converter Board - Configuration

## Hardware Setup

### Connections:
```
Raspberry Pi 5                    TTL to RS485 Board        NPK Sensor (x4)
────────────────                 ────────────────          ──────────────
GPIO 24 (DE/RE) ─────────────→  DE/ RE pin
3.3V ─────────────────────────→  VCC (3.3V input)
GND ───────────────────────────→  GND
GPIO 14 (TX) ──────────────────→ DI (or TXD)
GPIO 15 (RX) ──────────────────→ RO (or RXD)
                                 A+ (RS485) ───────────────→ A+ (on all sensors)
                                 B- (RS485) ───────────────→ B- (on all sensors)
                                 GND ───────────────────────→ GND (on all sensors)
```

## Pi GPIO Pin Reference (BCM Numbering)

- **GPIO 14**: UART0 TX (pin 8)
- **GPIO 15**: UART0 RX (pin 10)
- **GPIO 24**: DE/RE Control (recommended, pin 18)
- **3.3V Power**: Pin 1 or 17
- **GND**: Pin 6 or 9

## Current Configuration

**File:** `/home/mushroom/mushroom_project/modbus_sensor.py`

```python
# Default initialization
ModbusNPKReader(
    port='/dev/serial0',      # UART0 serial port
    baudrate=9600,             # Standard Modbus speed
    gpio_de_re=24              # DE/RE control pin
)
```

## Power Specifications

- **Input Voltage:** 3.3V DC
- **Max Current:** ~100-200 mA (check your board specs)
- **Recommended Pi Pin:** GPIO 3V3 (Pin 1 or 17)

## Testing

Run the sensor scanner to verify all connections:

```bash
# Single scan
scan-sensors

# Continuous monitoring
scan-sensors --loop

# Scan specific sensors
scan-sensors --sensors 1 2 3 4
```

## Expected Output

```
══════════════════════════════════════════════════════════════════════════
MODBUS SENSOR SCANNER - NPK SOIL SENSORS
══════════════════════════════════════════════════════════════════════════
Port: /dev/serial0 | Baudrate: 9600 | Timeout: 1.0s
══════════════════════════════════════════════════════════════════════════

Scanning Sensor 1... ✅ RESPONDING
  Raw Registers: [......]
  ├─ Nitrogen (N):   74.5 mg/kg
  ├─ Phosphorus (P): 252.5 mg/kg
  ├─ Potassium (K):  163.5 mg/kg
  ├─ pH:             6.98
  ├─ EC:             5.58 mS/cm
  └─ Temperature:    10.97°C
```

## Troubleshooting

### Sensors Not Responding
1. ✓ Check 3.3V power supply to converter board
2. ✓ Verify RX/TX connections
3. ✓ Confirm A+/B- RS485 wiring to sensors
4. ✓ Check GND connections

### High Impedance Issues
- Ensure termination resistors (120Ω) at end of RS485 line if having interference
- Keep RS485 cables twisted

### Power Issues
- Pi 3.3V pin can supply ~400 mA max
- Each converter board + sensors should be within this limit

## Advantages of This Setup

✅ Simpler wiring (powered directly from Pi)
✅ Cleaner board layout
✅ Lower power consumption
✅ No external 5V supply needed
✅ Reduced electrical noise

