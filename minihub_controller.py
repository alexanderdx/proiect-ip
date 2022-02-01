import json
import os
import subprocess

from flask import request
from flask import Blueprint

from app import db, app
from models import MiniHub

bp = Blueprint('minihub', __name__)


@bp.route('/minihub', methods=['GET'])
def get_minihubs():
    minihubs = MiniHub.query.all()
    output_minihubs = []
    for minihub in minihubs:
        minihub_data = {'id': minihub.id, 'description': minihub.description,
                        'connected_user_id': minihub.connected_user_id, 'volume': minihub.volume}
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
        minihub.volume = request_data['volume']
    elif action == 'change_connected_user':
        minihub.connected_user_id = request_data['connected_user_id']
    else:
        return json.dumps ({'message': 'invalid command'})

    db.session.commit()
    return {'id': minihub.id, 'description': minihub.description, 'connected_user_id': minihub.connected_user_id, 'volume': minihub.volume}


@bp.route('/minihub/<id>', methods=['DELETE'])
def delete_minihub(id):
    minihub = MiniHub.query.get_or_404(id)
    if minihub is None:
        return {"error": "MiniHub not found."}

    os.system (f"echo Killing minihub on {app.config['MINIHUBS_NETWORK']}:{minihub.port}")
    os.system (f"kill {minihub.pid} &")

    db.session.delete(minihub)
    db.session.commit()
    return {"message": "Minihub deleted successfully."}
