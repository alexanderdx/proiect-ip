import os
import json
import subprocess

from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from classes.media_player import media_player

app = Flask (__name__, instance_relative_config=True)
mp  = None
print ("Minihub started successfully")


@app.route ('/media_player', methods = ['POST'])
def create ():
    global mp

    title = None
    if request.data:
        request_data = request.get_json ()
        title        = request_data['title']
    
    if mp is None:
        mp = media_player (title)
        mp.set_media ('blank.mp4', is_youtube = False)
    return json.dumps ({'message': 'player created'})


@app.route ('/media_player', methods = ['PATCH'])
def update ():
    global mp
    
    request_data = request.get_json ()
    command      = request_data['command']
    if command == 'set_media':
        query = request_data['query']
        mp.set_media (mp.search (str (query)))
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
    elif command == 'set_time':
        time = request_data ['time']
        mp.set_time (int (time))
    else:
        return json.dumps ({'message': 'wrong command'})
    return json.dumps ({'message': 'command executed succesfully'})


@app.route ('/media_player', methods = ['DELETE'])
def destroy ():
    global mp
    
    mp.close ()
    mp = None
    return json.dumps ({'message': 'player destroyed'})


@app.route ('/media_player', methods = ['GET'])
def index ():
    global mp
    
    request_data = request.get_json ()
    command      = request_data['command']
    if command == 'get_time':
        return json.dumps ({'time': mp.get_time ()})
    elif command == 'get_volume':
        return json.dumps ({'volume': mp.get_volume ()})
    else:
        return json.dumps ({'message': 'wrong command'})