from flask import Flask, Blueprint
from flask_login import LoginManager
from word_data.config import Config

bp = Blueprint('main', __name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    login = LoginManager(app)
    login.login_view = 'login'

    return app

from word_data.main import routes
