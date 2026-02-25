# TTL to RS485 Power Supply Converter - QUICK REFERENCE

## Critical Connections (Don't forget!)

```
Pi 3.3V    → Converter VCC
Pi GND     → Converter GND + Sensor GND (all)  ⚠️ IMPORTANT!
Pi GPIO24  → Converter DE/RE
Pi GPIO14  → Converter DI (TX)
Pi GPIO15  → Converter RO (RX)
Converter A+ → All Sensors A+ (twisted pair)
Converter B- → All Sensors B- (twisted pair)
```

## Pre-Flight Checklist

- ☐ 3.3V power supply connected
- ☐ All GND connections complete (critical!)
- ☐ RS485 twisted pair connected to A+ and B-
- ☐ No short circuits between A+ and B-
- ☐ Sensor connectors firmly seated
- ☐ DE/RE pin connected (if using auto direction control)

## Testing Commands

```bash
# Hardware verification (run on Pi)
python3 test_hardware.py

# Quick sensor scan (show all sensors status)
scan-sensors

# Continuous monitoring (press Ctrl+C to stop)
scan-sensors --loop

# Test specific sensors
scan-sensors --sensors 1 2
```

## Expected Success Output

```
✅ Sensor 1... RESPONDING
✅ Sensor 2... RESPONDING
✅ Sensor 3... RESPONDING
✅ Sensor 4... RESPONDING
```

## Common Issues & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| "NO RESPONSE" on all sensors | 3.3V not connected | Check VCC connection to converter |
| "NO RESPONSE" on all sensors | GND not connected | **Check GND connection (most common!)** |
| "NO RESPONSE" on all sensors | TX/RX swapped | Swap GPIO 14 and 15 connections |
| Only sensor 1 responds | RS485 wiring incomplete | Check A+ and B- twisted pair |
| Random errors | Loose connections | Reseat all connectors |
| Intermittent failures | Noise on RS485 | Add 120Ω terminator at sensor end |

## Voltage Check (On Pi)

```bash
# Check power rail
vcgencmd measure_volts

# Should show approximately: volt=3.3V
```

## GPIO Pin Reference (Physical Location)

```
Pi GPIO Header (looking at board):
┌─────────────┐
│ 1(3V3) 2 (5V) │
│ 3(SDA) 4 (5V) │
│ 5(SCL) 6(GND) │
│ 7(GPIO4) 8(TX/GPIO14) ◄─── TX
│ 9(GND) 10(RX/GPIO15) ◄─── RX
│ 11(GPIO17) 12(GPIO18) │
│ 13(GPIO27) 14(GND) │
│ 15(GPIO22) 16(GPIO23) │
│ 17(3V3) 18(GPIO24) ◄─── DE/RE
│ 19(GPIO10) 20(GND) │
└─────────────┘
```

## Performance Notes

⚡ **Power Budget:**
- Pi 3.3V supply: ~400 mA available
- Board + 4 Sensors: ~200 mA typical, 250 mA peak
- **Safe**: ✅ (50% margin)

📊 **Data Rate:**
- Baudrate: 9600 bps (standard)
- Read 1 sensor: ~50-100 ms
- Read 4 sensors in sequence: ~200-400 ms
- Dashboard updates: Every 5 seconds

## Troubleshooting Last Steps

1. **Power off Pi completely** (wait 10 seconds)
2. **Check every connection** (especially GND!)
3. **Power back on**
4. **Run `scan-sensors`** to verify
5. **Check `/var/log/soil-monitor/app.log`** for errors

```bash
tail -f /var/log/soil-monitor/app.log
```

