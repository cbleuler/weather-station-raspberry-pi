from confme import BaseConfig
from confme.annotation import Secret


class APIConfig(BaseConfig):
    host: str
    port: int
    user: str
    password: str = Secret("API_PASSWORD")


class GPIOConfig(BaseConfig):
    sda_pin: int = 2
    scl_pin: int = 3
    i2c_address: int = 0x77


class WeatherStationConfig(BaseConfig):
    name: str
    uuid: str
    altitude: float
    normal_sea_level_pressure: float = 1013.25
    api: APIConfig
    gpio_config: GPIOConfig
