import datetime
import unittest.mock
from unittest.mock import MagicMock

import pytest

from api_client import ApiClient
from sensor_reading import SensorReading
from config import WeatherStationConfig, APIConfig, SensorConfig
from errors import AuthenticationError


@pytest.fixture
def api_config():
    api_config = APIConfig(host="http://127.0.0.1", port=8000, user="someuser", password="secret")
    sensor_config = SensorConfig(sda_pin=2, scl_pin=3, i2c_address=0x77, type="bme680")
    config = WeatherStationConfig(
        name="Weather Station",
        uuid="station-1",
        altitude=452.1,
        normal_sea_level_pressure=1013.25,
        api=api_config,
        sensor_config=sensor_config,
    )
    return config


@pytest.fixture
def api_client(api_config):
    api_client = ApiClient.init_from_config(api_config)
    return api_client


@pytest.fixture
def auth_header():
    return {"Authorization": "Bearer abc"}


@pytest.fixture
def sensor_reading():
    reading = SensorReading(
        temperature=20,
        pressure=1013.12,
        humidity=0.42,
        timestamp=datetime.datetime(2023, 1, 1),
        weather_station_uuid="station-1",
    )
    return reading


def test_init(api_client):
    assert api_client.base_url == "http://127.0.0.1:8000"
    assert api_client.authentication_path == "/api/token"
    assert api_client.request_path == "/api/v1/measurement"
    assert api_client.username == "someuser"
    assert api_client.password.get_secret_value() == "secret"

    assert api_client._auth_header == {}

    assert api_client.authentication_url == "http://127.0.0.1:8000/api/token"
    assert api_client.request_url == "http://127.0.0.1:8000/api/v1/measurement"


def test_init_from_config(api_config, api_client):
    api_client_from_config = ApiClient.init_from_config(api_config)
    assert api_client_from_config == api_client


@pytest.mark.parametrize(
    "auth_response,token",
    [
        (
            '{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
            ".eyJzdWIiOiJyb290Iiwic2NvcGVzIjpbIm1lYXN1cmVtZW50OndyaXRlIl0sImV4cCI6MTcwOTMzNjQ3N30"
            '.nZt6YP2WInjurtqDPKYFEJ4AEju59cZWEQypfsCfDSM","token_type":"bearer"}',
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiJyb290Iiwic2NvcGVzIjpbIm1lYXN1cmVtZW50OndyaXRlIl0sImV4cCI6MTcwOTMzNjQ3N30"
            ".nZt6YP2WInjurtqDPKYFEJ4AEju59cZWEQypfsCfDSM",
        ),
        (
            '{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
            ".eyJzdWIiOiJyb290Iiwic2NvcGVzIjpbIm1lYXN1cmVtZW50OndyaXRlIl0sImV4cCI6MTcwOTMzNjQ3N30"
            '.nZt6YP2WInjurtqDPKYFEJ4AEju59cZWEQypfsCfDSM","token_type":"bearer"}',
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiJyb290Iiwic2NvcGVzIjpbIm1lYXN1cmVtZW50OndyaXRlIl0sImV4cCI6MTcwOTMzNjQ3N30"
            ".nZt6YP2WInjurtqDPKYFEJ4AEju59cZWEQypfsCfDSM",
        ),
    ],
)
@unittest.mock.patch("requests.post")
def test_create_auth_header_valid_password(mock_auth_response, auth_response, token, api_client):
    mock_res = lambda: None
    mock_res.text = auth_response
    mock_res.status_code = 200
    mock_auth_response.return_value = mock_res

    actual_auth_header = api_client._create_auth_header()

    assert actual_auth_header == {"Authorization": f"Bearer {token}"}


@unittest.mock.patch("requests.post")
def test_create_auth_header_empty_password(mock_auth_response, api_client):
    mock_res = lambda: None
    mock_res.status_code = 422
    mock_auth_response.return_value = mock_res

    with pytest.raises(AuthenticationError) as e:
        api_client._create_auth_header()

    assert str(e.value) == "Non-empty password must be provided."


@unittest.mock.patch("requests.post")
def test_create_auth_header_wrong_password(mock_auth_response, api_client):
    mock_res = lambda: None
    mock_res.status_code = 401
    mock_auth_response.return_value = mock_res

    with pytest.raises(AuthenticationError) as e:
        api_client._create_auth_header()

    assert str(e.value) == "Username or password is incorrect."


@unittest.mock.patch("requests.post")
def test_create_auth_header_other_error(mock_auth_response, api_client):
    mock_res = lambda: None
    mock_res.status_code = 404
    mock_auth_response.return_value = mock_res

    with pytest.raises(AuthenticationError) as e:
        api_client._create_auth_header()

    assert str(e.value) == "Something went wrong during authentication."


def test_get_auth_header(api_client, auth_header):
    api_client._create_auth_header = MagicMock(return_value=auth_header)

    assert api_client.get_auth_header(refresh=False) == auth_header
    assert api_client.get_auth_header(refresh=False) == auth_header
    assert api_client.get_auth_header(refresh=True) == auth_header


@pytest.mark.parametrize(
    "status_code,return_value",
    [
        (200, True),  # Valid token successful request
        (404, False),  # Unsuccessful request
        (401, False),  # Invalid token
    ],
)
@unittest.mock.patch("requests.post")
def test_send_sync_reading(mock_auth_response, status_code, return_value, api_client, auth_header, sensor_reading):
    mock_res = lambda: None
    mock_res.status_code = status_code
    mock_res.reason = "Some reason."
    mock_auth_response.return_value = mock_res

    api_client.get_auth_header = MagicMock(return_value=auth_header)

    assert api_client.send_sync_reading(sensor_reading) == return_value
