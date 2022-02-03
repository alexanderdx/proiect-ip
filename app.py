import os
import time
import requests
import json
import atexit
import multiprocessing

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = None
db  = None

minihub_process_pool = {}

def create_app (testing = False):
    global app, db
    app = Flask (__name__, instance_relative_config = True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' if testing == False else 'sqlite:///test.db'
    # Supress flask warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MINIHUBS_NETWORK'] = 'localhost'

    if testing:
        app.config['TESTING'] = True

    db = SQLAlchemy (app)
    # db.session.no_autoflush

    import database.models as models
    db.create_all ()

    # import after db has been instantiated
    import controllers.hub_controller as hub_controller
    import controllers.user_controller as user_controller
    import controllers.minihub_controller as minihub_controller
    import controllers.swagger_controller as swagger_controller

    app.register_blueprint (hub_controller.bp)
    app.register_blueprint (user_controller.bp)
    app.register_blueprint (minihub_controller.bp)
    app.register_blueprint (swagger_controller.SWAGGERUI_BLUEPRINT)

    @app.route ('/')
    def hello_world ():
        return 'Hello World!'

    atexit.register(close_minihubs)
    launch_minihubs ()
    
    return app

def start_minihub_process(minihub):
    global app, minihub_process_pool

    t = multiprocessing.Process(target=minihub_process, name=f'minihub-{minihub.port}', args=(app.config['MINIHUBS_NETWORK'], minihub.port,))
    minihub_process_pool[minihub.id] = t
    minihub_process_pool[minihub.id].daemon = True
    minihub_process_pool[minihub.id].start()

def minihub_process(network_path, port):
    os.system (f"echo Starting minihub on {network_path}:{port} with PID {multiprocessing.current_process().pid}")
    os.system (f"cd minihub_server && flask run --port={port} &")

def start_blank_media_player(minihub):
    global app

    url = f"http://{app.config['MINIHUBS_NETWORK']}:{minihub.port}/media_player"
    payload = json.dumps ({'title': minihub.description})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data = payload, headers = headers)

def launch_minihubs ():
    global app, db, minihub_process_pool
    from database.models import MiniHub

    minihubs = MiniHub.query.all ()
    for minihub in minihubs:
        start_minihub_process(minihub)
        time.sleep(1.0)
        start_blank_media_player(minihub)


def close_minihubs():
    global minihub_process_pool

    print("Terminating MiniHub processes...")
    for proc in minihub_process_pool.values():
        proc.terminate()
        proc.close()


if __name__ == '__main__':
    create_app()
