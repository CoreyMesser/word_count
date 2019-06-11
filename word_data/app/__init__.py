import os
import logging
from logging.handlers import RotatingFileHandler

from word_data.config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from word_data.config import Config
from word_data.database import db_session

db = db_session()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    bootstrap.init_app(app)

    from word_data.app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from word_data.app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from word_data.app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:


        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/prose.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Prose startup')

    return app


from word_data.app.auth import routes


# from flask import Flask
#
# app = Flask(__name__)
# from word_data.app.auth import routes
