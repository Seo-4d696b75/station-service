import json
import urllib.request
from py.db import Station, Line, DataInfo, engine, Session
import sqlalchemy
import datetime
import os
import shutil

def parse_csv_line(i, d, cols, index):
    if d == '':
        return None
    cells = d.split(",")
    if len(cells) != cols:
        raise ValueError(f"unexpected csv lines: {d}")
    if i == 0 and cells[index] != "impl":
        raise ValueError(f"index:{index} is not target value: {d}")
    if i == 0 or cells[index] == "1":
        return d
    else:
        return None


def parse_csv(data, cols, index):
    return "\n".join(
        filter(
            lambda d: d is not None,
            map(
                lambda t: parse_csv_line(t[0], t[1], cols, index),
                enumerate(data.splitlines())
            )
        )
    )

STATION_FILEDS = ('code', 'id', 'name', 'original_name', 'name_kana', 'lat', 'lng', 'prefecture', 'postal_code', 'address', 'closed', 'open_date', 'closed_date', 'impl', 'attr')
LINE_FILEDS = ('code', 'id', 'name', 'name_kana', 'name_formal', 'station_size', 'company_code', 'color', 'symbol', 'closed', 'closed_date', 'impl')

def parse_station(s):
    s['original_name'] = s.get('original_name', s['name'])
    s['closed'] = s.get('closed', False)
    s['impl'] = True
    params = {k: s.get(k, None) for k in STATION_FILEDS}
    return params #Station(**params)

def parse_line(l):
    l['closed'] = l.get('closed', False)
    l['impl'] = True
    params = {k: l.get(k, None) for k in LINE_FILEDS}
    return params #Line(**params)

def get_url(url):
    try:
        with urllib.request.urlopen(url) as res:
            if res.getcode() == 200:
                return res.read().decode("utf-8").replace('\r', '')
            else:
                raise RuntimeError(
                    f"fail to get resourcees. url:{url} status:{res.getcode()}")
    except urllib.error.URLError as e:
        raise RuntimeError(e)

def get_data(info):
    url="https://raw.githubusercontent.com/Seo-4d696b75/station_database/master/src/station.csv"
    data = get_url(url)
    with open("data/station.csv", mode="w", encoding="utf-8") as f:
        f.write(parse_csv(data, 15, 13))
    url="https://raw.githubusercontent.com/Seo-4d696b75/station_database/master/src/line.csv"
    data= get_url(url)
    with open("data/line.csv", mode="w", encoding="utf-8") as f:
        f.write(parse_csv(data, 12, 11))

def check_data():
    id=Session().query(sqlalchemy.func.max(DataInfo.id)).first()[0]
    current=Session().query(DataInfo).filter(DataInfo.id == id).first() if id is not None else None
    url="https://raw.githubusercontent.com/Seo-4d696b75/station_database/master/latest_info.json"
    latest=json.loads(get_url(url))
    if current is None or current.data_version < latest['version']:
        print(f"new data found. info:{latest}")
        get_data(latest)
