#!/usr/bin/env python3
"""
Modbus Sensor Scanner - Diagnostic tool to scan and test NPK sensors
Scans up to 4 sensors on RS485 bus and displays register values
"""

import sys
import time
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException

class SensorScanner:
    """Scanner for NPK Modbus sensors on RS485"""
    
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, timeout=1.0):
        """Initialize scanner with Modbus connection parameters"""
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.client = None
    
    def connect(self):
        """Establish Modbus RTU connection"""
        try:
            self.client = ModbusClient(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            if self.client.connect():
                print(f"✅ Connected to Modbus RTU on {self.port} @ {self.baudrate} baud")
                return True
            else:
                print(f"❌ Failed to connect to {self.port}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def disconnect(self):
        """Close Modbus connection"""
        if self.client:
            self.client.close()
            print("Disconnected from Modbus")
    
    def read_sensor_registers(self, sensor_id, start_address=4, count=8, retries=3):
        """
        Read registers from a sensor
        
        Args:
            sensor_id: Modbus slave ID (1-4)
            start_address: Starting register address (default 4)
            count: Number of registers to read (default 8)
            retries: Number of retry attempts
            
        Returns:
            Tuple of (success: bool, registers: list or error_message: str)
        """
        if not self.client or not self.client.is_socket_open():
            return False, "Not connected to Modbus"
        
        for attempt in range(retries):
            try:
                result = self.client.read_holding_registers(
                    address=start_address,
                    count=count,
                    device_id=sensor_id
                )
                
                if isinstance(result, Exception) or result.isError():
                    if attempt == retries - 1:
                        return False, f"No response after {retries} attempts"
                    time.sleep(0.2)
                    continue
                
                return True, result.registers
                
            except Exception as e:
                if attempt == retries - 1:
                    return False, str(e)
                time.sleep(0.2)
        
        return False, f"Failed after {retries} retries"
    
    def parse_sensor_data(self, registers):
        """
        Parse NPK sensor registers
        
        Assumes layout:
        reg[0-1]: unused
        reg[2]: Nitrogen * 10
        reg[3]: Phosphorus * 10
        reg[4]: Potassium * 10
        reg[5]: pH * 100
        reg[6]: EC * 100
        reg[7]: Temperature * 100
        """
        if not registers or len(registers) < 8:
            return None
        
        try:
            return {
                'nitrogen': registers[2] / 10.0,
                'phosphorus': registers[3] / 10.0,
                'potassium': registers[4] / 10.0,
                'ph': registers[5] / 100.0,
                'ec': registers[6] / 100.0,
                'temperature': registers[7] / 100.0
            }
        except (IndexError, TypeError, ZeroDivisionError):
            return None
    
    def scan_all_sensors(self, sensor_ids=[1, 2, 3, 4]):
        """
        Scan all sensors and display results
        
        Args:
            sensor_ids: List of sensor IDs to scan (default [1, 2, 3, 4])
        """
        print("\n" + "="*70)
        print("MODBUS SENSOR SCANNER - NPK SOIL SENSORS")
        print("="*70)
        print(f"Port: {self.port} | Baudrate: {self.baudrate} | Timeout: {self.timeout}s")
        print("="*70 + "\n")
        
        results = {}
        for sensor_id in sensor_ids:
            print(f"Scanning Sensor {sensor_id}...", end=" ", flush=True)
            
            success, data = self.read_sensor_registers(sensor_id)
            
            if success:
                print("✅ RESPONDING")
                results[sensor_id] = {'success': True, 'registers': data}
                
                # Parse and display data
                parsed = self.parse_sensor_data(data)
                if parsed:
                    print(f"  Raw Registers: {data}")
                    print(f"  ├─ Nitrogen (N):  {parsed['nitrogen']:.1f} mg/kg")
                    print(f"  ├─ Phosphorus (P): {parsed['phosphorus']:.1f} mg/kg")
                    print(f"  ├─ Potassium (K):  {parsed['potassium']:.1f} mg/kg")
                    print(f"  ├─ pH:             {parsed['ph']:.2f}")
                    print(f"  ├─ EC:             {parsed['ec']:.2f} mS/cm")
                    print(f"  └─ Temperature:    {parsed['temperature']:.1f}°C")
                else:
                    print(f"  Raw Registers: {data}")
                    print(f"  ⚠️  Could not parse sensor data")
            else:
                print(f"❌ NO RESPONSE - {data}")
                results[sensor_id] = {'success': False, 'error': data}
            
            print()
        
        # Summary
        print("="*70)
        print("SCAN SUMMARY")
        print("="*70)
        working = sum(1 for r in results.values() if r['success'])
        total = len(results)
        print(f"Working Sensors: {working}/{total}")
        
        for sensor_id, result in results.items():
            status = "✅ WORKING" if result['success'] else "❌ NOT RESPONDING"
            print(f"  Sensor {sensor_id}: {status}")
        
        print("="*70 + "\n")
        return results


def main():
    """Main scanner function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Modbus Sensor Scanner - Test NPK sensors on RS485',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sensor_scanner.py                    # Scan default serial port
  python sensor_scanner.py --port COM3        # Windows serial port
  python sensor_scanner.py --port /dev/ttyUSB0  # Linux/Pi USB adapter
  python sensor_scanner.py --sensors 1 2 3   # Scan specific sensors
        """
    )
    
    parser.add_argument('--port', default='/dev/ttyAMA0',
                       help='Serial port (default: /dev/ttyAMA0 for Pi)')
    parser.add_argument('--baudrate', type=int, default=9600,
                       help='Modbus baudrate (default: 9600)')
    parser.add_argument('--timeout', type=float, default=1.0,
                       help='Read timeout in seconds (default: 1.0)')
    parser.add_argument('--sensors', type=int, nargs='+', default=[1, 2, 3, 4],
                       help='Sensor IDs to scan (default: 1 2 3 4)')
    parser.add_argument('--loop', action='store_true',
                       help='Run continuous scanning (Ctrl+C to stop)')
    parser.add_argument('--interval', type=int, default=5,
                       help='Scan interval in seconds for --loop mode (default: 5)')
    
    args = parser.parse_args()
    
    scanner = SensorScanner(
        port=args.port,
        baudrate=args.baudrate,
        timeout=args.timeout
    )
    
    if not scanner.connect():
        sys.exit(1)
    
    try:
        if args.loop:
            print(f"📊 Continuous scanning mode (scanning every {args.interval}s)")
            print("Press Ctrl+C to stop\n")
            iteration = 1
            while True:
                print(f"\n{'─'*70}")
                print(f"Scan Iteration {iteration} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'─'*70}\n")
                scanner.scan_all_sensors(args.sensors)
                iteration += 1
                time.sleep(args.interval)
        else:
            scanner.scan_all_sensors(args.sensors)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Scan interrupted by user")
    
    finally:
        scanner.disconnect()


if __name__ == '__main__':
    main()
