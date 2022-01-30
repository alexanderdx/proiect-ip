import sys, json
from flask import request
from app import app
from classes.media_player import media_player

media_players = dict ()


@app.route ('/media_player/<id>', methods = ['POST'])
def create (id):
    global media_players

    media_players[id] = media_player ()
    return json.dumps ({'message': 'player created'})


@app.route ('/media_player/<id>', methods = ['PATCH'])
def update (id):
    global media_players
    
    request_data = request.get_json ()
    command      = request_data['command']
    if command == 'set_media':
        query = request_data['query']
        media_players[id].set_media (media_players[id].search (str(query)))
    elif command == 'play':
        media_players[id].play ()
    elif command == 'pause':
        media_players[id].pause ()
    elif command == 'mute':
        media_players[id].mute ()
    elif command == 'unmute':
        media_players[id].unmute ()
    elif command == 'vup':
        media_players[id].volume_up ()
    elif command == 'vdown':
        media_players[id].volume_down ()
    else:
        return json.dumps ({'message': 'wrong command'})
    return json.dumps ({'message': 'command sent'})


@app.route ('/media_player/<id>', methods = ['DELETE'])
def destroy (id):
    global media_players
    
    media_players[id].close ()
    media_players[id] = None
    return json.dumps ({'message': 'player destroyed'})