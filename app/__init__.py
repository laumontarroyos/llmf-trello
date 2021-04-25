from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    db.create_all()

from .models import users
from .views import users, helper
from .routes import routes
