import datetime
import pytest

from sensor_reading import SensorReading


@pytest.fixture
def sensor_reading():
    reading = SensorReading(
        temperature=20,
        pressure=1013.12,
        humidity=0.42,
        timestamp=datetime.datetime(2023, 1, 1),
        weather_station_uuid="station-1",
    )
    return reading


def test_serialize(sensor_reading):
    assert sensor_reading.serialize() == {
        "air_temperature": 20,
        "air_pressure": 1013.12,
        "humidity": 0.42,
        "time_stamp": "2023-01-01T00:00:00",
        "weather_station_id": "station-1",
    }
