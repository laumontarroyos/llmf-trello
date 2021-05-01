from flask import request, jsonify
from werkzeug.security import check_password_hash
from app import jwt, app
from flask_jwt_extended import create_access_token


# Gerando token com base na Secret key do app
def auth():
    auth = request.authorization

    if (not auth or not auth.username or not auth.password):
        return jsonify({'message': 'could not verify', 'WWW-Authenticate1': 'Basic auth="Login required"'}), 401

    if (auth.username != app.config['LLMF_API_USER']):
        return jsonify({"message": "Bad username"}), 401


    if (check_password_hash(app.config['LLMF_API_PASSWORD_HASH'], auth.password)):
        
        token = create_access_token(identity = auth.username)

        return jsonify({'message': 'Validated successfully', 'token': token})

    return jsonify({'message': 'could not verify', 'WWW-Authenticate2': 'Basic auth="Login required"'}), 401