from flask import Blueprint

bp = Blueprint('main', __name__)

from word_data.main import routes