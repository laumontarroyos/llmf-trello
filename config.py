
import random
import string
from os import environ, path
from dotenv import load_dotenv
from datetime import timedelta


basedir = path.abspath(path.dirname(__file__))

# carregar configurações de acordo com opção de execução do App: servidor local ou remoto
load_dotenv(path.join(basedir, '.env'))
#load_dotenv(path.join(basedir, '.env-remote'))

class Config:
    
    
    key = ''.join(
        (random.choice(string.ascii_letters + string.digits + string.ascii_uppercase))
         for i in range(12))    
    
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    
    JWT_SECRET_KEY = key 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(environ.get('JWT_ACCESS_TOKEN_EXPIRES'))
    )
   
    DEBUG = environ.get('DEBUG')