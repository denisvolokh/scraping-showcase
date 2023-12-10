from typing import Optional

from api.utils.scrape import scrape_target_page


def task_scrape_target(url: str) -> Optional[dict]:
    """Task to scrape a target URL and return the result

    Args:
        url (str): URL to scrape

    Returns:
        ResultItemSchema: Result of scraping the URL
    """

    return scrape_target_page(url)
