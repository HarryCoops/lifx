from __future__ import annotations
import abc
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Json


class Color(BaseModel):
    """
    A Color as defined in the Lifx API, can be hue saturation brightness, or \
    just kelvin and brightness.
    """

    hue: Optional[int]
    saturation: Optional[float]
    kelvin: Optional[int]
    brightness: Optional[float]


class Group(BaseModel):
    """
    Model representing a group, which is a just a name and ID that groups lights together.
    """

    id: str
    name: str


class Location(BaseModel):
    """
    Model representing a location, which is a just a name and ID that groups lights together.
    """

    id: str
    name: str


class State(BaseModel):
    """
    Model representing the State of a light or many lights, depending on the selector \
    The selector attribute is there for compatibility with the return of list_scenes endpoint. \
    It does not need to be provided when changing states using the Selector class.
    """

    selector: Optional[str]
    brightness: Optional[float]
    color: Optional[Color]
    power: Optional[str]
    duration: Optional[float]
    infrared: Optional[float]


class Scene(BaseModel):
    """
    Model representing a Scene. A Scene is a list of states (with selectors) grouped \
    together under and ID and name.
    """

    uuid: UUID
    name: str
    states: List[State]


class StateDelta(BaseModel):
    """
    StateDelta defines a change in state. Each of its attributes are an offset \
    wich tells the lifx api how much to change each of the state attributes by \
    for a selection.
    """

    brightness: Optional[float]
    hue: Optional[float]
    saturation: Optional[float]
    power: Optional[str]
    duration: Optional[float]
    infrared: Optional[float]
    kelvin: Optional[float]


class Capabilities(BaseModel):
    """
    Model representing the capabilities of a single product.
    """

    has_color: bool
    has_variable_color_temp: bool
    has_ir: bool
    has_chain: bool = False
    has_matrix: bool = False
    has_multizone: bool = False
    min_kelvin: int
    max_kelvin: int


class Product(BaseModel):
    """
    Model representing a Lifx product.
    """

    name: str
    identifier: str
    company: str
    capabilities: Capabilities


class Light(BaseModel):
    """
    Model representing a single Lifx light. Contains all information that is \
    provided by the API including what the product is, its state, how long since \
    it was last online, and others.
    """

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
