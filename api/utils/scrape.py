import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup
from lxml import html

from api.utils.url import convert_to_base_url

logging.basicConfig(level=logging.INFO)

APP_NAME_XPATH = (
    '//*[@id="__next"]/div/div[2]/div/div[1]/div[2]/div[2]/div/div[3]/div[2]/div[1]/h1'
)
NO_DOWNLOADS_XPATH = '//*[@id="__next"]/div/div[2]/div/div[1]/div[2]/div[2]/div/div[3]/div[3]/div[1]/span[1]'
APP_DESCRIPTION_XPATH = (
    '//*[@id="__next"]/div/div[2]/div/div[1]/div[2]/div[4]/div[2]/div/div/p'
)
APP_RELEASE_DATE_XPATH = (
    '//*[@id="__next"]/div/div[2]/div/div[1]/div[2]/div[6]/div[3]/div[1]/span[5]/text()'
)
APP_VERSION_SELECTOR_CLASS = "appview-header__AppViewSpan-sc-924t8o-13 jTqVMH"


def fetch_page_content(url: str) -> Optional[str]:
    """Fetch the content of a webpage

    Args:
        url (str): URL of the webpage

    Returns:
        Optional[str]: Content of the webpage if successful, None otherwise
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        logging.error(f"Error fetching page content: {e}")
        return None
    except UnicodeDecodeError as e:
        logging.error(f"Error decoding content from {url}: {e}")
        return None


def scrape_element(tree: html, xpath: str) -> Optional[str]:
    """Scrape an element from a webpage by its XPath

    Args:
        tree (html): HTML tree of the webpage
        xpath (str): XPath of the element to scrape

    Returns:
        Optional[str]: Text content of the element if found, None otherwise
    """

    element = tree.xpath(xpath)
    return element[0].text if element else None


def scrape_app_name(tree: html) -> Optional[str]:
    """Scrape the app name from a webpage

    Args:
        tree (html): HTML tree of the webpage

    Returns:
        Optional[str]: App name if found, None otherwise
    """
    return scrape_element(tree, APP_NAME_XPATH)


def scrape_no_downloads(tree: html) -> Optional[str]:
    """Scrape the number of downloads of an app from a webpage

    Args:
        tree (html): HTML tree of the webpage

    Returns:
        Optional[str]: Number of downloads of the app or None if not found
    """

    return scrape_element(tree, NO_DOWNLOADS_XPATH)


def clean_up_text(text: str) -> Optional[str]:
    """Clean up the text by removing the leading and trailing whitespaces and newlines

    Args:
        text (str): Text to clean up

    Returns:
        str: Cleaned up text or None if the text is empty
    """

    clean_text = text.replace("\n", "").replace("\r", "").replace("\xa0", "").strip()
    return clean_text if clean_text else None


def scrape_app_description(tree: html) -> Optional[str]:
    """Scrape the app description from a webpage

    Args:
        tree (html): HTML tree of the webpage

    Returns:
        Optional[str]: App description if found, None otherwise
    """

    description_items = [
        clean_up_text(p.text_content()) for p in tree.xpath(APP_DESCRIPTION_XPATH)
    ]
    return " ".join(item for item in description_items if item)


def scrape_app_release_date(tree: html) -> Optional[str]:
    """Scrape the app release date from a webpage

    Args:
        tree (html): HTML tree of the webpage

    Returns:
        Optional[str]: App release date if found, None otherwise
    """

    element = tree.xpath(APP_RELEASE_DATE_XPATH)
    return element[1] if element else None


def scrape_app_version(url: str) -> Optional[str]:
    """Scrape the app version from the Versions URL

    Args:
        url (str): URL of the target page

    Returns:
        Optional[str]: App version if found, None otherwise
    """

    version_url = f"{url}/versions"
    content = fetch_page_content(version_url)
    if not content:
        return None

    soup = BeautifulSoup(content, "html.parser")
    app_version_element = soup.find("span", class_=APP_VERSION_SELECTOR_CLASS)

    return app_version_element.text if app_version_element else None


def scrape_target_page(url: str) -> Optional[dict]:
    """Scrape the target page

    Args:
        url (str): URL of the target page
    """

    base_url = convert_to_base_url(url)
    content = fetch_page_content(base_url)
    if not content:
        return None

    tree = html.fromstring(content)
    return {
        "app_url": base_url,
        "app_name": scrape_app_name(tree),
        "no_downloads": scrape_no_downloads(tree),
        "app_description": scrape_app_description(tree),
        "app_release_date": scrape_app_release_date(tree),
        "app_version": scrape_app_version(base_url),
    }
