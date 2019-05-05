import uvicorn
from fastapi import FastAPI

from scrum.api.v1.api import api_router
from scrum.core.config import API_V1_PREFIX
from scrum.db.session import Session

app = FastAPI(title='Scrum')

app.include_router(api_router, prefix=API_V1_PREFIX)


@app.middleware('http')
async def session_middleware(request, call_next):
    request.state.session = Session()
    response = await call_next(request)
    request.state.session.close()
    return response


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
