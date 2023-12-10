from typing import Optional

from celery import Celery, Task

from api.utils.scrape import scrape_target_page

app_name = "scrape-tasks-app"
broker_url = "redis://redis:6379/0"
result_backend = "redis://redis:6379/0"
include = ["api.tasks"]

celery = Celery(app_name, broker=broker_url, backend=result_backend, include=include)


@celery.task(bind=True)
def task_scrape_target(self: Task, url: str) -> Optional[dict]:
    """Wrapper for scrape_target_page function to be used as a celery task

    Args:
        self (Task): Celery task
        url (str): URL of the target page to scrape

    Returns:
        Optional[dict]: Dictionary containing the scraped data
    """

    return scrape_target_page(url)
