from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from scrum.api.utils.projects import has_access_to_project, is_project_owner
from scrum.repositories.projects import ProjectRepository


def validate_project(user_id: int, project_id: int, is_superuser: bool, *, session: Session = None,
                     check_owner: bool = False):
    project_repo = ProjectRepository(session)
    if project_repo.fetch(project_id) is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Проекта с данным id не существует'
        )
    if not is_superuser and not has_access_to_project(session, user_id, project_id):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f'Текущий пользователь не имеет доступа к проекту {project_id}'
        )
    if check_owner:
        if (not is_superuser and
                not is_project_owner(session, user_id, project_id)):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail='Текущий пользователь не имеет права на это действие в данном проекте'
            )