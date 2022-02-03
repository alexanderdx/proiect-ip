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


def test_hub_get(client):
    request = client.get('/hub')
    assert request.status_code == 200


def test_hub_post(client):
    payload = {'name': 'test-hub', 'user_number': 0}
    
    request = client.post('/hub', json=payload, follow_redirects=True)
    
    result = json.loads(request.data.decode())
    
    assert request.status_code == 200
    assert payload['name'] == result['name']
    assert payload['user_number'] == result['user_number']


def test_minihub_get(client):
    request = client.get('/hub')
    assert request.status_code == 200

def test_minihub_post(client):
    payload = {'description': 'Test description', 'headless': True, 'volume': 55, 'port': 5050}
    
    request = client.post('/minihub', json=payload, follow_redirects=True)
    
    result = json.loads(request.data.decode())
    
    assert request.status_code == 200
    assert payload['description'] == result['description']
    assert payload['port'] == result['port']
    assert payload['volume'] == result['volume']

def test_minihub_update_description(client):
    # Create a minihub
    payload = {'description': 'Test description', 'headless': True, 'volume': 60, 'port': 5051}
    request = client.post('/minihub', json=payload, follow_redirects=True)
    hub_id = json.loads(request.data.decode())['id']

    payload = {'action': 'change_description', 'description': 'New Description'}
    request = client.patch('/minihub/{}'.format(hub_id), json=payload, follow_redirects=True)
    
    result = json.loads(request.data.decode())

    assert request.status_code == 200
    assert payload['description'] == result['description']


def test_minihub_deletion(client):
    # Create a minihub
    payload = {'description': 'Test description', 'headless': True, 'volume': 60, 'port': 5053}
    request = client.post('/minihub', json=payload, follow_redirects=True)
    hub_id = json.loads(request.data.decode())['id']

    request = client.delete('/minihub/{}'.format(hub_id), follow_redirects=True)
    result = json.loads(request.data.decode())

    assert request.status_code == 200
    assert result['message'] == "MiniHub already deleted."


def test_user_get(client):
    request = client.get('/user')
    assert request.status_code == 200


def test_user_post(client):
    payload = {'name': 'Jon Doe', 'room': 0}

    request = client.post('/user', json=payload, follow_redirects=True)

    result = json.loads(request.data.decode())

    assert request.status_code == 200
    assert payload['name'] == result['name']
    assert payload['room'] == result['room']


def test_user_change_room(client):
    # Create a user
    payload = {'name': 'Alice Cooper', 'room': 1}
    request = client.post('/user', json=payload, follow_redirects=True)
    user_id = json.loads(request.data.decode())['id']

    payload = {'action': 'change_room', 'room': 12}
    request = client.patch('/user/{}'.format(user_id), json=payload, follow_redirects=True)

    result = json.loads(request.data.decode())

    assert request.status_code == 200
    assert result['message'] == 'No MiniHub exists in that room.'


def test_user_play(client):
    # Create a user
    payload = {'name': 'Karl Marx', 'playing': 'Soviet Anthem', 'room': 'Test room'}
    request = client.post('/user', json=payload, follow_redirects=True)
    user_id = json.loads(request.data.decode())['id']

    payload = {'action': 'play', 'query': 'Britney Spears'}
    request = client.patch('/user/{}'.format(user_id), json=payload, follow_redirects=True)

    result = json.loads(request.data.decode())

    assert request.status_code == 200
    assert result['message'] == "You're not connected to any MiniHub!"


def test_user_deletion(client):
    # Create a user
    payload = {'name': 'Stresu computers', 'playing': 'Test output', 'room': 'Test room'}
    request = client.post('/user', json=payload, follow_redirects=True)
    user_id = json.loads(request.data.decode())['id']

    payload = {'action': 'change_output', 'playing': 'New output'}
    request = client.delete('/user/{}'.format(user_id), json=payload, follow_redirects=True)

    assert request.status_code == 200