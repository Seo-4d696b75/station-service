"""テスト用の駅・路線データ

本番は station_database リポジトリから取得するデータを、検証しやすい少数のレコードで置き換える
"""

DATA_VERSION = 20240101

# 駅メモ実装の駅
STATION_TOKYO = {
    "code": 1130101,
    "id": 1,
    "name": "東京",
    "original_name": "東京",
    "name_kana": "とうきょう",
    "lat": 35.681391,
    "lng": 139.766103,
    "prefecture": 13,
    "postal_code": "100-0005",
    "address": "東京都千代田区丸の内一丁目",
    "closed": False,
    "open_date": "1914-12-20",
    "closed_date": None,
    "extra": False,
    "attr": "heat",
}
STATION_SHINJUKU = {
    "code": 1130208,
    "id": 2,
    "name": "新宿",
    "original_name": "新宿",
    "name_kana": "しんじゅく",
    "lat": 35.690921,
    "lng": 139.700258,
    "prefecture": 13,
    "postal_code": "160-0022",
    "address": "東京都新宿区新宿三丁目",
    "closed": False,
    "open_date": "1885-03-01",
    "closed_date": None,
    "extra": False,
    "attr": "cool",
}
# 駅名重複防止の接尾語あり
STATION_FUCHU_TOKYO = {
    "code": 1130330,
    "id": 3,
    "name": "府中(東京)",
    "original_name": "府中",
    "name_kana": "ふちゅう",
    "lat": 35.672245,
    "lng": 139.477142,
    "prefecture": 13,
    "postal_code": "183-0023",
    "address": "東京都府中市宮町",
    "closed": False,
    "open_date": "1916-10-31",
    "closed_date": None,
    "extra": False,
    "attr": "eco",
}
STATION_FUCHU_HIROSHIMA = {
    "code": 1150310,
    "id": 4,
    "name": "府中(広島)",
    "original_name": "府中",
    "name_kana": "ふちゅう",
    "lat": 34.568319,
    "lng": 133.236479,
    "prefecture": 34,
    "postal_code": "726-0005",
    "address": "広島県府中市府中町",
    "closed": False,
    "open_date": "1914-07-21",
    "closed_date": None,
    "extra": False,
    "attr": "unknown",
}
# 独自追加の廃駅
STATION_OLD_SHINBASHI = {
    "code": 9930001,
    "id": 5,
    "name": "旧新橋",
    "original_name": "旧新橋",
    "name_kana": "きゅうしんばし",
    "lat": 35.664,
    "lng": 139.762,
    "prefecture": 13,
    "postal_code": "105-0021",
    "address": "東京都港区東新橋一丁目",
    "closed": True,
    "open_date": "1872-10-14",
    "closed_date": "1914-12-20",
    "extra": True,
    "attr": None,
}

MAIN_STATIONS = [
    STATION_TOKYO,
    STATION_SHINJUKU,
    STATION_FUCHU_TOKYO,
    STATION_FUCHU_HIROSHIMA,
]
EXTRA_ONLY_STATIONS = [STATION_OLD_SHINBASHI]
ALL_STATIONS = MAIN_STATIONS + EXTRA_ONLY_STATIONS

LINE_YAMANOTE = {
    "code": 11302,
    "id": 1,
    "name": "山手線",
    "name_kana": "やまのてせん",
    "station_size": 30,
    "company_code": 2,
    "color": "#80C241",
    "symbol": "JY",
    "closed": False,
    "closed_date": None,
    "extra": False,
}
LINE_CHUO = {
    "code": 11312,
    "id": 2,
    "name": "中央線(快速)",
    "name_kana": "ちゅうおうせん",
    "station_size": 24,
    "company_code": 2,
    "color": "#F15A22",
    "symbol": "JC",
    "closed": False,
    "closed_date": None,
    "extra": False,
}
# 独自追加の廃線
LINE_TODEN = {
    "code": 99301,
    "id": 3,
    "name": "東京都電",
    "name_kana": "とうきょうとでん",
    "station_size": 2,
    "company_code": None,
    "color": None,
    "symbol": None,
    "closed": True,
    "closed_date": "1972-11-12",
    "extra": True,
}

ALL_LINES = [LINE_YAMANOTE, LINE_CHUO, LINE_TODEN]


def build_kd_tree(stations):
    """station_database の tree.json と同じ形式のkd-treeを構築する

    深さが偶数のノードは経度、奇数のノードは緯度で分割する（src/tree.py の探索と対応）
    """
    node_list = []

    def build(points, depth):
        if len(points) == 0:
            return None
        key = "lng" if depth % 2 == 0 else "lat"
        points = sorted(points, key=lambda s: s[key])
        mid = len(points) // 2
        node = {
            "code": points[mid]["code"],
            "lat": points[mid]["lat"],
            "lng": points[mid]["lng"],
        }
        node_list.append(node)
        left = build(points[:mid], depth + 1)
        right = build(points[mid + 1:], depth + 1)
        if left is not None:
            node["left"] = left
        if right is not None:
            node["right"] = right
        return node["code"]

    root = build(stations, 0)
    return {"root": root, "node_list": node_list}


# src/data.py が取得するURLの末尾 → レスポンス
RESPONSES = {
    "latest_info.extra.json": {"version": DATA_VERSION},
    "/extra/line.json": ALL_LINES,
    "/extra/station.json": ALL_STATIONS,
    "/main/tree.json": build_kd_tree(MAIN_STATIONS),
    "/extra/tree.json": build_kd_tree(ALL_STATIONS),
}
