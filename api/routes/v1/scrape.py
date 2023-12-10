import falcon
from falcon import Request, Response
from marshmallow import ValidationError

from api.schemas.scrape import ScrapeResultSchema
from api.utils.scrape import scrape_target_page


class ScrapeResource:
    def on_get(self, req: Request, resp: Response) -> None:
        """Request to scrape target URL (synchronous)
        ---
        description: Returns a scrape result from the target URL
        tags:
          - Sync Scrape
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
                schema: ScrapeResultSchema
          400:
            description: Invalid request
          500:
            description: Internal server error
        """

        target_url = req.get_param("target_url", "")

        schema = ScrapeResultSchema()

        try:
            result = schema.dump(
                {
                    "result": scrape_target_page(target_url),
                }
            )
            resp.media = result
            resp.status = falcon.HTTP_200
        except ValidationError as e:
            result = schema.dump(
                {
                    "error": f"Unable to scrape ({target_url}), exception: {e}",
                }
            )
            resp.media = result
            resp.status = falcon.HTTP_400
