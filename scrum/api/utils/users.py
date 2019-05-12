from typing import Tuple

from scrum.db_models.accessible_project import Roles
from scrum.db_models.user import User as DBUser
from scrum.models.users import User


def user_response(ext_user: Tuple[DBUser, Roles]) -> User:
    user = User(role=ext_user[1].value, **ext_user[0].__dict__)
    return user
