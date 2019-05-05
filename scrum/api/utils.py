from starlette.requests import Request

from scrum.db.session import SessionScope


def get_db(request: Request) -> SessionScope:
    return request.state.session
