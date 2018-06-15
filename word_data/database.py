import os
from word_data.config import SystemConstants as sc

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Base.query = db_session.query_property()

# db_uri = os.environ.get(SystemConstants.DATABASE_URI)
engine = create_engine(sc.DATABASE_URI)
db_session = sessionmaker(bind=engine)


# def before_request():
#     """Connect to the database before each request."""
#     g.db = db_session()
#     # g.db.connect()
#     # g.user = current_user
#
#
# def after_request(response):
#     """Close the database connection after each request."""
#     g.db.close()
#     return response
