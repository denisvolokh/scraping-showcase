from unittest.mock import patch

import pytest
from falcon.testing import ASGIConductor

from api.main import app

pytest_plugins = ["pytest_asyncio"]


TEST_APP_NAME = "app1"
TEST_APP_DESCRIPTION = "app1 desc"
TEST_APP_URL = "https://app1.com"


@pytest.fixture
def client():
    return ASGIConductor(app)


@pytest.mark.asyncio
@patch("api.routes.v1.scrape.scrape_target_page")
async def test_successgul_sync_scrape(mock_scrape, client):
    mocked_result = {
        "app_name": TEST_APP_NAME,
        "app_description": TEST_APP_DESCRIPTION,
        "app_url": TEST_APP_URL,
    }
    mock_scrape.return_value = mocked_result

    response = await client.simulate_get(
        "/v1/scrape", params={"target_url": TEST_APP_URL}
    )

    assert response.status_code == 200

    result = response.json["result"]
    assert result["app_name"] == TEST_APP_NAME
    assert result["app_description"] == TEST_APP_DESCRIPTION
    assert result["app_url"] == TEST_APP_URL
