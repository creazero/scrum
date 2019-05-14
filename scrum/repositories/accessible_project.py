import logging
from typing import List, Optional

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

    def fetch_user_role(self, user_id: int, project_id: int) -> Optional[str]:
        try:
            ap: AccessibleProject = self.session.query(AccessibleProject)\
                .filter_by(user_id=user_id, project_id=project_id).first()
            if ap is None:
                return None
            return ap.role
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Внутренняя ошибка сервера'
            )

    def delete(self, project_id: int, user_id: int) -> None:
        self.session.begin()
        try:
            ap = self.session.query(AccessibleProject)\
                .filter_by(project_id=project_id, user_id=user_id).first()
            if ap is not None:
                self.session.delete(ap)
                self.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Внутренняя ошибка сервера'
            )
