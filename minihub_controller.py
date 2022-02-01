import json
import os
import subprocess
import time
import requests

from flask import request
from flask import Blueprint

from app import db, app
from models import MiniHub, User

bp = Blueprint('minihub', __name__)


@bp.route('/minihub', methods=['GET'])
def get_minihubs():
    minihubs = MiniHub.query.all()
    output_minihubs = []
    for minihub in minihubs:
        minihub_data = {'id': minihub.id, 'description': minihub.description, 'connected_user_id': minihub.connected_user_id,
                        'connected_user': minihub.connected_user.name if minihub.connected_user is not None else None, 'volume': minihub.volume}
        output_minihubs.append(minihub_data)

    return {'minihubs': output_minihubs}


@bp.route('/minihub', methods=['POST'])
def add_minihub():
    minihub = MiniHub(description=request.json['description'],
                      connected_user_id=request.json['connected_user_id'], volume=request.json['volume'],
                      port=request.json['port'])

    os.system (f"echo Starting minihub on {app.config['MINIHUBS_NETWORK']}:{minihub.port}")
    os.system (f"cd minihub_server && flask run --port={minihub.port} &")
    result = subprocess.run(['echo', '$!'], stdout=subprocess.PIPE)
    minihub.pid = result.stdout

    time.sleep (3)

    url = f"http://{app.config['MINIHUBS_NETWORK']}:{minihub.port}/media_player"
    payload = json.dumps ({'title': minihub.description})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data = payload, headers = headers)

    db.session.add(minihub)
    db.session.commit()
    return {'id': minihub.id, 'description': minihub.description, 'connected_user_id': minihub.connected_user_id, 'volume': minihub.volume}


@bp.route('/minihub/<id>', methods=['PATCH'])
def update_minihub(id):
    minihub = MiniHub.query.get_or_404(id)
    request_data = request.get_json()
    action = request_data['action']

    if action == 'change_description':
        minihub.description = request_data['description']
    elif action == 'change_volume':
        try:
            volume = int(request_data['volume'])
            if volume < 0 or volume > 100:
                return json.dumps({'message': 'Invalid volume specified!'}), 403
        except ValueError:
            return json.dumps({'message': 'Invalid volume specified!'}), 403

        minihub.volume = request_data['volume']
    elif action == 'change_connected_user':
        user = User.query.get(minihub.connected_user_id)

        if user is None:
            return json.dumps({'message': 'User does not exist!'}), 404

        minihub.connected_user_id = request_data['connected_user_id']
        minihub.connected_user = user
    elif action == 'disconnect_user':
        if minihub.connected_user is None:
            return json.dumps({'message': 'No user is currently connected!'})

        minihub.connected_user_id = None
        minihub.connected_user = None
    else:
        return json.dumps({'message': 'Invalid command'}), 403

    db.session.commit()
    return {'id': minihub.id,
            'description': minihub.description,
            'connected_user_id': minihub.connected_user_id,
            'connected_user': minihub.connected_user.name if minihub.connected_user is not None else None,
            'volume': minihub.volume}


@bp.route('/minihub/<id>', methods=['DELETE'])
def delete_minihub(id):
    minihub = MiniHub.query.get(id)
    if minihub is None:
        return {"error": "MiniHub not found."}, 404

    os.system (f"echo Killing minihub on {app.config['MINIHUBS_NETWORK']}:{minihub.port}")
    os.system (f"kill {minihub.pid} &")

    db.session.delete(minihub)
    db.session.commit()
    return {"message": "Minihub deleted successfully."}
