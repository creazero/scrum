from fastapi import FastAPI

from scrum.api.v1.api import api_router
from scrum.core import config
from scrum.core.config import API_V1_PREFIX
from scrum.db.session import SessionScope

app = FastAPI(title='Scrum')

app.include_router(api_router, prefix=API_V1_PREFIX)

session_scope = SessionScope(config.SQLALCHEMY_DATABASE_URI)


@app.middleware('http')
async def session_middleware(request, call_next):
    request.state.session = session_scope
    response = await call_next(request)
    return response
