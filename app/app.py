import logging

import sentry_sdk
from fastapi import FastAPI

from app.ports.api.users.resources import router as users_router
from app.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version='1.0',
    )

    _init_logging()
    _init_sentry()

    app.include_router(users_router)

    return app


def _init_logging() -> None:
    logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)


def _init_sentry() -> None:
    sentry_sdk.init()
    # todo: install middleware
