import sys, json
from flask import request
from app import app
from classes.media_player import media_player

mp = None

@app.route ('/media_player', methods = ['POST'])
def create ():
    global mp 

    mp = media_player ()
    return json.dumps ({'message': 'player created'})


@app.route ('/media_player', methods = ['PATCH'])
def update ():
    global mp 
    
    request_data = request.get_json ()
    command      = request_data['command']
    if command == 'set_media':
        query = request_data['query']
        mp.set_media (mp.search (str(query)))
    elif command == 'play':
        mp.play ()
    elif command == 'pause':
        mp.pause ()
    elif command == 'mute':
        mp.mute ()
    elif command == 'unmute':
        mp.unmute ()
    elif command == 'vup':
        mp.volume_up ()
    elif command == 'vdown':
        mp.volume_down ()
    else:
        return json.dumps ({'message': 'wrong command'})
    return json.dumps ({'message': 'command sent'})


@app.route ('/media_player', methods = ['DELETE'])
def destroy ():
    global mp 
    
    mp.close ()
    mp = None
    return json.dumps ({'message': 'player destroyed'})