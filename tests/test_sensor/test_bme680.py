import unittest.mock
from unittest.mock import MagicMock
import pytest

from config import SensorConfig
from sensor.bme.bme680 import Bme680Sensor


@pytest.fixture
def mock_i2c():
    i2c_mocked = MagicMock(return_value=None)
    return i2c_mocked


@pytest.fixture
def mock_bme680():
    bme680_mock = lambda: None
    bme680_mock.sea_level_pressure = None
    bme680_mock.pressure = 898.9934
    bme680_mock.temperature = 21.5
    bme680_mock.relative_humidity = 0.42
    bme680_mock.gas = 0.55
    return bme680_mock


@pytest.fixture
def gpio_config():
    return SensorConfig(sda_pin=2, scl_pin=3, i2c_address=0x77)


@pytest.fixture
@unittest.mock.patch("sensor.bme.bme280.I2C")
@unittest.mock.patch("sensor.bme.bme680.Adafruit_BME680_I2C")
def sensor(bme680_mock, i2c_mock, mock_bme680, mock_i2c, gpio_config):
    bme680_mock.return_value = mock_bme680
    i2c_mock.return_value = mock_i2c

    sea_level_pressure = 1013.25
    altitude = 1000
    bme680_sensor = Bme680Sensor(sensor_config=gpio_config, altitude=altitude, std_sea_level_pressure=sea_level_pressure)
    return bme680_sensor


def test_init(sensor):
    sea_level_pressure = 1013.25
    altitude = 1000

    assert sensor.sensor.sea_level_pressure == sea_level_pressure
    assert sensor.altitude == altitude


def test_get_normalized_pressure(sensor):
    assert sensor.get_normalized_pressure() == 1013.6122280906383


def test_get_temperature(sensor):
    assert sensor.get_temperature() == 21.5


def test_get_relative_humidity(sensor):
    assert sensor.get_relative_humidity() == 0.42


def test_get_measurement(sensor):
    weather_station_uuid = "station-1"
    measurement = sensor.get_measurement(weather_station_uuid)

    assert measurement.weather_station_uuid == weather_station_uuid
    assert measurement.temperature == 21.5
    assert measurement.humidity == 0.42
    assert measurement.pressure == 1013.6122280906383
    assert measurement.air_quality == 0.55
