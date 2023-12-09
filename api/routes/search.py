import falcon
from falcon import Request, Response
from marshmallow import ValidationError

from api.schemas.search import ScrapeResultSchema


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
                    "result": {
                        "app_name": "app1",
                        "app_version": "1.0.0",
                        "app_description": "app1 desc",
                        "no_downloads": 100,
                        "app_url": "https://app1.com",
                        "app_release_date": "2020-01-01",
                    },
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
