from typing import List, Optional

from sqlalchemy.orm import Session

from scrum.api.utils.security import get_password_hash
from scrum.db_models.user import User as DBUser
from scrum.models.users import UserAuth


class UserRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_in: UserAuth) -> DBUser:
        user = DBUser(
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password)
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def fetch_all(self) -> List[DBUser]:
        return self.session.query(DBUser).all()

    def fetch(self, user_id: int) -> Optional[DBUser]:
        """
        Fetch user object by its id
        :param user_id: user's id
        :return: user's object or None
        """
        user_id = int(user_id)
        return self.session.query(DBUser).get(user_id)

    def fetch_by_username(self, username: str) -> Optional[DBUser]:
        """
        Fetch a user object by its username
        """
        return self.session.query(DBUser).filter_by(username=username).first()
