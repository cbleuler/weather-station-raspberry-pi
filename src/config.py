from confme import BaseConfig  # pylint: disable=import-error
from confme.annotation import Secret  # pylint: disable=import-error


class APIConfig(BaseConfig):
    host: str
    port: int
    user: str
    password: str = Secret("API_PASSWORD")


class SensorConfig(BaseConfig):
    i2c_address: int = 0x77
    type: str = "constant"


class WeatherStationConfig(BaseConfig):
    name: str
    uuid: str
    altitude: float
    std_sea_level_pressure: float = 1013.25
    api: APIConfig
    sensor_config: SensorConfig
