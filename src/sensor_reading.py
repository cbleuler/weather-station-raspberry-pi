from dataclasses import dataclass
import datetime


@dataclass
class SensorReading:
    temperature: float
    pressure: float
    humidity: float
    timestamp: datetime.datetime
    weather_station_uuid: str

    def serialize(self):
        serialized_data = {
            "air_temperature": self.temperature,
            "air_pressure": self.pressure,
            "humidity": self.humidity,
            "time_stamp": self.timestamp.isoformat(),
            "weather_station_id": self.weather_station_uuid,
        }
        return serialized_data
