from typing import List

import regex
from fastapi import APIRouter, Query

from py import models
from py.data import data

# Base Error


class APIException(Exception):
    def __init__(self, code, msg, detail='', headers={}):
        self.code = code
        self.msg = msg
        self.detail = detail
        self.headers = headers


router = APIRouter()

pattern_kana = regex.compile(r'[\p{Hiragana}\p{P}ー・]+')

@router.get("/api")
async def api_root():
    return {"msg": "this is api endpoint", "detail": "/api/docs"}


@router.get("/api/info", response_model=models.DataInfoOut, tags=['info'])
async def get_info():
    return data.version_info


@router.get("/api/station", response_model=models.StationOut, tags=['get', 'station'])
async def get_station(
        code: int = Query(0, description='駅コードの値'),
        id: str = Query(None, description='駅IDの値', min_length=6, max_length=6)
):
    if code == 0 and id is None:
        raise APIException(
            400,
            'lack of query',
            'either code or id must be specified.'
        )
    if id is not None:
        station = data.station_map.get(id, None)
        if station is None:
            raise APIException(
                404,
                'station not found',
                f"station identified by id:{id} not found"
            )
    else:
        station = data.station_map.get(code, None)
        if station is None:
            raise APIException(
                404,
                'station not found',
                f"station identified by code:{code} not found"
            )
    return station.dump()


@router.get("/api/line", response_model=models.LineOut, tags=['get', 'line'])
async def get_line(
        code: int = Query(0, description='路線コードの値'),
        id: str = Query(None, description='駅IDの値', min_length=6, max_length=6)
):
    if code == 0 and id is None:
        raise APIException(
            400,
            'lack of query',
            'either code or id must be specified.'
        )
    if id is not None:
        line = data.line_map.get(id, None)
        if line is None:
            raise APIException(
                404,
                'line not found',
                f"line identified by id:{id} not found"
            )
    else:
        line = data.line_map.get(code, None)
        if line is None:
            raise APIException(
                404,
                'line not found',
                f"line identified by code:{code} not found"
            )
    return line.dump()


@router.get("/api/station/search", response_model=List[models.BaseStationOut], tags=['station', 'name_search'])
async def search_for_station(
        name: str = Query(..., description='駅名称または読み仮名の全部・一部分', min_length=1),
        original: bool = Query(
            True, description='true:駅名称を検索するとき、駅名重複防止のための接尾語を無視する. 末尾に頻出する都道府県名や鉄道会社名に検索がヒットして欲しくない場合はtrueを指定する'),
):
    if len(name) == 1 and pattern_kana.fullmatch(name):
        return []
    criteria_name = [
        lambda e: name in e.original_name
        if original else
        lambda e: name in e.name
    ]
    if pattern_kana.fullmatch(name) is not None:
        criteria_name.append(
            lambda e: name in e.name_kana
        )
    stations = [
        s.dump() for s in data.stations
        if any([c(s) for c in criteria_name])
    ]
    return stations


@router.get("/api/line/search", response_model=List[models.BaseLineOut], tags=['line', 'name_search'])
async def search_for_line(
        name: str = Query(..., description='路線名称または読み仮名の全部・一部分', min_length=1),
):
    if len(name) == 1 and pattern_kana.fullmatch(name):
        return []
    criteria = (
        lambda e: name in e.name or name in e.name_kana
    ) if pattern_kana.fullmatch(name) is not None else (
        lambda e: name in e.name
    )
    lines = [l.dump() for l in data.lines if criteria(l)]
    return lines


@router.get("/api/station/nearest", response_model=List[models.NearestSearchOut], tags=['station', 'nearest_search'])
async def nearest_search(
        lat: float = Query(..., description='探索点の緯度', ge=-90, le=90),
        lng: float = Query(..., description='探索点の経度', ge=-180, le=180),
        k: int = Query(1, description='探索する近傍点の数', ge=1, le=10),
        s: bool = Query(False, description='球体を考慮して距離を計算する')
):
    neighbors = data.tree.search_nearest(lat, lng, k, 0, s)
    digit = 1 if s else 6
    list = [
        {
            'dist': round(d['dist'], digit),
            'station': data.station_map[d['code']].dump()
        }
        for d in neighbors
    ]
    return list
