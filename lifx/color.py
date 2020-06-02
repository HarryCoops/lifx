from typing_extensions import runtime, Protocol

from lifx import model
from lifx.session import Session


def get_color(session: Session, color: str) -> model.Color:
    """
    Generates a saturated Color object from a string
    
    :param session: authenticated session
    :param color: color string 
    """
    color_json = session.get(f"color?string={color}")
    return model.Color(**color_json)
