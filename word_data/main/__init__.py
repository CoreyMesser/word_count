from flask import Flask
from flask_login import LoginManager
from word_data.config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)

from word_data.main import routes
