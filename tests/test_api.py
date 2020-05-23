from lifx import api, model, session, light
import responses
import pytest
import pathlib
import json

test_data_path = pathlib.Path(__file__).parent.absolute() / "testdata"

@pytest.fixture
@responses.activate
def fx_test_api() -> api.Api:
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights",
        status=200
    )
    test_session = session.Session("test-token")
    return api.Api(test_session)

@responses.activate
def test_get_all__empty(fx_test_api: api.Api):
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights/all",
        json={}
    )
    lights = fx_test_api.list_all()
    assert len(lights) == 0

@responses.activate
def test_get_all__length_one(fx_test_api: api.Api):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights/all",
        json=req_json
    )
    lights = fx_test_api.list_all()
    assert len(lights) == 1
    assert isinstance(lights[0], light.Light)
    assert lights[0].id == "test_id"

@responses.activate
def test_get_all__length_two(fx_test_api: api.Api):
    req_json = {}
    with open(test_data_path / "list_all_2.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights/all",
        json=req_json
    )
    lights = fx_test_api.list_all()
    assert len(lights) == 2
    assert isinstance(lights[0], light.Light)
    assert isinstance(lights[1], light.Light)
    assert lights[0].id == "test_id_1"
    assert lights[1].id == "test_id_2"


@responses.activate
def test_get_group(fx_test_api: api.Api):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights/group:test_label",
        json=req_json
    )
    lights = fx_test_api.list_group_by_label("test_label")
    assert len(lights) == 1
    assert isinstance(lights[0], light.Light)
    assert lights[0].id == "test_id"

@responses.activate
def test_get_location(fx_test_api: api.Api):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights/location:test-label",
        json=req_json
    )
    lights = fx_test_api.list_location_by_label("test-label")
    assert len(lights) == 1
    assert isinstance(lights[0], light.Light)
    assert lights[0].id == "test_id"

@responses.activate
def test_get_by_label(fx_test_api: api.Api):
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights/label:test-label",
        json=req_json
    )    
    _light = fx_test_api.get_light_by_label("test-label")
    assert isinstance(_light, light.Light)
    assert _light.id == "test_id"