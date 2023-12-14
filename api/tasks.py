import json
import logging
from typing import Optional

from celery import Celery, Task
from redis import Redis

from api.utils.scrape import scrape_target_page

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BROKER_URL = "redis://redis:6379/0"
RESULT_BACKEND = "redis://redis:6379/0"

app_name = "scrape-tasks-app"
include = ["api.tasks"]

celery = Celery(app_name, broker=BROKER_URL, backend=RESULT_BACKEND, include=include)
redis_client = Redis(host="redis", port=6379, db=0)


@celery.task(bind=True)
def task_scrape_target(self: Task, url: str) -> Optional[dict]:
    """Wrapper for scrape_target_page function to be used as a celery task

    Args:
        self (Task): Celery task
        url (str): URL of the target page to scrape

    Returns:
        Optional[dict]: Dictionary containing the scraped data
    """

    logger.info(f"Started task to scrape URL: {url}, task ID: {self.request.id}")

    task_id = self.request.id
    result = scrape_target_page(url)

    # Store the result in Redis with the task_id as the key
    redis_client.set(task_id, json.dumps(result))

    return result
