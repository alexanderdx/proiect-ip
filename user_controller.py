from flask import request

from app import app
from app import db
from models import User

@app.route('/user')
def get_users():
    users = User.query.all()
    output_users = []
    for user in users:
        user_data = {'id': user.id, 'name': user.name, 'output': user.output, 'room': user.room}
        output_users.append(user_data)

    return {'users': output_users}

@app.route('/user', methods=['POST'])
def add_user():
    user = User(name=request.json['name'], output=request.json['output'], room=request.json['room'])
    db.session.add(user)
    db.session.commit()
    return {'id': user.id, 'name': user.name, 'room': user.room}

@app.route('/user/<id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get_or_404(id)
    request_data = request.get_json ()
    action = request_data['action']

    if action == 'change_room':
        user.room = request_data['room']
    elif action == 'change_output':
        user.output = request_data['output']

    db.session.commit()
    return {'id': user.id, 'name': user.name,'output': user.output, 'room': user.room}

@app.route('/user/<id>', methods = ['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    if user is None:
        return {"error": "User not found."}

    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully."}

