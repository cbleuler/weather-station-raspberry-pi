from typing import Optional
from dataclasses import dataclass
import datetime


@dataclass
class SensorReading:
    air_temperature: float
    air_pressure: float
    humidity: float
    timestamp: datetime.datetime
    weather_station_uuid: str
    air_quality: Optional[float] = None

    def serialize(self):
        serialized_data = {
            "air_temperature": self.air_temperature,
            "air_pressure": self.air_pressure,
            "humidity": self.humidity,
            "air_quality": self.air_quality,
            "time_stamp": self.timestamp.isoformat(),
            "weather_station_id": self.weather_station_uuid,
        }
        return serialized_data
