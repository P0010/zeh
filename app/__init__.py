from sqlalchemy import MetaData
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sassutils.wsgi import SassMiddleware # Sass css


# UPLOAD_FOLDER = 'app/static/images/product'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'gif'}


app = Flask(__name__)
app.config.from_object('config.DevConfig')  # Конфиги

app.wsgi_app = SassMiddleware(app.wsgi_app, {  # SCSS
    'app': ('static/sass', 'static/css', '/static/css')
})


manager = LoginManager(app)


db = SQLAlchemy(app)
migrate = Migrate(app,db)

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

from app import models_cases, models_main, routes_admin, routes_cases, routes_main, routes_redirect







