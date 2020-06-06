from typing import Optional, List
from typing_extensions import runtime, Protocol

from lifx import model
from lifx.session import Session


class Selector:
    """
    Class representing a single light or a group of lights that 
    share a selector e.g. group, location etc. This class provides
    methods to alter the state of the whole group of lights.

    :param selector: string used to select lights e.g. group:bedroom \
    or id:28sha2jn2 (possibe selectors can be listed using lifx.get_selectors)
    :param session: session object used to perform API calls

    """

    def __init__(self, selector: str, session: Session) -> None:
        self.session = session
        self.selector = selector
        self._update_lights()

    def set_state(self, state: model.State) -> None:
        """
        Set the state of the selected lights 

        :param state: state to be applied to the selected lights
        """
        self.session.put(
            f"lights/{self.selector}/state", state.dict(exclude_unset=True)
        )
        self._update_lights()

    def state_delta(self, state_delta: model.StateDelta) -> None:
        """
        Change the state of the selected lights relative to their current states
        Example selector.state_delta(StateDelta(brightness=-0.5)) reduces the brightness
        of selected lights by 0.5

        :param state_delta: Change in state to be applied to selected lights
        """
        self.session.post(
            f"lights/{self.selector}/state/delta", state_delta.dict(exclude_unset=True)
        )
        self._update_lights()

    def toggle_power(self) -> None:
        """
        Toggle the power of the selected lights
        """
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
        """
        Apply the breathe effect to the selected lights
        See https://api.developer.lifx.com/docs/breathe-effect

        :param color: The color to use for the breathe effect
        :param from_color: The color to start the effect from. \
        If this parameter is omitted then the color the bulb is currently \
        set to is used instead.
        :param period: The time in seconds for one cycle of the effect.
        :param cycle: The number of times to repeat the effect.
        :param persist: If false set the light back to its previous value \
        when effect ends, if true leave the last effect color.
        :param power_off: If true, turn the bulb on if it is not already on.
        :param peak: Defines where in a period the target color is at its maximum. \
        Minimum 0.0, maximum 1.0.
        """
        body = {
            "color": color,
            "from_color": from_color,
            "period": period,
            "cycles": cycles,
            "persist": persist,
            "power_on": power_on,
            "peak": peak,
        }

        body = {k: v for k, v in body.items() if v is not None}
        self.session.post(f"lights/{self.selector}/effects/breathe", body)
        self._update_lights()

    def move(
        self,
        direction: Optional[str] = None,
        period: Optional[float] = None,
        cycles: Optional[float] = None,
        power_on: Optional[bool] = None,
    ) -> None:
        """
        Apply the move effect to the selected lights
        See https://api.developer.lifx.com/docs/move-effect

        :param direction: Move direction, can be 'forward' or 'backward'
        :param period: The time in seconds for one cycle of the effect.
        :param cycle: The number of times to repeat the effect.
        :param power_off: If true, turn the bulb on if it is not already on.
        """
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
        """
        Apply the flame effect to the selected lights
        See https://api.developer.lifx.com/docs/flame-effect

        :param duration: How long the animation lasts for in seconds. \
        Not specifying a duration makes the animation never stop. \
        Specifying 0 makes the animation stop. Note that there is a known bug \
        where the tile remains in the animation once it has completed if \
        duration is nonzero.
        :param period: This controls how quickly the flame runs. It is measured \
        in seconds. A lower number means the animation is faster
        :param power_off: If true, turn the bulb on if it is not already on.
        """
        body = {"duration": duration, "period": period, "power_on": power_on}
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
        """
        Apply the pulse effect to the selected lights
        See https://api.developer.lifx.com/docs/pulse-effect

        :param color: The color to use for the pulse effect
        :param from_color: The color to start the effect from. \
        If this parameter is omitted then the color the bulb is currently \
        set to is used instead.
        :param period: The time in seconds for one cycle of the effect.
        :param cycle: The number of times to repeat the effect.
        :param persist: If false set the light back to its previous value \
        when effect ends, if true leave the last effect color.
        :param power_off: If true, turn the bulb on if it is not already on.
        """
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
        """
        Turns off any running effects on the device. This includes any waveform (breathe or pulse) as well as Tile or Multizone firmware effects.

        Also, if you specify power_off as true then the lights will also be powered off.
        """
        self.session.post(f"lights/{self.selector}/effects/off", {power_off: power_off})
        self._update_lights()

    def cycle(
        self,
        states: Optional[List[model.State]] = None,
        default: Optional[model.State] = None,
        direction: Optional[str] = None,
    ) -> None:
        """
        Cycle selected lights through states 
        See https://api.developer.lifx.com/docs/cycle

        :param states: list of States to be cycled through.
        :param default: Default values to use when not specified in each State object.
        :param direction: Direction in which to cycle through the list. Can be forward or backward
        """
        states_dicts = None
        default_dict = None
        if states is not None:
            states_dicts = [state.dict(exclude_unset=True) for state in states]
        if default is not None:
            default_dict = default.dict(exclude_unset=True)
        body = {"states": states_dicts, "default": default_dict, "direction": direction}
        body = {k: v for k, v in body.items() if v is not None}
        self.session.post(f"lights/{self.selector}/effects/cycle", body)
        self._update_lights()

    def _update_lights(self) -> None:
        res = self.session.get(f"lights/{self.selector}")
        self.lights = [model.Light(**light_json) for light_json in res]

    def get_lights(self) -> List[model.Light]:
        """
        Get the list of Lights selected
        """
        return self.lights
