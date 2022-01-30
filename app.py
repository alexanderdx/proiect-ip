from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Supress flask warning
db = SQLAlchemy(app)

import models
db.create_all()

import hub_controller
import user_controller
import media_controller
import minihub_controller
