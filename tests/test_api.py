from lifx import model, session, selector
import responses
import pytest
import pathlib
import json

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
    responses.add(responses.GET,
                  "https://api.lifx.com/v1/lights/all",
                  json=req_json)
    lights = selector.Selector("all", fx_test_session).get_lights()
    assert len(lights) == 1
    assert isinstance(lights[0], model.Light)
    assert lights[0].id == "test_id"


@responses.activate
def test_get_all__length_two(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "list_all_2.json") as f:
        req_json = json.loads(f.read())
    responses.add(responses.GET,
                  "https://api.lifx.com/v1/lights/all",
                  json=req_json)
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
    responses.add(responses.GET,
                  "https://api.lifx.com/v1/lights/group:test_label",
                  json=req_json)
    lights = selector.Selector("group:test_label",
                               fx_test_session).get_lights()
    assert len(lights) == 1
    assert isinstance(lights[0], model.Light)
    assert lights[0].id == "test_id"


@responses.activate
def test_get_location(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(responses.GET,
                  "https://api.lifx.com/v1/lights/location:test_label",
                  json=req_json)
    lights = selector.Selector("location:test_label",
                               fx_test_session).get_lights()
    assert len(lights) == 1
    assert isinstance(lights[0], model.Light)
    assert lights[0].id == "test_id"


@responses.activate
def test_get_by_label(fx_test_session: session.Session):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(responses.GET,
                  "https://api.lifx.com/v1/lights/label:test_label",
                  json=req_json)
    _light = selector.Selector("label:test_label",
                               fx_test_session).get_lights()[0]
    assert isinstance(_light, model.Light)
    assert _light.id == "test_id"
