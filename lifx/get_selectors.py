from typing import List
from typing_extensions import runtime, Protocol

from lifx.selector import Selector
from lifx.session import Session


def get_selectors(session: Session) -> List[str]:
    """
    List all the available selectors for a given session. See \
    https://api.developer.lifx.com/v1/docs/selectors
    """
    selector = Selector("all", session)
    selectors = set()
    for light in selector.get_lights():
        selectors.add("id:" + light.id)
        selectors.add("label:" + light.label)
        selectors.add("group:" + light.group.name)
        selectors.add("group_id:" + light.group.id)
        selectors.add("location:" + light.location.name)
        selectors.add("location_id:" + light.location.id)
    return list(selectors)
