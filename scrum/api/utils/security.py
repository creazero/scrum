import jwt
from fastapi import Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from scrum.api.utils.db import get_db
from scrum.core import config
from scrum.core.jwt import TOKEN_ALGORITHM
from scrum.db.session import Session
from scrum.db_models.user import User
from scrum.models.token import TokenPayload
from scrum.repositories.users import UserRepository


def get_oauth_schema() -> OAuth2PasswordBearer:
    """
    Create an OAuth2 schema for working with JWT
    """
    return OAuth2PasswordBearer(tokenUrl='')


def get_current_user(
        session: Session = Depends(get_db),
        token: str = Security(get_oauth_schema())
) -> User:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithm=TOKEN_ALGORITHM)
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Невозможно расшифорвать JWT'
        )
    repository = UserRepository(session)
    user = repository.fetch(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'Юзер с таким id не найден'
        )
    return user
