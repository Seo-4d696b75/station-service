import pytest

from fixture_data import (LINE_CHUO, LINE_TODEN, LINE_YAMANOTE,
                          STATION_FUCHU_HIROSHIMA, STATION_FUCHU_TOKYO,
                          STATION_OLD_SHINBASHI, STATION_TOKYO)

BASE_STATION_KEYS = {
    "code", "id", "name", "original_name", "name_kana", "prefecture", "extra",
}
BASE_LINE_KEYS = {"code", "id", "name", "name_kana", "extra"}


def codes(res):
    return {e["code"] for e in res.json()}


class TestStationSearch:

    def search(self, client, **params):
        res = client.get("/station/search", params=params)
        assert res.status_code == 200
        return res

    def test_response_format(self, client):
        res = self.search(client, name="東京")
        assert res.json() == [
            {k: v for k, v in STATION_TOKYO.items() if k in BASE_STATION_KEYS}
        ]

    def test_original_true_ignores_suffix(self, client):
        # 接尾語 "(東京)" にはヒットしない
        res = self.search(client, name="東京", original=True)
        assert codes(res) == {STATION_TOKYO["code"]}

    def test_original_is_true_by_default(self, client):
        res = self.search(client, name="東京")
        assert codes(res) == {STATION_TOKYO["code"]}

    def test_original_false_matches_suffix(self, client):
        res = self.search(client, name="東京", original=False)
        assert codes(res) == {STATION_TOKYO["code"], STATION_FUCHU_TOKYO["code"]}

    def test_original_false_filters_by_name(self, client):
        # https://github.com/Seo-4d696b75/station-service/issues/9
        res = self.search(client, name="該当なし", original=False)
        assert res.json() == []

    def test_original_false_with_kana(self, client):
        res = self.search(client, name="ふちゅう", original=False)
        assert codes(res) == {
            STATION_FUCHU_TOKYO["code"], STATION_FUCHU_HIROSHIMA["code"],
        }

    @pytest.mark.parametrize("original", [True, False])
    def test_same_original_name(self, client, original):
        res = self.search(client, name="府中", original=original)
        assert codes(res) == {
            STATION_FUCHU_TOKYO["code"], STATION_FUCHU_HIROSHIMA["code"],
        }

    def test_partial_match(self, client):
        res = self.search(client, name="京")
        assert codes(res) == {STATION_TOKYO["code"]}

    def test_kana(self, client):
        res = self.search(client, name="とうきょう")
        assert codes(res) == {STATION_TOKYO["code"]}

    def test_single_kana_returns_empty(self, client):
        res = self.search(client, name="ふ")
        assert res.json() == []

    def test_single_kanji(self, client):
        res = self.search(client, name="府")
        assert codes(res) == {
            STATION_FUCHU_TOKYO["code"], STATION_FUCHU_HIROSHIMA["code"],
        }

    def test_not_found(self, client):
        res = self.search(client, name="大阪")
        assert res.json() == []

    def test_extra_excluded_by_default(self, client):
        assert self.search(client, name="新橋").json() == []
        assert self.search(client, name="しんばし").json() == []

    @pytest.mark.parametrize("original", [True, False])
    @pytest.mark.parametrize("name", ["新橋", "しんばし"])
    def test_extra_included(self, client, name, original):
        res = self.search(client, name=name, extra=True, original=original)
        assert codes(res) == {STATION_OLD_SHINBASHI["code"]}

    def test_original_false_excludes_extra(self, client):
        res = self.search(client, name="新橋", original=False, extra=False)
        assert res.json() == []

    @pytest.mark.parametrize("params", [{}, {"name": ""}])
    def test_invalid_query(self, client, params):
        res = client.get("/station/search", params=params)
        assert res.status_code == 400
        assert res.json()["msg"] == "validation of request query failed."


class TestLineSearch:

    def search(self, client, **params):
        res = client.get("/line/search", params=params)
        assert res.status_code == 200
        return res

    def test_response_format(self, client):
        res = self.search(client, name="山手")
        assert res.json() == [
            {k: v for k, v in LINE_YAMANOTE.items() if k in BASE_LINE_KEYS}
        ]

    def test_partial_match(self, client):
        res = self.search(client, name="線")
        assert codes(res) == {LINE_YAMANOTE["code"], LINE_CHUO["code"]}

    def test_kana(self, client):
        res = self.search(client, name="やまのて")
        assert codes(res) == {LINE_YAMANOTE["code"]}

    def test_single_kana_returns_empty(self, client):
        res = self.search(client, name="や")
        assert res.json() == []

    def test_not_found(self, client):
        res = self.search(client, name="該当なし")
        assert res.json() == []

    def test_extra_excluded_by_default(self, client):
        assert self.search(client, name="都電").json() == []
        assert self.search(client, name="とでん").json() == []

    @pytest.mark.parametrize("name", ["都電", "とでん"])
    def test_extra_included(self, client, name):
        res = self.search(client, name=name, extra=True)
        assert codes(res) == {LINE_TODEN["code"]}

    @pytest.mark.parametrize("params", [{}, {"name": ""}])
    def test_invalid_query(self, client, params):
        res = client.get("/line/search", params=params)
        assert res.status_code == 400
        assert res.json()["msg"] == "validation of request query failed."
