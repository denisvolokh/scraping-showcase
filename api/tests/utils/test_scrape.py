import pytest
import requests_mock
from requests.exceptions import Timeout

from api.utils.scrape import fetch_page_content

TARGET_URL = "https://lords-mobile.en.aptoide.com"


@pytest.fixture
def mock_html_content():
    return """
    <html>
        <body>
            <div id="__next">
                <div>
                    <h1>Example App</h1>
                    <span class="downloads">5000</span>
                    <div class="description">This is an example app</div>
                    <span class="release-date">2023-01-01</span>
                    <div class="version">1.0.0</div>
                </div>
            </div>
        </body>
    </html>
    """


def test_fetch_page_content(mock_html_content):
    """Test that the fetch_page_content function returns the correct content

    Args:
        mock_html_content: Mock HTML content
    """

    with requests_mock.Mocker() as m:
        m.get(TARGET_URL, text=mock_html_content)
        content = fetch_page_content(TARGET_URL)

        assert content == mock_html_content


def test_fetch_page_content_not_found():
    """Test that the fetch_page_content function returns None if the request fails"""

    with requests_mock.Mocker() as m:
        m.get(TARGET_URL, status_code=404)
        content = fetch_page_content(TARGET_URL)

        assert content is None


def test_fetch_page_content_timeout():
    """Test that the fetch_page_content function returns None if the request times out"""

    with requests_mock.Mocker() as m:
        m.get(TARGET_URL, exc=Timeout)
        content = fetch_page_content(TARGET_URL)

        assert content is None


def test_fetch_page_content_unicode_exception():
    """Test that the fetch_page_content function returns None if the request raises a UnicodeDecodeError"""

    with requests_mock.Mocker() as m:
        invalid_utf8_content = b"\xff\xfe\xfd"
        m.get(TARGET_URL, content=invalid_utf8_content)
        content = fetch_page_content(TARGET_URL)

        assert content is None
