from typing import Optional, List

from scrum.users.models import User


class UserRepository(object):
    def __init__(self, session_scope):
        super().__init__()
        self.session_scope = session_scope

    def get(self, user_id: int) -> Optional[User]:
        with self.session_scope() as session:
            # making sure
            user_id = int(user_id)
            user = session.query(User).get(user_id)
            return user

    def get_all(self) -> List[User]:
        with self.session_scope() as session:
            return session.query(User).all()
