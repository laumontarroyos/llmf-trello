from flask import request, jsonify
from werkzeug.security import check_password_hash
from app import jwt
from flask_jwt_extended import create_access_token


# Gerando token com base na Secret key do app
def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'could not verify', 'WWW-Authenticate1': 'Basic auth="Login required"'}), 401
    

    if check_password_hash("colocar_aqui_a_senha_fixa", auth.password):
        
        token = create_access_token(identity = "123456789")

        return jsonify({'message': 'Validated successfully', 'token': token})

    return jsonify({'message': 'could not verify', 'WWW-Authenticate2': 'Basic auth="Login required"'}), 401

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    try:
        return "123456789"
    except:
        return None