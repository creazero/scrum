from fastapi import FastAPI

from scrum import users


def create_app() -> FastAPI:
    _api = FastAPI()

    register_routers(_api)

    return _api


def register_routers(app: FastAPI):
    app.include_router(users.router, prefix='/users', tags=['users'])
