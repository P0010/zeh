from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    API_TOKEN = environ.get('API_TOKEN') 
    PASSWORD_MAIL = environ.get('PASSWORD_MAIL')
    EMAIL = 'zeh@zeh-ufa.ru'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'gif'}
    
class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')
    UPLOAD_FOLDER = 'HelloFlask/app/static/images/product/'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    UPLOAD_FOLDER = 'app/static/images/product/'





