from typing import List

from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.task import Task as DBTask
from scrum.models.task import TaskCreate

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

    def create(self, task_in: TaskCreate, creator_id: int) -> DBTask:
        new_task = DBTask(task_in, creator_id)
        self.session.add(new_task)
        try:
            self.session.commit()
            self.session.refresh(new_task)
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise internal_error
        return new_task
