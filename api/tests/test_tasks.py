import json
from unittest.mock import patch

import pytest

from api.tasks import task_scrape_target

TEST_APP_URL = "https://test.com"
TEST_TASK_SCRAPE_TARGET_PAGE_RESULT = {
    "app_name": "test-app-name",
    "app_description": "test-app-description",
    "app_icon_url": "test-app-icon-url",
    "app_version": "test-app-version",
    "app_release_date": "test-app-release-date",
}
TEST_TASK_ID = "test-task-id"


@pytest.fixture
def mock_scrape_target_page(mocker):
    return mocker.patch(
        "api.tasks.scrape_target_page", return_value=TEST_TASK_SCRAPE_TARGET_PAGE_RESULT
    )


@patch("api.tasks.redis_client")
@patch("celery.app.task.Task.request")
def test_task_scrape_target(
    mock_task_request, mock_redis_client, mock_scrape_target_page
):
    """Test Celery task task_scrape_target function

    Args:
        mock_task_request (MagicMock): Mocked task request
        mock_redis_client (MagicMock): Mocked Redis client
        mock_scrape_target_page (MagicMock): Mocked scrape_target_page function
    """

    # Mock the task request ID
    mock_task_request.id = TEST_TASK_ID

    # Run the task
    result = task_scrape_target(TEST_APP_URL)

    assert result == TEST_TASK_SCRAPE_TARGET_PAGE_RESULT

    # Assert scrape_target_page was called correctly
    mock_scrape_target_page.assert_called_once_with(TEST_APP_URL)

    # Assert Redis set method was called with correct arguments
    mock_redis_client.set.assert_called_once_with(
        TEST_TASK_ID, json.dumps(TEST_TASK_SCRAPE_TARGET_PAGE_RESULT)
    )
