from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config.Config')

jwt = JWTManager(app)

from .views import helper
from .routes import routes
