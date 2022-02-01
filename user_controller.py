import json

from flask import request
from flask import Blueprint

from app import db
from models import MiniHub, User

bp = Blueprint('user', __name__)


@bp.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    output_users = []
    for user in users:
        user_data = {'id': user.id, 'name': user.name,
                     'output': user.output, 'room': user.room}
        output_users.append(user_data)

    return {'users': output_users}


@bp.route('/user', methods=['POST'])
def add_user():
    user = User(
        name=request.json['name'], output=request.json['output'], room=request.json['room'])
    db.session.add(user)
    db.session.commit()
    return {'id': user.id, 'name': user.name, 'output': user.output, 'room': user.room}


@bp.route('/user/<id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get_or_404(id)
    request_data = request.get_json()
    action = request_data['action']

    message = None

    if action == 'change_room':
        user.room = request_data['room']
    elif action == 'change_output':
        user.output = request_data['output']
    elif action == 'connect_to_minihub':
        minihub_id = request_data['minihub_id']
        minihub = MiniHub.query.get(minihub_id)

        if minihub is None:
            message = 'MiniHub does not exist!'
        elif minihub.connected_user is not None:
            message = 'Someone is already connected to the MiniHub!'
        else:
            minihub.connected_user = user
            minihub.connected_user_id = user.id
            message = 'Successfully connected to the MiniHub!'
    elif action == 'disconnect_from_minihub':
        minihub = MiniHub.query.filter(MiniHub.connected_user_id == user.id).first()

        if minihub is None:
            message = "You're not connected to any MiniHub!"
        else:
            minihub.connected_user = None
            minihub.connected_user_id = None
            message = "Successfully disconnected from MiniHub!"
    else:
        return json.dumps ({'message': 'Invalid command'})

    db.session.commit()
    return {'message': message, 'id': user.id, 'name': user.name, 'output': user.output, 'room': user.room}


@bp.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    if user is None:
        return {"error": "User not found."}

    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully."}
