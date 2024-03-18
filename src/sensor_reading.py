from typing import Optional
import datetime
from pydantic import model_validator  # pylint: disable=import-error
from pydantic.dataclasses import dataclass  # pylint: disable=import-error


@dataclass
class SensorReading:
    timestamp: datetime.datetime
    weather_station_uuid: str
    air_temperature: Optional[float] = None
    air_pressure: Optional[float] = None
    humidity: Optional[float] = None
    air_quality: Optional[float] = None

    @model_validator(mode="after")
    def check_at_least_one(self):
        if not any([self.air_temperature, self.air_quality, self.air_pressure, self.humidity]):
            raise ValueError(
                "At least one of 'air_temperature', 'air_quality', 'air_pressure', 'humidity' must be non-null"
            )
        return self

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
