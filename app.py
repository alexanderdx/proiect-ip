from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Hub(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_number = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.user_number}"


@app.route('/')
def hello():
    return 'Hello'


@app.route('/hubs')
def get_hubs():
    hubs = Hub.query.all()
    output = []
    for hub in hubs:
        hub_data = {"id": hub.id, "name": hub.name, "user_nr": hub.user_number}
        output.append(hub_data)

    return {"hubs": output}
