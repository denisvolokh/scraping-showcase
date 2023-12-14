from unittest.mock import patch

import pytest
from falcon.testing import ASGIConductor

from api.main import app

pytest_plugins = ["pytest_asyncio"]


TEST_APP_NAME = "app1"
TEST_APP_DESCRIPTION = "app1 desc"
TEST_APP_URL = "https://app1.com"
TEST_TASK_ID = "1234"
TEST_TASK_PENDING_STATE = "PENDING"
TEST_TASK_FAILED_STATE = "FAILED"
TEST_TASK_SUCCESS_STATE = "SUCCESS"


@pytest.fixture
def client():
    return ASGIConductor(app)


@pytest.fixture
def celery_task_mock():
    class CeleryTaskMock:
        def __init__(self) -> None:
            self.id = TEST_TASK_ID
            self.state = TEST_TASK_PENDING_STATE

    return CeleryTaskMock()


@pytest.fixture
def celery_task_async_result_pending_mock():
    class CeleryTaskAsyncResultMock:
        def __init__(self) -> None:
            self.id = TEST_TASK_ID
            self.state = TEST_TASK_PENDING_STATE

        def failed(self):
            return False

        def ready(self):
            return False

    return CeleryTaskAsyncResultMock()


@pytest.fixture
def celery_task_async_result_failed_mock():
    class CeleryTaskAsyncResultMock:
        def __init__(self) -> None:
            self.id = TEST_TASK_ID
            self.state = TEST_TASK_FAILED_STATE
            self.result = "Unable to scrape target URL"

        def ready(self):
            return False

        def failed(self):
            return True

    return CeleryTaskAsyncResultMock()


@pytest.fixture
def celery_task_async_result_success_mock():
    class CeleryTaskAsyncResultMock:
        def __init__(self) -> None:
            self.id = TEST_TASK_ID
            self.state = TEST_TASK_SUCCESS_STATE
            self.result = {
                "app_name": TEST_APP_NAME,
                "app_description": TEST_APP_DESCRIPTION,
                "app_url": TEST_APP_URL,
            }

        def ready(self):
            return True

        def failed(self):
            return False

    return CeleryTaskAsyncResultMock()


@pytest.mark.asyncio
@patch("api.routes.v1.scrape.scrape_target_page")
async def test_successful_sync_scrape_resource(mock_scrape, client):
    """Test /v1/scrape endpoint with synchronous scraping

    Args:
        mock_scrape (MagicMock): Mocked scrape_target_page function
        client (ASGIConductor): ASGIConductor client
    """

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


@pytest.mark.asyncio
async def test_failed_sync_scrape_resource(client):
    """Test /v1/scrape endpoint with synchronous scraping and missing target_url

    Args:
        client (ASGIConductor): ASGIConductor client
    """

    response = await client.simulate_get("/v1/scrape")

    assert response.status_code == 400


@pytest.mark.asyncio
@patch("api.routes.v2.scrape.task_scrape_target.apply_async")
async def test_successful_async_scrape_resource(
    mock_task_scrape, celery_task_mock, client
):
    """Test /v2/scrape endpoint with asynchronous scraping

    Args:
        mock_task_scrape (MagicMock): Mocked task_scrape_target function
        celery_task_mock (MagicMock): Mocked Celery task result
        client (ASGIConductor): ASGIConductor client
    """

    mock_task_scrape.return_value = celery_task_mock

    response = await client.simulate_get(
        "/v2/scrape", params={"target_url": TEST_APP_URL}
    )

    assert response.status_code == 200

    assert response.json["target_url"] == TEST_APP_URL
    assert response.json["task_id"] == TEST_TASK_ID
    assert response.json["status"] == TEST_TASK_PENDING_STATE


@pytest.mark.asyncio
async def test_failed_async_scrape_resource(client):
    """Test /v2/scrape endpoint with asynchronous scraping and missing target_url

    Args:
        client (ASGIConductor): ASGIConductor client
    """

    response = await client.simulate_get("/v2/scrape")

    assert response.status_code == 400


@pytest.mark.asyncio
@patch("api.routes.v2.scrape.task_scrape_target.AsyncResult")
async def test_async_scrape_pending_result_resource(
    mock_task_scrape, celery_task_async_result_pending_mock, client
):
    """Test /v2/scrape/result/{task_id} endpoint to get the result of the async scraping task

    Args:
        mock_task_scrape (MagicMock): Mocked task_scrape_target function
        celery_task_async_result_pending_mock (MagicMock): Mocked Celery task AsycnResult with pending state
        client (ASGIConductor): ASGIConductor client
    """

    mock_task_scrape.return_value = celery_task_async_result_pending_mock

    response = await client.simulate_get(f"/v2/scrape/result/{TEST_TASK_ID}")

    assert response.status_code == 200

    assert response.json["task_id"] == TEST_TASK_ID
    assert response.json["status"] == TEST_TASK_PENDING_STATE


@pytest.mark.asyncio
@patch("api.routes.v2.scrape.task_scrape_target.AsyncResult")
async def test_async_scrape_failed_result_resource(
    mock_task_scrape, celery_task_async_result_failed_mock, client
):
    """Test /v2/scrape/result/{task_id} endpoint to get the result of the async scraping task

    Args:
        mock_task_scrape (MagicMock): Mocked task_scrape_target function
        celery_task_async_result_failed_mock (MagicMock): Mocked Celery task AsycnResult with failed state
        client (ASGIConductor): ASGIConductor client
    """

    mock_task_scrape.return_value = celery_task_async_result_failed_mock

    response = await client.simulate_get(f"/v2/scrape/result/{TEST_TASK_ID}")

    assert response.status_code == 200

    assert response.json["task_id"] == TEST_TASK_ID
    assert response.json["status"] == TEST_TASK_FAILED_STATE


@pytest.mark.asyncio
@patch("api.routes.v2.scrape.task_scrape_target.AsyncResult")
async def test_async_scrape_success_result_resource(
    mock_task_scrape, celery_task_async_result_success_mock, client
):
    """Test /v2/scrape/result/{task_id} endpoint to get the result of the async scraping task

    Args:
        mock_task_scrape (MagicMock): Mocked task_scrape_target function
        celery_task_async_result_success_mock (MagicMock): Mocked Celery task AsycnResult with success state
        client (ASGIConductor): ASGIConductor client
    """

    mock_task_scrape.return_value = celery_task_async_result_success_mock

    response = await client.simulate_get(f"/v2/scrape/result/{TEST_TASK_ID}")

    assert response.status_code == 200

    assert response.json["task_id"] == TEST_TASK_ID
    assert response.json["status"] == TEST_TASK_SUCCESS_STATE
    assert response.json["result"]["app_name"] == TEST_APP_NAME
    assert response.json["result"]["app_description"] == TEST_APP_DESCRIPTION
    assert response.json["result"]["app_url"] == TEST_APP_URL
