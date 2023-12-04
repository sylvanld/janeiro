from typing import List

from fastapi import FastAPI, Depends

from janeiro.config import Config, ConfigOption
from janeiro.context import get_app_context
from janeiro.query import Pagination

API_TITLE_OPTION = ConfigOption(key="api.title", type=str, default=None)
API_DESCRIPTION_OPTION = ConfigOption(key="api.description", type=str, default=None)
API_SWAGGER_UI_PATH_OPTION = ConfigOption(
    key="api.swagger_ui.path", type=str, default="/"
)
API_CORS_ALLOW_ORIGINS_OPTION = ConfigOption(
    key="api.cors.allow_origins", type=List[str], default=None
)


def pagination_from_query() -> Pagination:
    def _pagination_dependency(page: int, limit: int):
        return Pagination(page, limit)
    return Depends(_pagination_dependency)


class RestAPI:
    def __init__(
        self,
        api_title: str = None,
        api_description: str = None,
        swagger_ui_url: str = "/",
        cors_allow_origins: List[str] = None,
    ):
        self.app = FastAPI(
            title=api_title, description=api_description, docs_url=swagger_ui_url
        )
        if cors_allow_origins:
            self._configure_cors(cors_allow_origins)

    def include_router(self, router):
        self.app.include_router(router)

    def _configure_cors(self, allow_origins: List[str]):
        from fastapi.middleware.cors import CORSMiddleware

        self.app.add_middleware(CORSMiddleware, allow_origins=allow_origins)

    @staticmethod
    def from_config(config: Config):
        api_title = config.get(API_TITLE_OPTION)
        if api_title is None:
            context = get_app_context()
            api_title = f"{context.app_name} API"
        return RestAPI(
            api_title=api_title,
            api_description=config.get(API_DESCRIPTION_OPTION),
            swagger_ui_url=config.get(API_SWAGGER_UI_PATH_OPTION),
            cors_allow_origins=config.get(API_CORS_ALLOW_ORIGINS_OPTION),
        )

    def start(self, host: str, port: int):
        import uvicorn

        uvicorn.run(self.app, host=host, port=port)
