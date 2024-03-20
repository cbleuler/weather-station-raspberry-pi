import pytest
from pathlib import Path

from runner import Runner

from config import WeatherStationConfig, SensorConfig
from api_client import ApiClient
from errors import InvalidSensorTypeError


@pytest.fixture
def weather_station_config_file():
    return Path("tests/testbed/test_config.yaml")


@pytest.fixture
def weather_station_config(weather_station_config_file):
    return WeatherStationConfig.load(weather_station_config_file)


@pytest.fixture
def runner(weather_station_config):
    return Runner(weather_station_config=weather_station_config)


def test_init(runner, weather_station_config):
    assert runner.weather_station_uuid == "station-1"
    assert runner.api_client == ApiClient.init_from_config(weather_station_config.api)


def test_init_from_config_file(weather_station_config_file):
    assert isinstance(Runner.init_from_config_file(weather_station_config_file), Runner)


def test_setup_sensor(runner):
    sensor_config = SensorConfig(type="inexisting")

    with pytest.raises(InvalidSensorTypeError) as e:
        runner._setup_sensor(sensor_config=sensor_config, altitude=0, std_sea_level_pressure=1013.25)

    assert str(e.value) == "Sensor type 'inexisting' is invalid. Must be in bme280, bme680, constant"
