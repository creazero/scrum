from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from scrum.api.utils.db import get_db
from scrum.api.utils.projects import has_access_to_project, is_project_owner
from scrum.api.utils.security import get_current_user
from scrum.api.utils.shared import validate_project
from scrum.api.utils.sprints import has_intersecting_sprint
from scrum.db_models.user import User
from scrum.models.sprint import SprintCreate, Sprint, OngoingSprint, IntersectionCheck
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
    validate_project(current_user.id, sprint_in.project_id,
                     current_user.is_superuser,
                     session=session, check_owner=True)
    sprint_repo = SprintRepository(session)
    # get all sprints for the intersection check
    sprints = sprint_repo.fetch_all([], sprint_in.project_id)
    if has_intersecting_sprint(sprint_in.start_date, sprints):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Для такой даты начала спринта существует пересекающийся спринт'
        )
    created_sprint = sprint_repo.create(sprint_in)
    return created_sprint


@router.delete('/sprints/{sprint_id}')
def delete_sprint(
        sprint_id: int,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    sprint_repo = SprintRepository(session)
    sprint = sprint_repo.fetch(sprint_id)
    if sprint is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Спринта с таким id не существует'
        )
    validate_project(current_user.id, sprint.project_id,
                     session=session, check_owner=True,
                     is_superuser=current_user.is_superuser)
    sprint_repo.delete(sprint)
    return {'status': 'ok'}


@router.get('/sprints/ongoing', response_model=OngoingSprint)
def ongoing_sprint(
        project_id: int,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    validate_project(current_user.id, project_id,
                     current_user.is_superuser, session=session)
    sprint_repo = SprintRepository(session)
    return {
        'sprint': sprint_repo.fetch_ongoing(project_id)
    }


@router.post('/sprints/intersection')
def check_intersection(
        data: IntersectionCheck,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    validate_project(current_user.id, data.project_id,
                     current_user.is_superuser, session=session)
    sprint_repo = SprintRepository(session)
    all_sprints = sprint_repo.fetch_by_project(data.project_id)
    return {
        'has_intersection': has_intersecting_sprint(data.start_date, all_sprints)
    }
