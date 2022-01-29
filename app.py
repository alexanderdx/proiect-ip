from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Supress flask warning
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)


class Hub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_number = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.user_number}'


@app.route('/')
def hello():
    return 'Hello'


@app.route('/hubs')
def get_hubs():
    hubs = Hub.query.all()
    output = []
    for hub in hubs:
        hub_data = {'id': hub.id, 'name': hub.name, 'user_nr': hub.user_number}
        output.append(hub_data)

    return {'hubs': output}


@app.route('/hubs/<id>')
def get_hub_by_id(id):
    hub = Hub.query.get_or_404(id)
    return {'id': hub.id, 'name': hub.name}


@app.route('/hubs', methods=['POST'])
def add_hub():
    hub = Hub(id=request.json['id'], name=request.json['name'],
              user_number=request.json['user_number'])
    db.session.add(hub)
    db.session.commit()
    return {'id': hub.id, 'name': hub.name}


@app.route('/hubs/<id>', methods=['DELETE'])
def delete_hub(id):
    hub = Hub.query.get(id)
    if hub is None:
        return {"error": "Hub not found."}

    db.session.delete(hub)
    db.session.commit()
    return {"message": "Hub deleted successfully."}
