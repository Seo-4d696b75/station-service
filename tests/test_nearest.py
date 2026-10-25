import math

import pytest

from fixture_data import (ALL_STATIONS, MAIN_STATIONS, STATION_OLD_SHINBASHI,
                          STATION_TOKYO)

SPHERE_RADIUS = 6371009.0

# 東京駅の近く
POS_NEAR_TOKYO = {"lat": 35.68, "lng": 139.77}


def euclid(lat, lng, s):
    return math.hypot(lat - s["lat"], lng - s["lng"])


def great_circle(lat, lng, s):
    lat1, lng1 = math.radians(lat), math.radians(lng)
    lat2, lng2 = math.radians(s["lat"]), math.radians(s["lng"])
    a = (math.sin((lat1 - lat2) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lng1 - lng2) / 2) ** 2)
    return SPHERE_RADIUS * 2 * math.asin(math.sqrt(a))


def expected_nearest(stations, lat, lng, k, sphere):
    measure = great_circle if sphere else euclid
    return sorted(stations, key=lambda s: measure(lat, lng, s))[:k]


def search(client, **params):
    res = client.get("/station/nearest", params=params)
    assert res.status_code == 200
    return res.json()


def test_response_format(client):
    result = search(client, **POS_NEAR_TOKYO)
    assert len(result) == 1
    assert result[0]["station"] == STATION_TOKYO
    assert result[0]["dist"] == pytest.approx(
        euclid(POS_NEAR_TOKYO["lat"], POS_NEAR_TOKYO["lng"], STATION_TOKYO),
        abs=1e-6,
    )


@pytest.mark.parametrize("k", [1, 2])
def test_sorted_by_distance(client, k):
    result = search(client, **POS_NEAR_TOKYO, k=k)
    expected = expected_nearest(
        MAIN_STATIONS, POS_NEAR_TOKYO["lat"], POS_NEAR_TOKYO["lng"], k, False)
    assert [r["station"]["code"] for r in result] == [s["code"] for s in expected]
    dists = [r["dist"] for r in result]
    assert dists == sorted(dists)


@pytest.mark.xfail(
    strict=True,
    reason="KdTree.search は探索中のリストがk件未満でも、末尾より遠い点を追加しないためk件に満たない場合がある",
)
def test_returns_k_stations(client):
    result = search(client, **POS_NEAR_TOKYO, k=3)
    expected = expected_nearest(
        MAIN_STATIONS, POS_NEAR_TOKYO["lat"], POS_NEAR_TOKYO["lng"], 3, False)
    assert [r["station"]["code"] for r in result] == [s["code"] for s in expected]


def test_sphere(client):
    result = search(client, **POS_NEAR_TOKYO, s=True)
    assert len(result) == 1
    assert result[0]["station"] == STATION_TOKYO
    # s=true では距離[m]を小数第1位で丸める
    assert result[0]["dist"] == pytest.approx(
        great_circle(POS_NEAR_TOKYO["lat"], POS_NEAR_TOKYO["lng"], STATION_TOKYO),
        abs=0.1,
    )


def test_extra_excluded_by_default(client):
    pos = {"lat": STATION_OLD_SHINBASHI["lat"],
           "lng": STATION_OLD_SHINBASHI["lng"]}
    result = search(client, **pos)
    expected = expected_nearest(MAIN_STATIONS, pos["lat"], pos["lng"], 1, False)
    assert [r["station"]["code"] for r in result] == [expected[0]["code"]]


def test_extra_included(client):
    pos = {"lat": STATION_OLD_SHINBASHI["lat"],
           "lng": STATION_OLD_SHINBASHI["lng"]}
    result = search(client, **pos, extra=True)
    expected = expected_nearest(ALL_STATIONS, pos["lat"], pos["lng"], 1, False)
    assert expected[0] == STATION_OLD_SHINBASHI
    assert result[0]["station"] == STATION_OLD_SHINBASHI
    assert result[0]["dist"] == pytest.approx(0.0, abs=1e-6)


@pytest.mark.parametrize("params", [
    {"lng": 139.77},
    {"lat": 35.68},
    {"lat": "abc", "lng": 139.77},
    {"lat": 90.1, "lng": 139.77},
    {"lat": -90.1, "lng": 139.77},
    {"lat": 35.68, "lng": 180.1},
    {"lat": 35.68, "lng": -180.1},
    {"lat": 35.68, "lng": 139.77, "k": 0},
    {"lat": 35.68, "lng": 139.77, "k": 11},
])
def test_invalid_query(client, params):
    res = client.get("/station/nearest", params=params)
    assert res.status_code == 400
    assert res.json()["msg"] == "validation of request query failed."
