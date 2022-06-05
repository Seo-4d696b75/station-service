from datetime import datetime
from typing import Union
import json
import urllib.request

import sqlalchemy
from py.db import DataInfo, Session
from py.schema import DataInfoSchema
from py.tree import KdTree

logo_text = open('./img/logo.txt', 'r', encoding='utf-8').read()


def get_url(url):
    try:
        with urllib.request.urlopen(url) as res:
            if res.getcode() == 200:
                return res.read().decode("utf-8").replace('\r', '')
            else:
                raise RuntimeError(
                    f"fail to get response. url:{url} status:{res.getcode()}")
    except urllib.error.URLError as e:
        raise RuntimeError(e)


data_env = json.load(open('./env.json', 'r', encoding='utf-8'))
URL_DATA_BASE = data_env["data_base_url"]
URL_DATA_VERSION = data_env["data_version_url"]


class Station:
    def __init__(self, obj: dict) -> None:
        self.code = int(obj["code"])
        self.id = str(obj["id"])
        self.name = str(obj["name"])
        self.original_name = str(obj["original_name"])
        self.name_kana = str(obj["name_kana"])
        self.lat = float(obj["lat"])
        self.lng = float(obj["lng"])
        self.prefecture = int(obj["prefecture"])
        self.postal_code = str(obj["postal_code"])
        self.address = str(obj["address"])
        self.closed = bool(obj["closed"])
        self.open_date: Union[str, None] = obj.get("open_date", None)
        self.closed_date: Union[str, None] = obj.get("closed_date", None)
        self.impl = bool(obj["impl"])
        self.attr: Union[str, None] = obj.get("attr", None)

    def dump(self):
        return {
            "code": self.code,
            "id": self.id,
            "name": self.name,
            "original_name": self.original_name,
            "name_kana": self.name_kana,
            "lat": self.lat,
            "lng": self.lng,
            "prefecture": self.prefecture,
            "postal_code": self.postal_code,
            "address": self.address,
            "closed": self.closed,
            "open_date": self.open_date,
            "closed_date": self.closed_date,
            "impl": self.impl,
            "attr": self.attr
        }


class Line:
    def __init__(self, obj: dict) -> None:
        self.code = int(obj["code"])
        self.id = str(obj["id"])
        self.name = str(obj["name"])
        self.name_kana = str(obj["name_kana"])
        self.station_size = int(obj["station_size"])
        self.company_code: Union[int, None] = obj.get("company_code", None)
        self.color: Union[str, None] = obj.get("color", None)
        self.symbol: Union[str, None] = obj.get("symbol", None)
        self.closed = bool(obj["closed"])
        self.closed_date: Union[str, None] = obj.get("closed_date", None)
        self.impl = bool(obj["impl"])

    def dump(self):
        return {
            "code": self.code,
            "id": self.id,
            "name": self.name,
            "name_kana": self.name_kana,
            "station_size": self.station_size,
            "company_code": self.company_code,
            "color": self.color,
            "symbol": self.symbol,
            "closed": self.closed,
            "closed_date": self.closed_date,
            "impl": self.impl,
        }


class InMemoryDB:
    station_map: "dict[Union[int, str], Station]" = {}
    stations: "list[Station]" = []
    line_map: "dict[Union[int, str], Line]" = {}
    lines: "list[Line]" = []
    tree: KdTree

    def __init__(self, version_info) -> None:
        self.version_info: dict = version_info
        # load line list
        lines = json.loads(
            get_url(f"{URL_DATA_BASE}/line.json")
        )
        for obj in lines:
            line = Line(obj)
            self.lines.append(line)
            self.line_map[line.code] = line
            self.line_map[line.id] = line
        # load station list
        stations = json.loads(
            get_url(f"{URL_DATA_BASE}/station.json")
        )
        for obj in stations:
            station = Station(obj)
            self.stations.append(station)
            self.station_map[station.code] = station
            self.station_map[station.id] = station
        # load kd-tree
        nodes = json.loads(
            get_url(f"{URL_DATA_BASE}/tree.json")
        )
        self.tree = KdTree(nodes)


session = Session()
id = session.query(sqlalchemy.func.max(DataInfo.id)).first()[0]
current = session.query(DataInfo).filter(
    DataInfo.id == id).first() if id is not None else None
latest = json.loads(get_url(URL_DATA_VERSION))
if current is None or current.data_version < latest['version']:
    print(f"new data found. info:{latest}")
    info = DataInfo()
    info.data_version = latest["version"]
    info.updated_at = datetime.now()
    session.add(info)
    session.commit()
    current = info
else:
    print(f"data is up-to-dated. version:{latest['version']}")


data_info_schema = DataInfoSchema()
info = data_info_schema.dump(current)

data = InMemoryDB(info)
