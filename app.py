import os
import subprocess
import time
import requests
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = None
db  = None


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

    launch_minihubs ()

    return app


def launch_minihubs ():
    global app, db
    from database.models import MiniHub

    minihubs = MiniHub.query.all ()

    for minihub in minihubs:
        os.system (f"echo Starting minihub on {app.config['MINIHUBS_NETWORK']}:{minihub.port}")
        os.system (f"cd minihub_server && flask run --port={minihub.port} &")
        result = subprocess.run (['echo', '$!'], stdout = subprocess.PIPE)
        minihub.pid = result.stdout

        time.sleep (3)

        url = f"http://{app.config['MINIHUBS_NETWORK']}:{minihub.port}/media_player"
        payload = json.dumps ({'title': minihub.description})
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data = payload, headers = headers)

    db.session.commit ()


if __name__ == '__main__':
    create_app()
