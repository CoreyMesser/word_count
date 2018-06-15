import os
from word_data.constants import SystemConstants


class Config(object):
    DATABASE_URI = os.environ.get(SystemConstants.DATABASE_URI)
