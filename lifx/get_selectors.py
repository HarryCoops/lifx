from typing import List
from typing_extensions import runtime, Protocol

from lifx.selector import Selector

@runtime
class Session(Protocol):

    def get(self, path: str) -> dict:
        ...

    def post(self, path: str, body: dict) -> dict:
        ...

    def put(self, path: str, body: dict) -> dict:
        ...

def get_selectors(session: Session) -> List[str]:
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