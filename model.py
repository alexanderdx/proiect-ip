from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Supress flask warning
db = SQLAlchemy(app)

class Hub(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_number = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.user_number}'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    output = db.Column(db.String(100))
    room = db.Column(db.Integer)

class MiniHub(db.Model):
    __tablename__ = 'mini_hubs'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    connected_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    connected_user = db.relationship("User", backref=backref('users', uselist=False))
    volume = db.Column(db.Integer)
