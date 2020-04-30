from __future__ import annotations

from typing import List
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Json


class Color(BaseModel):
    hue: int
    saturation: int
    kelvin: int


class Group(BaseModel):
    id: str
    name: str


class Location(BaseModel):
    id: str
    name: str


class Scene(BaseModel):
    id: str
    states: List[State]


class State(BaseModel):
    selector: str
    brightness: float
    color: Color


class Capabilities(BaseModel):
    has_color: bool
    has_variable_color_temp: bool
    has_ir: bool
    has_chain: bool
    has_matrix: bool
    has_multizone: bool
    min_kelvin: int
    max_kelvin: int


class Product(BaseModel):
  name: str
  identifier: str
  company: str
  capabilities: Capabilities


class Light(BaseModel):
    id: str
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