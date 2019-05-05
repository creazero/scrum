from datetime import timedelta, datetime

import jwt

from scrum.core import config

TOKEN_ALGORITHM = 'HS256'
TOKEN_SUBJECT = 'access'


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    A function for creating a new access token for user's authentication
    :param data: actual data for encoding
    :param expires_delta: a timedelta for the token's lifetime
    """
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire, 'sub': TOKEN_SUBJECT})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return encoded_jwt
