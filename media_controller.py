import sys
from app import app

from classes.media_player import media_player
mp = media_player ()

@app.route("/controlls/play/<query>")
def set_media (query):
    mp.set_media (mp.search (str(query)))
    return 'Command sent'

@app.route("/controlls/play")
def play ():
    mp.play ()
    return 'Command sent'

@app.route("/controlls/pause")
def pause ():
    mp.pause ()
    return 'Command sent'

@app.route("/controlls/mute")
def mute ():
    mp.mute ()
    return 'Command sent'

@app.route("/controlls/unmute")
def unmute ():
    mp.unmute ()
    return 'Command sent'

@app.route("/controlls/vup")
def volume_up ():
    mp.volume_up ()
    return 'Command sent'

@app.route("/controlls/vdown")
def volume_down ():
    mp.volume_down ()
    return 'Command sent'