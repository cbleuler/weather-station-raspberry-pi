import pytest
from sensor import Sensor


def test_init():
    with pytest.raises(TypeError) as e:
        Sensor()
        assert e.value == "Can't instantiate abstract class Sensor with abstract methods get_measurement, read_value"
