from flask import request

from app import app
from app import db
from models import Hub


@app.route('/hub')
def get_hubs():
    hubs = Hub.query.all()
    output = []
    for hub in hubs:
        hub_data = {'id': hub.id, 'name': hub.name, 'user_nr': hub.user_number}
        output.append(hub_data)

    return {'hubs': output}


@app.route('/hub/<id>')
def get_hub_by_id(id):
    hub = Hub.query.get_or_404(id)
    return {'id': hub.id, 'name': hub.name}


@app.route('/hub', methods=['POST'])
def add_hub():
    hub = Hub(name=request.json['name'],
              user_number=request.json['user_number'])
    db.session.add(hub)
    db.session.commit()
    return {'id': hub.id, 'name': hub.name}


@app.route('/hub/<id>', methods=['DELETE'])
def delete_hub(id):
    hub = Hub.query.get(id)
    if hub is None:
        return {"error": "Hub not found."}

    db.session.delete(hub)
    db.session.commit()
    return {"message": "Hub deleted successfully."}
