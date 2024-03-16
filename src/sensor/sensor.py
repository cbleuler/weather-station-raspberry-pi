from abc import ABC
from abc import abstractmethod


class Sensor(ABC):

    @abstractmethod
    def read_value(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_measurement(self, weather_station_uuid: str):
        raise NotImplementedError
