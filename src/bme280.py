from datetime import datetime
import math

from busio import I2C  # pylint: disable=import-error
from adafruit_bme280.basic import Adafruit_BME280_I2C  # pylint: disable=import-error
from config import GPIOConfig
from sensor_reading import SensorReading


class Bme280Sensor:
    def __init__(self, gpio_config: GPIOConfig, altitude: float, std_sea_level_pressure: float):
        i2c = I2C(3, 2)
        self.bme280 = Adafruit_BME280_I2C(i2c, address=gpio_config.i2c_address)
        self.bme280.sea_level_pressure = std_sea_level_pressure
        self.altitude = altitude

    def get_normalized_pressure(self):
        c = 0.00012
        abs_pressure = self.bme280.pressure
        normalized_pressure = abs_pressure * math.exp(c * self.altitude)
        return normalized_pressure

    def get_temperature(self):
        return self.bme280.temperature

    def get_relative_humidity(self):
        return self.bme280.relative_humidity

    def get_measurement(self, weather_station_uuid: str):
        sensor_reading = SensorReading(
            temperature=self.get_temperature(),
            pressure=self.get_normalized_pressure(),
            humidity=self.get_relative_humidity(),
            timestamp=datetime.now(),
            weather_station_uuid=weather_station_uuid,
        )
        return sensor_reading
