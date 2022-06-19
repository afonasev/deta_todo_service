import logging

import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.ports.api.users.resources import router as users_router
from app.settings import get_settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=get_settings().PROJECT_NAME,
        version='1.0',
    )

    _configure_logging()
    _configure_sentry()
    _configure_cors(app)

    app.include_router(users_router, prefix="/api/users")

    return app


def _configure_logging() -> None:
    logging.basicConfig(
        format=get_settings().LOGGING_FORMAT, level=get_settings().LOGGING_LEVEL
    )


def _configure_sentry() -> None:
    sentry_sdk.init()
    # todo: install middleware


def _configure_cors(app: FastAPI) -> None:
    # Set all CORS enabled origins
    if get_settings().BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=get_settings().BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
