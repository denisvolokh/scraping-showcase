import json
import pathlib

import falcon
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon_swagger_ui import register_swaggerui_app

from api.routes.search import ScrapeResource
from api.routes.static import StaticFileHandler
from api.schemas.search import ScrapeResultSchema

STATIC_PATH = pathlib.Path(__file__).parent / "static"
SWAGGERUI_URL = "/swagger"
SCHEMA_URL = "/static/v1/swagger.json"

app = falcon.App()


def create_spec(app: falcon.App) -> APISpec:
    """Create API specification, register schemas and paths

    Args:
        app (falcon.App): Falcon application

    Returns:
        APISpec: API specification
    """

    spec = spec = APISpec(
        title="Swagger Search App API",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[
            MarshmallowPlugin(),
        ],
    )
    spec.components.schema("ScrapeResult", schema=ScrapeResultSchema)
    spec.path(
        path="/scrape",
        operations=dict(
            get=dict(
                responses={
                    200: {"description": "successful operation"},
                    400: {"description": "Invalid request"},
                    500: {"description": "Internal server error"},
                },
                summary="Get scrape result",
                description="Returns a scrape result from the target URL",
                tags=["Scrape"],
                parameters=[
                    {
                        "in": "query",
                        "name": "target_url",
                        "required": True,
                        "schema": {
                            "type": "string",
                        },
                        "description": "Target URL to scrape",
                    }
                ],
            )
        ),
    )

    return spec


def setup_routes(app: falcon.App) -> None:
    """Setup routes for the application

    Args:
        app (falcon.App): Falcon application
    """

    app.add_route("/scrape", ScrapeResource())
    app.add_route(
        "/static/v1/swagger.json", StaticFileHandler(f"{STATIC_PATH}/v1/swagger.json")
    )


def save_swagger_json(spec: APISpec) -> None:
    """Save swagger json file to the static folder

    Args:
        spec (APISpec): API specification
    """

    swagger_json = json.dumps(spec.to_dict(), indent=2)
    with open("api/static/v1/swagger.json", "w") as file:
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


spec = create_spec(app)
setup_routes(app)
save_swagger_json(spec)
initialize_swagger_ui(app)
