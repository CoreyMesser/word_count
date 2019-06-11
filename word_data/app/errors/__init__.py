from flask import Blueprint

bp = Blueprint('errors', __name__)

from word_data.app.errors import handlers