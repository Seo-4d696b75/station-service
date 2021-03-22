import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Float, Date, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import BOOLEAN as Boolean, NUMERIC as Numeric
from sqlalchemy.orm import sessionmaker, scoped_session
import json
from sqlalchemy.ext.declarative import declarative_base
import os
import urllib

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


class Station(Base):
    __tablename__ = "station_list"
    code = Column(Integer, primary_key=True, index=True)
    id = Column(String(16), unique=True, index=True)
    name = Column(String(64), nullable=False)
    original_name = Column(String(64), nullable=False)
    name_kana = Column(String(64), nullable=False)
    lat = Column(Numeric, nullable=False)
    lng = Column(Numeric, nullable=False)
    prefecture = Column(Integer, nullable=False)
    postal_code = Column(String(16))
    address = Column(String(128))
    closed = Column(Boolean, nullable=False)
    open_date = Column(Date)
    closed_date = Column(Date)
    impl = Column(Boolean, nullable=False)
    attr = Column(String(16))


class Line(Base):
    __tablename__ = "line_list"
    code = Column(Integer, primary_key=True, index=True)
    id = Column(String(16), unique=True, index=True)
    name = Column(String(64), nullable=False)
    name_kana = Column(String(64), nullable=False)
    name_formal = Column(String(64))
    station_size = Column(Integer, nullable=False)
    company_code = Column(Integer)
    color = Column(String(16))
    symbol = Column(String(16))
    closed = Column(Boolean, nullable=False)
    closed_date = Column(Date)
    impl = Column(Boolean, nullable=False)


class DataInfo(Base):
    __tablename__ = 'data_info'
    id = Column(Integer, primary_key=True, index=True)
    data_version = Column(BigInteger, nullable=False)
    updated_at = Column(DateTime, nullable=False)
