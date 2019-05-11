from fastapi import APIRouter

from scrum.api.v1.endpoints import users, auth, projects, sprints, tasks, tags

api_router = APIRouter()

api_router.include_router(auth.router, tags=['auth'])
api_router.include_router(users.router, tags=['users'])
api_router.include_router(projects.router, tags=['projects'])
api_router.include_router(sprints.router, tags=['sprints'])
api_router.include_router(tasks.router, tags=['tasks'])
api_router.include_router(tags.router, tags=['tags'])
