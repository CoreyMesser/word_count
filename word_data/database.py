import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

Base = declarative_base()
def get_uri():
    return "postgresql://%s:%s@%s/%s" % (
        os.getenv('DB_USER'),
        os.getenv('DB_PW'),
        os.getenv('DB_HOST'),
        os.getenv('DB_NAME'),
    )


engine = create_engine(get_uri(), poolclass=NullPool)
db_session = sessionmaker(bind=engine)
