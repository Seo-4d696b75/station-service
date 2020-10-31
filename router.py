from fastapi import APIRouter, Depends, Query
from db import Station, Session
from sqlalchemy import or_

# Base Error
class APIException(Exception):
    def __init__(self, code, msg, detail='', headers={}):
        self.code = code
        self.msg = msg
        self.detail = detail
        self.headers = headers

router = APIRouter()

@router.get("/api/")
async def api_root():
  	return {"msg":"this is api endpoint"}

@router.get("/api/station")
async def get_station(
	code: int = Query(..., description='駅コードの値')
):
	data = Session().query(Station).filter(Station.code == code ).first()
	if data is None:
		raise APIException(404, 'station not found', f"station identified by code:{code} not found")
	return data

@router.get("/api/station/search")
async def search_for_station(
	name: str = Query(..., description='駅名称または読み仮名の全部・一部分', min_length=1)
):
	data = Session().query(Station)\
		.filter(or_(Station.name.like(f"%{name}%"), Station.name_kana.like(f"%{name}%")))\
		.all()
	return data