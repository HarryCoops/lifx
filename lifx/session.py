import requests

from lifx.exception import AuthorizationException

class Session:

    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
        self.base = "https://api.lifx.com/v1/"
        response = requests.get(self.base + "lights", headers=self.headers)
        if response.status_code == 401:
            raise AuthorizationException(f"Authorization failed for token {token}")

    def get(self, path: str) -> dict:
        response = requests.get(
            self.base + path,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def post(self, path: str, body: dict) -> dict:
        response = requests.post(
            self.base + path,
            json=body,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def put(self, path: str, body: dict) -> dict:
        response = requests.put(
            self.base + path,
            json=body,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

