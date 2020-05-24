from typing import Optional
import abc

from lifx import model


class Session(abc.ABC):

    def get(self, path: str) -> dict:
        ...

    def post(self, path: str, body: dict) -> dict:
        ...

    def put(self, path: str, body: dict) -> dict:
        ...


class Light:

    def __init__(self, properties: model.LightProperties, session: Session) -> None:
        self.session = session
        self.properties = properties

    def set_state(self, state: model.State) -> None:
        '''
        if state.color is not None:
            res = self.session.get(f"color?string={state.color}")
            if res.status_code != 200:
                raise ValueError(f"Invalid color string in state: {state.color}")
        '''
        self.session.put(f"lights/id:{self.properties.id}/state", state.dict(exclude_unset=True))

    def state_delta(self, state_delta: model.StateDelta) -> None:
        self.session.post(
            f"lights/id:{self.properties.id}/state/delta",
            state_delta.dict(exclude_unset=True)
        )

    def toggle_power(self) -> None:
        self.session.post(f"lights/id:{self.properties.id}/toggle", {})

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
        body = {k:v for k, v in body.items() if v is not None}
        self.session.post(f"lights/id:{self.properties.id}/effects/breathe", body)

    def move(
        self, 
        direction: Optional[str],
        period: Optional[float],
        cycles: Optiona[float],
        power_on: Optional[bool],
    ) -> None:
        body = {
            "direction": direction,
            "period": period,
            "cycles": cycles,
            "power_on": power_on,
        }
        body = {k:v for k, v in body.items() if v is not None}
        self.session.post(f"lights/id:{self.properties.id}/effects/move", body)

    def flame(
        self, 
        period: Optional[float],
        duration: Optiona[float],
        power_on: Optional[bool],
    ) -> None:
        body = {
            "duration": duration,
            "period": period,
            "power_on": power_on,
        }
        body = {k:v for k, v in body.items() if v is not None}
        self.session.post(f"lights/id:{self.properties.id}/effects/flame", body)

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
        body = {k:v for k, v in body.items() if v is not None}
        self.session.post(f"lights/id:{self.properties.id}/effects/pulse", body)

    def effects_off(self, power_off: Optional[bool] = None) -> None:
        self.session.post(
            f"lights'/id:{self.properties.id}/effects/off", {power_off: power_off}
        )

    def cycle(
        self, 
        states: Optional[List[State]] = None, 
        default: Optional[State] = None,
        direction: Optional[str] = None,
    ) -> None:
        if states is not None:
            states = [state.dict(exclude_unset=True) for state in states]
        if default is not None:
            default = default.dict(exclude_unset=True)
        body = {
            "states": states,
            "default": default,
            "direction": direction
        }
        body = {k:v for k, v in body.items() if v is not None}
        self.session.post(
            f"lights/id:{self.properties.id}/effects/cycle",
            body
        )





    def __getattr__(self, item):
        return getattr(self.properties, item)
