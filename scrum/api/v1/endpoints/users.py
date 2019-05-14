from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from scrum.api.utils.db import get_db
from scrum.api.utils.security import get_current_user
from scrum.api.utils.shared import validate_project
from scrum.api.utils.users import user_response
from scrum.db_models.user import User as DBUser
from scrum.models.users import User, UserAuth
from scrum.repositories.accessible_project import AccessibleProjectRepository
from scrum.repositories.users import UserRepository

router = APIRouter()


@router.get('/users', response_model=List[User])
def get_users(
        project_id: int = None,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Fetch all users
    :param session: db session
    :return: a list of users
    """
    repository = UserRepository(session)
    if project_id is not None:
        validate_project(current_user.id, project_id, current_user.is_superuser,
                         session=session)
        users = repository.fetch_by_project(project_id)
        return [user_response(user) for user in users]
    return repository.fetch_all()


@router.post('/users', response_model=User)
def create_user(user_in: UserAuth, session: Session = Depends(get_db)):
    repository = UserRepository(session)
    user = repository.fetch_by_username(user_in.username)
    if user is not None:
        raise HTTPException(
            status_code=400,
            detail='Пользователь с таким именем уже существует'
        )
    return repository.create_user(user_in)


@router.get('/current_user', response_model=User)
def current_user(
        project_id: int = None,
        session: Session = Depends(get_db),
        user: DBUser = Depends(get_current_user)
):
    if project_id is None:
        return user
    ap_repo = AccessibleProjectRepository(session)
    role = ap_repo.fetch_user_role(user.id, project_id)
    return User(role=role, **ap_repo.__dict__)
