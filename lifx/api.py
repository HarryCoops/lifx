from __future__ import annotations
import abc
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from lifx.model import LightProperties
from lifx.light import Light

import requests
from pydantic import BaseModel, Json


class Session(abc.ABC):

    def get(self, path: str) -> dict:
        ...

    def post(self, path: str, body: dict) -> dict:
        ...

    def put(self, path: str, body: dict) -> dict:
        ...


class Api:
    
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> List[Light]:
        light_jsons = self.session.get("lights/all")
        return [
            Light(
                LightProperties(**light_json), 
                self.session
            ) for light_json in light_jsons
        ]

    def list_group_by_label(self, label: str) -> List[Light]:
        light_jsons = self.session.get(f"lights/group:{label}")
        return [
            Light(
                LightProperties(**light_json), 
                self.session
            ) for light_json in light_jsons
        ]

    def list_location_by_label(self, label: str) -> List[Light]:
        light_jsons = self.session.get(f"lights/location:{label}")
        return [
            Light(
                LightProperties(**light_json), 
                self.session
            ) for light_json in light_jsons
        ]

    def get_light_by_label(self, label: str) -> Optional[Light]:
        light_json = self.session.get(f"lights/label:{label}")
        if len(light_json) > 0:
            return Light(
                LightProperties(**light_json[0]), 
                self.session
            )
        else:
            return None