from starlette.requests import Request
from passlib.hash import bcrypt

from scrum.db.session import SessionScope


def get_db(request: Request) -> SessionScope:
    return request.state.session


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)


def get_password_hash(plain_password: str) -> str:
    return bcrypt.hash(plain_password)
