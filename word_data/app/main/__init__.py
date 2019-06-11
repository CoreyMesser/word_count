from flask import Blueprint

bp = Blueprint('main', __name__)

from word_data.app.main import routes