import datetime

from sensor.sensor import Sensor
from sensor_reading import SensorReading


class ConstantSensor(Sensor):
    def __init__(self, *args, **kwargs):
        pass

    def get_measurement(self, weather_station_uuid: str) -> SensorReading:
        return SensorReading(
            air_temperature=21.5,
            air_pressure=1013.25,
            air_quality=0.55,
            humidity=0.5,
            timestamp=datetime.datetime(year=2023, month=4, day=20, hour=8, minute=15),
            weather_station_uuid=weather_station_uuid,
        )
