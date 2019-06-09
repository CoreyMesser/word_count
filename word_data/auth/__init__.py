from flask import Blueprint

bp = Blueprint('auth', __name__)

from word_data.auth import routes