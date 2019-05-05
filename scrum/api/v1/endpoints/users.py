from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from scrum.api.utils.db import get_db
from scrum.api.utils.security import get_oauth_schema
from scrum.models.users import User, UserAuth
from scrum.repositories.users import UserRepository

router = APIRouter()


@router.get('/users', response_model=List[User])
def get_users(session: Session = Depends(get_db), _ = Depends(get_oauth_schema())):
    """
    Fetch all users
    :param session: db session
    :return: a list of users
    """
    repository = UserRepository(session)
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
