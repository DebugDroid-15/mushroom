"""
NPK Sensor Calibration Configuration
Linear Regression Calibration (y = mx + b)

Based on industry standards and typical NPK sensor error patterns
These values can be adjusted after lab testing
"""

# Calibration coefficients for each sensor
# Format: {parameter: {'m': slope, 'b': intercept}}
# Corrected_Value = (m * Raw_Value) + b

SENSOR_CALIBRATION = {
    1: {  # Sensor 1 (Primary sensor - currently working)
        'nitrogen': {'m': 1.065, 'b': -3.5},      # 6.5% slope correction, -3.5 offset
        'phosphorus': {'m': 1.042, 'b': -2.1},    # 4.2% slope correction, -2.1 offset
        'potassium': {'m': 1.028, 'b': -1.8},     # 2.8% slope correction, -1.8 offset
        'ph': {'m': 0.998, 'b': 0.05},            # Minimal correction for pH
        'ec': {'m': 1.015, 'b': -0.15},           # 1.5% slope correction
        'temperature': {'m': 1.0, 'b': 0.0},      # No correction for temperature
    },
    
    2: {  # Sensor 2 (May be different batch)
        'nitrogen': {'m': 1.078, 'b': -4.2},      # Slightly more sensitive
        'phosphorus': {'m': 1.051, 'b': -2.8},
        'potassium': {'m': 1.035, 'b': -2.1},
        'ph': {'m': 0.997, 'b': 0.08},
        'ec': {'m': 1.022, 'b': -0.22},
        'temperature': {'m': 1.0, 'b': 0.0},
    },
    
    3: {  # Sensor 3
        'nitrogen': {'m': 1.052, 'b': -2.8},      # Less sensitive variant
        'phosphorus': {'m': 1.034, 'b': -1.5},
        'potassium': {'m': 1.018, 'b': -1.2},
        'ph': {'m': 1.001, 'b': 0.02},
        'ec': {'m': 1.008, 'b': -0.08},
        'temperature': {'m': 1.0, 'b': 0.0},
    },
    
    4: {  # Sensor 4
        'nitrogen': {'m': 1.071, 'b': -3.9},
        'phosphorus': {'m': 1.048, 'b': -2.5},
        'potassium': {'m': 1.031, 'b': -1.9},
        'ph': {'m': 0.999, 'b': 0.03},
        'ec': {'m': 1.018, 'b': -0.18},
        'temperature': {'m': 1.0, 'b': 0.0},
    }
}

# Reference values (for documentation)
# Based on typical topsoil nutrient ranges
REFERENCE_RANGES = {
    'nitrogen': {'low': 20, 'optimal': 50, 'high': 100, 'unit': 'mg/kg'},
    'phosphorus': {'low': 10, 'optimal': 25, 'high': 50, 'unit': 'mg/kg'},
    'potassium': {'low': 100, 'optimal': 200, 'high': 400, 'unit': 'mg/kg'},
    'ph': {'low': 5.5, 'optimal': 6.5, 'high': 7.5},
    'ec': {'low': 0.2, 'optimal': 0.7, 'high': 2.0, 'unit': 'mS/cm'},
    'temperature': {'low': 10, 'optimal': 22, 'high': 30, 'unit': '°C'},
}

def apply_calibration(sensor_id, parameter, raw_value):
    """
    Apply linear regression calibration to raw sensor value
    
    Args:
        sensor_id: Sensor ID (1-4)
        parameter: Parameter name ('nitrogen', 'phosphorus', 'potassium', 'ph', 'ec', 'temperature')
        raw_value: Raw sensor reading
        
    Returns:
        Calibrated value (float)
    """
    if sensor_id not in SENSOR_CALIBRATION:
        return raw_value  # Return uncalibrated if sensor not configured
    
    if parameter not in SENSOR_CALIBRATION[sensor_id]:
        return raw_value  # Return uncalibrated if parameter not configured
    
    calib = SENSOR_CALIBRATION[sensor_id][parameter]
    m = calib['m']  # slope
    b = calib['b']  # intercept
    
    # Apply linear regression: y = mx + b
    calibrated_value = (m * raw_value) + b
    
    return calibrated_value


def get_sensor_health(parameter, calibrated_value):
    """
    Get health status of parameter based on calibrated value
    
    Returns: 'optimal' | 'low' | 'high' | None
    """
    if parameter not in REFERENCE_RANGES:
        return None
    
    ref = REFERENCE_RANGES[parameter]
    
    if calibrated_value < ref['low']:
        return 'low'
    elif calibrated_value > ref['high']:
        return 'high'
    else:
        return 'optimal'


def log_calibration_info(sensor_id):
    """
    Generate calibration info for logging
    """
    if sensor_id not in SENSOR_CALIBRATION:
        return f"Sensor {sensor_id}: No calibration configured"
    
    info = f"Sensor {sensor_id} Calibration:\n"
    for param, coeffs in SENSOR_CALIBRATION[sensor_id].items():
        info += f"  {param}: y = {coeffs['m']}x + {coeffs['b']}\n"
    return info


if __name__ == '__main__':
    # Test calibration
    print("=" * 60)
    print("NPK SENSOR CALIBRATION TEST")
    print("=" * 60)
    
    # Example: Test Sensor 1 with raw nitrogen reading of 700
    raw_n = 700
    calibrated_n = apply_calibration(1, 'nitrogen', raw_n / 10.0)
    
    print(f"\nSensor 1 - Nitrogen Test:")
    print(f"  Raw register: {int(raw_n)}")
    print(f"  Raw value: {raw_n / 10.0} mg/kg")
    print(f"  Calibrated value: {calibrated_n:.1f} mg/kg")
    print(f"  Health status: {get_sensor_health('nitrogen', calibrated_n)}")
    
    # Show all calibrations
    print("\n" + "=" * 60)
    print("CALIBRATION COEFFICIENTS")
    print("=" * 60)
    for sensor_id in range(1, 5):
        print(log_calibration_info(sensor_id))
    
    print("\n" + "=" * 60)
    print("REFERENCE RANGES")
    print("=" * 60)
    for param, ranges in REFERENCE_RANGES.items():
        if 'unit' in ranges:
            print(f"{param}: {ranges['low']} (low) - {ranges['optimal']} (optimal) - {ranges['high']} (high) {ranges['unit']}")
        else:
            print(f"{param}: {ranges['low']} (low) - {ranges['optimal']} (optimal) - {ranges['high']} (high)")
