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


def test_sensor_reading_without_values():
    with pytest.raises(ValueError):
        SensorReading(weather_station_uuid="station-1", timestamp=datetime.datetime(2023, 1, 1))


@pytest.mark.parametrize(
    "air_temperature,dew_point,water_temperature,humidity,air_pressure,precipitation_amount,precipitation_type,wind_speed,gusts_of_wind_speed,wind_direction,solar_radiation,air_quality,soil_moisture",
    [
        (21.5, 2.5, 14.23, 0.34, 1013.25, 0.1, "rain", 10.5, 12.34, 180, 350.12, 0.11, 0.77),
        (21.5, None, None, None, None, None, None, None, None, None, None, None, None),
        (None, 2.5, None, None, None, None, None, None, None, None, None, None, None),
        (None, None, 14.23, None, None, None, None, None, None, None, None, None, None),
        (None, None, None, 0.34, None, None, None, None, None, None, None, None, None),
        (None, None, None, None, 1013.25, None, None, None, None, None, None, None, None),
        (None, None, None, None, None, 0.1, None, None, None, None, None, None, None),
        (None, None, None, None, None, None, "rain", None, None, None, None, None, None),
        (None, None, None, None, None, None, None, 10.5, None, None, None, None, None),
        (None, None, None, None, None, None, None, None, 12.34, None, None, None, None),
        (None, None, None, None, None, None, None, None, None, 180, None, None, None),
        (None, None, None, None, None, None, None, None, None, None, 350.12, None, None),
        (None, None, None, None, None, None, None, None, None, None, None, 0.11, None),
        (None, None, None, None, None, None, None, None, None, None, None, None, 0.77),
    ],
)
def test_serialize_valid_values(
    air_temperature,
    dew_point,
    water_temperature,
    humidity,
    air_pressure,
    precipitation_amount,
    precipitation_type,
    wind_speed,
    gusts_of_wind_speed,
    wind_direction,
    solar_radiation,
    air_quality,
    soil_moisture,
):
    sensor_reading = SensorReading(
        timestamp=datetime.datetime(year=2021, month=1, day=13, hour=12, minute=23, second=12),
        weather_station_uuid="station-1",
        air_temperature=air_temperature,
        dew_point=dew_point,
        water_temperature=water_temperature,
        humidity=humidity,
        air_pressure=air_pressure,
        precipitation_amount=precipitation_amount,
        precipitation_type=precipitation_type,
        wind_speed=wind_speed,
        gusts_of_wind_speed=gusts_of_wind_speed,
        wind_direction=wind_direction,
        solar_radiation=solar_radiation,
        air_quality=air_quality,
        soil_moisture=soil_moisture,
    )
    assert sensor_reading.serialize() == {
        "air_temperature": float(air_temperature) if air_temperature else None,
        "dew_point": float(dew_point) if dew_point else None,
        "water_temperature": float(water_temperature) if water_temperature else None,
        "humidity": float(humidity) if humidity else None,
        "air_pressure": float(air_pressure) if air_pressure else None,
        "precipitation_amount": float(precipitation_amount) if precipitation_amount else None,
        "precipitation_type": precipitation_type,
        "wind_speed": float(wind_speed) if wind_speed else None,
        "gusts_of_wind_speed": float(gusts_of_wind_speed) if gusts_of_wind_speed else None,
        "wind_direction": float(wind_direction) if wind_direction else None,
        "solar_radiation": float(solar_radiation) if solar_radiation else None,
        "air_quality": float(air_quality) if air_quality else None,
        "soil_moisture": float(soil_moisture) if soil_moisture else None,
        "time_stamp": "2021-01-13T12:23:12",
        "weather_station_id": "station-1",
    }
