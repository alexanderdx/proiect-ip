import json
import requests as req
from requests.structures import CaseInsensitiveDict

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
    user = User(name=request.json['name'],
                room=request.json['room'],
                volume=100,
                timestamp=0)

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
        new_room = request_data['room']

        if user.room == new_room:
            return json.dumps({'message': 'The user is already in that room.'}), 200

        if new_room is None:
            return json.dumps({'message': 'Destination room must be specified.'}), 403
        
        user.room = new_room

        db.session.commit()

        current_minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()
        new_minihub = MiniHub.query.get(new_room)

        if current_minihub is not None:
            if current_minihub.id == new_room: # User is returning to his room
                payload = json.dumps({
                    "command": "play",
                })
                change_data(current_minihub, payload)
                return json.dumps({'message': f'{user.name} returning to his room. Resuming...'}), 200

            else: # User has left his room
                # Save current timestamp and volume
                user.timestamp = get_data(current_minihub, json.dumps(get_time_payload)).json()["time"]
                user.volume = get_data(current_minihub, json.dumps(get_volume_payload)).json()["volume"]

                # Pause the current minihub if the new one is taken
                payload = json.dumps({
                    "command": "pause",
                })
                change_data(current_minihub, payload)

        if new_minihub is None:
            return json.dumps({'message': 'No MiniHub exists in that room.'}), 403

        if new_minihub.connected_user is None:
            # No one is using the new minihub, we can disconnect from the old one
            current_minihub.connected_user_id = None
            current_minihub.connected_user = None
            # And clear its player
            payload = json.dumps({
                "command": "stop",
            })
            change_data(current_minihub, payload)

            # Connect to the new one
            new_minihub.connected_user_id = user.id
            new_minihub.connected_user = user

            # Resume with our media, timestamp and volume
            payload = json.dumps({
                "command": "set_media",
                "query": f"{user.playing}",
            })
            change_data(new_minihub, payload)

            payload = json.dumps({
                "command": "set_time",
                "time": user.timestamp,
            })
            change_data(new_minihub, payload)

            payload = json.dumps({
                "command": "set_volume",
                "volume": user.volume,
            })
            change_data(new_minihub, payload)
        else:
            return json.dumps({'message': f'Going to room {new_room}. {new_minihub.connected_user.name} is connected to this room.'}), 200

        db.session.commit()

    elif action == 'play':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            if 'query' in request_data:
                user.playing = request_data['query']
                
            payload = json.dumps({
                "command": "set_media",
                "query": f"{user.playing}",
            })
            change_data(minihub, payload)

    elif action == 'pause':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            payload = json.dumps({
                "command": "pause",
            })
            change_data(minihub, payload)

    elif action == 'stop':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            payload = json.dumps({
                "command": "stop",
            })
            change_data(minihub, payload)

    elif action == 'resume':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            payload = json.dumps({
                "command": "play",
            })
            change_data(minihub, payload)

    elif action == 'mute':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            payload = json.dumps({
                "command": "mute",
            })
            change_data(minihub, payload)

    elif action == 'unmute':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            payload = json.dumps({
                "command": "unmute",
            })
            change_data(minihub, payload)

    elif action == 'vup':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            payload = json.dumps({
                "command": "vup",
            })
            change_data(minihub, payload)

    elif action == 'vdown':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            payload = json.dumps({
                "command": "vdown",
            })
            change_data(minihub, payload)

    elif action == 'set_time':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            payload = json.dumps({
                "command": "set_time",
                "time": request_data ['time']
            })
            change_data(minihub, payload)

    elif action == 'set_volume':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            return json.dumps({'message': "You're not connected to any MiniHub!"})
        else:
            try:
                volume = int(request_data['volume'])
                if volume < 0 or volume > 100:
                    return json.dumps({'message': 'Invalid volume specified!'}), 403
            except ValueError:
                return json.dumps({'message': 'Invalid volume specified!'}), 403

            payload = json.dumps({
                "command": "set_volume",
                "volume": request_data['volume']
            })
            change_data(minihub, payload)
            user.volume = volume
            minihub.volume = volume

    elif action == 'connect_to_minihub':
        minihub_id = request_data['minihub_id']
        minihub = MiniHub.query.get(minihub_id)

        if minihub is None:
            return json.dumps({'message': 'MiniHub does not exist!'}), 404
        elif minihub.connected_user is not None:
            return json.dumps({'message': 'Someone is already connected to the MiniHub!'}), 403
        else:
            current_minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()
            if current_minihub is not None:
                return json.dumps({'message': f"You're already connected to MiniHub {current_minihub.id}! Please disconnect first and try again."})
            
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

            payload = json.dumps({
                "command": "stop",
            })
            change_data(minihub, payload)

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
        'playing': user.playing,
        'room': user.room,
        'connected_to': "MiniHub {}".format(connected_minihub.id) if connected_minihub is not None else None
    }
