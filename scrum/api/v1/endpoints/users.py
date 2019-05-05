from typing import List

from fastapi import APIRouter, Depends, HTTPException

from scrum.api.utils import get_db
from scrum.db.session import SessionScope
from scrum.models.users import User, UserAuth
from scrum.repositories.users import UserRepository

router = APIRouter()


@router.get('/users', response_model=List[User])
def get_users(
        session: SessionScope = Depends(get_db)
):
    """
    Fetch all users
    :param session: db session
    :return: a list of users
    """
    repository = UserRepository(session)
    return repository.fetch_all()


@router.post('/users', response_model=User)
def create_user(user_in: UserAuth, session: SessionScope = Depends(get_db)):
    repository = UserRepository(session)
    user = repository.fetch_by_username(user_in.username)
    if user is not None:
        raise HTTPException(
            status_code=400,
            detail='Пользователь с таким именем уже существует'
        )
    return repository.create_user(user_in)
