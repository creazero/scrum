from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from scrum.api.utils import get_db, verify_password
from scrum.core import config
from scrum.core.jwt import create_access_token
from scrum.models.token import Token
from scrum.models.users import UserAuth
from scrum.repositories.users import UserRepository

router = APIRouter()


@router.post('/login', response_model=Token)
def login(session: Session = Depends(get_db), user_auth: UserAuth = None):
    repository = UserRepository(session)
    user = repository.fetch_by_username(user_auth.username)
    if user is None or not verify_password(user_auth.password, user.hashed_password):
        raise HTTPException(400, detail='Неверное имя пользователя или пароль')
    if not user.is_active:
        raise HTTPException(400, detail='Аккаунт данного пользователя не активен')
    token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'token': create_access_token(data={'user_id': user.id}, expires_delta=token_expires)
    }
