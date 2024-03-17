import datetime
from sensor.sensor_constant import ConstantSensor
from sensor_reading import SensorReading


def test_get_measurement():
    sensor = ConstantSensor()
    expected_sensor_reading = SensorReading(
        air_temperature=21.5,
        air_pressure=1013.25,
        air_quality=0.55,
        humidity=0.5,
        timestamp=datetime.datetime(year=2023, month=4, day=20, hour=8, minute=15),
        weather_station_uuid="station-1",
    )

    assert sensor.get_measurement(weather_station_uuid="station-1") == expected_sensor_reading
