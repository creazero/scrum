from typing import List, Optional

from scrum.api.utils import get_password_hash
from scrum.db.session import SessionScope
from scrum.db_models.user import User as DBUser
from scrum.models.users import UserAuth


class UserRepository(object):
    def __init__(self, scoped_session: SessionScope):
        self.scoped_session = scoped_session

    def create_user(self, user_in: UserAuth) -> DBUser:
        with self.scoped_session(commit_on_exit=False) as session:
            user = DBUser(
                username=user_in.username,
                hashed_password=get_password_hash(user_in.password)
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def fetch_all(self) -> List[DBUser]:
        with self.scoped_session() as session:
            return session.query(DBUser).all()

    def fetch(self, user_id: int) -> Optional[DBUser]:
        """
        Fetch user object by its id
        :param user_id: user's id
        :return: user's object or None
        """
        with self.scoped_session() as session:
            user_id = int(user_id)
            return session.query(DBUser).get(user_id)

    def fetch_by_username(self, username: str) -> Optional[DBUser]:
        """
        Fetch a user object by its username
        """
        with self.scoped_session() as session:
            return session.query(DBUser).filter_by(username=username).first()
