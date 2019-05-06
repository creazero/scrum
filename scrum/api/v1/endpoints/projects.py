from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from scrum.api.utils.db import get_db
from scrum.models.project import Project
from scrum.repositories.projects import ProjectRepository

router = APIRouter()


@router.get('/projects', response_model=List[Project])
def get_projects(session: Session = Depends(get_db)):
    repository = ProjectRepository(session)
    return repository.fetch_all()


@router.get('/projects/{project_id}', response_model=Project)
def get_project(
        project_id: int,
        session: Session = Depends(get_db)
):
    repository = ProjectRepository(session)
    project = repository.fetch(project_id)
    if project_id is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Проект с таким id не найден'
        )
    return project
