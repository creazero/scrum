from fastapi import FastAPI

from scrum.api.v1.api import api_router
from scrum.core.config import API_V1_PREFIX


def create_app() -> FastAPI:
    _api = FastAPI(title='Scrum')

    _api.include_router(api_router, prefix=API_V1_PREFIX)

    return _api
