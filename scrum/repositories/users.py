from typing import List, Optional

from scrum.db.session import SessionScope
from scrum.db_models.user import User


class UserRepository(object):
    def __init__(self, scoped_session: SessionScope):
        self.scoped_session = scoped_session

    def fetch_all(self) -> List[User]:
        with self.scoped_session() as session:
            return session.query(User).all()

    def fetch(self, user_id: int) -> Optional[User]:
        """
        Fetch user object by its id
        :param user_id: user's id
        :return: user's object or None
        """
        with self.scoped_session() as session:
            user_id = int(user_id)
            return session.query(User).get(user_id)

    def fetch_by_username(self, username: str) -> Optional[User]:
        """
        Fetch a user object by its username
        """
        with self.scoped_session() as session:
            return session.query(User).filter_by(username=username).first()
