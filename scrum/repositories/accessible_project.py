import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.accessible_project import AccessibleProject

logger = logging.getLogger(__name__)


class AccessibleProjectRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def fetch_accessible_for_user(self, user_id: int, only_owner: bool = False) -> List[int]:
        try:
            accessible = self.session.query(AccessibleProject).filter_by(user_id=user_id)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Внутренняя ошибка сервера'
            )
        if only_owner:
            accessible = accessible.filter_by(role='owner')
        return [row.project_id for row in accessible.all()]
