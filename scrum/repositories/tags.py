import logging

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
