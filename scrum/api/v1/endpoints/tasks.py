from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from scrum.api.utils.db import get_db
from scrum.api.utils.projects import has_access_to_project
from scrum.api.utils.security import get_current_user
from scrum.db_models.user import User
from scrum.models.task import Task
from scrum.repositories.accessible_project import AccessibleProjectRepository
from scrum.repositories.projects import ProjectRepository
from scrum.repositories.tasks import TaskRepository

router = APIRouter()


@router.get('/tasks', response_model=List[Task])
def get_tasks(
        project_id: int = None,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    task_repo = TaskRepository(session)
    if project_id is not None:
        project_repo = ProjectRepository(session)
        if project_repo.fetch(project_id) is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Проекта с данным id не существует'
            )
        if not has_access_to_project(session, current_user.id, project_id):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f'Текущий пользователь не имеет доступа к проекту {project_id}'
            )
        return task_repo.fetch_from_project(project_id)
    elif current_user.is_superuser:
        return task_repo.fetch_all()
    else:
        accessible_repo = AccessibleProjectRepository(session)
        return task_repo.fetch_accessible(accessible_repo.fetch_accessible_for_user(current_user.id))
