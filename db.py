import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Float, Date
from sqlalchemy.dialects.postgresql import BOOLEAN as Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
import json
from sqlalchemy.ext.declarative import declarative_base
import os

Base=declarative_base()

# init db client
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_DATABASE = os.environ["DB_DATABASE"]
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"


engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'sslmode':'require'}, echo=False)
Session = scoped_session(sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True
))

class Station(Base):
    __tablename__ = "station_list"
    code = Column(Integer, primary_key=True, index=True)
    id = Column(String(16), unique=True)
    name = Column(String(64), nullable=False)
    name_kana = Column(String(64), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    prefecture = Column(Integer, nullable=False)
    postal_code = Column(String(16))
    address = Column(String(128))
    closed = Column(Boolean, nullable=False)
    open_date = Column(Date)
    closed_date = Column(Date)
    impl = Column(Boolean, nullable=False)
    attr = Column(String(16))
