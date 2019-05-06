from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from scrum.api.utils.db import get_db
from scrum.api.utils.security import get_current_user
from scrum.db_models.user import User
from scrum.models.project import Project, ProjectCreate
from scrum.repositories.projects import ProjectRepository

router = APIRouter()


@router.get('/projects', response_model=List[Project])
def get_projects(
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    repository = ProjectRepository(session)
    return repository.fetch_all()


@router.get('/projects/{project_id}', response_model=Project)
def get_project(
        project_id: int,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    repository = ProjectRepository(session)
    project = repository.fetch(project_id)
    if project is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Проект с таким id не найден'
        )
    return project


@router.post('/projects', response_model=Project, status_code=201)
def create_project(
        data: ProjectCreate,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    repository = ProjectRepository(session)
    try:
        new_project = repository.create(data, current_user.id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Внутренняя ошибка сервера'
        )
    return new_project


@router.delete('/projects/{project_id}')
def delete_project(
        project_id: int,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    repository = ProjectRepository(session)
    repository.delete(project_id)
    return {'status': 'ok'}
