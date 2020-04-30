from __future__ import annotations

from typing import List
from datetime import datetime
from uuid import UUID
from model import Light

import requests
from pydantic import BaseModel, Json


class Api():
    pass


if __name__ == "__main__":
    creds = "Bearer c82ebac79a2a02ff2693c31f2f3f2634d14e43426218aa1a56771331e23241c8"
    light_id = "d073d52bcee3"
    response = requests.get(f"https://api.lifx.com/v1/lights/id:{light_id}/", headers={"Authorization": creds})
    tess_room = Light(**response.json()[0])
    print(tess_room)



