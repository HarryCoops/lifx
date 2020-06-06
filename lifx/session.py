import requests

from lifx.exception import AuthorizationException


class Session:
    """
    Layer of abstraction between API Classes and the requests library.
    Handles the actual API calls and authentication.

    :param token: Lifx api authorization token 
    """

    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
        self.base = "https://api.lifx.com/v1/"
        response = requests.get(self.base + "lights", headers=self.headers)
        if response.status_code == 401:
            raise AuthorizationException(token)

    def get(self, path: str) -> dict:
        """
        Perform a GET reqeust to https://api.lifx.com/v1/{path}

        :param path: string containing path and any query string

        :return: serialized JSON dictionary of reponse from API
        """
        response = requests.get(self.base + path, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, body: dict) -> dict:
        """
        Perform a POST reqeust to https://api.lifx.com/v1/{path}


        :param path: string containing path and any query string
        :param body: JSON serializable dict to send in request body

        :return: serialized JSON dictionary of reponse from API 
        """
        response = requests.post(self.base + path, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def put(self, path: str, body: dict) -> dict:
        """
        Perform a PUT reqeust to https://api.lifx.com/v1/{path}


        :param path: string containing path and any query string
        :param body: JSON serializable dict to send in request body

        :return: serialized JSON dictionary of reponse from API
        """
        response = requests.put(self.base + path, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()
