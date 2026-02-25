#!/usr/bin/env python3
"""
Hardware verification script for TTL to RS485 Power Supply Converter Board
Tests GPIO pins, serial port, and sensor communications
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except (ImportError, RuntimeError):
    GPIO_AVAILABLE = False
    print("⚠️  GPIO not available (not on Raspberry Pi or not enough privileges)")

import time
import subprocess

def check_serial_port(port='/dev/serial0'):
    """Verify serial port exists and is readable."""
    print(f"\n🔌 Checking Serial Port: {port}")
    if os.path.exists(port):
        print(f"  ✅ {port} exists")
        try:
            os.access(port, os.R_OK | os.W_OK)
            print(f"  ✅ {port} is readable and writable")
            return True
        except PermissionError:
            print(f"  ❌ Permission denied - try: sudo chmod 666 {port}")
            return False
    else:
        print(f"  ❌ {port} not found")
        print(f"     Try: /dev/ttyAMA0 or check: ls /dev/tty*")
        return False

def check_gpio_pins():
    """Verify GPIO pins are accessible."""
    print(f"\n⚡ Checking GPIO Pins")
    
    if not GPIO_AVAILABLE:
        print("  ⚠️  GPIO library not available")
        return False
    
    test_pins = {
        24: "DE/RE Control",
        14: "UART0 TX",
        15: "UART0 RX"
    }
    
    try:
        GPIO.setmode(GPIO.BCM)
        for pin, description in test_pins.items():
            try:
                GPIO.setup(pin, GPIO.OUT)
                print(f"  ✅ GPIO {pin} ({description}) - OK")
                GPIO.setup(pin, GPIO.IN)  # Reset to input
            except Exception as e:
                print(f"  ⚠️  GPIO {pin} ({description}) - {e}")
        
        GPIO.cleanup()
        return True
    except Exception as e:
        print(f"  ❌ GPIO Error: {e}")
        return False

def check_power_supply():
    """Check power supply info."""
    print(f"\n🔋 Checking Power Supply")
    
    try:
        result = subprocess.run(
            ["vcgencmd", "measure_volts"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"  {result.stdout.strip()}")
        
        result = subprocess.run(
            ["vcgencmd", "measure_clock", "arm"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"  {result.stdout.strip()}")
        
        return True
    except Exception as e:
        print(f"  ⚠️  Power check unavailable: {e}")
        return False

def run_sensor_test():
    """Run sensor scanner to test full setup."""
    print(f"\n📡 Running Sensor Scanner Test")
    print("  This will attempt to read from all 4 sensors...")
    
    try:
        result = subprocess.run(
            ["python3", "sensor_scanner.py", "--timeout", "2"],
            capture_output=True,
            text=True,
            timeout=20
        )
        
        if "RESPONDING" in result.stdout:
            print(f"  ✅ Sensor communication successful!")
            # Print first few lines of output
            lines = result.stdout.split('\n')[:10]
            for line in lines:
                print(f"     {line}")
            return True
        else:
            print(f"  ⚠️  No sensors responding")
            print(f"     Check RS485 wiring and power connections")
            return False
            
    except Exception as e:
        print(f"  ⚠️  Sensor test error: {e}")
        return False

def main():
    """Run all hardware checks."""
    print("="*70)
    print("TTL to RS485 CONVERTER BOARD - HARDWARE VERIFICATION")
    print("="*70)
    
    checks = {
        "Serial Port": check_serial_port(),
        "GPIO Pins": check_gpio_pins(),
        "Power Supply": check_power_supply(),
    }
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "⚠️  CHECK"
        print(f"{check_name:.<40} {status}")
    
    # Offer to run sensor test
    print("\n" + "="*70)
    if all(checks.values()):
        print("✅ All hardware checks passed!")
        print("\nRun sensor test? (y/n): ", end="", flush=True)
        if input().lower() == 'y':
            run_sensor_test()
    else:
        print("⚠️  Some checks did not pass. Check connections before testing sensors.")
    
    print("="*70)

if __name__ == '__main__':
    main()
