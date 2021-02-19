from fastapi import APIRouter, Depends, Query
from py.db import Station, Line, Session, DataInfo
from py import schema, models
from sqlalchemy import or_, func
import re
import json
from py.tree import KdTree
from typing import Optional, List, Union
from py.data import get_url

# Base Error


class APIException(Exception):
    def __init__(self, code, msg, detail='', headers={}):
        self.code = code
        self.msg = msg
        self.detail = detail
        self.headers = headers


router = APIRouter()

pattern_kana = re.compile('[\u3041-\u309F]+')


url="https://raw.githubusercontent.com/Seo-4d696b75/station_database/master/out/tree.json"
data=get_url(url)
tree = KdTree(json.loads(data))

station_schema = schema.StationSchema()
short_station_schema = schema.ShortStationSchema()
line_schema = schema.LineSchema()
short_line_schema = schema.ShortLineSchema()
data_info_schema = schema.DataInfoSchema()

@router.get("/api")
async def api_root():
    return {"msg": "this is api endpoint", "detail":"/api/docs"}

@router.get("/api/info", response_model=models.DataInfoOut, tags=['info'])
async def get_info():
	id = Session().query(func.max(DataInfo.id)).first()[0]
	if id is None:
		raise APIException(404, "data not initialized yet")
	data = Session().query(DataInfo).filter(DataInfo.id == id).first()
	return data_info_schema.dump(data)

@router.get("/api/station", response_model=models.StationOut, tags=['get', 'station'])
async def get_station(
        code: int = Query(0, description='駅コードの値'),
        id: str = Query(None, description='駅IDの値', min_length=6, max_length=6)
):
    if code == 0 and id is None:
        raise APIException(400, 'lack of query',
                           'either code or id must be spesified.')
    if id is not None:
        data = Session().query(Station).filter(Station.id == id).first()
        if data is None:
            raise APIException(404, 'station not found',
                               f"station identified by id:{id} not found")
    else:
        data = Session().query(Station).filter(Station.code == code).first()
        if data is None:
            raise APIException(404, 'station not found',
                               f"station identified by code:{code} not found")
    return station_schema.dump(data)


@router.get("/api/line", response_model=models.LineOut, tags=['get', 'line'])
async def get_line(
        code: int = Query(0, description='路線コードの値'),
        id: str = Query(None, description='駅IDの値', min_length=6, max_length=6)
):
    if code == 0 and id is None:
        raise APIException(400, 'lack of query',
                           'either code or id must be spesified.')
    if id is not None:
        data = Session().query(Line).filter(Line.id == id).first()
        if data is None:
            raise APIException(404, 'line not found',
                               f"line identified by id:{id} not found")
    else:
        data = Session().query(Line).filter(Line.code == code).first()
        if data is None:
            raise APIException(404, 'line not found',
                               f"line identified by code:{code} not found")
    return line_schema.dump(data)


@router.get("/api/station/search", response_model=List[Union[models.StationOut, models.BaseStationOut]], tags=['station', 'name_search'])
async def search_for_station(
        name: str = Query(..., description='駅名称または読み仮名の全部・一部分', min_length=1),
        original: bool = Query(
            True, description='true:駅名称を検索するとき、駅名重複防止のための接尾語を無視する. 末尾に頻出する都道府県名や鉄道会社名に検索がヒットして欲しくない場合はtrueを指定する'),
        details: bool = Query(
            False, description='false:駅名（かな含む）・駅コード・駅id・都道府県コードのみ取得, true:全属性取得')
):
    if len(name) == 1 and pattern_kana.fullmatch(name):
        return []
    criteria_name = Station.original_name.like(
        f"%{name}%") if original else Station.name.like(f"%{name}%")
    criteria = or_(
        criteria_name,
        Station.name_kana.like(f"%{name}%")
    ) if pattern_kana.fullmatch(name) is not None else criteria_name
    if details:
        data = Session().query(Station).filter(criteria).all()
        return list(map(lambda d: station_schema.dump(d), data))
    else:
        data = Session().query(Station.code, Station.id, Station.name, Station.original_name, Station.name_kana, Station.prefecture)\
            .filter(criteria).all()
        return list(map(lambda d: short_station_schema.dump(d), data))


@router.get("/api/line/search", response_model=List[Union[models.BaseLineOut, models.LineOut]], tags=['line', 'name_search'])
async def search_for_line(
        name: str = Query(..., description='路線名称または読み仮名の全部・一部分', min_length=1),
        details: bool = Query(
            False, description='false:路線（かな含む）・路線コード。路線id, true:全属性取得')
):
    if len(name) == 1 and pattern_kana.fullmatch(name):
        return []
    criteria = or_(
        Line.name.like(f"%{name}%"),
        Line.name_kana.like(f"%{name}%")
    ) if pattern_kana.fullmatch(name) is not None else Line.name.like(f"%{name}%")
    if details:
        data = Session().query(Line).filter(criteria).all()
        return list(map(lambda d: line_schema.dump(d), data))
    else:
        data = Session().query(Line.code, Line.id, Line.name, Line.name_kana)\
            .filter(criteria).all()
        return list(map(lambda d: short_line_schema.dump(d), data))


@router.get("/api/station/nearest", response_model=List[models.NearestSearchOut], tags=['station', 'nearest_search'])
async def nearest_search(
        lat: float = Query(..., description='探索点の緯度', ge=-90, le=90),
        lng: float = Query(..., description='探索点の経度', ge=-180, le=180),
        k: int = Query(1, description='探索する近傍点の数', ge=1, le=10),
        s: bool = Query(False, description='球体を考慮して距離を計算する')
):
    neighbors = tree.search_nearest(lat, lng, k, 0, s)
    session = Session()
    digit = 1 if s else 6
    data = list(map(lambda d: {
        'dist': round(d['dist'], digit),
        'station': station_schema.dump(
                    session.query(Station).filter(
                        Station.code == d['code']).first()
                    )
    }, neighbors))
    return data
