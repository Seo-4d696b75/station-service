from fixture_data import DATA_VERSION, STATION_TOKYO


def test_root_returns_html(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/html")
    assert 'href="/docs"' in res.text


def test_info(client):
    res = client.get("/info")
    assert res.status_code == 200
    assert res.json() == {"data_version": DATA_VERSION}


def test_docs_available(client):
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def test_unknown_path_returns_404(client):
    res = client.get("/unknown")
    assert res.status_code == 404
    assert res.json() == {
        "detail": "Not Found. See API docs for more details at /docs"
    }


def test_old_api_path_redirects_with_query(client):
    code = STATION_TOKYO["code"]
    res = client.get(f"/api/station?code={code}", follow_redirects=False)
    assert res.status_code == 301
    assert res.headers["location"] == f"/station?code={code}"


def test_old_api_path_redirect_is_followable(client):
    res = client.get(f"/api/station?code={STATION_TOKYO['code']}")
    assert res.status_code == 200
    assert res.json() == STATION_TOKYO


def test_old_api_path_redirect_stays_on_same_origin(client):
    # 空のパスセグメントを詰めてもプロトコル相対URL "//host" にならない
    res = client.get("/api//example.com", follow_redirects=False)
    assert res.status_code == 301
    assert not res.headers["location"].startswith("//")
