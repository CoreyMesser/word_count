import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
def get_uri():
    return "postgresql://%s:%s@%s/%s" % (
        os.getenv('DB_USER'),
        os.getenv('DB_PW'),
        os.getenv('DB_HOST'),
        os.getenv('DB_NAME'),
    )


engine = create_engine(get_uri())
db_session = sessionmaker(bind=engine)
