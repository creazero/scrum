import logging
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.tag import Tag as DBTag
from scrum.models.tag import TagCreate

internal_error = HTTPException(
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Внутренняя ошибка'
)
logger = logging.getLogger(__name__)


class TagRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def create(self, tag_in: TagCreate) -> DBTag:
        tag = DBTag(name=tag_in.name, color=tag_in.color,
                    project_id=tag_in.project_id)
        self.session.begin()
        self.session.add(tag)
        try:
            self.session.commit()
            self.session.refresh(tag)
            return tag
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error

    def fetch(self, tag_id: int) -> Optional[DBTag]:
        try:
            return self.session.query(DBTag).get(tag_id)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise internal_error

    def fetch_accessible(self, accessible_projects: List[int]) -> List[DBTag]:
        try:
            return self.session.query(DBTag)\
                .filter(DBTag.project_id.in_(accessible_projects)).all()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise internal_error

    def fetch_by_project(self, project_id: int) -> List[DBTag]:
        try:
            return self.session.query(DBTag).filter_by(project_id=project_id).all()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise internal_error
