import falcon
from falcon import Request, Response
from marshmallow import ValidationError

from api.schemas.scrape import ScrapeResultSchema
from api.tasks import task_scrape_target


class ScrapeResource:
    def on_get(self, req: Request, resp: Response) -> None:
        """Handles GET requests for scrape endpoint

        Args:
            req (Request): Request object
            resp (Response): Response object
        """

        target_url = req.get_param("target_url", "")

        schema = ScrapeResultSchema()

        try:
            result = schema.dump(
                {
                    "target_url": target_url,
                    "result": task_scrape_target(target_url),
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
