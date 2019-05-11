from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN

from scrum.api.utils.db import get_db
from scrum.api.utils.projects import has_access_to_project, is_project_owner, project_response
from scrum.api.utils.security import get_current_user
from scrum.db_models.user import User
from scrum.models.project import Project, ProjectCreate
from scrum.repositories.accessible_project import AccessibleProjectRepository
from scrum.repositories.projects import ProjectRepository

router = APIRouter()


@router.get('/projects', response_model=List[Project])
def get_projects(
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    project_repo = ProjectRepository(session)
    if current_user.is_superuser:
        projects = project_repo.fetch_all([], current_user.is_superuser)
    else:
        accessible_repo = AccessibleProjectRepository(session)
        projects = project_repo.fetch_all(accessible_repo.fetch_accessible_for_user(current_user.id),
                                          current_user.is_superuser)
    return [project_response(project) for project in projects]


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
    if not current_user.is_superuser and not has_access_to_project(session, current_user.id, project_id):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='У текущего пользователя нет доступа к данному проекту'
        )
    return project_response(project)


@router.post('/projects', response_model=Project, status_code=201)
def create_project(
        data: ProjectCreate,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    repository = ProjectRepository(session)
    new_project = repository.create(data, current_user.id)
    return new_project


@router.put('/projects/{project_id}', response_model=Project)
def update_project(
        project_id: int,
        project_in: Project,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    project_repo = ProjectRepository(session)
    project = project_repo.fetch(project_id)
    if project is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Проекта с данным id не существует'
        )
    if not current_user.is_superuser and not is_project_owner(session, current_user.id, project_id):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Текущий пользователь не является владельцем проекта'
        )
    project = project_repo.update(project, project_in)
    return project


@router.delete('/projects/{project_id}')
def delete_project(
        project_id: int,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    repository = ProjectRepository(session)
    project = repository.fetch(project_id)
    if project is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Проект с данным id не найден'
        )
    if not has_access_to_project(session, current_user.id, project_id):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='У текущего пользователя нет доступа к данному проекту'
        )
    if not is_project_owner(session, current_user.id, project_id):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Текущий пользователь не является владельцем проекта'
        )
    repository.delete(project)
    return {'status': 'ok'}
