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

    def __getattr__(self, item):
        return getattr(self.properties, item)
