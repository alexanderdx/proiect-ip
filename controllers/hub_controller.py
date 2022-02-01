import json

from flask import request
from flask import Blueprint

from app import db
from database.models import Hub

bp = Blueprint('hub', __name__)


@bp.route('/hub', methods = ['GET'])
def get_hubs ():
    hubs = Hub.query.all ()
    output = []
    for hub in hubs:
        hub_data = {'id': hub.id,
                    'name': hub.name,
                    'user_nr': hub.user_number}
        output.append (hub_data)

    return {
        'hubs': output
    }


@bp.route('/hub/<id>', methods = ['GET'])
def get_hub_by_id (id):
    hub = Hub.query.get_or_404 (id)

    return {
        'id': hub.id,
        'name': hub.name,
        'user_number': hub.user_number
    }


@bp.route('/hub', methods = ['POST'])
def add_hub ():
    hub = Hub (name = request.json['name'],
              user_number = request.json['user_number'])
    db.session.add (hub)
    db.session.commit()

    return {
        'id': hub.id,
        'name': hub.name,
        'user_number': hub.user_number
    }


@bp.route('/hub/<id>', methods = ['PATCH'])
def update_hub (id):
    hub          = Hub.query.get_or_404 (id)
    request_data = request.get_json ()
    action       = request_data['action']

    if action == 'update_name':
        hub.name = request_data['name']
    elif action == 'update_connected_user':
        hub.user_number = request_data['user_number']
    else:
        return json.dumps ({'message': 'Invalid command'})

    db.session.commit ()
    return {
        'id': hub.id,
        'name': hub.name,
        'user_number': hub.user_number
    }


@bp.route('/hub/<id>', methods = ['DELETE'])
def delete_hub (id):
    hub = Hub.query.get_or_404 (id)
    if hub is None:
        return {"error": "Hub not found."}

    db.session.delete (hub)
    db.session.commit ()
    return {"message": "Hub deleted successfully."}
