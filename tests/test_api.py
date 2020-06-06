from lifx import model, session, selector, get_selectors, scenes
import responses
import pytest
import pathlib
import json
import uuid

test_data_path = pathlib.Path(__file__).parent.absolute() / "testdata"


@pytest.fixture
@responses.activate
def fx_test_session() -> session.Session:
    responses.add(responses.GET, "https://api.lifx.com/v1/lights", json={})
    test_session = session.Session("test-token")
    return test_session


@responses.activate
def test_get_all__empty(fx_test_session: session.Session):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    lights = selector.Selector("all", fx_test_session).get_lights()
    assert len(lights) == 0


@responses.activate
def test_get_all__length_one(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json=req_json)
    lights = selector.Selector("all", fx_test_session).get_lights()
    assert len(lights) == 1
    assert isinstance(lights[0], model.Light)
    assert lights[0].id == "test_id"


@responses.activate
def test_get_all__length_two(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "list_all_2.json") as f:
        req_json = json.loads(f.read())
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json=req_json)
    lights = selector.Selector("all", fx_test_session).get_lights()
    assert len(lights) == 2
    assert isinstance(lights[0], model.Light)
    assert isinstance(lights[1], model.Light)
    assert lights[0].id == "test_id_1"
    assert lights[1].id == "test_id_2"


@responses.activate
def test_get_group(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET, "https://api.lifx.com/v1/lights/group:test_label", json=req_json
    )
    lights = selector.Selector("group:test_label", fx_test_session).get_lights()
    assert len(lights) == 1
    assert isinstance(lights[0], model.Light)
    assert lights[0].id == "test_id"


@responses.activate
def test_get_location(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET,
        "https://api.lifx.com/v1/lights/location:test_label",
        json=req_json,
    )
    lights = selector.Selector("location:test_label", fx_test_session).get_lights()
    assert len(lights) == 1
    assert isinstance(lights[0], model.Light)
    assert lights[0].id == "test_id"


@responses.activate
def test_get_by_label(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET, "https://api.lifx.com/v1/lights/label:test_label", json=req_json
    )
    _light = selector.Selector("label:test_label", fx_test_session).get_lights()[0]
    assert isinstance(_light, model.Light)
    assert _light.id == "test_id"


"""
Below are tests for methods that modify the state of lights. Currently, the responses 
library doesn't have functionality for checking the bdoy of POST or PUT requests, so
these tests are not that useful / thorough, however there are open PRs to add this 
functionality so these tests will be updated when that happens.
"""


@pytest.fixture
@responses.activate
def fx_test_selector(fx_test_session: session.Session) -> selector.Selector:
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    return selector.Selector("all", fx_test_session)


@responses.activate
def test_set_state(fx_test_selector: selector.Selector):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    responses.add(responses.PUT, "https://api.lifx.com/v1/lights/all/state", json={})
    test_state = model.State(brightness=0.1)
    fx_test_selector.set_state(test_state)


@responses.activate
def test_state_delta(fx_test_selector: selector.Selector):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    responses.add(
        responses.POST, "https://api.lifx.com/v1/lights/all/state/delta", json={}
    )
    test_state = model.StateDelta(brightness=0.1)
    fx_test_selector.state_delta(test_state)


@responses.activate
def test_toggle_power(fx_test_selector: selector.Selector):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    responses.add(responses.POST, "https://api.lifx.com/v1/lights/all/toggle", json={})
    fx_test_selector.toggle_power()


@responses.activate
def test_breathe_effect(fx_test_selector: selector.Selector):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    responses.add(
        responses.POST, "https://api.lifx.com/v1/lights/all/effects/breathe", json={}
    )
    fx_test_selector.breathe_effect(period=0.1)


@responses.activate
def test_move(fx_test_selector: selector.Selector):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    responses.add(
        responses.POST, "https://api.lifx.com/v1/lights/all/effects/move", json={}
    )
    fx_test_selector.move(period=0.1)


@responses.activate
def test_flame_effect(fx_test_selector: selector.Selector):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    responses.add(
        responses.POST, "https://api.lifx.com/v1/lights/all/effects/flame", json={}
    )
    fx_test_selector.flame_effect(period=0.1)


@responses.activate
def test_pulse_effect(fx_test_selector: selector.Selector):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    responses.add(
        responses.POST, "https://api.lifx.com/v1/lights/all/effects/pulse", json={}
    )
    fx_test_selector.pulse_effect(period=0.1)


@responses.activate
def test_effects_off(fx_test_selector: selector.Selector):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    responses.add(
        responses.POST, "https://api.lifx.com/v1/lights/all/effects/off", json={}
    )
    fx_test_selector.effects_off()


@responses.activate
def test_cycle(fx_test_selector: selector.Selector):
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json={})
    responses.add(
        responses.POST, "https://api.lifx.com/v1/lights/all/effects/cycle", json={}
    )
    fx_test_selector.cycle()


@responses.activate
def test_get_selectors(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(responses.GET, "https://api.lifx.com/v1/lights/all", json=req_json)
    selectors = get_selectors(fx_test_session)
    correct_selectors = [
        "label:Test",
        "group:Test Room",
        "id:test_id",
        "location:Test Location",
        "group_id:3732ed2776c09c2831cc5501b69a0218",
        "location_id:7fd25780251cc4edf526707c259b5493",
    ]
    assert all([s in selectors for s in correct_selectors])
    assert all([s in correct_selectors for s in selectors])


@responses.activate
def test_list_scenes(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "scenes.json") as f:
        req_json = json.loads(f.read())
    responses.add(responses.GET, "https://api.lifx.com/v1/scenes", json=req_json)
    _scenes = scenes.list_scenes(fx_test_session)
    assert len(_scenes) == 1
    assert _scenes[0].name == "Test"


@responses.activate
def test_activate_scene_by_id(fx_test_session: session.Session):
    responses.add(
        responses.PUT,
        "https://api.lifx.com/v1/scenes/scene_id:3732ed27-76c0-9c28-31cc-5501b69a0218/activate",
        json={},
    )
    scenes.activate_scene_by_id(
        fx_test_session, uuid.UUID("3732ed2776c09c2831cc5501b69a0218")
    )
