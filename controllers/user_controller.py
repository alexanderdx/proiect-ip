from hashlib import new
import json
import requests as req
from requests.structures import CaseInsensitiveDict
import time

from flask import request
from flask import Blueprint

from app import db
from database.models import MiniHub, User


def change_data(minihub, payload):
    url = "http://localhost"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    response = req.patch(f"{url}:{minihub.port}/media_player", headers=headers, data=payload)
    print(response)

def get_data(minihub, payload):
    url = "http://localhost"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    response = req.get(f"{url}:{minihub.port}/media_player", headers=headers, data=payload)
    return response


get_volume_payload = {
    "command" : "get_volume"
}

get_time_payload = {
    "command" : "get_time"
}






bp = Blueprint('user', __name__)


@bp.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    output_users = []
    for user in users:
        user_data = get_user_data(user)
        output_users.append(user_data)

    return {'users': output_users}


@bp.route('/user/<id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get_or_404(id)

    user_data = get_user_data(user)

    return user_data


@bp.route('/user', methods=['POST'])
def add_user():
    user = User(name=request.json['name'], output=request.json['output'], room=request.json['room'])

    db.session.add(user)
    db.session.commit()
    return get_user_data(user)


@bp.route('/user/<id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get(id)

    if user is None:
        return {"error": "User not found."}, 404

    request_data = request.get_json()
    action = request_data['action']

    if action == 'change_room':
        old_time = 0
        old_volume = 100

        new_room = request_data['room']
        if user.room == new_room:
            return json.dumps({'message': 'The user is already in that room.'}), 200

        if(user.room != 0):
            old_minihub = MiniHub.query.get(user.room)
            old_minihub.connected_user_id = None
            old_minihub.connected_user = None
            old_time =  get_data(old_minihub, json.dumps(get_time_payload))
            old_time = old_time.json()["time"]
            old_volume = get_data(old_minihub, json.dumps(get_volume_payload))
            old_volume = old_volume.json()["volume"]

            payload = json.dumps({
                "command" : "pause",
                })
            change_data(old_minihub, payload)
            db.session.commit()


        user.room = new_room
        if user.room != 0:
            new_minihub = MiniHub.query.get(user.room)
            if (new_minihub.connected_user_id == None or new_minihub.connected_user_id == 0) and new_minihub.connected_user_id != user.id:
                new_minihub.connected_user_id = user.id
                new_minihub.connected_user = user
                payload = json.dumps({
                    "command" : "set_media", 
                    "query": f"{user.output}",
                    })
                change_data(new_minihub, payload)
                time.sleep(3)
                payload = json.dumps({
                    "command" : "set_time", 
                    "time": old_time,
                    })
                change_data(new_minihub, payload)
                payload = json.dumps({
                    "command" : "set_volume", 
                    "volume": old_volume,
                    })
                change_data(new_minihub, payload)
                db.session.commit()
                


    elif action == 'change_output':
        user.output = request_data['output']
    elif action == 'connect_to_minihub':
        minihub_id = request_data['minihub_id']
        minihub = MiniHub.query.get(minihub_id)

        if minihub is None:
            return json.dumps({'message': 'MiniHub does not exist!'}), 404
        elif minihub.connected_user is not None:
            return json.dumps({'message': 'Someone is already connected to the MiniHub!'}), 403
        else:
            minihub.connected_user = user
            minihub.connected_user_id = user.id

            db.session.commit()
            return json.dumps({'message': 'Successfully connected to the MiniHub!'})

    elif action == 'disconnect_from_minihub':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            minihub.connected_user = None
            minihub.connected_user_id = None

            db.session.commit()
            return json.dumps({'message': "Successfully disconnected from MiniHub!"})
    else:
        return json.dumps({'message': 'Invalid command'}), 403

    db.session.commit()
    return get_user_data(user)


@bp.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return {"error": "User not found."}, 404

    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully."}


def get_user_data(user):
    connected_minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()
    
    return {
        'id': user.id,
        'name': user.name,
        'output': user.output,
        'room': user.room,
        'connected_to': "MiniHub {}".format(connected_minihub.id) if connected_minihub is not None else None
    }
