import pytest
import json
from app import create_app

"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.

"""


@pytest.fixture
def client():
    app = create_app(testing=True)
    client = app.test_client()

    yield client


def test_root_endpoint(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert 'Hello World!' in html
    assert landing.status_code == 200


def test_hub_root_endpoint(client):
    request = client.get('/hub/')
    assert request.status_code == 200


def test_hub_post(client):
    payload = {'name': 'test-hub', 'user_number': 0}
    request = client.post('/hub/', data=payload, follow_redirects=True)
    assert request.status_code == 200
