import pytest

from fixture_data import (LINE_CHUO, LINE_TODEN, LINE_YAMANOTE,
                          STATION_OLD_SHINBASHI, STATION_SHINJUKU,
                          STATION_TOKYO)


class TestGetStation:

    @pytest.mark.parametrize("station", [STATION_TOKYO, STATION_OLD_SHINBASHI])
    def test_by_code(self, client, station):
        res = client.get("/station", params={"code": station["code"]})
        assert res.status_code == 200
        assert res.json() == station

    @pytest.mark.parametrize("station", [STATION_TOKYO, STATION_OLD_SHINBASHI])
    def test_by_id(self, client, station):
        res = client.get("/station", params={"id": station["id"]})
        assert res.status_code == 200
        assert res.json() == station

    def test_id_takes_precedence_over_code(self, client):
        res = client.get(
            "/station",
            params={"code": STATION_SHINJUKU["code"], "id": STATION_TOKYO["id"]},
        )
        assert res.status_code == 200
        assert res.json() == STATION_TOKYO

    def test_lack_of_query(self, client):
        res = client.get("/station")
        assert res.status_code == 400
        assert res.json()["msg"] == "lack of query"

    def test_code_not_found(self, client):
        res = client.get("/station", params={"code": 1})
        assert res.status_code == 404
        assert res.json() == {
            "msg": "station not found",
            "detail": "station identified by code:1 not found",
        }

    def test_id_not_found(self, client):
        res = client.get("/station", params={"id": 9999})
        assert res.status_code == 404
        assert res.json() == {
            "msg": "station not found",
            "detail": "station identified by id:9999 not found",
        }

    @pytest.mark.parametrize("params", [{"code": "abc"}, {"id": "1.5"}])
    def test_invalid_query(self, client, params):
        res = client.get("/station", params=params)
        assert res.status_code == 400
        assert res.json()["msg"] == "validation of request query failed."


class TestGetLine:

    @pytest.mark.parametrize("line", [LINE_YAMANOTE, LINE_TODEN])
    def test_by_code(self, client, line):
        res = client.get("/line", params={"code": line["code"]})
        assert res.status_code == 200
        assert res.json() == line

    @pytest.mark.parametrize("line", [LINE_YAMANOTE, LINE_TODEN])
    def test_by_id(self, client, line):
        res = client.get("/line", params={"id": line["id"]})
        assert res.status_code == 200
        assert res.json() == line

    def test_id_takes_precedence_over_code(self, client):
        res = client.get(
            "/line",
            params={"code": LINE_CHUO["code"], "id": LINE_YAMANOTE["id"]},
        )
        assert res.status_code == 200
        assert res.json() == LINE_YAMANOTE

    def test_lack_of_query(self, client):
        res = client.get("/line")
        assert res.status_code == 400
        assert res.json()["msg"] == "lack of query"

    def test_code_not_found(self, client):
        res = client.get("/line", params={"code": 1})
        assert res.status_code == 404
        assert res.json() == {
            "msg": "line not found",
            "detail": "line identified by code:1 not found",
        }

    def test_id_not_found(self, client):
        res = client.get("/line", params={"id": 9999})
        assert res.status_code == 404
        assert res.json() == {
            "msg": "line not found",
            "detail": "line identified by id:9999 not found",
        }

    @pytest.mark.parametrize("params", [{"code": "abc"}, {"id": "1.5"}])
    def test_invalid_query(self, client, params):
        res = client.get("/line", params=params)
        assert res.status_code == 400
        assert res.json()["msg"] == "validation of request query failed."
