import asyncio
import datetime
import logging
import time
from pathlib import Path

from api_client import ApiClient
from config import WeatherStationConfig, SensorConfig
from errors import InvalidSensorTypeError
from sensor.bme.bme280 import Bme280Sensor
from sensor.bme.bme680 import Bme680Sensor
from sensor.sensor_constant import ConstantSensor

SENSOR_MAPPING = {"bme280": Bme280Sensor, "bme680": Bme680Sensor, "constant": ConstantSensor}


class Runner:
    def __init__(self, weather_station_config: WeatherStationConfig):
        self.weather_station_config = weather_station_config
        self.sensor = self._setup_sensor(
            sensor_config=self.weather_station_config.sensor_config,
            altitude=self.weather_station_config.altitude,
            std_sea_level_pressure=self.weather_station_config.std_sea_level_pressure,
        )
        self.api_client = ApiClient.init_from_config(api_config=self.weather_station_config.api)
        self.weather_station_uuid = self.weather_station_config.uuid

    @staticmethod
    def init_from_config_file(config_file: Path):
        weather_station_config = WeatherStationConfig.load(config_file)
        return Runner(weather_station_config=weather_station_config)

    @staticmethod
    def _setup_sensor(sensor_config: SensorConfig, altitude: float, std_sea_level_pressure: float):
        try:
            sensor = SENSOR_MAPPING[sensor_config.type.lower()](
                sensor_config=sensor_config, altitude=altitude, std_sea_level_pressure=std_sea_level_pressure
            )
            logging.debug("Sensor of type %s is initialized.", sensor_config.type)
            return sensor
        except KeyError as e:
            raise InvalidSensorTypeError(
                f"Sensor type '{sensor_config.type}' is invalid. Must be in {', '.join(SENSOR_MAPPING.keys())}"
            ) from e

    async def process_new_reading(self):
        reading = self.sensor.get_measurement(weather_station_uuid=self.weather_station_uuid)
        await self.api_client.send_reading(reading)

    async def run(self):
        while True:
            try:
                await asyncio.gather(self.process_new_reading(), asyncio.sleep(1))
                logging.debug("Measurement sent at %s.", datetime.datetime.utcnow().isoformat())
            except ConnectionError as e:
                logging.warning("Connection error occurred: %s", e)
                time.sleep(5)
