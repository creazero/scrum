from typing import List

from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.task import Task as DBTask

internal_error = HTTPException(
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Внутренняя ошибка сервера'
)


class TaskRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def fetch_all(self) -> List[DBTask]:
        try:
            return self.session.query(DBTask).all()
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise internal_error

    def fetch_accessible(self, accessible_projects: List[int]) -> List[DBTask]:
        try:
            return self.session.query(DBTask).\
                filter(DBTask.project_id.in_(accessible_projects)).all()
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise internal_error

    def fetch_from_project(self, project_id: int) -> List[DBTask]:
        try:
            return self.session.query(DBTask).filter_by(project_id=project_id).all()
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise internal_error
