from typing import List, Optional
from uuid import UUID

from typing_extensions import runtime, Protocol
from lifx.model import Scene, State
from lifx.session import Session


def list_scenes(session: Session) -> List[Scene]:
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

    body = {
        "ignore": ignore,
        "duration": duration,
        "overrides": overrides,
        "fast": fast,
    }
    body = {k: v for k, v in body.items() if v is not None}
    session.put(f"scenes/scene_id:{str(scene_id)}/activate", body=body)
