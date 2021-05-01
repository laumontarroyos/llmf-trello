from app import app
from flask import jsonify, url_for, redirect, Response, request
from ..views import helper
from flask_jwt_extended import jwt_required, get_current_user, get_jwt_identity

import requests, json


@app.route('/check', methods=['GET'])
@jwt_required
def check():
    return jsonify({'message': f'Ok, checked...'})

@app.route('/login', methods=['POST'])
def authenticate():
    return helper.auth()

def limpar_escolhas(login):
    # recuperar todas as varas
    payload = {   
        "key": f"{app.config['TRELLO_KEY']}",
        "token": f"{app.config['TRELLO_TOKEN']}",
        "fields": "id,name,subscribed"
    }
    url = f"https://api.trello.com/1/boards/{app.config['TRELLO_BOARD']}/lists"
    r = requests.get(url, json=payload)
    varas = json.loads( r.text )
    if(varas!=None):
        for vara in varas:
            if(vara['subscribed'] == False):
                # recuperar todos os magistrados concorrendo a uma Vara
                payload = {   
                    "key": f"{app.config['TRELLO_KEY']}",
                    "token": f"{app.config['TRELLO_TOKEN']}"
                }    
                url = f"https://api.trello.com/1/lists/{vara['id']}/cards"
                r = requests.get(url, json=payload)
                magistrados = json.loads( r.text )
                if(magistrados!=None):
                    for magistrado in magistrados:
                        if(login in(magistrado['name'])):
                            # excluir magistrado desta escolha de vara
                            payload = {   
                                "key": f"{app.config['TRELLO_KEY']}",
                                "token": f"{app.config['TRELLO_TOKEN']}"
                            }
                            url = f"https://api.trello.com/1/cards/{magistrado['id']}"
                            r = requests.delete(url, json=payload)
                            break
    return                        

@app.route('/trello/limpar', methods=['POST'])
@jwt_required
def post_limpar_escolhas():
    data = request.get_json()
    if(data!=None):
        limpar_escolhas(data['login'])
        return jsonify({"Mensagem": "Limpar escolhas do Magistrados", "retorno": "As escolhas existentes para o magistrado foram apagadas."})
    return jsonify({"Mensagem": "Limpar escolhas do Magistrados", "retorno": "Não foi possível identificar o magistrado para limpar suas escolhas."})

    

# Preencher escolhas dos Magistrados/
#  Lista de varas deve chegar na ordem escolhida
@app.route('/trello/magistrados', methods=['POST'])
@jwt_required
def post_preencher_escolhas():
    data = request.get_json()
    if(data!=None):
        limpar_escolhas(data['login'])
        nome_magistrado = f"{data['magistrado']}/{data['login']}"
        NumeroOpcao = 1
        for vara in data['varas']:
            #Inclusão do magistrado em cada vara escolhida pela ordem de preferência
            payload = {   
                "key": f"{app.config['TRELLO_KEY']}",
                "token": f"{app.config['TRELLO_TOKEN']}",
                "idList": f"{vara['id']}",
                "name" : f"{NumeroOpcao} - {nome_magistrado}"
            }
            url = f"https://api.trello.com/1/cards"
            r = requests.post(url, json=payload)
            NumeroOpcao = NumeroOpcao + 1
        return jsonify({"Mensagem": "Preencher escolhas do Magistrado", "retorno": "Escolhas feitas pelo magistrado enviadas ao quadro do Trello."})  
    return jsonify({"Mensagem": "Preencher escolhas do Magistrado", "retorno": "Não foi possível identificar as escolhas do magistrado."})

#Consultar Varas disponíveis para procedimento de remoção de magistrados
@app.route('/trello/varas', methods=['GET'])
@jwt_required
def get_varas():
    payload = {   
            "key": f"{app.config['TRELLO_KEY']}",
            "token": f"{app.config['TRELLO_TOKEN']}",
            "fields": "id,name"
    }
    url = f"https://api.trello.com/1/boards/{app.config['TRELLO_BOARD']}/lists"
    r = requests.get(url, json=payload)
    return jsonify({"Mensagem": "Consultar Varas para Remoção de Magistrados", "retorno": f"{r.text}" })


#Consulta Listas de um Quadro <id>
@app.route('/trello/lists', methods=['GET'])
@jwt_required
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
@jwt_required
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
@jwt_required
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
@jwt_required
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
@jwt_required
def delete_cards(id):
    payload = {   
            "key": f"{app.config['TRELLO_KEY']}",
            "token": f"{app.config['TRELLO_TOKEN']}"
    }
    url = f"https://api.trello.com/1/cards/{id}"
    r = requests.delete(url, json=payload)
    return jsonify({"Mensagem": "Excluir Cartão de uma Lista", "retorno": f"{r.status_code}" })