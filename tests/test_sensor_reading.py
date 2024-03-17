import datetime
import pytest

from sensor_reading import SensorReading


@pytest.fixture
def sensor_reading_without_air_quality():
    reading = SensorReading(
        air_temperature=20,
        air_pressure=1013.12,
        humidity=0.42,
        timestamp=datetime.datetime(2023, 1, 1),
        weather_station_uuid="station-1",
    )
    return reading


@pytest.fixture
def sensor_reading_with_air_quality():
    reading = SensorReading(
        air_temperature=20,
        air_pressure=1013.12,
        humidity=0.42,
        air_quality=0.55,
        timestamp=datetime.datetime(2023, 1, 1),
        weather_station_uuid="station-1",
    )
    return reading


def test_serialize_without_air_quality(sensor_reading_without_air_quality):
    assert sensor_reading_without_air_quality.serialize() == {
        "air_temperature": 20,
        "air_pressure": 1013.12,
        "humidity": 0.42,
        "air_quality": None,
        "time_stamp": "2023-01-01T00:00:00",
        "weather_station_id": "station-1",
    }


def test_serialize_with_air_quality(sensor_reading_with_air_quality):
    assert sensor_reading_with_air_quality.serialize() == {
        "air_temperature": 20,
        "air_pressure": 1013.12,
        "humidity": 0.42,
        "air_quality": 0.55,
        "time_stamp": "2023-01-01T00:00:00",
        "weather_station_id": "station-1",
    }
