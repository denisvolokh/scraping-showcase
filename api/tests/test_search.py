import falcon
import falcon.testing as testing
import pytest

from api.main import app


@pytest.fixture()
def client():
    return testing.TestClient(app)


def test_search_resource(client):
    result = client.simulate_get("/search", params={"query": "test"})
    assert result.status == falcon.HTTP_200
    assert result.json == {
        "query": "test",
        "results": [
            {
                "app_name": "app1",
                "app_version": "1.0.0",
                "app_description": "app1 desc",
                "no_downloads": 100,
                "app_url": "https://app1.com",
                "app_release_date": "2020-01-01",
            },
        ],
    }
