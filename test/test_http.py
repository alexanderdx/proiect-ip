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
    payload = {'description': 'Test description', 'connected_user_id': 0, 'volume': 55}
    
    request = client.post('/minihub', json=payload, follow_redirects=True)
    
    result = json.loads(request.data.decode())
    
    assert request.status_code == 200
    assert payload['description'] == result['description']
    assert payload['connected_user_id'] == result['connected_user_id']
    assert payload['volume'] == result['volume']

def test_minihub_update_description(client):
    # Create a minihub
    payload = {'description': 'Test description', 'connected_user_id': 0, 'volume': 55}
    request = client.post('/minihub', json=payload, follow_redirects=True)
    hub_id = json.loads(request.data.decode())['id']

    payload = {'action': 'change_description', 'description': 'New Description'}
    request = client.patch('/minihub/{}'.format(hub_id), json=payload, follow_redirects=True)
    
    result = json.loads(request.data.decode())

    assert request.status_code == 200
    assert payload['description'] == result['description']

def test_minihub_update_volume(client):
    # Create a minihub
    payload = {'description': 'Test description', 'connected_user_id': 0, 'volume': 55}
    request = client.post('/minihub', json=payload, follow_redirects=True)
    hub_id = json.loads(request.data.decode())['id']

    payload = {'action': 'change_volume', 'volume': 100}
    request = client.patch('/minihub/{}'.format(hub_id), json=payload, follow_redirects=True)
    
    result = json.loads(request.data.decode())
    
    assert request.status_code == 200
    assert payload['volume'] == result['volume']

def test_minihub_deletion(client):
    # Create a minihub
    payload = {'description': 'Test description', 'connected_user_id': 0, 'volume': 55}
    request = client.post('/minihub', json=payload, follow_redirects=True)
    hub_id = json.loads(request.data.decode())['id']

    payload = {'action': 'change_volume', 'volume': 100}
    request = client.delete('/minihub/{}'.format(hub_id), json=payload, follow_redirects=True)
    
    assert request.status_code == 200


def test_user_get(client):
    request = client.get('/user')
    assert request.status_code == 200


def test_user_post(client):
    payload = {'name': 'Jon Doe', 'output': 'Test output', 'room': 'Test room'}

    request = client.post('/user', json=payload, follow_redirects=True)

    result = json.loads(request.data.decode())

    assert request.status_code == 200
    assert payload['name'] == result['name']
    assert payload['output'] == result['output']
    assert payload['room'] == result['room']


def test_user_update_room(client):
    # Create a user
    payload = {'name': 'Alice Cooper', 'output': 'Test output', 'room': 'Test room'}
    request = client.post('/user', json=payload, follow_redirects=True)
    user_id = json.loads(request.data.decode())['id']

    payload = {'action': 'change_room', 'room': 'New room'}
    request = client.patch('/user/{}'.format(user_id), json=payload, follow_redirects=True)

    result = json.loads(request.data.decode())

    assert request.status_code == 200
    assert payload['room'] == result['room']


def test_user_update_output(client):
    # Create a user
    payload = {'name': 'Karl Marx', 'output': 'Test output', 'room': 'Test room'}
    request = client.post('/user', json=payload, follow_redirects=True)
    user_id = json.loads(request.data.decode())['id']

    payload = {'action': 'change_output', 'output': 'New output'}
    request = client.patch('/user/{}'.format(user_id), json=payload, follow_redirects=True)

    result = json.loads(request.data.decode())

    assert request.status_code == 200
    assert payload['output'] == result['output']


def test_user_deletion(client):
    # Create a user
    payload = {'name': 'Stresu computers', 'output': 'Test output', 'room': 'Test room'}
    request = client.post('/user', json=payload, follow_redirects=True)
    user_id = json.loads(request.data.decode())['id']

    payload = {'action': 'change_output', 'output': 'New output'}
    request = client.delete('/user/{}'.format(user_id), json=payload, follow_redirects=True)

    assert request.status_code == 200