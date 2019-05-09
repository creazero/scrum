from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from scrum.api.utils.db import get_db
from scrum.api.utils.projects import has_access_to_project, is_project_owner
from scrum.api.utils.security import get_current_user
from scrum.db_models.user import User
from scrum.models.sprint import SprintCreate, Sprint
from scrum.repositories.accessible_project import AccessibleProjectRepository
from scrum.repositories.projects import ProjectRepository
from scrum.repositories.sprints import SprintRepository

router = APIRouter()


@router.get('/sprints', response_model=List[Sprint])
def get_sprints(
        project_id: int = None,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    accessible_repo = AccessibleProjectRepository(session)
    accessible_projects = accessible_repo.fetch_accessible_for_user(current_user.id)
    sprint_repo = SprintRepository(session)
    return sprint_repo.fetch_all(accessible_projects, project_id)


@router.post('/sprints', status_code=201, response_model=Sprint)
def create_sprint(
        sprint_in: SprintCreate,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    project_repo = ProjectRepository(session)
    if project_repo.fetch(sprint_in.project_id) is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Проекта с данным id не существует'
        )
    if not has_access_to_project(session, current_user.id, sprint_in.project_id):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f'Текущий пользователь не имеет доступа к проекту {sprint_in.project_id}'
        )
    if (not current_user.is_superuser and
            not is_project_owner(session, current_user.id, sprint_in.project_id)):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Текущий пользователь не имеет права на создание спринтов в данном проекте'
        )
    sprint_repo = SprintRepository(session)
    created_sprint = sprint_repo.create(sprint_in)
    return created_sprint
