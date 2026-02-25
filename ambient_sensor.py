"""
Ambient Temperature and Humidity Sensor Reader (DHT22)
Reads ambient environmental conditions for AC and dehumidification control
"""

import logging
import time
from typing import Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    import board
    import adafruit_dht
    DHT_AVAILABLE = True
except (ImportError, RuntimeError):
    DHT_AVAILABLE = False
    logger.warning("DHT sensor library not installed. Install with: pip install adafruit-circuitpython-dht")


class AmbientSensorData:
    """Container for ambient sensor readings"""
    
    def __init__(self):
        self.temperature: Optional[float] = None
        self.humidity: Optional[float] = None
        self.timestamp: Optional[str] = None
        self.is_valid: bool = False
        self.error: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'timestamp': self.timestamp,
            'is_valid': self.is_valid,
            'error': self.error
        }


class AmbientSensorReader:
    """
    Reads DHT22 temperature and humidity sensor
    GPIO pin 25 (physical pin 37) on Raspberry Pi
    """
    
    def __init__(self, pin='D25', timeout: float = 2.0):
        """
        Initialize DHT22 sensor reader
        
        Args:
            pin: GPIO pin identifier (default: 'D25' for GPIO 25)
            timeout: Read timeout in seconds
        """
        self.pin = pin
        self.timeout = timeout
        self.sensor = None
        self._initialize_sensor()
    
    def _initialize_sensor(self):
        """Initialize DHT22 sensor connection"""
        if not DHT_AVAILABLE:
            logger.warning("DHT sensor library not available - sensor disabled")
            return
        
        try:
            # Using board.D25 for GPIO 25
            import board
            pin_mapping = {
                'D25': board.D25,
                'D26': board.D26,
                'D24': board.D24,
            }
            
            if self.pin not in pin_mapping:
                logger.error(f"Invalid pin: {self.pin}. Use D24, D25, or D26")
                return
            
            import adafruit_dht
            self.sensor = adafruit_dht.DHT22(pin_mapping[self.pin])
            logger.info(f"DHT22 sensor initialized on pin {self.pin}")
        except Exception as e:
            logger.error(f"Failed to initialize DHT22 sensor: {e}")
            self.sensor = None
    
    def read(self, retries: int = 3) -> AmbientSensorData:
        """
        Read temperature and humidity from DHT22
        
        Args:
            retries: Number of retry attempts
            
        Returns:
            AmbientSensorData object with readings
        """
        data = AmbientSensorData()
        data.timestamp = datetime.now().isoformat()
        
        if not self.sensor:
            data.error = "DHT22 sensor not initialized"
            logger.error(data.error)
            return data
        
        for attempt in range(retries):
            try:
                temp = self.sensor.temperature
                humidity = self.sensor.humidity
                
                if temp is None or humidity is None:
                    if attempt == retries - 1:
                        data.error = f"Failed to read after {retries} attempts"
                    time.sleep(0.5)
                    continue
                
                # Validate readings
                if -40 <= temp <= 80 and 0 <= humidity <= 100:
                    data.temperature = round(temp, 1)
                    data.humidity = round(humidity, 1)
                    data.is_valid = True
                    logger.debug(f"Ambient: Temp={data.temperature}°C, Humidity={data.humidity}%")
                    return data
                else:
                    logger.warning(f"Out-of-range readings: T={temp}°C, H={humidity}%")
                    if attempt == retries - 1:
                        data.error = "Out-of-range sensor values"
                    time.sleep(0.5)
                    continue
                
            except RuntimeError as e:
                if attempt == retries - 1:
                    data.error = str(e)
                    logger.error(f"DHT22 read error: {e}")
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Unexpected error reading DHT22: {e}")
                data.error = str(e)
                break
        
        return data
    
    def disconnect(self):
        """Clean up sensor connection"""
        if self.sensor:
            try:
                self.sensor.exit()
            except:
                pass


class ACControlAutomation:
    """
    Automatic AC control based on ambient temperature and humidity
    """
    
    def __init__(self, 
                 temp_on_threshold: float = 28.0,
                 temp_off_threshold: float = 24.0,
                 humidity_on_threshold: float = 70.0,
                 humidity_off_threshold: float = 60.0):
        """
        Initialize AC control parameters
        
        Args:
            temp_on_threshold: Temperature (°C) at which AC turns ON
            temp_off_threshold: Temperature (°C) at which AC turns OFF
            humidity_on_threshold: Humidity (%) at which AC turns ON for dehumidification
            humidity_off_threshold: Humidity (%) at which AC turns OFF
        """
        self.temp_on = temp_on_threshold
        self.temp_off = temp_off_threshold
        self.humidity_on = humidity_on_threshold
        self.humidity_off = humidity_off_threshold
        
        self.ac_active = False
        self.previous_state = None
        
        logger.info(f"AC Control initialized:")
        logger.info(f"  Temperature: {temp_off_threshold}°C (OFF) - {temp_on_threshold}°C (ON)")
        logger.info(f"  Humidity: {humidity_off_threshold}% (OFF) - {humidity_on_threshold}% (ON)")
    
    def decide(self, temperature: Optional[float], humidity: Optional[float]) -> Tuple[bool, str]:
        """
        Decide whether AC should be ON or OFF
        
        Args:
            temperature: Current ambient temperature in °C
            humidity: Current ambient humidity in %
            
        Returns:
            Tuple of (ac_should_be_on: bool, reason: str)
        """
        if temperature is None or humidity is None:
            return self.ac_active, "Missing sensor data"  # Keep current state
        
        # Decision logic with hysteresis
        if self.ac_active:
            # AC is ON - check OFF conditions
            if temperature <= self.temp_off and humidity <= self.humidity_off:
                self.ac_active = False
                reason = f"AC OFF: Temp={temperature}°C (≤{self.temp_off}), Humidity={humidity}% (≤{self.humidity_off})"
            else:
                reason = f"AC ON: Temp={temperature}°C, Humidity={humidity}%"
        else:
            # AC is OFF - check ON conditions
            if temperature >= self.temp_on or humidity >= self.humidity_on:
                self.ac_active = True
                if temperature >= self.temp_on:
                    reason = f"AC ON: Temp={temperature}°C (≥{self.temp_on})"
                else:
                    reason = f"AC ON: Humidity={humidity}% (≥{self.humidity_on})"
            else:
                reason = f"AC OFF: Temp={temperature}°C, Humidity={humidity}%"
        
        return self.ac_active, reason


def initialize_logger(log_file: Optional[str] = None, level: int = logging.INFO):
    """Setup logging configuration"""
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create log file {log_file}: {e}")
    
    logger.setLevel(level)


if __name__ == '__main__':
    initialize_logger()
    
    # Test ambient sensor
    sensor = AmbientSensorReader(pin='D25')
    
    print("\nTesting ambient sensor (5 reads)...")
    for i in range(5):
        data = sensor.read()
        if data.is_valid:
            print(f"Read {i+1}: Temp={data.temperature}°C, Humidity={data.humidity}%")
        else:
            print(f"Read {i+1}: Error - {data.error}")
        time.sleep(2)
    
    # Test AC control logic
    print("\n\nTesting AC control logic...")
    ac_control = ACControlAutomation(temp_on_threshold=28.0, humidity_on_threshold=70.0)
    
    test_cases = [
        (20, 50, "Cool and dry"),
        (25, 65, "Warm and moderate"),
        (28, 70, "Hot and humid"),
        (32, 80, "Very hot and humid"),
        (26, 55, "Warm but dry"),
    ]
    
    for temp, hum, desc in test_cases:
        should_run, reason = ac_control.decide(temp, hum)
        print(f"{desc:25} → AC {'ON' if should_run else 'OFF':3} ({reason})")
    
    sensor.disconnect()
