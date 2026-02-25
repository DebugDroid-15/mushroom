# NPK Sensor Power Requirements - IMPORTANT!

## ⚠️ CRITICAL FINDING

**The NPK soil sensors are NOT responding because they need 5V power, not 3.3V!**

### Sensor Specifications

Most NPK 7-parameter soil sensors operate at:
- **Operating Voltage:** 5V DC (±10%)
- **Current Draw:** 30-50 mA per sensor
- **Minimum Voltage:** 4.5V (below this, sensors fail or give invalid readings)

### Your Current Problem

- **Provided:** 3.3V from Raspberry Pi
- **Required:** 5V DC
- **Result:** Sensors offline ❌

## Solution: Use External 5V Power Supply

### Recommended Setup

```
External 5V PSU (USB or dedicated)
│
├─ 5V ──────────────────────────→ TTL-RS485 Converter VCC
├─ GND ──────────────────────────→ TTL-RS485 Converter GND
│                                  │
│                                  ├─ A+ (RS485) ──→ All Sensors A+
│                                  ├─ B- (RS485) ──→ All Sensors B-
│                                  └─ GND ─────────→ All Sensors GND

Pi (3.3V Logic Level)
│
├─ GPIO 24 ─────────────────────→ TTL-RS485 DE/RE
├─ GPIO 14 (TX) ─────────────────→ TTL-RS485 DI (with level shifter)
├─ GPIO 15 (RX) ─────────────────→ TTL-RS485 RO (with level shifter)
└─ GND (common with 5V PSU GND)

```

## Why This Works

✅ Sensors get proper 5V operating voltage
✅ TTL-RS485 board operates correctly at 5V
✅ Pi logic levels (3.3V) are compatible with converter input (usually 5V tolerant)
✅ Common GND between Pi and external PSU

## Power Supply Options

### Option 1: USB Power Adapter (Easiest)
- Any 5V USB power supply (phone charger, etc.)
- Can power converter board + all 4 sensors simultaneously
- Cost: ~$5-10

### Option 2: Raspberry Pi USB Power
- If Pi's USB port has spare 5V output (sometimes available)
- Not recommended if already powering Pi from it

### Option 3: Regulated 5V Power Supply
- Dedicated lab power supply or converter
- Most reliable option

## Wiring Changes Required

```
BEFORE (Not Working):
Pi 3.3V → Converter VCC

NOW (Correct):
External 5V PSU →  Converter VCC
Pi GND (common) ←  5V PSU GND (same return path)
```

**TX/RX/DE-RE pins stay the same** (Pi 3.3V logic to converter is fine)

## Verification Steps

1. **Connect 5V power supply to converter board VCC**
2. **Common ground** Pi GND with 5V PSU GND
3. **Blue LED** on converter should light up (if present)
4. **Run test:**

```bash
python3 test_hardware.py
scan-sensors
```

## Expected Result After Fix

```
Scanning Sensor 1... ✅ RESPONDING
  Raw Registers: [0, 0, 745, 2525, 1635, 698, 558, 1097]
  ├─ Nitrogen (N):   74.5 mg/kg
  ├─ Phosphorus (P): 252.5 mg/kg
  ├─ Potassium (K):  163.5 mg/kg
  ├─ pH:             6.98
  ├─ EC:             5.58 mS/cm
  └─ Temperature:    10.97°C
```

## Power Budget With 5V Supply

```
Component              Current @ 5V
────────────────────────────────────
TTL-RS485 Board        ~10 mA
NPK Sensor (idle)      ~5 mA
NPK Sensor (reading)   ~40 mA

Peak (all 4 reading):  ~200 mA
Typical USB Supply:    ~500-1000 mA

✅ SAFE WITH MARGIN
```

## No Voltage Divider Needed!

The TTL-RS485 converter boards are usually **5V tolerant on all inputs** from the Pi 3.3V GPIO pins:
- TX/RX: 3.3V → 5V converter accepts both
- DE/RE: 3.3V enables just fine

So you don't need a level shifter - just power it with 5V!

