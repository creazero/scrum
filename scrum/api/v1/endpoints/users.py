from typing import List

from fastapi import APIRouter, Depends

from scrum.api.utils import get_db
from scrum.db.session import SessionScope
from scrum.models.users import User
from scrum.repositories.users import UserRepository

router = APIRouter()


@router.get('/', response_model=List[User])
def get_users(
        session: SessionScope = Depends(get_db)
):
    """
    Fetch all users
    :param session: db session
    :return: a list of users
    """
    repository = UserRepository(session)
    return repository.fetch_all()
