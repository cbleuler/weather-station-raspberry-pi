import datetime
from typing import Optional

from pydantic import model_validator  # pylint: disable=import-error
from pydantic.dataclasses import dataclass  # pylint: disable=import-error


@dataclass
class SensorReading:
    timestamp: datetime.datetime
    weather_station_uuid: str
    air_temperature: Optional[float] = None
    dew_point: Optional[float] = None
    water_temperature: Optional[float] = None
    humidity: Optional[float] = None
    air_pressure: Optional[float] = None
    precipitation_amount: Optional[float] = None
    precipitation_type: Optional[str] = None
    wind_speed: Optional[float] = None
    gusts_of_wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    solar_radiation: Optional[float] = None
    air_quality: Optional[float] = None
    soil_moisture: Optional[float] = None

    @model_validator(mode="after")
    def check_at_least_one(self):
        if not any(
            [
                self.air_temperature,
                self.dew_point,
                self.water_temperature,
                self.air_quality,
                self.air_pressure,
                self.humidity,
                self.precipitation_amount,
                self.precipitation_type,
                self.wind_speed,
                self.gusts_of_wind_speed,
                self.wind_direction,
                self.solar_radiation,
                self.soil_moisture,
            ]
        ):
            raise ValueError("Failed to initialize SensorReading: at least one measurement must be non-null")
        return self

    def serialize(self):
        serialized_data = {
            "air_temperature": self.air_temperature,
            "dew_point": self.dew_point,
            "water_temperature": self.water_temperature,
            "humidity": self.humidity,
            "air_pressure": self.air_pressure,
            "precipitation_amount": self.precipitation_amount,
            "precipitation_type": self.precipitation_type,
            "wind_speed": self.wind_speed,
            "gusts_of_wind_speed": self.gusts_of_wind_speed,
            "wind_direction": self.wind_direction,
            "solar_radiation": self.solar_radiation,
            "air_quality": self.air_quality,
            "soil_moisture": self.soil_moisture,
            "time_stamp": self.timestamp.isoformat(),
            "weather_station_id": self.weather_station_uuid,
        }
        return serialized_data
