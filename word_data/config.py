import os
from word_data.constants import SystemConstants


class Config(object):
    sc = SystemConstants()
    DATABASE_URI = os.getenv('DATABASE_URI')
