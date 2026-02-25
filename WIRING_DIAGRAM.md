# TTL to RS485 Converter Board - Wiring Diagram

## ASCII Wiring Diagram

```
╔════════════════════════════════════════════════════════════════╗
║                    RASPBERRY PI 5                              ║
╠════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  3V3  GND  GPIO24  GPIO14  GPIO15                              ║
║  │    │     │       │       │                                  ║
║  │    │     │       │       │                                  ║
║  │    │     │       │       │                                  ║
║  └────┼─────┼───────┼───────┘                                  ║
║       │     │       │                                          ║
└───────┼─────┼───────┼──────────────────────────────────────────┘
        │     │       │
        │     │       ├─────────────────────────────────────┐
        │     │       │                                      │
        ▼     │       │    ┌──────────────────────────────┐  │
    ┌───────┐│       │    │ TTL to RS485 Board           │  │
    │ 3.3V  ││       │    │                              │  │
    │ Power ││       │    │  VCC ◄─┘ 3.3V               │  │
    └───────┘│       │    │ GND ◄─┘ GND                 │  │
        ▲     │       │    │ DE/RE ◄─┘ GPIO24           │┌─┤─ TX (DI)
        │     │       │    │ DI (TX) ◄──────────────────┘│ │
        │     │       └───►│ RO (RX) ◄──────────────────┐│ │
        │     │            │ A+ ─────────────────┐      ││ │
        │     │            │ B- ─────────────────┼──────┘│ │
        │     │            │ GND ────────────────┼─────┐ │ │
        │     │            └────────────────────┬┘      │ │ │
        │     ▼                                 │       │ │ │
     Battery/ │                        ╔═══════╧═══════╧═╧═╧═════════╗
     USB PSU  │                        ║   RS485 Bus - 2 Wire        ║
              │                        ╠════════════════════════════╣
              └────────────────────────╫──────────┬──────┬──────────║
                                       ║          │      │          ║
                        ┌──────────────╨──────────┼──────┼──────────╨─┐
                        │                         │      │            │
                        │                    ┌────▼──────▼────┐       │
                        │    NPK Sensor 1    │ A+  B-  GND   │       │
                        │                    │ 7-pin DIN      │       │
                        │                    └────┬──┬──┬─────┘       │
                        │                         │  │  │            │
                        │                    ┌────▼──▼──▼─────┐       │
                        │    NPK Sensor 2    │ A+  B-  GND   │       │
                        │                    │ 7-pin DIN      │       │
                        │                    └────┬──┬──┬─────┘       │
                        │                         │  │  │            │
                        │                    ┌────▼──▼──▼─────┐       │
                        │    NPK Sensor 3    │ A+  B-  GND   │       │
                        │                    │ 7-pin DIN      │       │
                        │                    └────┬──┬──┬─────┘       │
                        │                         │  │  │            │
                        │                    ┌────▼──▼──▼─────┐       │
                        │    NPK Sensor 4    │ A+  B-  GND   │       │
                        │                    │ 7-pin DIN      │       │
                        │                    └────┬──┬──┬─────┘       │
                        │                         │  │  │            │
                        └─────────────────────────┴──┴──┴────────────┘

```

## Pin-by-Pin Connections

### Raspberry Pi → Converter Board

| Pi Pin | GPIO | Function | → | Converter |
|--------|------|----------|---|-----------|
| 1      | -    | 3.3V     | → | VCC       |
| 6      | -    | GND      | → | GND       |
| 8      | 14   | UART TX  | → | DI        |
| 10     | 15   | UART RX  | → | RO        |
| 18     | 24   | GPIO     | → | DE/RE     |

### Converter Board → Sensors (All in parallel)

| Converter | Function | → | NPK Sensors Port |
|-----------|----------|---|------------------|
| A+        | RS485 A+ | → | Sensor A+ (all)  |
| B-        | RS485 B- | → | Sensor B- (all)  |
| GND       | Ground   | → | Sensor GND (all) |

## Cable Recommendations

- **RS485 Bus:** Twisted pair, 120Ω impedance (Cat5e works)
- **Power/GND:** Multi-conductor cable (separate from RS485)
- **Max Length:** ~30-50m for RS485 with good shielding
- **Sensor Connections:** Use DIN connectors for reliability

## Power Consumption Estimation

```
Component               Current @ 3.3V    Notes
─────────────────────────────────────────────────────
Converter Board         ~5-10 mA          Always on
NPK Sensor (1)          ~30-50 mA         During read
NPK Sensor (4 total)    ~120-200 mA peak  All reading
─────────────────────────────────────────────────────
Total Estimated         ~150-250 mA       Peak usage
Available from Pi 3.3V: ~400 mA           Safe margin
```

✅ **Power budget is adequate**

