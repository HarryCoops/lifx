from typing import Optional, List
from typing_extensions import runtime, Protocol

from lifx import model
from lifx.session import Session


class Selector:
    def __init__(self, selector: str, session: Session) -> None:
        self.session = session
        self.selector = selector
        self._update_lights()

    def set_state(self, state: model.State) -> None:
        self.session.put(f"lights/{self.selector}/state",
                         state.dict(exclude_unset=True))
        self._update_lights()

    def state_delta(self, state_delta: model.StateDelta) -> None:
        self.session.post(f"lights/{self.selector}/state/delta",
                          state_delta.dict(exclude_unset=True))
        self._update_lights()

    def toggle_power(self) -> None:
        self.session.post(f"lights/{self.selector}/toggle", {})
        self._update_lights()

    def breathe_effect(
        self,
        color: Optional[str] = None,
        from_color: Optional[str] = None,
        period: Optional[float] = None,
        cycles: Optional[float] = None,
        persist: Optional[bool] = None,
        power_on: Optional[bool] = None,
        peak: Optional[float] = None,
    ) -> None:
        body = {
            "color": color,
            "from_color": from_color,
            "period": period,
            "cycles": cycles,
            "persist": persist,
            "power_on": power_on,
            "peak": peak
        }
        body = {k: v for k, v in body.items() if v is not None}
        self.session.post(f"lights/{self.selector}/effects/breathe", body)
        self._update_lights()

    def move(
        self,
        direction: Optional[str],
        period: Optional[float],
        cycles: Optional[float],
        power_on: Optional[bool],
    ) -> None:
        body = {
            "direction": direction,
            "period": period,
            "cycles": cycles,
            "power_on": power_on,
        }
        body = {k: v for k, v in body.items() if v is not None}
        self.session.post(f"lights/{self.selector}/effects/move", body)
        self._update_lights()

    def flame_effect(
        self,
        period: Optional[float] = None,
        duration: Optional[float] = None,
        power_on: Optional[bool] = None,
    ) -> None:
        body = {
            "duration": duration,
            "period": period,
            "power_on": power_on,
        }
        body = {k: v for k, v in body.items() if v is not None}
        self.session.post(f"lights/{self.selector}/effects/flame", body)
        self._update_lights()

    def pulse_effect(
        self,
        color: Optional[str] = None,
        from_color: Optional[str] = None,
        period: Optional[float] = None,
        cycles: Optional[float] = None,
        persist: Optional[bool] = None,
        power_on: Optional[bool] = None,
    ) -> None:
        body = {
            "color": color,
            "from_color": from_color,
            "period": period,
            "cycles": cycles,
            "persist": persist,
            "power_on": power_on,
        }
        body = {k: v for k, v in body.items() if v is not None}
        self.session.post(f"lights/{self.selector}/effects/pulse", body)
        self._update_lights()

    def effects_off(self, power_off: Optional[bool] = None) -> None:
        self.session.post(f"lights'/{self.selector}/effects/off",
                          {power_off: power_off})
        self._update_lights()

    def cycle(
        self,
        states: Optional[List[model.State]] = None,
        default: Optional[model.State] = None,
        direction: Optional[str] = None,
    ) -> None:
        states_dicts = None
        default_dict = None
        if states is not None:
            states_dicts = [state.dict(exclude_unset=True) for state in states]
        if default is not None:
            default_dict = default.dict(exclude_unset=True)
        body = {
            "states": states_dicts,
            "default": default_dict,
            "direction": direction
        }
        body = {k: v for k, v in body.items() if v is not None}
        self.session.post(f"lights/{self.selector}/effects/cycle", body)
        self._update_lights()

    def _update_lights(self) -> None:
        res = self.session.get(f"lights/{self.selector}")
        self.lights = [model.Light(**light_json) for light_json in res]

    def get_lights(self) -> List[model.Light]:
        return self.lights
