from fastapi import APIRouter, Depends, Query
from db import Station, Line, Session
from sqlalchemy import or_
import re

# Base Error
class APIException(Exception):
    def __init__(self, code, msg, detail='', headers={}):
        self.code = code
        self.msg = msg
        self.detail = detail
        self.headers = headers

router = APIRouter()

pattern_kana = re.compile('[\u3041-\u309F]+')

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

@router.get("/api/line")
async def get_line(
	code: int = Query(..., description='路線コードの値')
):
	data = Session().query(Line).filter(Line.code == code ).first()
	if data is None:
		raise APIException(404, 'line not found', f"line identified by code:{code} not found")
	return data


@router.get("/api/station/search")
async def search_for_station(
	name: str = Query(..., description='駅名称または読み仮名の全部・一部分', min_length=1),
	details: bool = Query(False, description='false:駅名（かな含む）・駅コード。駅id・都道府県コードのみ取得, true:全属性取得')
):
	if len(name) == 1 and pattern_kana.fullmatch(name):
		return []
	criteria = or_(
		Station.name.like(f"%{name}%"), 
		Station.name_kana.like(f"%{name}%")
		) if pattern_kana.fullmatch(name) is not None else Station.name.like(f"%{name}%")
	if details:
		data = Session().query(Station).filter(criteria).all()
	else:
		data = Session().query(Station.code, Station.id, Station.name, Station.name_kana, Station.prefecture)\
			.filter(criteria).all()
		data = list(map(lambda d: {
			'code': d[0],
			'id':d[1],
			'name':d[2],
			'name_kana':d[3],
			'prefecture':d[4]
			}, data))
	return data

@router.get("/api/line/search")
async def search_for_line(
	name: str = Query(..., description='路線名称または読み仮名の全部・一部分', min_length=1),
	details: bool = Query(False, description='false:路線（かな含む）・路線コード。路線id, true:全属性取得')
):
	if len(name) == 1 and pattern_kana.fullmatch(name):
		return []
	criteria = or_(
		Line.name.like(f"%{name}%"), 
		Line.name_kana.like(f"%{name}%")
		) if pattern_kana.fullmatch(name) is not None else Line.name.like(f"%{name}%")
	if details:
		data = Session().query(Line).filter(criteria).all()
	else:
		data = Session().query(Line.code, Line.id, Line.name, Line.name_kana)\
			.filter(criteria).all()
		data = list(map(lambda d: {
			'code': d[0],
			'id':d[1],
			'name':d[2],
			'name_kana':d[3]
			}, data))
	return data