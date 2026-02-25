#!/usr/bin/env python3
"""
Quick NPK Sensor Verification Script
Tests register communication and displays sensor data
"""

import sys
sys.path.insert(0, '/home/mushroom/mushroom_project')

from pymodbus.client import ModbusSerialClient as ModbusClient
import time

def test_sensor(sensor_id, port='/dev/ttyAMA0'):
    """Test individual sensor"""
    print(f"\n{'='*60}")
    print(f"Testing Sensor {sensor_id}")
    print(f"{'='*60}")
    
    client = ModbusClient(port=port, baudrate=9600, timeout=1.0)
    
    if not client.connect():
        print(f"❌ Failed to connect to {port}")
        return False
    
    try:
        # Read registers
        result = client.read_holding_registers(address=4, count=8, device_id=sensor_id)
        
        if result.isError():
            print(f"❌ Sensor {sensor_id}: NO RESPONSE")
            return False
        
        registers = result.registers
        print(f"✅ Sensor {sensor_id}: RESPONDING")
        print(f"   Raw Registers: {registers}")
        
        if len(registers) >= 8:
            # Parse data
            n = registers[2] / 10.0
            p = registers[3] / 10.0
            k = registers[4] / 10.0
            ph = registers[5] / 100.0
            ec = registers[6] / 100.0
            temp = registers[7] / 100.0
            
            print(f"\n   📊 Sensor Data:")
            print(f"   ├─ Nitrogen (N):   {n:.1f} mg/kg")
            print(f"   ├─ Phosphorus (P): {p:.1f} mg/kg")
            print(f"   ├─ Potassium (K):  {k:.1f} mg/kg")
            print(f"   ├─ pH:             {ph:.2f}")
            print(f"   ├─ EC:             {ec:.2f} mS/cm")
            print(f"   └─ Temperature:    {temp:.1f}°C")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading sensor {sensor_id}: {e}")
        return False
    finally:
        client.close()

def main():
    """Test all sensors"""
    print("\n" + "="*60)
    print("NPK SENSOR QUICK TEST")
    print("="*60)
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Port: /dev/ttyAMA0 | Baudrate: 9600")
    
    results = []
    for sensor_id in [1, 2, 3, 4]:
        success = test_sensor(sensor_id)
        results.append((sensor_id, success))
        time.sleep(0.5)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    working = sum(1 for _, success in results if success)
    print(f"Sensors Responding: {working}/4")
    
    for sensor_id, success in results:
        status = "✅ OK" if success else "❌ NO RESPONSE"
        print(f"  Sensor {sensor_id}: {status}")
    
    print("="*60 + "\n")
    
    if working > 0:
        print("✅ SUCCESS! Sensors are responding.")
        print("   Run 'scan-sensors --loop' for continuous monitoring")
    else:
        print("❌ No sensors responding. Check:")
        print("   1. RX/TX connections are CROSSED (RX→TX pin, TX→RX pin)")
        print("   2. 5V power is connected to converter board")
        print("   3. GND is common between Pi and 5V supply")
        print("   4. RS485 A+/B- connected to all sensors")

if __name__ == '__main__':
    main()
