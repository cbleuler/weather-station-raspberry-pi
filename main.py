import logging
import time
import asyncio

from sensor.bme.bme280 import Bme280Sensor
from api_client import ApiClient
from config import WeatherStationConfig
from requests.exceptions import ConnectionError

logging.basicConfig(level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")

auth_header = {}


async def process_new_reading(sensor: Bme280Sensor, api_client: ApiClient, weather_station_uuid: str):
    reading = sensor.get_measurement(weather_station_uuid=weather_station_uuid)
    await api_client.send_reading(reading)


async def main(config: WeatherStationConfig):
    api_client, sensor = await initialize(config)

    logging.debug("Readings will be sent to: %s", api_client.request_url)

    while True:
        try:
            await asyncio.gather(process_new_reading(sensor, api_client, config.uuid), asyncio.sleep(1))
            logging.debug("Measurement sent.")
        except ConnectionError as e:
            logging.warning("Connection error occurred: %s", e)
            time.sleep(5)


async def initialize(config):
    sensor = Bme280Sensor(
        config.sensor_config, altitude=config.altitude, std_sea_level_pressure=config.normal_sea_level_pressure
    )
    logging.debug("Sensor is initialized.")
    api_client = ApiClient.init_from_config(config=config)
    return api_client, sensor


if __name__ == "__main__":
    weather_station_config = WeatherStationConfig.load("config/dev.yaml")
    asyncio.run(main(weather_station_config))
