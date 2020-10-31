import databases
import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Float, Date
from sqlalchemy.dialects.postgresql import BOOLEAN as Boolean
import json
from starlette.requests import Request

# init db client
db = json.load(open('./db_setting.json','r',encoding='utf-8'))
DATABASE_URL = f"postgresql://{db['User']}:{db['Password']}@{db['Host']}:{db['Port']}/{db['Database']}"

database = databases.Database(DATABASE_URL, min_size=5, max_size=20)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'sslmode':'require'}, echo=False)
metadata = sqlalchemy.MetaData()

Station = sqlalchemy.Table(
    "station_list",
    metadata,
    Column("code", Integer, primary_key=True, index=True),
    Column("id", String(16), unique=True),
    Column("name", String(64), nullable=False),
    Column("name_kana", String(64), nullable=False),
    Column("lat", Float, nullable=False),
    Column("lng", Float, nullable=False),
    Column("prefecture", Integer, nullable=False),
    Column("postal_code", String(16)),
    Column("address", String(128)),
    Column("closed", Boolean, nullable=False),
    Column("open_date", Date),
    Column("closed_date", Date),
    Column("impl", Boolean, nullable=False),
    Column("attr", String(16))
)

metadata.create_all(bind=engine)

# middlewareでrequestに格納したconnection(Databaseオブジェクト)を返します。
def get_connection(request: Request):
    return request.state.connection
