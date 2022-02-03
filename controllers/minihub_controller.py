import json
import time
import requests

from flask import request
from flask import Blueprint
from sqlalchemy import exc

from app import db, app, minihub_process_pool
from app import start_minihub_process, start_blank_media_player
from database.models import MiniHub, User

bp = Blueprint('minihub', __name__)


@bp.route('/minihub', methods=['GET'])
def get_minihubs():
    minihubs = MiniHub.query.all()
    output_minihubs = []
    for minihub in minihubs:
        minihub_data = get_minihub_data(minihub)
        output_minihubs.append(minihub_data)

    return {'minihubs': output_minihubs}


@bp.route('/minihub', methods=['POST'])
def add_minihub():
    minihub = MiniHub(description=request.json['description'],
                      volume=100 if 'volume' not in request.json else request.json['volume'],
                      port=request.json['port'])
    
    try:
        db.session.add(minihub)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return json.dumps({'message': 'Port already in use!'}), 403

    db.session.refresh(minihub) # Receive back the db auto-assigned id

    start_minihub_process(minihub)
    time.sleep(0.5)
    if 'headless' not in request.json:
        start_blank_media_player(minihub)

    return get_minihub_data(minihub)


@bp.route('/minihub/<id>', methods=['PATCH'])
def update_minihub(id):
    minihub = MiniHub.query.get_or_404(id)
    request_data = request.get_json()
    action = request_data['action']

    if action == 'change_description':
        minihub.description = request_data['description']

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
    return get_minihub_data(minihub)


@bp.route('/minihub/<id>', methods=['DELETE'])
def delete_minihub(id):
    minihub = MiniHub.query.get(id)
    if minihub is None:
        return {"error": "MiniHub not found."}, 404

    url = f"http://{app.config['MINIHUBS_NETWORK']}:{minihub.port}/media_player"
    response = requests.delete(url)

    if response.status_code != 200:
        return {"error": "Failed to delete the MiniHub's media player."}, 500

    try:
        minihub_process_pool[minihub.id].terminate()
        minihub_process_pool[minihub.id].close()
        del minihub_process_pool[minihub.id]
    except ValueError:
        return {"message": "MiniHub already deleted."}, 200
    except KeyError:
        pass

    db.session.delete(minihub)
    db.session.commit()

    return {"message": "Minihub deleted successfully."}


def get_minihub_data(minihub):
    return {
        'id': minihub.id,
        'description': minihub.description,
        'connected_user_id': minihub.connected_user_id,
        'connected_user': minihub.connected_user.name if minihub.connected_user is not None else None,
        'volume': minihub.volume,
        'port': minihub.port
    }
