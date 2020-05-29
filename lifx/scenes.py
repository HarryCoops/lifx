from typing import List, Optional
from uuid import UUID

from typing_extensions import runtime, Protocol
from lifx.model import Scene, State
from lifx.session import Session


def list_scenes(session: Session) -> List[Scene]:
    """
    List all the configured scenes
    
    :param session: session object used to perform API calls
    """
    scene_jsons = session.get("scenes")
    scenes = [Scene(**scene_json) for scene_json in scene_jsons]
    return scenes


def activate_scene_by_id(
    session: Session,
    scene_id: UUID,
    ignore: Optional[List[str]] = None,
    duration: Optional[float] = None,
    overrides: Optional[State] = None,
    fast: Optional[bool] = None,
) -> None:
    """
    Activate a scene by its id.

    :param session: session object used to perform API calls
    :param scene_id: UUID of a scene, can be accessed from a scene object \
    by scene.uuid
    :param ignore: Any of "power", "infrared", "duration", "intensity", \
    "hue", "saturation", "brightness" or "kelvin", specifying that these \
    properties should not be changed on devices when applying the scene.
    :param overrides: A state object as per Set State specifying properties \
    to apply to all devices in the scene, overriding those configured in the scene.
    :param fast: Execute the query fast, without initial state checks and wait \
    for no results.
    """
    body = {
        "ignore": ignore,
        "duration": duration,
        "overrides": overrides,
        "fast": fast,
    }
    body = {k: v for k, v in body.items() if v is not None}
    session.put(f"scenes/scene_id:{str(scene_id)}/activate", body=body)
