import json
import pathlib

import falcon
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon_apispec import FalconPlugin
from falcon_swagger_ui import register_swaggerui_app

from api.routes.static import StaticFileHandler
from api.routes.v1.scrape import ScrapeResource
from api.routes.v2.scrape import AsyncScrapeResource, AsyncScrapeResultResource
from api.schemas.scrape import AsyncScrapeResultSchema, ScrapeResultSchema

STATIC_PATH = pathlib.Path(__file__).parent / "static"
SWAGGERUI_URL = "/swagger"
SCHEMA_URL = "/static/swagger.json"

app = falcon.App()

scrape_resource = ScrapeResource()
async_scrape_resource = AsyncScrapeResource()
async_scrape_result_resource = AsyncScrapeResultResource()


def create_spec(app: falcon.App) -> APISpec:
    """Create API specification, register schemas and paths

    Args:
        app (falcon.App): Falcon application

    Returns:
        APISpec: API specification
    """

    spec = spec = APISpec(
        title="Swagger Scrape App API",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[
            FalconPlugin(app),
            MarshmallowPlugin(),
        ],
    )
    spec.components.schema("ScrapeResult", schema=ScrapeResultSchema)
    spec.components.schema("AsyncScrapeResult", schema=AsyncScrapeResultSchema)

    spec.path(resource=scrape_resource)
    spec.path(resource=async_scrape_resource)
    spec.path(resource=async_scrape_result_resource)

    return spec


def setup_routes(app: falcon.App) -> None:
    """Setup routes for the application

    Args:
        app (falcon.App): Falcon application
    """

    app.add_route("/v1/scrape", scrape_resource)

    app.add_route("/v2/scrape", async_scrape_resource)
    app.add_route("/v2/scrape/result/{task_id}", async_scrape_result_resource)

    app.add_route(
        "/static/swagger.json", StaticFileHandler(f"{STATIC_PATH}/swagger.json")
    )


def save_swagger_json(spec: APISpec) -> None:
    """Save swagger json file to the static folder

    Args:
        spec (APISpec): API specification
    """

    swagger_json = json.dumps(spec.to_dict(), indent=2)
    with open("api/static/swagger.json", "w") as file:
        file.write(swagger_json)


def initialize_swagger_ui(app: falcon.App) -> None:
    """Initializes Swagger UI for the Falcon app."""
    register_swaggerui_app(
        app,
        SWAGGERUI_URL,
        SCHEMA_URL,
        config={
            "supportedSubmitMethods": ["get"],
        },
    )


setup_routes(app)
spec = create_spec(app)
save_swagger_json(spec)
initialize_swagger_ui(app)
