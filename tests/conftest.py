from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture(scope='session')
def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope='session')
def client(app) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
