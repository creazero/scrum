import datetime as dt
import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.sprint import Sprint as DBSprint
from scrum.db_models.task import Task as DBTask
from scrum.db_models.task_state import TaskState
from scrum.models.sprint import SprintCreate

internal_error = HTTPException(
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Внутренняя ошибка сервера'
)
logger = logging.getLogger(__name__)


class SprintRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def fetch_all(self, accessible_projects: List[int], project_id: int) -> List[DBSprint]:
        try:
            if project_id is None:
                return self.session.query(DBSprint).\
                    filter(DBSprint.project_id.in_(accessible_projects)).all()
            else:
                return self.session.query(DBSprint).filter_by(project_id=project_id).all()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error

    def fetch_by_project(self, project_id: int) -> List[DBSprint]:
        try:
            return self.session.query(DBSprint).filter_by(project_id=project_id).all()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error

    def fetch(self, sprint_id: int) -> Optional[DBSprint]:
        try:
            return self.session.query(DBSprint).get(sprint_id)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error

    def fetch_ongoing(self, project_id: int) -> Optional[DBSprint]:
        today = dt.date.today()
        try:
            return self.session.query(DBSprint).filter(DBSprint.project_id == project_id,
                                                       DBSprint.start_date <= today,
                                                       DBSprint.end_date >= today).first()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error

    def create(self, sprint_in: SprintCreate, sprint_length: int = 2) -> DBSprint:
        sprint = DBSprint(length=sprint_length, start_date=sprint_in.start_date,
                          project_id=sprint_in.project_id)
        self.session.begin()
        self.session.add(sprint)
        self.session.flush()
        for task_id in sprint_in.tasks:
            task_db: DBTask = self.session.query(DBTask).get(task_id)
            task_db.sprint_id = sprint.id
            task_db.state = TaskState.todo
        try:
            self.session.commit()
            self.session.refresh(sprint)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error
        return sprint

    def delete(self, sprint: DBSprint) -> None:
        self.session.begin()
        for task in sprint.tasks:
            task.state = None
        try:
            self.session.delete(sprint)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error

    def update(self, sprint: DBSprint, sprint_in: SprintCreate) -> DBSprint:
        self.session.begin()
        sprint.start_date = sprint_in.start_date
        for task in sprint.tasks:
            if task.id not in sprint_in.tasks:
                task.sprint_id = None
                task.state = None
            else:
                sprint_in.tasks.remove(task.id)
        for task_id in sprint_in.tasks:
            task_db: DBTask = self.session.query(DBTask).get(task_id)
            if task_db is not None and task_db.sprint_id is None:
                task_db.state = TaskState.todo
                task_db.sprint_id = sprint.id
        try:
            self.session.commit()
            self.session.refresh(sprint)
            return sprint
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error
