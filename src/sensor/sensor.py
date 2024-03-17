from abc import ABC
from abc import abstractmethod

from sensor_reading import SensorReading


class Sensor(ABC):

    @abstractmethod
    def get_measurement(self, weather_station_uuid: str) -> SensorReading:
        raise NotImplementedError
