
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from word_data.config import Config
from word_data.database import db_session

db = db_session()
app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'

# bp = Blueprint('auth', __name__)
#
# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     login = LoginManager(app)
#     login.login_view = 'login'
#
#     return app

from word_data.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from word_data.errors import bp as errors_bp
app.register_blueprint(errors_bp)


from word_data.auth import routes
import word_data.models
