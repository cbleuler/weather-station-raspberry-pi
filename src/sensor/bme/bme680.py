from datetime import datetime

from adafruit_bme680 import Adafruit_BME680_I2C  # pylint: disable=import-error
from sensor_reading import SensorReading
from sensor.bme.bme280 import Bme280Sensor


class Bme680Sensor(Bme280Sensor):
    @staticmethod
    def _setup_sensor(i2c_interface, i2c_address):
        return Adafruit_BME680_I2C(i2c_interface, address=i2c_address)

    def get_air_quality(self):
        return self.sensor.gas

    def get_measurement(self, weather_station_uuid: str):
        sensor_reading = SensorReading(
            temperature=self.get_temperature(),
            pressure=self.get_normalized_pressure(),
            humidity=self.get_relative_humidity(),
            air_quality=self.get_air_quality(),
            timestamp=datetime.now(),
            weather_station_uuid=weather_station_uuid,
        )
        return sensor_reading
