from flask import Flask

app = Flask(__name__)
from testapp.app import views