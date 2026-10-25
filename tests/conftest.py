import json
import os
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from fixture_data import RESPONSES

# api_setting.json などを相対パスで読み込むため
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)


class FakeResponse:
    def __init__(self, body: str):
        self.body = body.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def getcode(self):
        return 200

    def read(self):
        return self.body


def fake_urlopen(url):
    for suffix, obj in RESPONSES.items():
        if url.endswith(suffix):
            return FakeResponse(json.dumps(obj, ensure_ascii=False))
    raise AssertionError(f"unexpected url:{url}")


@pytest.fixture(scope="session")
def client():
    # py.data はimport時にデータを取得するので、その間だけネットワークアクセスを差し替える
    with mock.patch("urllib.request.urlopen", fake_urlopen):
        from main import app
    return TestClient(app)
