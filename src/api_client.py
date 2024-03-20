import asyncio
import json
import logging

import requests
from pydantic import SecretStr  # pylint: disable=import-error
from pydantic.dataclasses import dataclass  # pylint: disable=import-error

from config import APIConfig
from errors import AuthenticationError
from sensor_reading import SensorReading


class TokenExpiredError(Exception):
    pass


@dataclass
class ApiClient:
    base_url: str
    authentication_path: str
    request_path: str
    username: str
    password: SecretStr

    def __post_init__(self):
        self._auth_header = {}

    @property
    def request_url(self):
        return self.base_url + self.request_path

    @property
    def authentication_url(self):
        return self.base_url + self.authentication_path

    def get_auth_header(self, refresh: bool = False):
        if not refresh and self._auth_header:
            return self._auth_header

        logging.info("Token was refreshed.")
        self._auth_header = self._create_auth_header()
        return self._auth_header

    def _create_auth_header(self):
        res = requests.post(
            self.authentication_url,
            data={
                "username": self.username,
                "password": self.password.get_secret_value(),
                "scope": "measurement:write",
            },
            timeout=10,
        )

        if res.status_code == 422:
            raise AuthenticationError("Non-empty password must be provided.")
        if res.status_code == 401:
            raise AuthenticationError("Username or password is incorrect.")
        if res.status_code != 200:
            raise AuthenticationError("Something went wrong during authentication.")

        data = json.loads(res.text)
        try:
            token = data["token"]
        except KeyError:
            token = data["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def send_sync_reading(self, reading: SensorReading) -> bool:
        res = requests.post(self.request_url, headers=self.get_auth_header(), json=reading.serialize(), timeout=10)
        if res.status_code == 200:
            return True
        if res.status_code == 401:
            res = requests.post(
                self.request_url, headers=self.get_auth_header(refresh=True), json=reading.serialize(), timeout=10
            )
        else:
            logging.warning(
                "Sending new reading failed with response code %s and message %s", res.status_code, res.reason
            )
            return False

        if res.status_code == 200:
            return True
        logging.warning("Sending new reading failed with response code %s and message %s", res.status_code, res.reason)
        return False

    async def send_reading(self, reading: SensorReading) -> bool:
        return await asyncio.to_thread(self.send_sync_reading, reading)

    @classmethod
    def init_from_config(cls, api_config: APIConfig):
        api_client = cls(
            base_url=f"{api_config.host}:{api_config.port}",
            authentication_path="/api/token",
            request_path="/api/v1/measurement/",
            username=api_config.user,
            password=SecretStr(api_config.password),
        )
        logging.debug("APIClient initialized: %s", api_client)
        return api_client
