import os
import urllib

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import BigInteger, DateTime, Integer


url = os.environ.get("DATABASE_URL", None)
if url is None:
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_DATABASE = os.environ["DB_DATABASE"]
    url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
else:
    u = urllib.parse.urlparse(url)
    # scheme 'postgres' may not be accepted
    url = urllib.parse.urlunparse(
        ('postgresql', u.netloc, u.path, u.params, u.query, u.fragment))

DATABASE_URL = url
print(f"db url: {DATABASE_URL}")

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={'sslmode': 'require'}, echo=False)
Session = scoped_session(sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True
))

Base = declarative_base()

class DataInfo(Base):
    __tablename__ = 'data_info'
    id = Column(Integer, primary_key=True, index=True)
    data_version = Column(BigInteger, nullable=False)
    updated_at = Column(DateTime, nullable=False)
