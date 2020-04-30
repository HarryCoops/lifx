from __future__ import annotations

from typing import List, Optional
from datetime import datetime
from uuid import UUID
from model import Light

import requests
from pydantic import BaseModel, Json

from exception import AuthorizationException


class Api:
    
    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("https://api.lifx.com/v1/lights/all", headers=self.headers)
        if response.status_code == 401:
            raise AuthorizationException(f"Authorization failed for token {token}")

    def list_all(self) -> List[Light]:
        response = requests.get(f"https://api.lifx.com/v1/lights/all", headers=self.headers)
        response.raise_for_status()
        light_jsons = response.json()
        return [Light(**light_json) for light_json in light_jsons]

    def list_group_by_label(self, label: str) -> List[Light]:
        response = requests.get(f"https://api.lifx.com/v1/lights/group:{label}", headers=self.headers)
        response.raise_for_status()
        light_jsons = response.json()
        return [Light(**light_json) for light_json in light_jsons]

    def list_location_by_label(self, label: str) -> List[Light]:
        response = requests.get(f"https://api.lifx.com/v1/lights/location:{label}", headers=self.headers)
        response.raise_for_status()
        light_jsons = response.json()
        return [Light(**light_json) for light_json in light_jsons]

    def get_light_by_label(self, label: str) -> Optional[Light]:
        response = requests.get(f"https://api.lifx.com/v1/lights/label:{label}", headers=self.headers)
        response.raise_for_status()
        light_json = response.json()
        if len(light_json) > 0:
            return Light(**light_json[0])
        else:
            return None


if __name__ == "__main__":
    token = "c82ebac79a2a02ff2693c31f2f3f2634d14e43426218aa1a56771331e23241c8"
    #light_id = "d073d52bcee3"
    api = Api(token)
    print(api.list_group_by_label("Bedroom"))
    print(api.list_location_by_label("Home"))
    print(api.get_light_by_label("Tess Ceiling"))
    #response = requests.get(f"https://api.lifx.com/v1/lights/id:{light_id}/", headers={"Authorization": creds})
    #tess_room = Light(**response.json()[0])