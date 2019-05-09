import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scrum.core.security import get_password_hash
from scrum.db_models.user import User as DBUser
from scrum.models.users import UserAuth

commit_exception = HTTPException(
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Произошла внутренняя ошибка'
)
logger = logging.getLogger(__name__)


class UserRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_in: UserAuth) -> DBUser:
        user = DBUser(
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password)
        )
        self.session.add(user)
        try:
            self.session.commit()
            self.session.refresh(user)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise commit_exception
        return user

    def fetch_all(self) -> List[DBUser]:
        try:
            return self.session.query(DBUser).all()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise commit_exception

    def fetch(self, user_id: int) -> Optional[DBUser]:
        """
        Fetch user object by its id
        :param user_id: user's id
        :return: user's object or None
        """
        try:
            return self.session.query(DBUser).get(user_id)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise commit_exception

    def fetch_by_username(self, username: str) -> Optional[DBUser]:
        """
        Fetch a user object by its username
        """
        try:
            return self.session.query(DBUser).filter_by(username=username).first()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise commit_exception
