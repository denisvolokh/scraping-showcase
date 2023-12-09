import falcon
from falcon import Request, Response
from marshmallow import ValidationError

from api.schemas.search import SearchResultSchema


class SearchResource:
    def on_get(self, req: Request, resp: Response) -> None:
        """Handles GET requests for search endpoint

        Args:
            req (Request): Request object
            resp (Response): Response object
        """

        query = req.get_param("query", "")

        schema = SearchResultSchema()

        try:
            result = schema.dump(
                {
                    "query": query,
                    "results": [
                        {
                            "app_name": "app1",
                            "app_version": "1.0.0",
                            "app_description": "app1 desc",
                            "no_downloads": 100,
                            "app_url": "https://app1.com",
                            "app_release_date": "2020-01-01",
                        },
                    ],
                }
            )
            resp.media = result
            resp.status = falcon.HTTP_200
        except ValidationError as e:
            result = schema.dump(
                {
                    "query": query,
                    "error": str(e),
                }
            )
            resp.media = result
            resp.status = falcon.HTTP_400
