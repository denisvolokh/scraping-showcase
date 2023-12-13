import falcon
from falcon import Request, Response

from api.schemas.scrape import ScrapeResultSchema
from api.utils.scrape import scrape_target_page


class ScrapeResource:
    async def on_get(self, req: Request, resp: Response) -> None:
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
        if not target_url:
            raise falcon.HTTPBadRequest(
                title="Missing required parameter", description="target_url"
            )

        schema = ScrapeResultSchema()
        scraped_result = scrape_target_page(target_url)

        result = schema.dump({"result": scraped_result})
        resp.media = result
        resp.status = falcon.HTTP_200
