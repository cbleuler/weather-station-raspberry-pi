from datetime import datetime
import math

from busio import I2C  # pylint: disable=import-error
from adafruit_bme280.basic import Adafruit_BME280_I2C  # pylint: disable=import-error
from config import SensorConfig
from sensor_reading import SensorReading


class Bme280Sensor:
    def __init__(self, sensor_config: SensorConfig, altitude: float, std_sea_level_pressure: float):
        i2c = I2C(3, 2)
        self.sensor = self._setup_sensor(i2c_interface=i2c, i2c_address=sensor_config.i2c_address)
        self.sensor.sea_level_pressure = std_sea_level_pressure
        self.altitude = altitude

    @staticmethod
    def _setup_sensor(i2c_interface, i2c_address):
        return Adafruit_BME280_I2C(i2c_interface, address=i2c_address)

    def get_normalized_pressure(self):
        c = 0.00012
        abs_pressure = self.sensor.pressure
        normalized_pressure = abs_pressure * math.exp(c * self.altitude)
        return normalized_pressure

    def get_temperature(self):
        return self.sensor.temperature

    def get_relative_humidity(self):
        return self.sensor.relative_humidity

    def get_measurement(self, weather_station_uuid: str):
        sensor_reading = SensorReading(
            temperature=self.get_temperature(),
            pressure=self.get_normalized_pressure(),
            humidity=self.get_relative_humidity(),
            timestamp=datetime.now(),
            weather_station_uuid=weather_station_uuid,
        )
        return sensor_reading
