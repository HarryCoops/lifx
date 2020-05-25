from __future__ import annotations
import abc
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Json


class Color(BaseModel):
    hue: int
    saturation: int
    kelvin: int
    brightness: Optional[float]

    def __str__(self) -> str:
        ret = ""
        if self.hue:
            ret += f"hue:{self.hue}"
        if self.saturation:
            ret += f"saturation:{self.saturation}"
        if self.kelvin:
            ret += f"kelvin:{self.kelvin}"
        if self.brightness:
            ret += f"brightness:{self.brightness}"
        return ret


class Group(BaseModel):
    id: str
    name: str


class Location(BaseModel):
    id: str
    name: str


class Scene(BaseModel):
    uuid: UUID
    id: str
    states: List[State]


class State(BaseModel):
    selector: Optional[str]
    brightness: Optional[float]
    color: Optional[str]
    power: Optional[str]
    duration: Optional[float]
    infrared: Optional[float]


class StateDelta(BaseModel):
    brightness: Optional[float]
    hue: Optional[float]
    saturation: Optional[float]
    power: Optional[str]
    duration: Optional[float]
    infrared: Optional[float]
    kelvin: Optional[float]


class Capabilities(BaseModel):
    has_color: bool
    has_variable_color_temp: bool
    has_ir: bool
    has_chain: bool = False
    has_matrix: bool = False
    has_multizone: bool = False
    min_kelvin: int
    max_kelvin: int


class Product(BaseModel):
    name: str
    identifier: str
    company: str
    capabilities: Capabilities


class Light(BaseModel):
    id: str
    uuid: UUID
    label: str
    connected: bool
    power: str
    color: Color
    brightness: float
    effect: str
    group: Group
    location: Location
    product: Product
    last_seen: datetime
    seconds_since_seen: int
