"""
Configuration for Soil Monitoring System

Copy this file to config.py and update settings as needed.
Environment variables override these defaults.
"""

import os

# UART Configuration
MODBUS_PORT = os.getenv('MODBUS_PORT', '/dev/serial0')
MODBUS_BAUDRATE = int(os.getenv('MODBUS_BAUDRATE', '9600'))
MODBUS_TIMEOUT = float(os.getenv('MODBUS_TIMEOUT', '1.0'))

# Sensor Configuration
SENSOR_IDS = [1, 2, 3, 4]

# Modbus Register Addresses (verify with your sensor datasheet)
REGISTER_NITROGEN = 0x0000
REGISTER_PHOSPHORUS = 0x0001
REGISTER_POTASSIUM = 0x0002
REGISTER_MOISTURE = 0x0003

# Scale factors (divide register value by this to get actual value)
# Common NPK sensors use factor 10 (e.g., raw 1855 → 185.5 mg/kg)
REGISTER_SCALE_FACTOR = 10.0

# Flask Configuration
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Logging
LOG_FILE = '/var/log/soil-monitor/app.log'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Data Caching (for redundancy if read fails)
CACHE_READINGS = True
CACHE_DURATION = 300  # seconds

# GPIO Configuration (optional - for manual DE/RE control)
# If using GPIO for RS-485 direction control, specify the pin number
# Set to None to disable GPIO control
GPIO_DE_RE_PIN = None  # os.getenv('GPIO_DE_RE_PIN', None)

# Advanced: Custom register mapping if your sensors differ
# Uncomment and modify if needed:
# REGISTER_MAP = {
#     1: {'N': 0x0000, 'P': 0x0001, 'K': 0x0002, 'Moisture': 0x0003},
#     2: {'N': 0x0000, 'P': 0x0001, 'K': 0x0002, 'Moisture': 0x0003},
#     # ... etc
# }
