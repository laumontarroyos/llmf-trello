from app import app
from flask import jsonify, url_for, redirect, Response, request
from ..views import helper
from flask_jwt_extended import jwt_required, get_current_user, get_jwt_identity

import requests


@app.route('/teste', methods=['GET'])
def teste():
    return jsonify({'message': f'Olá Laureano!'})


@app.route('/', methods=['GET'])
@jwt_required
def root():
    return jsonify({'message': f'Hello {get_current_user()}'})


@app.route('/authenticate', methods=['POST'])
def authenticate():
    return helper.auth()

#@jwt_required
#@app.route('/users/<id>', methods=['DELETE'])
#def delete_users(id):
#    return users.delete_user(id)


#Consulta Listas de um Quadro <id>
@app.route('/trello/lists', methods=['GET'])
def get_lists():
    payload = {   
            "key": f"{app.config['TRELLO_KEY']}",
            "token": f"{app.config['TRELLO_TOKEN']}"
    }
    url = f"https://api.trello.com/1/boards/{app.config['TRELLO_BOARD']}/lists"
    r = requests.get(url, json=payload)
    return jsonify({"Mensagem": "Consultar Listas de um Quadro", "retorno": f"{r.text}" })

#Consulta uma Lista <id>
@app.route('/trello/lists/<id>', methods=['GET'])
def get_list(id):
    payload = {   
            "key": f"{app.config['TRELLO_KEY']}",
            "token": f"{app.config['TRELLO_TOKEN']}"
    } 
    url = f"https://api.trello.com/1/lists/{id}"
    r = requests.get(url, json=payload)
    return jsonify({"Mensagem": "Consultar uma Lista", "retorno": f"{r.text}" })

#Consulta Cartões de uma Lista <id>
@app.route('/trello/lists/<id>/cards', methods=['GET'])
def get_list_cards(id):
    payload = {   
            "key": f"{app.config['TRELLO_KEY']}",
            "token": f"{app.config['TRELLO_TOKEN']}"
    }    
    url = f"https://api.trello.com/1/lists/{id}/cards"
    r = requests.get(url, json=payload)
    return jsonify({"Mensagem": "Consultar Cartões de uma Lista", "retorno": f"{r.text}" })

#Inclusão de um Cartão 'name' na lista <id>
@app.route('/trello/lists/<id>/cards', methods=['POST'])
def post_list_cards(id):
    payload = {   
            "key": f"{app.config['TRELLO_KEY']}",
            "token": f"{app.config['TRELLO_TOKEN']}",
            "idList": f"{id}",
            "name" : f"{request.json['name']}"
    }
    url = f"https://api.trello.com/1/cards"
    r = requests.post(url, json=payload)
    return jsonify({"Mensagem": "Incluir Cartão em uma Lista", "retorno": f"{r.text}" })

# Exclusão de um Cartão <id>
@app.route('/trello/cards/<id>', methods=['DELETE'])
def delete_cards(id):
    payload = {   
            "key": f"{app.config['TRELLO_KEY']}",
            "token": f"{app.config['TRELLO_TOKEN']}"
    }
    url = f"https://api.trello.com/1/cards/{id}"
    r = requests.delete(url, json=payload)
    return jsonify({"Mensagem": "Excluir Cartão de uma Lista", "retorno": f"{r.status_code}" })