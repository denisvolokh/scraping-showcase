import asyncio
import logging
from typing import AsyncGenerator

import falcon
from falcon import Request, Response
from marshmallow import ValidationError
from redis.asyncio.client import Redis

from api.schemas.scrape import AsyncScrapeResultSchema
from api.tasks import task_scrape_target

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncScrapeResource:
    async def on_get(self, req: Request, resp: Response) -> None:
        """Request to scrape target URL (asynchronous)
        ---
        description: Returns a task ID for the started async scraping task
        tags:
          - Async Scrape
        parameters:
          - in: query
            name: target_url
            required: true
            schema:
              type: string
            description: Target URL to scrape
        responses:
          200:
            description: Successful operation
            content:
              application/json:
                schema: AsyncScrapeResultSchema
          400:
            description: Invalid request
          500:
            description: Internal server error
        """

        target_url = req.get_param("target_url", "")

        task = task_scrape_target.apply_async(args=[target_url])

        schema = AsyncScrapeResultSchema()

        try:
            result = schema.dump(
                {
                    "target_url": target_url,
                    "task_id": task.id,
                    "status": task.state,
                }
            )
            resp.media = result
            resp.status = falcon.HTTP_200
        except ValidationError as e:
            result = schema.dump(
                {
                    "target_url": target_url,
                    "error": str(e),
                }
            )
            resp.media = result
            resp.status = falcon.HTTP_400


class AsyncScrapeResultResource:
    async def on_get(self, req: Request, resp: Response, task_id: str) -> None:
        """Request to get the result of the async scraping task
        ---
        description: Returns the result of the async scraping task
        tags:
          - Async Scrape
        parameters:
          - in: path
            name: task_id
            required: true
            schema:
              type: string
            description: ID of the task to get the result for
        responses:
          200:
            description: Successful operation
            content:
              application/json:
                schema: AsyncScrapeResultSchema
          400:
            description: Invalid request
          500:
            description: Internal server error
        """

        task_result = task_scrape_target.AsyncResult(task_id)

        logging.info(f"Task ID: {task_id} - {task_result.state}")

        schema = AsyncScrapeResultSchema()

        if not task_result.ready():
            resp.media = schema.dump(
                {
                    "task_id": task_id,
                    "status": task_result.state,
                }
            )
            resp.status = falcon.HTTP_200
            return

        if task_result.failed():
            resp.media = schema.dump(
                {
                    "task_id": task_id,
                    "status": task_result.state,
                    "error": str(task_result.result),
                }
            )
            resp.status = falcon.HTTP_400
            return

        resp.media = schema.dump(
            {
                "task_id": task_id,
                "status": task_result.state,
                "result": task_result.result,
            }
        )
        resp.status = falcon.HTTP_200


class SSEScrapeUpdateResource:
    async def on_get(self, req: Request, resp: Response, task_id: str) -> None:
        """Resource to handle server-sent events for the async scraping task
        ---
        description: Returns successful server-sent events for the async scraping task
        tags:
          - Async Scrape
        parameters:
          - in: path
            name: task_id
            required: true
            schema:
              type: string
            description: ID of the task to get the result for
        responses:
          200:
            description: Successful operation
          400:
            description: Invalid request
          500:
            description: Internal server error
        """

        resp.content_type = "text/event-stream"
        redis_client = Redis(host="redis", port=6379, db=0)
        resp.stream = self.stream_response(redis_client, task_id)

    async def stream_response(
        self, redis_client: Redis, task_id: str
    ) -> AsyncGenerator:
        """Stream response for the async scraping task

        Args:
            task_id (str): ID of the task to get the result for

        Yields:
            dict: Server-sent event data
        """

        logger.info(f"Task ID: {task_id} - Streaming response")

        while True:
            result = await redis_client.get(task_id)

            logger.info(f"Task ID: {task_id} - {result}")

            if result is not None:
                yield f"data: {result.decode()}\n\n".encode()
                break

            # Wait for 10ms before checking again
            await asyncio.sleep(0.01)
