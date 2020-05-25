from __future__ import annotations
import abc
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Json


class Color(BaseModel):
    hue:  Optional[int]
    saturation: Optional[float]
    kelvin: Optional[int]
    brightness: Optional[float]


class Group(BaseModel):
    id: str
    name: str


class Location(BaseModel):
    id: str
    name: str


class State(BaseModel):
    selector: Optional[str]
    brightness: Optional[float]
    color: Optional[Color]
    power: Optional[str]
    duration: Optional[float]
    infrared: Optional[float]


class Scene(BaseModel):
    uuid: UUID
    name: str
    states: List[State]


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
