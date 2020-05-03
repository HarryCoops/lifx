from lifx import api, model
import responses
import pytest
import pathlib
import json

test_data_path = pathlib.Path(__file__).parent.absolute() / "testdata"

@responses.activate
def test_get_all__empty():
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights/all",
        json={}
    )
    test_api = api.Api("test-token")
    lights = test_api.list_all()
    assert len(lights) == 0

@responses.activate
def test_get_all__length_one():
    req_json = {}
    with open(test_data_path / "list_all_1.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights/all",
        json=req_json
    )
    test_api = api.Api("test-token")
    lights = test_api.list_all()
    assert len(lights) == 1
    assert isinstance(lights[0], model.Light)
    assert lights[0].id == "test_id"

@responses.activate
def test_get_all__length_two():
    req_json = {}
    with open(test_data_path / "list_all_2.json") as f:
        req_json = json.loads(f.read())
    responses.add(
        responses.GET, 
        "https://api.lifx.com/v1/lights/all",
        json=req_json
    )
    test_api = api.Api("test-token")
    lights = test_api.list_all()
    assert len(lights) == 2
    assert isinstance(lights[0], model.Light)
    assert isinstance(lights[1], model.Light)
    assert lights[0].id == "test_id_1"
    assert lights[1].id == "test_id_2"