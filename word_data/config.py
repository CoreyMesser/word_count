import os
from word_data.constants import SystemConstants

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    sc = SystemConstants()
    DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    POSTS_PER_PAGE = 3
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')