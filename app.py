from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = None
db = None


def create_app(testing=False):
    global app, db
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' if testing == False else 'sqlite:///test.db'
    # Supress flask warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if testing:
        app.config['TESTING'] = True

    db = SQLAlchemy(app)

    import models
    db.create_all()

    # import after db has been instantiated
    import hub_controller
    import user_controller
    import media_controller
    import minihub_controller
    import swagger_controller

    app.register_blueprint(hub_controller.bp)
    app.register_blueprint(user_controller.bp)
    app.register_blueprint(media_controller.bp)
    app.register_blueprint(minihub_controller.bp)
    app.register_blueprint(swagger_controller.SWAGGERUI_BLUEPRINT)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    return app


if __name__ == '__main__':
    create_app()
